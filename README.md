# PubMed Paper Analyzer

A command-line tool to analyze PubMed papers and identify those with industry-affiliated authors.

## Features

- Search PubMed using full query syntax
- Identify papers with pharmaceutical/biotech company affiliated authors
- Export results to CSV with detailed author and affiliation information
- Command-line interface with debugging support

## Installation

### Option 1:Install from github

```bash
# Clone the repository
git clone https://github.com/aditya1-dot/pubmed-analyzer-adityaSinha
cd pubmed-analyzer

# Install using Poetry
poetry install
```

### Option 2: Install from Test PyPI
To install the package directly from Test PyPI, use the following command:
```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ pubmed-analyzer-adityaSinha
## Usage

Basic usage:
```bash
get-papers-list "your search query" -e your.email@example.com
```

Options:
- `-f/--file`: Output file path (optional, defaults to stdout)
- `-d/--debug`: Enable debug logging
- `-e/--email`: Email for PubMed API (required)
- `-k/--api-key`: PubMed API key (optional)
- `-h/--help`: Show help message

## Code Organization

The project is organized into several modules:

- `api.py`: Handles PubMed API interactions
- `filters.py`: Implements author affiliation analysis
- `cli.py`: Command-line interface implementation

## Tools Used

- Poetry: Dependency management and packaging
- Click: Command-line interface creation
- Requests: HTTP client for API calls
- Logging: Debug and error tracking
- Type hints: Static typing throughout the codebase

## Development

1. Clone repository
2. Install dependencies: `poetry install`
3. Run the tool: `poetry run get-papers-list`

## Error Handling

The tool includes robust error handling for:
- Invalid queries
- API failures
- Network issues
- Missing or malformed data
- Output file access issues