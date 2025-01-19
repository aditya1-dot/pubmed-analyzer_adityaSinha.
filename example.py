from pubmed_analyzer.api import PubMedAPI
from pubmed_analyzer.filters import AuthorFilter
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def main():
    # User inputs
    email = "your.email@example.com"  # Replace with your email
    api_key = None  # Optional: Replace with your PubMed API key if you have one
    query = "cancer research"  # PubMed search query
    max_results = 10  # Number of papers to fetch

    # Initialize PubMedAPI and AuthorFilter
    pubmed_api = PubMedAPI(email=email, api_key=api_key)
    author_filter = AuthorFilter()

    # Search PubMed and fetch papers
    logging.info(f"Searching PubMed for query: {query}")
    papers = pubmed_api.search_papers(query, max_results=max_results)

    # Analyze papers for non-academic authors
    logging.info(f"Analyzing {len(papers)} papers for non-academic affiliations...")
    for paper in papers:
        analysis = author_filter.analyze_paper(paper)

        if analysis["non_academic_authors"]:
            print("--------------------------------------------------")
            print(f"PMID: {paper['pmid']}")
            print(f"Title: {paper['title']}")
            print(f"Publication Date: {paper['publication_date']}")
            print(f"Non-academic Authors: {', '.join(analysis['non_academic_authors'])}")
            print(f"Company Affiliations: {', '.join(analysis['company_affiliations'])}")
            print(f"Corresponding Author Email: {paper['corresponding_email']}")
            print("--------------------------------------------------")
        else:
            logging.info(f"No non-academic authors found for paper: {paper['title']}")

if __name__ == "__main__":
    main()
