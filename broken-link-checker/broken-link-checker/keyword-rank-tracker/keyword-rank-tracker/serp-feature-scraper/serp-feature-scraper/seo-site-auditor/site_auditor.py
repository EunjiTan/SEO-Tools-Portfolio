"""
SEO Site Auditor
Author: Tristan Plaus
Description: Comprehensive technical SEO audit tool checking meta tags, performance, and on-page elements
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import json
from datetime import datetime
import time

class SEOAuditor:
    def __init__(self, url):
        self.url = url if url.startswith('http') else f'https://{url}'
        self.domain = urlparse(self.url).netloc
        self.audit_results = {
            'url': self.url,
            'audit_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'scores': {},
            'issues': [],
            'warnings': [],
            'passed': []
        }
    
    def fetch_page(self):
        """Fetch page content and response data"""
        try:
            response = requests.get(
                self.url,
                timeout=15,
                headers={'User-Agent': 'SEO-Auditor-Bot/1.0'},
                allow_redirects=True
            )
            
            self.response = response
            self.html = response.text
            self.soup = BeautifulSoup(self.html, 'html.parser')
            self.status_code = response.status_code
            self.load_time = response.elapsed.total_seconds()
            
            return True
            
        except Exception as e:
            print(f"Error fetching page: {e}")
            return False
    
    def check_title_tag(self):
        """Audit title tag"""
        title = self.soup.find('title')
        
        if not title:
            self.audit_results['issues'].append({
                'type': 'CRITICAL',
                'element': 'Title Tag',
                'issue': 'Missing title tag'
            })
            return
        
        title_text = title.get_text().strip()
        title_length = len(title_text)
        
        if title_length == 0:
            self.audit_results['issues'].append({
                'type': 'CRITICAL',
                'element': 'Title Tag',
                'issue': 'Empty title tag'
            })
        elif title_length < 30:
            self.audit_results['warnings'].append({
                'type': 'WARNING',
                'element': 'Title Tag',
                'issue': f'Title too short ({title_length} chars). Recommended: 30-60 chars',
                'value': title_text
            })
        elif title_length > 60:
            self.audit_results['warnings'].append({
                'type': 'WARNING',
                'element': 'Title Tag',
                'issue': f'Title too long ({title_length} chars). May be truncated in SERPs',
                'value': title_text[:60] + '...'
            })
        else:
            self.audit_results['passed'].append({
                'element': 'Title Tag',
                'status': 'Good length',
                'value': title_text
            })
    
    def check_meta_description(self):
        """Audit meta description"""
        meta_desc = self.soup.find('meta', attrs={'name': 'description'})
        
        if not meta_desc:
            self.audit_results['warnings'].append({
                'type': 'WARNING',
                'element': 'Meta Description',
                'issue': 'Missing meta description'
            })
            return
        
        desc_text = meta_desc.get('content', '').strip()
        desc_length = len(desc_text)
        
        if desc_length == 0:
            self.audit_results['warnings'].append({
                'type': 'WARNING',
                'element': 'Meta Description',
                'issue': 'Empty meta description'
            })
        elif desc_length < 120:
            self.audit_results['warnings'].append({
                'type': 'WARNING',
                'element': 'Meta Description',
                'issue': f'Description too short ({desc_length} chars). Recommended: 120-160 chars',
                'value': desc_text
            })
        elif desc_length > 160:
            self.audit_results['warnings'].append({
                'type': 'WARNING',
                'element': 'Meta Description',
                'issue': f'Description too long ({desc_length} chars). May be truncated',
                'value': desc_text[:160] + '...'
            })
        else:
            self.audit_results['passed'].append({
                'element': 'Meta Description',
                'status': 'Good length',
                'value': desc_text
            })
    
    def check_headings(self):
        """Audit heading structure"""
        h1_tags = self.soup.find_all('h1')
        
        if len(h1_tags) == 0:
            self.audit_results['issues'].append({
                'type': 'CRITICAL',
                'element': 'H1 Tag',
                'issue': 'No H1 tag found'
            })
        elif len(h1_tags) > 1:
            self.audit_results['warnings'].append({
                'type': 'WARNING',
                'element': 'H1 Tag',
                'issue': f'Multiple H1 tags found ({len(h1_tags)}). Recommended: 1 per page',
                'value': [h1.get_text().strip()[:50] for h1 in h1_tags]
            })
        else:
            h1_text = h1_tags[0].get_text().strip()
            self.audit_results['passed'].append({
                'element': 'H1 Tag',
                'status': 'Single H1 found',
                'value': h1_text
            })
        
        # Check heading hierarchy
        all_headings = []
        for i in range(1, 7):
            headings = self.soup.find_all(f'h{i}')
            for h in headings:
                all_headings.append((f'H{i}', h.get_text().strip()[:50]))
        
        self.audit_results['passed'].append({
            'element': 'Heading Structure',
            'status': f'Total headings: {len(all_headings)}',
            'value': dict([(f'H{i}', len(self.soup.find_all(f'h{i}'))) for i in range(1, 7)])
        })
    
    def check_images(self):
        """Audit images for alt text"""
        images = self.soup.find_all('img')
        images_without_alt = []
        
        for img in images:
            if not img.get('alt'):
                src = img.get('src', 'unknown')[:50]
                images_without_alt.append(src)
        
        if images_without_alt:
            self.audit_results['warnings'].append({
                'type': 'WARNING',
                'element': 'Image Alt Text',
                'issue': f'{len(images_without_alt)} images missing alt text',
                'value': images_without_alt[:5]  # Show first 5
            })
        else:
            self.audit_results['passed'].append({
                'element': 'Image Alt Text',
                'status': f'All {len(images)} images have alt text'
            })
    
    def check_robots_meta(self):
        """Check robots meta tag"""
        robots_meta = self.soup.find('meta', attrs={'name': 'robots'})
        
        if robots_meta:
            content = robots_meta.get('content', '').lower()
            if 'noindex' in content:
                self.audit_results['issues'].append({
                    'type': 'CRITICAL',
                    'element': 'Robots Meta',
                    'issue': 'Page is set to NOINDEX - will not be indexed by search engines',
                    'value': content
                })
            elif 'nofollow' in content:
                self.audit_results['warnings'].append({
                    'type': 'WARNING',
                    'element': 'Robots Meta',
                    'issue': 'Page has NOFOLLOW directive',
                    'value': content
                })
            else:
                self.audit_results['passed'].append({
                    'element': 'Robots Meta',
                    'status': 'Indexable',
                    'value': content
                })
        else:
            self.audit_results['passed'].append({
                'element': 'Robots Meta',
                'status': 'No restrictions (default indexable)'
            })
    
    def check_canonical(self):
        """Check canonical URL"""
        canonical = self.soup.find('link', attrs={'rel': 'canonical'})
        
        if canonical:
            canonical_url = canonical.get('href')
            self.audit_results['passed'].append({
                'element': 'Canonical URL',
                'status': 'Present',
                'value': canonical_url
            })
            
            if canonical_url != self.url:
                self.audit_results['warnings'].append({
                    'type': 'INFO',
                    'element': 'Canonical URL',
                    'issue': 'Canonical points to different URL',
                    'value': canonical_url
                })
        else:
            self.audit_results['warnings'].append({
                'type': 'WARNING',
                'element': 'Canonical URL',
                'issue': 'No canonical URL specified'
            })
    
    def check_open_graph(self):
        """Check Open Graph tags"""
        og_tags = {
            'og:title': self.soup.find('meta', attrs={'property': 'og:title'}),
            'og:description': self.soup.find('meta', attrs={'property': 'og:description'}),
            'og:image': self.soup.find('meta', attrs={'property': 'og:image'}),
            'og:url': self.soup.find('meta', attrs={'property': 'og:url'})
        }
        
        missing_og = [tag for tag, element in og_tags.items() if not element]
        
        if missing_og:
            self.audit_results['warnings'].append({
                'type': 'WARNING',
                'element': 'Open Graph',
                'issue': f'Missing OG tags: {", ".join(missing_og)}'
            })
        else:
            self.audit_results['passed'].append({
                'element': 'Open Graph',
                'status': 'All basic OG tags present'
            })
    
    def check_schema_markup(self):
        """Check for structured data"""
        json_ld = self.soup.find_all('script', attrs={'type': 'application/ld+json'})
        
        if json_ld:
            self.audit_results['passed'].append({
                'element': 'Structured Data',
                'status': f'Found {len(json_ld)} JSON-LD block(s)'
            })
        else:
            self.audit_results['warnings'].append({
                'type': 'INFO',
                'element': 'Structured Data',
                'issue': 'No JSON-LD structured data found'
            })
    
    def check_performance(self):
        """Check basic performance metrics"""
        if self.load_time > 3:
            self.audit_results['warnings'].append({
                'type': 'WARNING',
                'element': 'Page Load Time',
                'issue': f'Slow load time: {self.load_time:.2f}s. Recommended: < 3s',
                'value': f'{self.load_time:.2f}s'
            })
        else:
            self.audit_results['passed'].append({
                'element': 'Page Load Time',
                'status': f'Good: {self.load_time:.2f}s'
            })
        
        # Check page size
        page_size_kb = len(self.html) / 1024
        if page_size_kb > 1024:
            self.audit_results['warnings'].append({
                'type': 'WARNING',
                'element': 'Page Size',
                'issue': f'Large page size: {page_size_kb:.2f} KB',
                'value': f'{page_size_kb:.2f} KB'
            })
        else:
            self.audit_results['passed'].append({
                'element': 'Page Size',
                'status': f'{page_size_kb:.2f} KB'
            })
    
    def check_links(self):
        """Analyze internal and external links"""
        all_links = self.soup.find_all('a', href=True)
        internal_links = []
        external_links = []
        
        for link in all_links:
            href = link.get('href')
            if href.startswith('http'):
                if self.domain in href:
                    internal_links.append(href)
                else:
                    external_links.append(href)
            elif href.startswith('/'):
                internal_links.append(href)
        
        self.audit_results['passed'].append({
            'element': 'Links',
            'status': f'Internal: {len(internal_links)}, External: {len(external_links)}'
        })
    
    def check_https(self):
        """Check HTTPS usage"""
        if self.url.startswith('https://'):
            self.audit_results['passed'].append({
                'element': 'HTTPS',
                'status': 'Site uses HTTPS'
            })
        else:
            self.audit_results['issues'].append({
                'type': 'CRITICAL',
                'element': 'HTTPS',
                'issue': 'Site not using HTTPS - security risk and ranking factor'
            })
    
    def calculate_score(self):
        """Calculate overall SEO score"""
        total_checks = (
            len(self.audit_results['passed']) +
            len(self.audit_results['warnings']) +
            len(self.audit_results['issues'])
        )
        
        # Scoring: passed = 1, warning = 0.5, issue = 0
        passed_score = len(self.audit_results['passed'])
        warning_score = len(self.audit_results['warnings']) * 0.5
        
        if total_checks > 0:
            score = ((passed_score + warning_score) / total_checks) * 100
        else:
            score = 0
        
        self.audit_results['scores'] = {
            'overall': round(score, 1),
            'passed': len(self.audit_results['passed']),
            'warnings': len(self.audit_results['warnings']),
            'critical_issues': len(self.audit_results['issues'])
        }
    
    def run_audit(self):
        """Run complete SEO audit"""
        print(f"\n{'='*60}")
        print(f"Running SEO Audit for: {self.url}")
        print(f"{'='*60}\n")
        
        if not self.fetch_page():
            print("Failed to fetch page!")
            return None
        
        print("✓ Page fetched successfully")
        print(f"  Status Code: {self.status_code}")
        print(f"  Load Time: {self.load_time:.2f}s\n")
        
        print("Running checks...")
        self.check_https()
        self.check_title_tag()
        self.check_meta_description()
        self.check_headings()
        self.check_images()
        self.check_robots_meta()
        self.check_canonical()
        self.check_open_graph()
        self.check_schema_markup()
        self.check_performance()
        self.check_links()
        
        self.calculate_score()
        
        print("✓ Audit complete!\n")
        return self.audit_results
    
    def print_report(self):
        """Print formatted audit report"""
        if not self.audit_results.get('scores'):
            print("No audit results available!")
            return
        
        scores = self.audit_results['scores']
        
        print("\n" + "="*60)
        print("SEO AUDIT REPORT")
        print("="*60)
        print(f"URL: {self.url}")
        print(f"Audit Date: {self.audit_results['audit_date']}\n")
        
        # Overall Score
        print(f"📊 OVERALL SEO SCORE: {scores['overall']}/100")
        print(f"   ✓ Passed: {scores['passed']}")
        print(f"   ⚠ Warnings: {scores['warnings']}")
        print(f"   ✗ Critical Issues: {scores['critical_issues']}\n")
        
        # Critical Issues
        if self.audit_results['issues']:
            print("🚨 CRITICAL ISSUES")
            print("-" * 60)
            for issue in self.audit_results['issues']:
                print(f"   ✗ {issue['element']}: {issue['issue']}")
                if 'value' in issue:
                    print(f"     Value: {issue['value']}")
            print()
        
        # Warnings
        if self.audit_results['warnings']:
            print("⚠️  WARNINGS")
            print("-" * 60)
            for warning in self.audit_results['warnings'][:10]:  # Show first 10
                print(f"   ⚠ {warning['element']}: {warning['issue']}")
            if len(self.audit_results['warnings']) > 10:
                print(f"   ... and {len(self.audit_results['warnings']) - 10} more")
            print()
        
        # Passed Checks
        print("✅ PASSED CHECKS")
        print("-" * 60)
        for passed in self.audit_results['passed'][:10]:
            print(f"   ✓ {passed['element']}: {passed['status']}")
        if len(self.audit_results['passed']) > 10:
            print(f"   ... and {len(self.audit_results['passed']) - 10} more")
        
        print("=" * 60 + "\n")
    
    def export_json(self, filename='seo_audit.json'):
        """Export audit results to JSON"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.audit_results, f, indent=2)
        print(f"Detailed report exported to: {filename}")


if __name__ == "__main__":
    # Example usage
    URL = "https://example.com"  # Replace with your URL
    
    # Run audit
    auditor = SEOAuditor(URL)
    results = auditor.run_audit()
    
    # Print report
    auditor.print_report()
    
    # Export results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    auditor.export_json(f'audit_{timestamp}.json')
