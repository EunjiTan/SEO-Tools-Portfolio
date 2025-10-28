"""
SEO Keyword Rank Tracker
Author: Tristan Plaus
Description: Tracks keyword rankings in Google search results over time.
"""

import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import time
import json
import os
from urllib.parse import quote_plus

class KeywordRankTracker:
    def __init__(self, domain, keywords, location='', language='en'):
        self.domain = domain
        self.keywords = keywords if isinstance(keywords, list) else [keywords]
        self.location = location
        self.language = language
        self.results = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def search_google(self, keyword, num_results=100):
        """
        Search Google for a keyword and return results.
        Note: For production use, consider Google Custom Search API or SEO tools API.
        """
        query = quote_plus(keyword)
        url = f"https://www.google.com/search?q={query}&num={num_results}&hl={self.language}"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"Error searching for '{keyword}': {e}")
            return None
    
    def parse_serp(self, html_content):
        """Extract organic search results from Google SERP"""
        soup = BeautifulSoup(html_content, 'html.parser')
        results = []
        
        # Find search result divs (Google's structure changes, this is a common pattern)
        search_results = soup.find_all('div', class_='g')
        
        for idx, result in enumerate(search_results, 1):
            try:
                # Extract URL
                link_tag = result.find('a')
                if not link_tag:
                    continue
                    
                url = link_tag.get('href', '')
                
                # Extract title
                title_tag = result.find('h3')
                title = title_tag.get_text() if title_tag else 'No title'
                
                # Extract snippet
                snippet_tag = result.find('div', class_='VwiC3b')
                snippet = snippet_tag.get_text() if snippet_tag else ''
                
                results.append({
                    'position': idx,
                    'url': url,
                    'title': title,
                    'snippet': snippet[:200]
                })
                
            except Exception as e:
                continue
        
        return results
    
    def find_domain_position(self, serp_results):
        """Find the position of our domain in search results"""
        for result in serp_results:
            if self.domain.lower() in result['url'].lower():
                return {
                    'position': result['position'],
                    'url': result['url'],
                    'title': result['title'],
                    'found': True
                }
        
        return {
            'position': None,
            'url': None,
            'title': None,
            'found': False
        }
    
    def check_keyword(self, keyword):
        """Check ranking for a single keyword"""
        print(f"Checking: '{keyword}'")
        
        html = self.search_google(keyword)
        if not html:
            return None
        
        serp_results = self.parse_serp(html)
        domain_result = self.find_domain_position(serp_results)
        
        result = {
            'keyword': keyword,
            'domain': self.domain,
            'position': domain_result['position'],
            'ranking_url': domain_result['url'],
            'page_title': domain_result['title'],
            'found_in_top_100': domain_result['found'],
            'total_results_found': len(serp_results),
            'check_date': datetime.now().strftime('%Y-%m-%d'),
            'check_time': datetime.now().strftime('%H:%M:%S'),
            'timestamp': datetime.now().isoformat()
        }
        
        if domain_result['found']:
            print(f"  ✓ Ranking at position {domain_result['position']}")
        else:
            print(f"  ✗ Not found in top 100")
        
        return result
    
    def track_all_keywords(self, delay=5):
        """Track all keywords with delay between requests"""
        print(f"\nTracking {len(self.keywords)} keywords for domain: {self.domain}\n")
        
        for keyword in self.keywords:
            result = self.check_keyword(keyword)
            if result:
                self.results.append(result)
            
            # Be polite - don't hammer Google
            time.sleep(delay)
        
        print(f"\nTracking complete! Checked {len(self.results)} keywords.")
        return self.results
    
    def export_to_csv(self, filename='keyword_rankings.csv'):
        """Export results to CSV"""
        if not self.results:
            print("No results to export!")
            return
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=self.results[0].keys())
            writer.writeheader()
            writer.writerows(self.results)
        
        print(f"\nResults exported to: {filename}")
    
    def append_to_history(self, filename='ranking_history.csv'):
        """Append results to historical tracking file"""
        file_exists = os.path.isfile(filename)
        
        with open(filename, 'a', newline='', encoding='utf-8') as f:
            if self.results:
                writer = csv.DictWriter(f, fieldnames=self.results[0].keys())
                
                if not file_exists:
                    writer.writeheader()
                
                writer.writerows(self.results)
        
        print(f"Results appended to history: {filename}")
    
    def print_summary(self):
        """Print summary of rankings"""
        if not self.results:
            return
        
        ranked = [r for r in self.results if r['found_in_top_100']]
        not_ranked = [r for r in self.results if not r['found_in_top_100']]
        
        top_10 = [r for r in ranked if r['position'] <= 10]
        top_20 = [r for r in ranked if 11 <= r['position'] <= 20]
        top_50 = [r for r in ranked if 21 <= r['position'] <= 50]
        
        print("\n" + "="*60)
        print(f"RANKING SUMMARY FOR {self.domain}")
        print("="*60)
        print(f"Total Keywords Tracked: {len(self.results)}")
        print(f"\n📊 Position Breakdown:")
        print(f"  Top 10:       {len(top_10)} keywords")
        print(f"  Position 11-20:  {len(top_20)} keywords")
        print(f"  Position 21-50:  {len(top_50)} keywords")
        print(f"  Position 51-100: {len(ranked) - len(top_10) - len(top_20) - len(top_50)} keywords")
        print(f"  Not in Top 100:  {len(not_ranked)} keywords")
        
        if top_10:
            print(f"\n🏆 Top Performing Keywords:")
            for result in sorted(top_10, key=lambda x: x['position'])[:5]:
                print(f"  #{result['position']}: {result['keyword']}")
        
        print("="*60)
    
    def export_to_json(self, filename='rankings.json'):
        """Export results to JSON for easy parsing"""
        if not self.results:
            return
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"JSON export saved to: {filename}")


def load_keywords_from_file(filename):
    """Load keywords from a text file (one per line)"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"File {filename} not found!")
        return []


if __name__ == "__main__":
    # Configuration
    DOMAIN = "example.com"  # Your domain to track
    
    # Option 1: List keywords directly
    KEYWORDS = [
        "seo tools",
        "keyword research",
        "backlink checker",
        "rank tracker"
    ]
    
    # Option 2: Load from file (uncomment to use)
    # KEYWORDS = load_keywords_from_file('keywords.txt')
    
    # Initialize tracker
    tracker = KeywordRankTracker(
        domain=DOMAIN,
        keywords=KEYWORDS,
        language='en'
    )
    
    # Track rankings
    results = tracker.track_all_keywords(delay=5)  # 5 second delay between searches
    
    # Print summary
    tracker.print_summary()
    
    # Export results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    tracker.export_to_csv(f'rankings_{timestamp}.csv')
    tracker.append_to_history('ranking_history.csv')
    tracker.export_to_json(f'rankings_{timestamp}.json')
