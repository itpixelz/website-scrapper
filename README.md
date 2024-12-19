# 🌐 Website Documentation Scraper

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Selenium](https://img.shields.io/badge/Selenium-4.11%2B-green.svg)](https://www.selenium.dev/)
[![Maintained by itpixelz](https://img.shields.io/badge/maintained%20by-itpixelz-blue.svg)](https://github.com/itpixelz)

A powerful Python-based documentation scraper that downloads and converts documentation websites into well-structured markdown or HTML files. Specifically optimized for API documentation websites with dynamic JavaScript content. Perfect for offline documentation reading, content migration, or documentation archival.

[Live Demo](https://github.com/itpixelz/website-scraper) | [Report Bug](https://github.com/itpixelz/website-scraper/issues) | [Request Feature](https://github.com/itpixelz/website-scraper/issues)

## ✨ Features

- 📚 **Dynamic Content Support**: Handles JavaScript-rendered content using Selenium
- 🔄 **Multiple Output Formats**: Supports both Markdown and HTML output
- 🌳 **Structure Preservation**: Maintains original site hierarchy
- 🎯 **API Documentation Focus**: Specialized in scraping API reference pages
- 🔍 **Smart Navigation**: Automatically detects and follows API section links
- 🛡️ **Robust Error Handling**: Includes retry logic and graceful failures
- ⏱️ **Rate Limiting**: Respectful scraping with built-in delays
- 📝 **Detailed Logging**: Comprehensive progress tracking

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Chrome/Chromium browser installed
- pip (Python package installer)

### Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/website-scraper.git
cd website-scraper
```

2. Set up a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Basic Usage

```bash
# Basic scraping (outputs in Markdown format by default)
python website-scraper.py https://example.com/api-reference --output-dir docs

# Scrape with HTML output
python website-scraper.py https://example.com/api-reference --output-dir docs --format html
```

## 📁 Project Structure

```
website-scraper/
├── website-scraper.py   # Main script
├── requirements.txt     # Project dependencies
├── README.md           # Documentation
└── docs/              # Default output directory
    └── <website-name>/  # Scraped content organized by website
        ├── index.md    # Main page
        └── sections/   # Individual API sections
```

## 🔧 Command Line Options

```bash
Options:
  url                   URL of the API documentation to scrape
  --output-dir DIR      Output directory for scraped content (default: docs)
  --format FORMAT       Output format: 'md' or 'html' (default: md)
```

## 🎯 Features in Detail

### Automatic Content Processing
- Handles dynamically loaded JavaScript content
- Converts HTML to clean, readable Markdown
- Preserves API endpoint structure
- Maintains internal link references

### Smart Navigation
- Automatically detects API sections
- Handles nested documentation structures
- Follows proper rate limiting practices
- Respects robots.txt guidelines

### Output Formats
- **Markdown (Default)**
  - Clean, readable documentation
  - Preserved formatting and structure
  - GitHub-compatible markdown

- **HTML**
  - Complete HTML content preservation
  - Original styling information
  - Interactive elements preserved

## 🔍 Supported Websites

The scraper is specifically tested with:
- RingCentral API Documentation
- Other API reference sites using similar structures
- JavaScript-based documentation platforms

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create your feature branch:
```bash
git checkout -b feature/amazing-feature
```
3. Commit your changes:
```bash
git commit -m 'feat: add amazing feature'
```
4. Push to the branch:
```bash
git push origin feature/amazing-feature
```
5. Open a Pull Request

### Contribution Guidelines
- Follow [Conventional Commits](https://www.conventionalcommits.org/) for commit messages
- Maintain existing code style
- Add tests for new features
- Update documentation as needed

## 📝 Dependencies

- beautifulsoup4 >= 4.12.0: HTML parsing
- selenium >= 4.11.0: Dynamic content handling
- html2text >= 2020.1.16: HTML to Markdown conversion
- webdriver-manager >= 4.0.0: Chrome WebDriver management
- requests >= 2.31.0: HTTP requests
- urllib3 >= 2.0.0: HTTP client
- typing-extensions >= 4.7.0: Type hinting support

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔒 Security

- Respects robots.txt
- Implements rate limiting
- No credential storage
- Safe file handling

## 🐛 Known Issues

- May require adjustments for heavily JavaScript-dependent sites
- Some complex interactive elements might not convert perfectly to Markdown
- Rate limiting might need adjustment for different sites

## 📮 Support

Need help? Got questions?

- [Create an issue](https://github.com/itpixelz/website-scraper/issues/new/choose) for bug reports
- [Start a discussion](https://github.com/itpixelz/website-scraper/discussions/new) for feature requests
- Check [existing issues](https://github.com/itpixelz/website-scraper/issues) before posting

## 🙏 Acknowledgments

- Selenium team for browser automation
- Beautiful Soup team for HTML parsing
- html2text team for Markdown conversion
- All contributors and users

---
<p align="center">
  Made with ❤️ by <a href="https://github.com/itpixelz">itpixelz</a><br>
  © 2024 itpixelz. All rights reserved.
</p>
