# Website Documentation Scraper

A versatile documentation scraper that can download and convert documentation websites into markdown files while maintaining the original structure and formatting.

## Features

- Scrapes entire documentation websites
- Maintains directory structure
- Converts HTML to Markdown
- Handles versioned documentation
- Supports various documentation systems (Sphinx, Docusaurus, etc.)
- Version-aware scraping
- Rate limiting and retry logic
- Comprehensive logging
- Unit tests included

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/website-scraper.git
cd website-scraper
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Basic usage:
```bash
python website-scraper.py https://example.com/docs
```

With custom output directory:
```bash
python website-scraper.py https://example.com/docs --output-dir my_docs
```

With custom retry count:
```bash
python website-scraper.py https://example.com/docs --max-retries 5
```

## Output Structure

The scraper organizes content in dedicated directories:

```
website-scraper/
├── docs/                 # All scraped documentation
│   ├── example.com/     # Domain-specific documentation
│   └── other-site.com/  # Another site's documentation
│
└── logs/                # All log files
    ├── example.com_scraping.log
    └── other-site.com_scraping.log
```

### Output Details

- Documentation files are stored in `docs/<domain>/`
- Each documentation page is converted to Markdown
- Original site structure is maintained within domain directory
- Logs are stored in `logs/` with domain-specific names

## Configuration

The scraper automatically:
- Detects and respects version paths
- Excludes non-documentation content (assets, images, etc.)
- Handles rate limiting
- Retries failed requests
- Converts HTML to clean Markdown

## Project Structure

```
website-scraper/
├── website-scraper.py     # Main scraper script
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── .gitignore           # Git ignore rules
├── docs/                # Scraped documentation output
├── logs/                # Log files directory
└── tests/               # Test files (future)
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 