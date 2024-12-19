import requests
from bs4 import BeautifulSoup
import os
import time
from urllib.parse import urljoin, urlparse, unquote
import re
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import html2text

def create_output_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def setup_driver():
    """Setup Chrome WebDriver with appropriate options."""
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run in headless mode
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    
    # Use webdriver-manager to handle driver installation
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def convert_to_markdown(html_content):
    """Convert HTML content to Markdown."""
    h = html2text.HTML2Text()
    h.ignore_links = False
    h.ignore_images = False
    h.ignore_tables = False
    h.body_width = 0  # Don't wrap lines
    return h.handle(html_content)

def save_content(content, filepath, format='md'):
    """Save content in the specified format."""
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    # Adjust file extension based on format
    base_path = os.path.splitext(filepath)[0]
    if format == 'md':
        filepath = f"{base_path}.md"
    elif format == 'html':
        filepath = f"{base_path}.html"
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    return filepath

def get_api_sections(driver):
    """Extract API sections from the sidebar navigation using Selenium."""
    sections = []
    
    try:
        # Wait for the navigation menu to load
        print("Waiting for navigation menu to load...")
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[class*='sidebar'], [class*='nav']"))
        )
        
        # Additional wait for dynamic content
        time.sleep(5)
        
        # Print the page source for debugging
        print("Page source loaded. Looking for navigation elements...")
        
        # Try to find the Voice, SMS, etc. sections
        main_sections = [
            "Voice",
            "SMS and Fax",
            "Team Messaging",
            "Video",
            "Webinar",
            "Analytics",
            "Authentication",
            "Account",
            "Provisioning"
        ]
        
        found_elements = []
        for section in main_sections:
            try:
                elements = driver.find_elements(By.XPATH, f"//*[contains(text(), '{section}')]")
                for element in elements:
                    if element.is_displayed():
                        parent = element
                        # Try to find the closest clickable parent or link
                        for _ in range(3):  # Check up to 3 levels up
                            try:
                                href = parent.get_attribute('href')
                                if href:
                                    found_elements.append((section, href))
                                    print(f"Found section: {section} with URL: {href}")
                                    break
                            except:
                                parent = parent.find_element(By.XPATH, '..')
            except Exception as e:
                print(f"Error finding section {section}: {str(e)}")
                continue
        
        # Add found sections
        for title, url in found_elements:
            if url and 'api-reference' in url.lower():
                sections.append({
                    'title': title,
                    'url': url
                })
                print(f"Added API section: {title}")
        
        if not sections:
            print("No sections found using main section names, trying alternative approach...")
            # Try to find any elements that might be API sections
            elements = driver.find_elements(By.XPATH, "//*[contains(@href, 'api-reference')]")
            for element in elements:
                try:
                    href = element.get_attribute('href')
                    text = element.text.strip()
                    if href and text and not any(ext in href.lower() for ext in ['.jpg', '.png', '.gif', '.css', '.js']):
                        sections.append({
                            'title': text,
                            'url': href
                        })
                        print(f"Found API section using alternative approach: {text}")
                except Exception as e:
                    print(f"Error processing element: {str(e)}")
                    continue
        
    except Exception as e:
        print(f"Error getting API sections: {str(e)}")
    
    return sections

def scrape_api_page(driver, url, output_dir, section_name, format='md'):
    """Scrape individual API documentation page using Selenium."""
    try:
        print(f"Navigating to {url}")
        driver.get(url)
        
        # Wait for the content to load
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Additional wait to ensure dynamic content loads
        time.sleep(5)
        
        # Create section directory
        section_dir = os.path.join(output_dir, re.sub(r'[<>:"|?*]', '_', section_name))
        os.makedirs(section_dir, exist_ok=True)
        
        # Get the rendered HTML
        page_source = driver.page_source
        
        # Save the main page content
        if format == 'md':
            content = convert_to_markdown(page_source)
        else:
            content = page_source
            
        filepath = os.path.join(section_dir, 'index')
        save_content(content, filepath, format)
        
        # Parse the page for API endpoints
        soup = BeautifulSoup(page_source, 'html.parser')
        
        # Try different selectors for API endpoints
        endpoint_selectors = [
            ['div', 'endpoint'],
            ['div', 'api-method'],
            ['section', 'api-console-section'],
            ['div', 'method-item'],
            ['div', 'api-endpoint']
        ]
        
        endpoints = []
        for tag, class_pattern in endpoint_selectors:
            found = soup.find_all(tag, class_=re.compile(class_pattern))
            if found:
                endpoints.extend(found)
                print(f"Found {len(found)} endpoints using {tag}.{class_pattern}")
        
        if endpoints:
            for i, endpoint in enumerate(endpoints):
                endpoint_content = str(endpoint.prettify())
                if format == 'md':
                    endpoint_content = convert_to_markdown(endpoint_content)
                
                endpoint_name = f"endpoint_{i+1}"
                endpoint_path = os.path.join(section_dir, endpoint_name)
                save_content(endpoint_content, endpoint_path, format)
                
            print(f"Saved {len(endpoints)} endpoints for {section_name}")
        else:
            print(f"No endpoints found in {section_name}")
        
        return True
        
    except Exception as e:
        print(f"Error scraping {url}: {str(e)}")
        return False

def scrape_ringcentral_api(base_url, output_dir, format='md'):
    """Main function to scrape RingCentral API documentation."""
    print(f"Starting to scrape RingCentral API documentation from {base_url}")
    print(f"Output format: {format}")
    
    driver = None
    try:
        driver = setup_driver()
        
        # Load the main page
        print("Loading main page...")
        driver.get(base_url)
        
        # Wait for the page to load
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Additional wait to ensure dynamic content loads
        time.sleep(5)
        
        # Save the main page
        page_source = driver.page_source
        if format == 'md':
            content = convert_to_markdown(page_source)
        else:
            content = page_source
            
        save_content(content, os.path.join(output_dir, 'index'), format)
        
        # Get all API sections
        print("Getting API sections...")
        sections = get_api_sections(driver)
        
        total_sections = len(sections)
        print(f"Found {total_sections} API sections to scrape")
        
        # Scrape each section
        for i, section in enumerate(sections, 1):
            print(f"Scraping section {i}/{total_sections}: {section['title']}")
            success = scrape_api_page(driver, section['url'], output_dir, section['title'], format)
            
            if success:
                print(f"Successfully scraped {section['title']}")
            else:
                print(f"Failed to scrape {section['title']}")
            
            # Be respectful with rate limiting
            time.sleep(2)
        
        print("Completed scraping all sections")
        
    except Exception as e:
        print(f"Error during scraping: {str(e)}")
    
    finally:
        if driver:
            driver.quit()

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Scrape RingCentral API documentation')
    parser.add_argument('url', help='URL to scrape')
    parser.add_argument('--output-dir', help='Directory to save scraped content')
    parser.add_argument('--format', choices=['md', 'html'], default='md',
                      help='Output format (default: md)')
    
    args = parser.parse_args()
    
    create_output_dir(args.output_dir)
    scrape_ringcentral_api(args.url, args.output_dir, args.format)
    print(f"Scraping completed. Content saved to {args.output_dir}")

if __name__ == "__main__":
    main()