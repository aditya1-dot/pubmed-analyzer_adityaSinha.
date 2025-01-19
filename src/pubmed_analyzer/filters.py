from typing import Dict, List, Set
import re

class AuthorFilter:
    """Filter papers based on author affiliations."""
    
    ACADEMIC_KEYWORDS: Set[str] = {
        "university", "college", "institute", "school",
        "faculty", "academy", "hospital", "clinic",
        "medical center", "research center"
    }
    
    COMPANY_KEYWORDS: Set[str] = {
        "pharma", "biotech", "therapeutics", "laboratories",
        "inc", "corp", "ltd", "llc", "gmbh", "pharmaceutical",
        "biotechnology", "drug", "bioscience"
    }
    
    def analyze_paper(self, paper: Dict) -> Dict:
        """
        Analyze paper to identify non-academic authors and their affiliations.
        
        Args:
            paper: Paper metadata dictionary
            
        Returns:
            Dictionary with non-academic authors and their company affiliations
        """
        non_academic_authors: List[str] = []
        company_affiliations: Set[str] = set()
        
        for author in paper.get("authors", []):
            affiliation = author.get("affiliation", "").lower()
            if affiliation and not self._is_academic_affiliation(affiliation):
                company = self._extract_company_name(affiliation)
                if company:
                    non_academic_authors.append(author["name"])
                    company_affiliations.add(company)
        
        return {
            "non_academic_authors": non_academic_authors,
            "company_affiliations": list(company_affiliations)
        }
    
    def _is_academic_affiliation(self, affiliation: str) -> bool:
        """Check if an affiliation is academic."""
        return any(keyword in affiliation for keyword in self.ACADEMIC_KEYWORDS)
    
    def _extract_company_name(self, affiliation: str) -> str:
        """Extract company name from affiliation string."""
        # Look for company keywords and try to extract full company name
        for keyword in self.COMPANY_KEYWORDS:
            if keyword in affiliation:
                # Simple company name extraction - could be improved
                words = affiliation.split()
                keyword_idx = next(i for i, word in enumerate(words) if keyword in word)
                
                # Take up to 3 words before and after the keyword
                start = max(0, keyword_idx - 3)
                end = min(len(words), keyword_idx + 4)
                return " ".join(words[start:end])
        return ""