import requests
import csv
import xml.etree.ElementTree as ET
from typing import List, Dict
import calendar
import re

# Keywords that typically indicate a non-academic company
COMPANY_KEYWORDS = [
    "Inc", "Ltd", "LLC", "Corporation", "Corp", "Pharma", "Biotech",
    "Diagnostics", "Therapeutics", "Laboratories"
]

def search_pubmed(query: str, max_results: int = 50) -> List[str]:
    """
    Search PubMed for article IDs matching the query.
    """
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": max_results,
        "retmode": "json"
    }
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    data = response.json()
    return data["esearchresult"]["idlist"]

def fetch_details(pubmed_ids: List[str]) -> List[Dict]:
    """
    Fetch article details from PubMed and filter for industry authors.
    """
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
        "db": "pubmed",
        "id": ",".join(pubmed_ids),
        "retmode": "xml"
    }
    response = requests.get(base_url, params=params)
    response.raise_for_status()

    root = ET.fromstring(response.content)
    papers = []
    seen_ids = set()

    for article in root.findall(".//PubmedArticle"):
        try:
            medline = article.find("MedlineCitation")
            article_info = medline.find("Article")
            pubmed_id = medline.find("PMID").text if medline.find("PMID") is not None else ""
            if pubmed_id in seen_ids:
                continue
            seen_ids.add(pubmed_id)

            title = article_info.findtext("ArticleTitle", default="No Title")
            journal = article_info.findtext("Journal/Title", default="Unknown Journal")


            # Extract and format publication date
            pub_date_elem = article_info.find(".//Journal/JournalIssue/PubDate")
            if pub_date_elem is not None:
                year = pub_date_elem.findtext("Year", "")
                month_str = pub_date_elem.findtext("Month", "")
                day = pub_date_elem.findtext("Day", "01")
                month = (
                    str(list(calendar.month_abbr).index(month_str[:3])).zfill(2)
                    if month_str[:3] in calendar.month_abbr else "01"
                )
                pub_date_str = f"{year}-{month}-{day.zfill(2)}" if year else ""
            else:
                pub_date_str = ""

            non_academic_authors = []
            company_affiliations = []
            corresponding_email = ""

            for author in article_info.findall(".//Author"):
                affiliation_info = author.find("AffiliationInfo")
                if affiliation_info is not None:
                    affiliation = affiliation_info.findtext("Affiliation", "")
                    if any(keyword in affiliation for keyword in COMPANY_KEYWORDS):
                        first = author.findtext("ForeName", "")
                        last = author.findtext("LastName", "")
                        full_name = " ".join(part for part in [first, last] if part)
                        if full_name:
                            non_academic_authors.append(full_name)
                        company_affiliations.append(affiliation)

                        # Primary email extraction
                        if "@" in affiliation and not corresponding_email:
                            for word in affiliation.replace(",", " ").split():
                                if "@" in word:
                                    corresponding_email = word.strip(";,.)(")

                        # Fallback email regex
                        if not corresponding_email:
                            email_match = re.search(r'[\w\.-]+@[\w\.-]+', affiliation)
                            if email_match:
                                corresponding_email = email_match.group(0)

            if non_academic_authors:
               papers.append({
               "PubmedID": pubmed_id,
               "Title": title,
               "Journal": journal,
               "Publication Date": pub_date_str,
               "Non-academicAuthor(s)": "; ".join(non_academic_authors),
               "CompanyAffiliation(s)": "; ".join(company_affiliations),
               "Corresponding Author Email": corresponding_email
               })


        except Exception as e:
            print(f"⚠️ Skipped invalid paper entry: {pubmed_id} due to error: {str(e)}")

    return papers

def write_to_csv(papers: List[Dict], output_path: str):
    """
    Write filtered paper data to CSV.
    """
    fieldnames = [
    "PubmedID",
    "Title",
    "Journal",  # ← Add this
    "Publication Date",
    "Non-academicAuthor(s)",
    "CompanyAffiliation(s)",
    "Corresponding Author Email"
]

    with open(output_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for paper in papers:
            if isinstance(paper, dict):
                writer.writerow(paper)
            else:
                print(f"⚠️ Skipped invalid paper entry: {paper}")
