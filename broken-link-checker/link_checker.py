"""
SEO Broken Link Checker
Author: Tristan Plaus
Description: Crawls a website and identifies broken links, redirect chains, and site health issues.
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import csv
from datetime import datetime
import time
from collections import deque

class BrokenLinkChecker:
    def __init__(self, start_url, max_pages=100):
        self.start_url = start_url
        self.domain = urlparse(start_url).netloc
        self.visited = set()
        self.to_visit = deque([start_url])
        self.max_pages = max_pages
        self.results = []
        
    def is_valid_url(self, url):
        """Check if URL belongs to the same domain"""
        parsed = urlparse(url)
        return parsed.netloc == self.domain or parsed.netloc == ''
    
    def get_links(self, url, html_content):
        """Extract all links from a page"""
        soup = BeautifulSoup(html_content, 'html.parser')
        links = []
        
        for link in soup.find_all('a', href=True):
            href = link.get('href')
            full_url = urljoin(url, href)
            
            # Only include HTTP/HTTPS links from same domain
            if full_url.startswith('http') and self.is_valid_url(full_url):
                links.append({
                    'url': full_url,
                    'anchor_text': link.get_text(strip=True)[:100],
                    'source_page': url
                })
        
        return links
    
    def check_url(self, url):
        """Check if a URL is accessible and return status"""
        try:
            response = requests.get(
                url, 
                timeout=10,
                allow_redirects=True,
                headers={'User-Agent': 'SEO-Crawler-Bot/1.0'}
            )
            
            redirect_chain = len(response.history)
            
            return {
                'status_code': response.status_code,
                'redirect_chain': redirect_chain,
                'final_url': response.url if redirect_chain > 0 else url,
                'response_time': response.elapsed.total_seconds(),
                'error': None
            }
            
        except requests.exceptions.Timeout:
            return {'status_code': 0, 'redirect_chain': 0, 'final_url': url, 
                    'response_time': 0, 'error': 'Timeout'}
        except requests.exceptions.ConnectionError:
            return {'status_code': 0, 'redirect_chain': 0, 'final_url': url, 
                    'response_time': 0, 'error': 'Connection Error'}
        except Exception as e:
            return {'status_code': 0, 'redirect_chain': 0, 'final_url': url, 
                    'response_time': 0, 'error': str(e)}
    
    def crawl(self):
        """Main crawling function"""
        print(f"Starting crawl of {self.start_url}")
        print(f"Max pages: {self.max_pages}\n")
        
        page_count = 0
        
        while self.to_visit and page_count < self.max_pages:
            current_url = self.to_visit.popleft()
            
            if current_url in self.visited:
                continue
            
            self.visited.add(current_url)
            page_count += 1
            
            print(f"[{page_count}/{self.max_pages}] Checking: {current_url}")
            
            # Check current URL
            status = self.check_url(current_url)
            
            # Record result
            result = {
                'url': current_url,
                'status_code': status['status_code'],
                'redirect_chain': status['redirect_chain'],
                'final_url': status['final_url'],
                'response_time': round(status['response_time'], 2),
                'error': status['error'],
                'issue_type': self.categorize_issue(status),
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            self.results.append(result)
            
            # If page is accessible, extract links
            if status['status_code'] == 200 and status['error'] is None:
                try:
                    response = requests.get(current_url, timeout=10)
                    links = self.get_links(current_url, response.text)
                    
                    # Add new links to queue
                    for link in links:
                        if link['url'] not in self.visited:
                            self.to_visit.append(link['url'])
                            
                except Exception as e:
                    print(f"  Error extracting links: {e}")
            
            time.sleep(0.5)  # Be polite to the server
        
        print(f"\nCrawl complete! Checked {page_count} pages.")
        return self.results
    
    def categorize_issue(self, status):
        """Categorize the type of issue found"""
        if status['error']:
            return 'Connection Error'
        elif status['status_code'] == 404:
            return 'Broken Link (404)'
        elif status['status_code'] == 403:
            return 'Forbidden (403)'
        elif status['status_code'] == 500:
            return 'Server Error (500)'
        elif status['redirect_chain'] > 2:
            return 'Redirect Chain'
        elif status['redirect_chain'] > 0:
            return 'Redirect'
        elif status['status_code'] == 200:
            return 'OK'
        else:
            return f'Other ({status["status_code"]})'
    
    def export_to_csv(self, filename='broken_links_report.csv'):
        """Export results to CSV"""
        if not self.results:
            print("No results to export!")
            return
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=self.results[0].keys())
            writer.writeheader()
            writer.writerows(self.results)
        
        print(f"\nReport exported to: {filename}")
    
    def print_summary(self):
        """Print summary of findings"""
        if not self.results:
            return
        
        broken = sum(1 for r in self.results if r['status_code'] == 404)
        errors = sum(1 for r in self.results if r['error'] is not None)
        redirects = sum(1 for r in self.results if r['redirect_chain'] > 0)
        ok = sum(1 for r in self.results if r['status_code'] == 200 and r['redirect_chain'] == 0)
        
        print("\n" + "="*50)
        print("CRAWL SUMMARY")
        print("="*50)
        print(f"Total URLs checked: {len(self.results)}")
        print(f"✓ OK (200):         {ok}")
        print(f"⚠ Redirects:        {redirects}")
        print(f"✗ Broken (404):     {broken}")
        print(f"✗ Errors:           {errors}")
        print("="*50)


if __name__ == "__main__":
    # Example usage
    START_URL = "https://example.com"  # Replace with your target URL
    MAX_PAGES = 50  # Number of pages to crawl
    
    # Initialize and run crawler
    checker = BrokenLinkChecker(START_URL, max_pages=MAX_PAGES)
    results = checker.crawl()
    
    # Print summary
    checker.print_summary()
    
    # Export results
    checker.export_to_csv(f'link_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv')
