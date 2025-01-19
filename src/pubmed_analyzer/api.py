from typing import Dict, List, Optional
import logging
import xml.etree.ElementTree as ET
import requests
from time import sleep
from datetime import datetime

class PubMedAPI:
    """Handle interactions with the PubMed API."""
    
    BASE_URL: str = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    
    def __init__(self, email: str, api_key: Optional[str] = None):
        self.email: str = email
        self.api_key: Optional[str] = api_key
        self.logger: logging.Logger = logging.getLogger(__name__)

    def search_papers(self, query: str, max_results: int = 100) -> List[Dict]:
        """
        Search PubMed for papers matching the query.
        
        Args:
            query: PubMed search query
            max_results: Maximum number of results to return
            
        Returns:
            List of paper dictionaries with required fields
        """
        search_url: str = f"{self.BASE_URL}/esearch.fcgi"
        params: Dict = {
            "db": "pubmed",
            "term": query,
            "retmax": max_results,
            "retmode": "json",
            "email": self.email
        }
        if self.api_key:
            params["api_key"] = self.api_key
            
        response = requests.get(search_url, params=params)
        response.raise_for_status()
        
        data = response.json()
        pmids: List[str] = data["esearchresult"]["idlist"]
        
        results: List[Dict] = []
        for pmid in pmids:
            paper = self._fetch_paper_details(pmid)
            if paper:
                results.append(paper)
            sleep(0.34)  # Rate limiting
            
        return results
    
    def _fetch_paper_details(self, pmid: str) -> Optional[Dict]:
        """
        Fetch detailed information for a single paper.
        
        Args:
            pmid: PubMed ID of the paper
            
        Returns:
            Dictionary containing paper details or None if fetch fails
        """
        fetch_url: str = f"{self.BASE_URL}/efetch.fcgi"
        params: Dict = {
            "db": "pubmed",
            "id": pmid,
            "retmode": "xml",
            "email": self.email
        }
        if self.api_key:
            params["api_key"] = self.api_key
            
        try:
            response = requests.get(fetch_url, params=params)
            response.raise_for_status()
            
            # Parse XML response
            root = ET.fromstring(response.text)
            article = root.find(".//Article")
            if article is None:
                return None
                
            # Extract required information
            title: str = article.findtext(".//ArticleTitle", "")
            pub_date: str = self._parse_publication_date(article)
            
            # Extract author information
            authors_info = self._extract_authors_info(article)
            
            return {
                "pmid": pmid,
                "title": title,
                "publication_date": pub_date,
                "authors": authors_info["authors"],
                "affiliations": authors_info["affiliations"],
                "corresponding_email": authors_info["corresponding_email"]
            }
            
        except Exception as e:
            self.logger.error(f"Error fetching paper {pmid}: {str(e)}")
            return None
            
    def _parse_publication_date(self, article: ET.Element) -> str:
        """Extract and format publication date from article XML."""
        pub_date = article.find(".//PubDate")
        if pub_date is None:
            return ""
            
        year = pub_date.findtext("Year", "")
        month = pub_date.findtext("Month", "01")
        day = pub_date.findtext("Day", "01")
        
        try:
            date = datetime(int(year), int(month), int(day))
            return date.strftime("%Y-%m-%d")
        except (ValueError, TypeError):
            return year if year else ""
            
    def _extract_authors_info(self, article: ET.Element) -> Dict:
        """Extract author information including affiliations and email."""
        authors: List[Dict] = []
        affiliations: List[str] = []
        corresponding_email: str = ""
        
        author_list = article.find(".//AuthorList")
        if author_list is not None:
            for author in author_list.findall("Author"):
                author_info: Dict = {
                    "name": f"{author.findtext('LastName', '')} {author.findtext('ForeName', '')}".strip(),
                    "affiliation": "",
                    "email": ""
                }
                
                # Get affiliation
                aff = author.find("AffiliationInfo/Affiliation")
                if aff is not None:
                    author_info["affiliation"] = aff.text
                    affiliations.append(aff.text)
                
                # Get email from author details
                email = author.findtext(".//Email")
                if email:
                    author_info["email"] = email
                    if not corresponding_email:
                        corresponding_email = email
                
                authors.append(author_info)
        
        return {
            "authors": authors,
            "affiliations": affiliations,
            "corresponding_email": corresponding_email
        }