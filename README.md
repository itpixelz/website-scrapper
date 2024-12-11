# 🌐 Website Documentation Scraper

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A powerful Python-based documentation scraper that downloads and converts documentation websites into well-structured markdown files. Perfect for offline documentation reading, content migration, or documentation archival.

## ✨ Features

- 📚 **Complete Documentation Scraping**: Downloads entire documentation websites
- 🌳 **Structure Preservation**: Maintains original site hierarchy
- ⚡ **Smart Version Handling**: Detects and respects documentation versions
- 🔄 **Format Conversion**: Converts HTML to clean Markdown
- 🛡️ **Robust Error Handling**: Rate limiting and retry logic
- 📝 **Comprehensive Logging**: Detailed logs for debugging
- 🧪 **Test Coverage**: Includes unit tests
- 🎯 **Framework Support**: Works with Sphinx, Docusaurus, and more

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
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
# Basic scraping
python website-scraper.py https://example.com/docs

# Custom output directory
python website-scraper.py https://example.com/docs --output-dir custom_docs

# Adjust retry attempts
python website-scraper.py https://example.com/docs --max-retries 5
```

## 📁 Project Structure

```
website-scraper/
├── 📂 docs/                 # Scraped documentation storage
│   ├── example.com/        # Domain-specific content
│   └── other-site.com/     # Separate by domain
│
├── 📂 logs/                # Log files directory
│   ├── example.com_scraping.log
│   └── other-site.com_scraping.log
│
├── 📄 website-scraper.py   # Main script
├── 📄 requirements.txt     # Dependencies
├── 📄 README.md           # Documentation
└── 📂 tests/              # Test files
```

## 🔧 Configuration

The scraper includes smart defaults and can be configured through command-line arguments:

```bash
Options:
  --output-dir DIR    Custom output directory (default: docs/<domain>)
  --max-retries N     Maximum retry attempts for failed requests (default: 3)
```

### Automatic Features:
- 🔍 Version detection in URLs
- 🚫 Asset filtering (images, CSS, JS)
- ⏱️ Rate limiting
- 🔄 Retry logic for failed requests
- 🧹 Clean Markdown conversion

## 📝 Output Format

### Documentation Files
- Stored in `docs/<domain>/`
- Maintains original site structure
- Converts to clean Markdown format
- Preserves metadata and links

### Logs
- Stored in `logs/<domain>_scraping.log`
- Includes timestamps and error details
- Tracks scraping progress
- Helps with debugging

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create your feature branch:
```bash
git checkout -b feature/amazing-feature
```
3. Commit your changes:
```bash
git commit -m 'Add amazing feature'
```
4. Push to the branch:
```bash
git push origin feature/amazing-feature
```
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Beautiful Soup for HTML parsing
- Requests for HTTP handling
- All our contributors and users

## 📧 Support

- Create an issue for bug reports
- Start a discussion for feature requests
- Check existing issues before posting

---
Made with ❤️ by [Your Name] 