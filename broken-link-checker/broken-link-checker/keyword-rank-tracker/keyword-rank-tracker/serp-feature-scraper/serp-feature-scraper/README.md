# 🔍 SERP Feature Scraper & Analyzer

Python tool to extract and analyze Google SERP features (Featured Snippets, People Also Ask, Knowledge Panels, Local Packs, etc.) for SEO research and opportunity identification.

## 🎯 Features

- ✅ Detects **9 different SERP features**
- ✅ Featured Snippets extraction with source URL
- ✅ People Also Ask questions capture
- ✅ Knowledge Panel data extraction
- ✅ Local Pack detection
- ✅ Video carousel identification
- ✅ Image pack detection
- ✅ Site links tracking
- ✅ Top Stories/News detection
- ✅ Organic result count
- ✅ Batch analysis for multiple keywords
- ✅ Export to JSON and CSV

## 📊 Use Cases

- **Opportunity Analysis**: Find keywords with featured snippet opportunities
- **Content Strategy**: Identify PAA questions to target
- **Competitor Research**: See what SERP features competitors trigger
- **SERP Tracking**: Monitor how SERP features change over time
- **Client Reporting**: Show SERP feature presence in rankings
- **Keyword Research**: Understand search intent from SERP features

## 🚀 Quick Start

### Installation

```bash
git clone https://github.com/yourusername/serp-feature-scraper.git
cd serp-feature-scraper

pip install -r requirements.txt
```

### Basic Usage

```python
from serp_scraper import SERPScraper

# Initialize scraper
scraper = SERPScraper(language='en')

# Analyze single keyword
result = scraper.analyze_serp("best seo tools")

# Batch analyze multiple keywords
keywords = ["python tutorial", "weather today", "pizza near me"]
results = scraper.batch_analyze(keywords, delay=5)

# Print report
scraper.print_detailed_report()

# Export results
scraper.export_to_json('serp_data.json')
scraper.export_summary_csv('serp_summary.csv')
```

### Analyze Keywords from File

Create `keywords.txt`:
```
how to learn seo
best wordpress plugins
iphone 15 review
coffee shops near me
```

Run analysis:
```python
from serp_scraper import SERPScraper, load_keywords_from_file

keywords = load_keywords_from_file('keywords.txt')
scraper = SERPScraper()
results = scraper.batch_analyze(keywords)
scraper.print_detailed_report()
```

## 📦 Requirements

```
requests>=2.31.0
beautifulsoup4>=4.12.0
```

## 📈 SERP Features Tracked

| Feature | Description | SEO Impact |
|---------|-------------|------------|
| **Featured Snippet** | Answer box at position 0 | Highest CTR opportunity |
| **People Also Ask (PAA)** | Related questions | Content expansion ideas |
| **Knowledge Panel** | Entity information box | Brand authority signal |
| **Local Pack** | Map + 3 local businesses | Critical for local SEO |
| **Video Results** | Video carousel | Video content opportunity |
| **Image Pack** | Image grid results | Visual content ranking |
| **Site Links** | Sub-page links under result | Shows site authority |
| **Top Stories** | News articles | Timely content ranking |
| **Organic Results** | Standard blue links | Traditional ranking count |

## 📊 Output Formats

### JSON Export (Detailed)

```json
{
  "keyword": "best seo tools",
  "check_date": "2024-01-15",
  "featured_snippet": {
    "type": "featured_snippet",
    "present": true,
    "content": "The best SEO tools include...",
    "source_url": "https://example.com/seo-tools"
  },
  "people_also_ask": {
    "type": "people_also_ask",
    "present": true,
    "count": 4,
    "questions": [
      "What are the top 10 SEO tools?",
      "Which SEO tool is best for beginners?",
      "Are free SEO tools worth it?",
      "What tools do SEO professionals use?"
    ]
  }
}
```

### CSV Export (Summary)

| keyword | featured_snippet | people_also_ask | paa_count | knowledge_panel | local_pack | video_results | organic_count |
|---------|-----------------|-----------------|-----------|-----------------|------------|---------------|---------------|
| seo tools | TRUE | TRUE | 4 | FALSE | FALSE | TRUE | 8 |
| pizza near me | FALSE | TRUE | 3 | FALSE | TRUE | FALSE | 5 |

## 📊 Example Output

```
============================================================
Starting SERP Analysis for 3 keywords
============================================================

Analyzing SERP for: 'best seo tools'
  SERP Features: Featured Snippet, PAA (4), Videos
  Organic Results: 8

Analyzing SERP for: 'pizza near me'
  SERP Features: PAA (3), Local Pack
  Organic Results: 5

Analyzing SERP for: 'python tutorial'
  SERP Features: Featured Snippet, PAA (5), Videos, Images
  Organic Results: 9

============================================================
Analysis Complete!
============================================================

============================================================
SERP FEATURES ANALYSIS REPORT
============================================================
Total Keywords Analyzed: 3

SERP Feature Frequency:
  Featured Snippets:  2/3 (66.7%)
  People Also Ask:    3/3 (100.0%)
  Knowledge Panels:   0/3 (0.0%)
  Local Packs:        1/3 (33.3%)
  Video Results:      2/3 (66.7%)
============================================================
```

## 🎓 SEO Strategy Tips

### Featured Snippet Opportunities
- Target keywords with snippets but not owned by you
- Structure content with clear, concise answers
- Use proper heading hierarchy (H2, H3)
- Include lists, tables, and definitions

### PAA Optimization
- Create FAQ sections targeting PAA questions
- Use exact PAA questions as H2/H3 headings
- Provide comprehensive, direct answers
- Link between related PAA topics

### SERP Intent Analysis
- **Local Pack present** = Local business intent
- **Videos present** = Visual/tutorial intent
- **Featured Snippet present** = Quick answer intent
- **Knowledge Panel** = Informational/entity query

## ⚙️ Configuration

```python
SERPScraper(
    language='en',    # Search language
    location=''       # Geographic location (future feature)
)
```

### Batch Analysis Parameters

```python
scraper.batch_analyze(
    keywords=['keyword1', 'keyword2'],
    delay=5  # Seconds between requests (recommended: 3-10)
)
```

## 🛠️ Advanced Use Cases

### Track SERP Changes Over Time

```python
import schedule

def daily_serp_check():
    scraper = SERPScraper()
    keywords = load_keywords_from_file('target_keywords.txt')
    scraper.batch_analyze(keywords)
    scraper.export_summary_csv(f'serp_{datetime.now().strftime("%Y%m%d")}.csv')

schedule.every().day.at("09:00").do(daily_serp_check)
```

### Find Featured Snippet Opportunities

```python
# Analyze your target keywords
results = scraper.batch_analyze(keywords)

# Find keywords with snippets you don't own
opportunities = [
    r['keyword'] for r in scraper.results
    if r['featured_snippet']['present'] and 
       'yoursite.com' not in r['featured_snippet'].get('source_url', '')
]

print(f"Featured snippet opportunities: {opportunities}")
```

### PAA Content Ideas

```python
# Extract all PAA questions
all_questions = []
for result in scraper.results:
    if result['people_also_ask']['present']:
        all_questions.extend(result['people_also_ask']['questions'])

# Create content outline
print("Content ideas from PAA:")
for q in set(all_questions):
    print(f"  - {q}")
```

## ⚠️ Important Notes

### Rate Limiting
- Default 5-second delay between requests
- Avoid analyzing 100+ keywords in one session
- Consider spreading large batches across days

### Search Engine Policies
- Tool makes direct HTTP requests to Google
- For production use at scale, consider official APIs:
  - Google Custom Search API
  - SEO tool APIs (SEMrush, Ahrefs)
  - SERP API services

### Data Accuracy
- SERP features vary by location and personalization
- Results may differ from logged-in Google search
- Some features may not be detected due to HTML changes

## 📝 Future Enhancements

- [ ] Shopping results detection
- [ ] Related searches extraction
- [ ] Twitter cards detection
- [ ] Recipe cards and rich snippets
- [ ] Ads count and positions
- [ ] SERP volatility tracking
- [ ] Multi-location support
- [ ] Historical comparison reports

## 🤝 Contributing

Contributions welcome! Please open issues or submit PRs.

## 📄 License

MIT License - Free for personal and commercial use.

## 👤 Author

**Tristan Plaus**
- GitHub: [@EunjiTan ](https://github.com/EunjiTan)
- Email: Plaustristan@gmail.com

---

**Analyze SERPs like a pro!** 🔍📊
