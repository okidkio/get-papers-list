import sys
import os
import pytest
from unittest.mock import patch, MagicMock

# Fix path for importing from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from get_papers_list import pubmed

def test_search_pubmed_success():
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "esearchresult": {"idlist": ["12345678", "87654321"]}
        }

        results = pubmed.search_pubmed("cancer")
        assert isinstance(results, list)
        assert "12345678" in results
        assert "87654321" in results

def test_search_pubmed_failure():
    with patch("requests.get") as mock_get:
        mock_get.return_value.raise_for_status.side_effect = Exception("API error")

        with pytest.raises(Exception):
            pubmed.search_pubmed("error query")

def test_write_to_csv(tmp_path):
    papers = [
        {
            "PubmedID": "123456",
            "Title": "Test Paper",
            "Publication Date": "2023-01-01",
            "Non-academicAuthor(s)": "John Doe",
            "CompanyAffiliation(s)": "Pfizer Inc",
            "Corresponding Author Email": "john@example.com"
        }
    ]
    output_file = tmp_path / "test_output.csv"
    pubmed.write_to_csv(papers, output_file)

    with open(output_file, "r", encoding="utf-8") as f:
        content = f.read()
        assert "PubmedID" in content
        assert "123456" in content
        assert "Test Paper" in content

def test_fetch_details_success():
    with patch("requests.get") as mock_get:
        # Use real efetch-like XML structure
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"""
        <PubmedArticleSet>
          <PubmedArticle>
            <MedlineCitation>
              <PMID>12345678</PMID>
              <Article>
                <ArticleTitle>Sample Title</ArticleTitle>
                <Journal>
                  <JournalIssue>
                    <PubDate>
                      <Year>2024</Year>
                      <Month>Jul</Month>
                    </PubDate>
                  </JournalIssue>
                  <Title>Test Journal</Title>
                </Journal>
                <AuthorList>
                  <Author>
                    <LastName>Doe</LastName>
                    <ForeName>John</ForeName>
                    <AffiliationInfo>
                      <Affiliation>Pfizer Inc, USA</Affiliation>
                    </AffiliationInfo>
                  </Author>
                </AuthorList>
              </Article>
            </MedlineCitation>
          </PubmedArticle>
        </PubmedArticleSet>
        """
        mock_get.return_value = mock_response

        results = pubmed.fetch_details(["12345678"])

        assert isinstance(results, list)
        assert len(results) == 1
        assert results[0]["PubmedID"] == "12345678"
        assert results[0]["Title"] == "Sample Title"
        assert results[0]["Journal"] == "Test Journal"
        assert results[0]["CompanyAffiliation(s)"] == "Pfizer Inc, USA"
        assert "Doe" in results[0]["Non-academicAuthor(s)"] or "John" in results[0]["Non-academicAuthor(s)"]
