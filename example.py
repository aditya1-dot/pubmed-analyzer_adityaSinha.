from pubmed_analyzer.api import PubMedAPI
from pubmed_analyzer.filters import analyze_affiliations

# Initialize API client
client = PubMedAPI(email="your.email@example.com", api_key="your_api_key")

# Fetch papers
papers = client.fetch_papers(query="Artificial Intelligence AND Drug Discovery AND 2023[DP]")

# Analyze affiliations
industry_papers = analyze_affiliations(papers)

# Export results
with open("results.csv", "w") as f:
    client.export_to_csv(industry_papers, f)
