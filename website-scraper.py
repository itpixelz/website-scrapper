import requests
from bs4 import BeautifulSoup
import os
import time
import logging
from urllib.parse import urljoin, urlparse
import re
import json
import unittest
from typing import Set, Optional
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import argparse

class WebsiteScraper:
    def __init__(self, base_url: str, output_dir: Optional[str] = None, max_retries: int = 3):
        self.base_url = base_url.rstrip('/')
        # Extract version from URL if present
        version_match = re.search(r'/(\d+\.\d+(?:\.\d+)?(?:\.dev\d+)?(?:\.post\d+)?(?:\.alpha\d+)?(?:\.beta\d+)?)', self.base_url)
        self.version = version_match.group(1) if version_match else None
        self.domain = urlparse(base_url).netloc
        self.output_dir = output_dir or f"{self.domain}_docs"
        self.visited_urls = set()
        self.max_retries = max_retries
        
        # Setup session with retry logic
        self.session = requests.Session()
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        # Setup logging
        log_file = f"{self.domain}_scraping.log"
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()  # Also log to console
            ]
        )
        
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def get_page_content(self, url: str) -> Optional[str]:
        """Fetch page content with error handling and rate limiting"""
        try:
            time.sleep(1)  # Rate limiting
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = self.session.get(url, headers=headers)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logging.error(f"Error fetching {url}: {str(e)}")
            return None

    def get_navigation_structure(self) -> Set[str]:
        """Try to find navigation structure from common patterns"""
        nav_urls = set()
        try:
            # Try common navigation endpoints
            nav_patterns = [
                '/navigation.json',
                '/nav.json',
                '/sitemap.xml',
                '/docs/navigation.json',
                '/api/navigation'
            ]
            
            for pattern in nav_patterns:
                try:
                    url = urljoin(self.base_url, pattern)
                    response = self.session.get(url)
                    if response.status_code == 200:
                        content_type = response.headers.get('content-type', '')
                        if 'json' in content_type:
                            nav_data = response.json()
                            self._extract_urls_from_nav(nav_data, nav_urls)
                        elif 'xml' in content_type:
                            soup = BeautifulSoup(response.text, 'xml')
                            for loc in soup.find_all('loc'):
                                if self._is_valid_doc_url(loc.text):
                                    nav_urls.add(loc.text)
                        logging.info(f"Successfully fetched navigation from {url}")
                        break
                except:
                    continue
            
            # Fallback to HTML parsing
            if not nav_urls:
                content = self.get_page_content(self.base_url)
                if content:
                    soup = BeautifulSoup(content, 'html.parser')
                    nav_urls.update(self.extract_doc_urls(soup))
                    
        except Exception as e:
            logging.error(f"Error fetching navigation data: {str(e)}")
        
        return nav_urls

    def _extract_urls_from_nav(self, nav_data: dict, urls: Set[str]) -> None:
        """Recursively extract URLs from navigation data"""
        if isinstance(nav_data, dict):
            for key, value in nav_data.items():
                if isinstance(key, str) and ('url' in key.lower() or 'href' in key.lower()):
                    full_url = urljoin(self.base_url, str(value))
                    if self._is_valid_doc_url(full_url):
                        urls.add(full_url)
                self._extract_urls_from_nav(value, urls)
        elif isinstance(nav_data, list):
            for item in nav_data:
                self._extract_urls_from_nav(item, urls)

    def extract_doc_urls(self, soup: BeautifulSoup) -> Set[str]:
        """Extract documentation URLs from the page"""
        urls = set()
        
        # Special handling for Sphinx documentation
        sphinx_nav = soup.find('div', class_='sphinxsidebar') or soup.find('div', class_='sidebar-tree')
        if sphinx_nav:
            # Extract all links from the sidebar
            for link in sphinx_nav.find_all('a', href=True):
                href = link['href']
                if not href.startswith(('http://', 'https://', '#', 'mailto:')):
                    # Handle relative paths in Sphinx docs
                    current_path = urlparse(self.base_url).path
                    base_dir = '/'.join(current_path.split('/')[:-1])
                    if not base_dir.endswith('/'):
                        base_dir += '/'
                    full_url = urljoin(self.base_url, base_dir + href)
                else:
                    full_url = urljoin(self.base_url, href)
                
                if self._is_valid_doc_url(full_url):
                    urls.add(full_url)
        
        # Find all links in the main content
        main_content = soup.find('div', class_=['body', 'content', 'document']) or soup
        for link in main_content.find_all(['a', 'nav']):
            # Handle nav elements by finding nested links
            if link.name == 'nav':
                for a in link.find_all('a', href=True):
                    href = a['href']
                    if not href.startswith(('http://', 'https://', '#', 'mailto:')):
                        current_path = urlparse(self.base_url).path
                        base_dir = '/'.join(current_path.split('/')[:-1])
                        if not base_dir.endswith('/'):
                            base_dir += '/'
                        full_url = urljoin(self.base_url, base_dir + href)
                    else:
                        full_url = urljoin(self.base_url, href)
                    
                    if self._is_valid_doc_url(full_url):
                        urls.add(full_url)
            # Handle direct links
            elif link.name == 'a' and link.get('href'):
                href = link['href']
                if not href.startswith(('http://', 'https://', '#', 'mailto:')):
                    current_path = urlparse(self.base_url).path
                    base_dir = '/'.join(current_path.split('/')[:-1])
                    if not base_dir.endswith('/'):
                        base_dir += '/'
                    full_url = urljoin(self.base_url, base_dir + href)
                else:
                    full_url = urljoin(self.base_url, href)
                
                if self._is_valid_doc_url(full_url):
                    urls.add(full_url)
        
        return urls

    def _is_valid_doc_url(self, url: str) -> bool:
        """Check if URL is a valid documentation page"""
        parsed_url = urlparse(url)
        
        # Check if URL is from the same domain
        if parsed_url.netloc != self.domain:
            return False
            
        # If we have a version, ensure URL matches that version
        if self.version:
            if self.version not in url:
                return False
            
            # Don't allow links to other versions
            other_version = re.search(r'/(\d+\.\d+(?:\.\d+)?(?:\.dev\d+)?(?:\.post\d+)?(?:\.alpha\d+)?(?:\.beta\d+)?)', url)
            if other_version and other_version.group(1) != self.version:
                return False
        
        # Common patterns to exclude
        excluded_patterns = [
            '/assets/', '/static/', '/images/', '/js/', '/css/',
            '/fonts/', '/icons/', '#', 'mailto:', 'tel:', '_sources'
        ]
        excluded_extensions = (
            '.png', '.jpg', '.jpeg', '.gif', '.svg', '.css', '.js',
            '.woff', '.woff2', '.ttf', '.eot', '.ico', '.pdf'
        )
        
        return not (
            any(pattern in url for pattern in excluded_patterns) or
            url.endswith(excluded_extensions)
        )

    def clean_text(self, text: str) -> str:
        """Clean and format the text for markdown"""
        text = re.sub(r'\n\s*\n', '\n\n', text)
        text = re.sub(r' +', ' ', text)
        return text.strip()

    def html_to_markdown(self, soup: BeautifulSoup) -> str:
        """Convert HTML content to markdown-style text"""
        # Remove common non-content elements
        for elem in soup.find_all(['nav', 'footer', 'script', 'style', 'noscript']):
            elem.decompose()
        
        content = []
        
        # Get title
        title = soup.find(['h1']) or soup.find('title')
        if title:
            content.append(f"# {title.get_text().strip()}\n")
        
        # Get main content
        main_content = soup.find(['main', 'article']) or soup.find('body')
        if main_content:
            # Process headings
            for h in main_content.find_all(['h2', 'h3', 'h4', 'h5', 'h6']):
                level = int(h.name[1])
                text = h.get_text().strip()
                h.replace_with(f"\n{'#' * level} {text}\n")
            
            # Process code blocks
            for pre in main_content.find_all('pre'):
                code = pre.find('code')
                if code:
                    language = code.get('class', [''])[0].replace('language-', '') if code.get('class') else ''
                    code_text = code.get_text().strip()
                    pre.replace_with(f"\n```{language}\n{code_text}\n```\n")
            
            # Process inline code
            for code in main_content.find_all('code'):
                if code.parent.name != 'pre':
                    code.replace_with(f"`{code.get_text()}`")
            
            # Process lists
            for ul in main_content.find_all(['ul', 'ol']):
                for li in ul.find_all('li', recursive=False):
                    prefix = '*' if ul.name == 'ul' else '1.'
                    li.string = f"\n{prefix} {li.get_text().strip()}"
            
            content.append(self.clean_text(main_content.get_text()))
        
        return '\n'.join(content)

    def save_content(self, url: str, content: str) -> None:
        """Save the scraped content to a markdown file"""
        try:
            parsed_url = urlparse(url)
            filepath = parsed_url.path.strip('/')
            if not filepath:
                filepath = 'index'
            
            full_path = os.path.join(self.output_dir, filepath)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            
            content_with_source = f"""---
Source: {url}
Scraped: {time.strftime('%Y-%m-%d %H:%M:%S')}
---

{content}
"""
            
            with open(f"{full_path}.md", 'w', encoding='utf-8') as f:
                f.write(content_with_source)
                
            logging.info(f"Saved content from {url} to {full_path}.md")
            
        except Exception as e:
            logging.error(f"Error saving content from {url}: {str(e)}")

    def scrape_website(self):
        """Main scraping function"""
        # Get initial URLs from navigation
        urls_to_visit = self.get_navigation_structure()
        
        # Add base URL if no URLs found
        if not urls_to_visit:
            urls_to_visit.add(self.base_url)
        
        total_urls = len(urls_to_visit)
        logging.info(f"Found {total_urls} pages to scrape")
        
        while urls_to_visit:
            current_url = urls_to_visit.pop()
            
            if current_url in self.visited_urls:
                continue
            
            logging.info(f"Scraping ({len(self.visited_urls) + 1}/{total_urls}): {current_url}")
            content = self.get_page_content(current_url)
            
            if not content:
                continue
            
            soup = BeautifulSoup(content, 'html.parser')
            
            # Extract and save content
            markdown_content = self.html_to_markdown(soup)
            if markdown_content.strip():
                self.save_content(current_url, markdown_content)
            
            # Mark as visited
            self.visited_urls.add(current_url)
            
            # Find new URLs to visit
            new_urls = self.extract_doc_urls(soup)
            new_valid_urls = {url for url in new_urls if self._is_valid_doc_url(url)}
            urls_to_visit.update(new_valid_urls - self.visited_urls)
            
            total_urls = len(urls_to_visit) + len(self.visited_urls)
            logging.info(f"Progress: {len(self.visited_urls)}/{total_urls} pages processed")

class TestWebsiteScraper(unittest.TestCase):
    def setUp(self):
        self.scraper = WebsiteScraper('https://example.com', output_dir='test_output')
        if not os.path.exists('test_output'):
            os.makedirs('test_output')

    def tearDown(self):
        if os.path.exists('test_output'):
            for file in os.listdir('test_output'):
                os.remove(os.path.join('test_output', file))
            os.rmdir('test_output')

    def test_url_validation(self):
        valid_urls = [
            'https://example.com/docs/guide',
            'https://example.com/tutorial/intro',
        ]
        invalid_urls = [
            'https://example.com/assets/image.png',
            'https://other-domain.com/docs',
            'https://example.com/style.css',
            'mailto:contact@example.com',
        ]
        
        for url in valid_urls:
            self.assertTrue(self.scraper._is_valid_doc_url(url))
        
        for url in invalid_urls:
            self.assertFalse(self.scraper._is_valid_doc_url(url))

    def test_content_saving(self):
        test_url = 'https://example.com/test-page'
        test_content = '# Test Content\n\nThis is a test.'
        self.scraper.save_content(test_url, test_content)
        
        saved_file = os.path.join('test_output', 'test-page.md')
        self.assertTrue(os.path.exists(saved_file))
        
        with open(saved_file, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn('# Test Content', content)
            self.assertIn('Source: https://example.com/test-page', content)

def main():
    parser = argparse.ArgumentParser(description='Scrape documentation from any website')
    parser.add_argument('url', help='The base URL to scrape (e.g., https://example.com)')
    parser.add_argument('--output-dir', help='Output directory for scraped content (default: domain_docs)')
    parser.add_argument('--max-retries', type=int, default=3, help='Maximum number of retries for failed requests')
    args = parser.parse_args()

    # Run tests first
    if not args.url.startswith(('http://', 'https://')):
        print("Error: URL must start with http:// or https://")
        return

    test_loader = unittest.TestLoader()
    test_suite = test_loader.loadTestsFromTestCase(TestWebsiteScraper)
    test_runner = unittest.TextTestRunner()
    test_result = test_runner.run(test_suite)
    
    if test_result.wasSuccessful():
        print("\nTests passed successfully! Starting scraping...\n")
        scraper = WebsiteScraper(args.url, args.output_dir, args.max_retries)
        scraper.scrape_website()
        print(f"\nScraping complete! Documents saved in '{scraper.output_dir}' directory")
        print(f"Total pages scraped: {len(scraper.visited_urls)}")
        print(f"Check '{scraper.domain}_scraping.log' for detailed information")
    else:
        print("\nTests failed. Please fix the issues before running the scraper.")

if __name__ == "__main__":
    main()