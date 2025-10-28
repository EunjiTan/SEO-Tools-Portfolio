# 📊 SEO Keyword Rank Tracker

Automated Python tool to track your website's keyword rankings in Google search results over time.

## 🎯 Features

- ✅ Track unlimited keywords for your domain
- ✅ Identifies exact ranking position (1-100)
- ✅ Records ranking URL and page title
- ✅ Historical tracking with CSV append
- ✅ Multiple export formats (CSV, JSON)
- ✅ Position breakdown analysis (Top 10, Top 20, etc.)
- ✅ Load keywords from file for batch tracking

## 📊 Use Cases

- **Daily Rank Monitoring**: Track keyword positions over time
- **Competitor Analysis**: See which pages rank for target keywords
- **SEO Campaign Tracking**: Measure impact of optimization efforts
- **Client Reporting**: Generate ranking reports automatically
- **Content Strategy**: Identify ranking opportunities

## 🚀 Quick Start

### Installation

```bash
git clone https://github.com/yourusername/keyword-rank-tracker.git
cd keyword-rank-tracker

pip install -r requirements.txt
```

### Basic Usage

```python
from rank_tracker import KeywordRankTracker

# Initialize tracker
tracker = KeywordRankTracker(
    domain="yoursite.com",
    keywords=["seo tools", "keyword research", "rank tracking"]
)

# Track rankings
results = tracker.track_all_keywords(delay=5)

# View summary
tracker.print_summary()

# Export results
tracker.export_to_csv('my_rankings.csv')
tracker.append_to_history('ranking_history.csv')
```

### Track Keywords from File

Create `keywords.txt`:
```
seo tools
keyword research
backlink analysis
technical seo
on-page optimization
```

Then run:
```python
from rank_tracker import load_keywords_from_file

keywords = load_keywords_from_file('keywords.txt')
tracker = KeywordRankTracker("yoursite.com", keywords)
results = tracker.track_all_keywords()
```

## 📦 Requirements

```
requests>=2.31.0
beautifulsoup4>=4.12.0
```

## 📈 Output Format

### CSV Export

| Column | Description |
|--------|-------------|
| keyword | The search keyword |
| domain | Your domain being tracked |
| position | Ranking position (1-100) or None |
| ranking_url | The specific URL that's ranking |
| page_title | Page title in search results |
| found_in_top_100 | Boolean: whether domain ranks |
| total_results_found | Number of results parsed |
| check_date | Date of the check |
| check_time | Time of the check |
| timestamp | Full ISO timestamp |

### Example Output

```
==================================================
RANKING SUMMARY FOR yoursite.com
==================================================
Total Keywords Tracked: 10

📊 Position Breakdown:
  Top 10:       3 keywords
  Position 11-20:  2 keywords
  Position 21-50:  3 keywords
  Position 51-100: 1 keywords
  Not in Top 100:  1 keywords

🏆 Top Performing Keywords:
  #2: seo tools
  #5: keyword tracker
  #8: rank monitoring
==================================================
```

## ⚙️ Configuration

```python
KeywordRankTracker(
    domain="example.com",      # Your domain to track
    keywords=["keyword1"],      # List of keywords
    location='',                # Geographic location (future)
    language='en'               # Search language
)
```

### Tracking Parameters

```python
tracker.track_all_keywords(
    delay=5  # Seconds between searches (recommended: 3-10)
)
```

## 📊 Historical Tracking

The `append_to_history()` function maintains a cumulative CSV file:

```python
# Run daily/weekly
tracker.track_all_keywords()
tracker.append_to_history('ranking_history.csv')
```

This creates a time-series dataset for trend analysis:
- Track ranking improvements over time
- Identify ranking fluctuations
- Measure SEO campaign ROI
- Spot algorithm update impacts

## 🎓 SEO Insights

**Why Track Rankings:**
- Monitor SEO progress and ROI
- Identify high-performing content
- Spot ranking drops early
- Validate optimization strategies
- Understand SERP competition

**Best Practices:**
- Track 10-50 core keywords regularly
- Include brand and non-brand terms
- Monitor competitor rankings
- Track featured snippet opportunities
- Review weekly/monthly trends

## ⚠️ Important Notes

### Rate Limiting
- Built-in delay between requests (default: 5 seconds)
- Avoid checking 100+ keywords in one session
- Spread large keyword lists across multiple runs

### Search Engine Guidelines
- This tool makes direct HTTP requests to Google
- For production use, consider:
  - Google Custom Search API (official)
  - SEO tool APIs (SEMrush, Ahrefs, Moz)
  - Search Console API for your own site

### Accuracy
- Tracks organic results only (no ads)
- Results may vary by:
  - User location
  - Search personalization
  - Time of day
  - Device type

## 🛠️ Advanced Features

### Scheduled Tracking with Cron

```bash
# Track daily at 9 AM
0 9 * * * cd /path/to/tracker && python rank_tracker.py
```

### Integrate with Data Visualization

```python
import pandas as pd
import matplotlib.pyplot as plt

# Load historical data
df = pd.read_csv('ranking_history.csv')

# Plot trends
df.groupby(['check_date', 'keyword'])['position'].first().unstack().plot()
plt.title('Keyword Ranking Trends')
plt.ylabel('Position')
plt.gca().invert_yaxis()  # Lower numbers = better
plt.show()
```

## 📝 Future Enhancements

- [ ] Add support for multiple search engines (Bing, Yahoo)
- [ ] Track SERP features (featured snippets, PAA, local pack)
- [ ] Competitor comparison mode
- [ ] Email alerts for major ranking changes
- [ ] Integration with Google Search Console
- [ ] Automated chart generation
- [ ] Support for location-specific searches

## 🤝 Contributing

Found a bug or have a feature idea? Open an issue or submit a PR!

## 📄 License

MIT License - Use freely for personal or commercial projects.

## 👤 Author

**Tristan Plaus**
- GitHub: [@EunjiTan ](https://github.com/EunjiTan)
- Email: Plaustristan@gmail.com

---

**Built with ❤️ for SEO professional and web developer**
