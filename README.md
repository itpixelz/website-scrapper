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

## Output

The scraper creates:
- A directory named after the domain (e.g., `example.com_docs`)
- Markdown files for each documentation page
- Log file with scraping details (`domain_scraping.log`)
- Maintains the original site structure

## Configuration

The scraper automatically:
- Detects and respects version paths
- Excludes non-documentation content (assets, images, etc.)
- Handles rate limiting
- Retries failed requests
- Converts HTML to clean Markdown

## Development

To run tests:
```bash
python website-scraper.py --test
```

## Project Structure

```
website-scraper/
├── website-scraper.py     # Main scraper script
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── .gitignore           # Git ignore rules
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