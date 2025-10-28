"""
SERP Feature Scraper
Author: Tristan Plaus
Description: Extracts and analyzes SERP features (Featured Snippets, PAA, Knowledge Panels, etc.)
"""

import requests
from bs4 import BeautifulSoup
import json
import csv
from datetime import datetime
from urllib.parse import quote_plus
import time

class SERPScraper:
    def __init__(self, language='en', location=''):
        self.language = language
        self.location = location
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        self.results = []
    
    def search_google(self, keyword, num_results=10):
        """Perform Google search and return HTML"""
        query = quote_plus(keyword)
        url = f"https://www.google.com/search?q={query}&num={num_results}&hl={self.language}"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"Error searching for '{keyword}': {e}")
            return None
    
    def extract_featured_snippet(self, soup):
        """Extract featured snippet if present"""
        snippet = soup.find('div', class_='xpdopen') or soup.find('div', class_='kp-blk')
        
        if snippet:
            text_content = snippet.get_text(strip=True, separator=' ')
            source_link = snippet.find('a')
            
            return {
                'type': 'featured_snippet',
                'present': True,
                'content': text_content[:500],
                'source_url': source_link.get('href') if source_link else None
            }
        
        return {'type': 'featured_snippet', 'present': False}
    
    def extract_people_also_ask(self, soup):
        """Extract People Also Ask questions"""
        paa_section = soup.find_all('div', class_='related-question-pair')
        
        questions = []
        for question_div in paa_section[:5]:  # Limit to first 5
            question_text = question_div.get_text(strip=True)
            if question_text:
                questions.append(question_text)
        
        return {
            'type': 'people_also_ask',
            'present': len(questions) > 0,
            'count': len(questions),
            'questions': questions
        }
    
    def extract_knowledge_panel(self, soup):
        """Extract Knowledge Graph/Panel data"""
        kg = soup.find('div', class_='kp-wholepage') or soup.find('div', class_='knowledge-panel')
        
        if kg:
            title = kg.find('h2')
            subtitle = kg.find('div', attrs={'data-attrid': 'subtitle'})
            description = kg.find('div', class_='kno-rdesc')
            
            return {
                'type': 'knowledge_panel',
                'present': True,
                'title': title.get_text(strip=True) if title else None,
                'subtitle': subtitle.get_text(strip=True) if subtitle else None,
                'description': description.get_text(strip=True)[:300] if description else None
            }
        
        return {'type': 'knowledge_panel', 'present': False}
    
    def extract_local_pack(self, soup):
        """Extract local pack results"""
        local_results = soup.find('div', class_='rllt__details')
        
        if local_results:
            businesses = []
            local_items = soup.find_all('div', class_='rllt__details')[:3]
            
            for item in local_items:
                name = item.find('div', class_='dbg0pd')
                businesses.append(name.get_text(strip=True) if name else 'Unknown')
            
            return {
                'type': 'local_pack',
                'present': True,
                'count': len(businesses),
                'businesses': businesses
            }
        
        return {'type': 'local_pack', 'present': False}
    
    def extract_video_results(self, soup):
        """Extract video carousel/results"""
        video_section = soup.find('g-scrolling-carousel') or soup.find('div', class_='xpdopen')
        
        if video_section and 'video' in str(video_section).lower():
            videos = video_section.find_all('a')[:3]
            video_titles = [v.get_text(strip=True) for v in videos if v.get_text(strip=True)]
            
            return {
                'type': 'video_results',
                'present': len(video_titles) > 0,
                'count': len(video_titles),
                'videos': video_titles
            }
        
        return {'type': 'video_results', 'present': False}
    
    def extract_image_pack(self, soup):
        """Extract image pack"""
        images = soup.find('div', attrs={'id': 'imagebox_bigimages'})
        
        if images:
            return {
                'type': 'image_pack',
                'present': True
            }
        
        return {'type': 'image_pack', 'present': False}
    
    def extract_site_links(self, soup):
        """Extract site links for top result"""
        sitelinks = soup.find_all('div', class_='usJj9c')
        
        if sitelinks:
            links = []
            for link in sitelinks[:6]:
                text = link.get_text(strip=True)
                if text:
                    links.append(text)
            
            return {
                'type': 'site_links',
                'present': len(links) > 0,
                'count': len(links),
                'links': links
            }
        
        return {'type': 'site_links', 'present': False}
    
    def extract_top_stories(self, soup):
        """Extract top stories/news results"""
        news = soup.find('g-section-with-header') or soup.find('div', class_='top-stories')
        
        if news and ('news' in str(news).lower() or 'stories' in str(news).lower()):
            stories = news.find_all('a')[:3]
            story_titles = [s.get_text(strip=True) for s in stories if s.get_text(strip=True)]
            
            return {
                'type': 'top_stories',
                'present': len(story_titles) > 0,
                'count': len(story_titles),
                'headlines': story_titles
            }
        
        return {'type': 'top_stories', 'present': False}
    
    def extract_organic_results(self, soup):
        """Extract standard organic results"""
        results = soup.find_all('div', class_='g')
        organic_count = 0
        
        for result in results:
            link = result.find('a')
            if link and link.get('href', '').startswith('http'):
                organic_count += 1
        
        return {
            'type': 'organic_results',
            'count': organic_count
        }
    
    def analyze_serp(self, keyword):
        """Complete SERP analysis for a keyword"""
        print(f"\nAnalyzing SERP for: '{keyword}'")
        
        html = self.search_google(keyword)
        if not html:
            return None
        
        soup = BeautifulSoup(html, 'html.parser')
        
        # Extract all SERP features
        analysis = {
            'keyword': keyword,
            'check_date': datetime.now().strftime('%Y-%m-%d'),
            'check_time': datetime.now().strftime('%H:%M:%S'),
            'featured_snippet': self.extract_featured_snippet(soup),
            'people_also_ask': self.extract_people_also_ask(soup),
            'knowledge_panel': self.extract_knowledge_panel(soup),
            'local_pack': self.extract_local_pack(soup),
            'video_results': self.extract_video_results(soup),
            'image_pack': self.extract_image_pack(soup),
            'site_links': self.extract_site_links(soup),
            'top_stories': self.extract_top_stories(soup),
            'organic_results': self.extract_organic_results(soup)
        }
        
        # Print summary
        features_present = []
        if analysis['featured_snippet']['present']:
            features_present.append('Featured Snippet')
        if analysis['people_also_ask']['present']:
            features_present.append(f"PAA ({analysis['people_also_ask']['count']})")
        if analysis['knowledge_panel']['present']:
            features_present.append('Knowledge Panel')
        if analysis['local_pack']['present']:
            features_present.append('Local Pack')
        if analysis['video_results']['present']:
            features_present.append('Videos')
        if analysis['top_stories']['present']:
            features_present.append('Top Stories')
        
        print(f"  SERP Features: {', '.join(features_present) if features_present else 'None detected'}")
        print(f"  Organic Results: {analysis['organic_results']['count']}")
        
        return analysis
    
    def batch_analyze(self, keywords, delay=5):
        """Analyze multiple keywords"""
        print(f"\n{'='*60}")
        print(f"Starting SERP Analysis for {len(keywords)} keywords")
        print(f"{'='*60}")
        
        for keyword in keywords:
            result = self.analyze_serp(keyword)
            if result:
                self.results.append(result)
            
            time.sleep(delay)  # Be polite
        
        print(f"\n{'='*60}")
        print("Analysis Complete!")
        print(f"{'='*60}\n")
        
        return self.results
    
    def export_to_json(self, filename='serp_analysis.json'):
        """Export detailed results to JSON"""
        if not self.results:
            print("No results to export!")
            return
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        print(f"Detailed results exported to: {filename}")
    
    def export_summary_csv(self, filename='serp_features_summary.csv'):
        """Export summary to CSV"""
        if not self.results:
            return
        
        rows = []
        for result in self.results:
            row = {
                'keyword': result['keyword'],
                'check_date': result['check_date'],
                'featured_snippet': result['featured_snippet']['present'],
                'people_also_ask': result['people_also_ask']['present'],
                'paa_count': result['people_also_ask'].get('count', 0),
                'knowledge_panel': result['knowledge_panel']['present'],
                'local_pack': result['local_pack']['present'],
                'video_results': result['video_results']['present'],
                'image_pack': result['image_pack']['present'],
                'site_links': result['site_links']['present'],
                'top_stories': result['top_stories']['present'],
                'organic_count': result['organic_results']['count']
            }
            rows.append(row)
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)
        
        print(f"Summary CSV exported to: {filename}")
    
    def print_detailed_report(self):
        """Print detailed analysis report"""
        if not self.results:
            return
        
        total = len(self.results)
        featured_snippet_count = sum(1 for r in self.results if r['featured_snippet']['present'])
        paa_count = sum(1 for r in self.results if r['people_also_ask']['present'])
        knowledge_panel_count = sum(1 for r in self.results if r['knowledge_panel']['present'])
        local_pack_count = sum(1 for r in self.results if r['local_pack']['present'])
        video_count = sum(1 for r in self.results if r['video_results']['present'])
        
        print("\n" + "="*60)
        print("SERP FEATURES ANALYSIS REPORT")
        print("="*60)
