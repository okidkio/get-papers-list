from get_papers_list.pubmed import search_pubmed, fetch_details, write_to_csv
import argparse

def main():
    parser = argparse.ArgumentParser(description="Fetch PubMed papers with industry authors.")
    parser.add_argument("--query", required=True, help="Search query for PubMed")
    parser.add_argument("--output", required=True, help="Output CSV file path")
    parser.add_argument("--max_results", type=int, default=20, help="Maximum number of papers to fetch")
    args = parser.parse_args()

    print(f"Running PubMed fetcher with query: {args.query}")
    print(f"Output will be saved to: {args.output}")
    print(f"Max results: {args.max_results}")

    # Step 1: Get PubMed IDs
    pubmed_ids = search_pubmed(args.query, args.max_results)
    print(f"Total papers fetched: {len(pubmed_ids)}")

    # Step 2: Get paper details + filter those with industry authors
    filtered_papers = fetch_details(pubmed_ids)
    print(f"Papers with at least one industry author: {len(filtered_papers)}")

    # Step 3: Write to CSV
    write_to_csv(filtered_papers, args.output)
    print("CSV write complete.")

if __name__ == "__main__":
    main()
