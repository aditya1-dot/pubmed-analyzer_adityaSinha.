import click
import csv
import logging
import sys
from pathlib import Path
from typing import Optional, TextIO, List, Dict

from .api import PubMedAPI
from .filters import AuthorFilter

@click.command()
@click.argument('query')
@click.option('-f', '--file', type=click.Path(), help='Output file path')
@click.option('-d', '--debug', is_flag=True, help='Enable debug logging')
@click.option('-e', '--email', required=True, help='Email for PubMed API access')
@click.option('-k', '--api-key', help='PubMed API key (optional)')
def main(query: str, file: Optional[str], debug: bool, email: str,
         api_key: Optional[str]) -> None:
    """
    Query PubMed and filter for papers with industry-affiliated authors.
    
    QUERY: PubMed search query string
    """
    # Setup logging
    log_level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)
    
    try:
        # Initialize components
        api = PubMedAPI(email=email, api_key=api_key)
        author_filter = AuthorFilter()
        
        # Search papers
        logger.debug(f"Searching PubMed for: {query}")
        papers = api.search_papers(query)
        
        # Process results
        results: List[Dict] = []
        for paper in papers:
            analysis = author_filter.analyze_paper(paper)
            if analysis["non_academic_authors"]:
                results.append({
                    'PubmedID': paper['pmid'],
                    'Title': paper['title'],
                    'Publication Date': paper['publication_date'],
                    'Non-academic Author(s)': '; '.join(analysis['non_academic_authors']),
                    'Company Affiliation(s)': '; '.join(analysis['company_affiliations']),
                    'Corresponding Author Email': paper['corresponding_email']
                })
        
        # Output results
        fieldnames = [
            'PubmedID', 'Title', 'Publication Date',
            'Non-academic Author(s)', 'Company Affiliation(s)',
            'Corresponding Author Email'
        ]
        
        if file:
            output_path = Path(file)
            logger.debug(f"Writing {len(results)} results to {output_path}")
            with output_path.open('w', newline='') as f:
                write_results(f, results, fieldnames)
        else:
            write_results(sys.stdout, results, fieldnames)
                
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise click.ClickException(str(e))

def write_results(output: TextIO, results: List[Dict], fieldnames: List[str]) -> None:
    """Write results to the specified output stream."""
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    for result in results:
        writer.writerow(result)

if __name__ == '__main__':
    main()