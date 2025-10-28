# 🔗 SEO Broken Link Checker

A Python-based web crawler that identifies broken links, redirect chains, and site health issues for SEO auditing.

## 🎯 Features

- ✅ Crawls websites and checks all internal links
- ✅ Identifies 404 errors, broken links, and connection errors
- ✅ Detects redirect chains (harmful to SEO)
- ✅ Measures page response times
- ✅ Exports detailed CSV reports
- ✅ Respects crawl rate limits (polite crawler)
- ✅ Provides summary statistics

## 📊 Use Cases

- **Technical SEO Audits**: Identify and fix broken links that hurt rankings
- **Site Migrations**: Verify all redirects are working correctly
- **Regular Monitoring**: Schedule weekly checks for site health
- **Client Reports**: Generate professional CSV reports for clients

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/seo-broken-link-checker.git
cd seo-broken-link-checker

# Install dependencies
pip install -r requirements.txt
```

### Usage

```python
from link_checker import BrokenLinkChecker

# Initialize crawler
checker = BrokenLinkChecker(
    start_url="https://yourwebsite.com",
    max_pages=100  # Number of pages to crawl
)

# Run the crawl
results = checker.crawl()

# View summary
checker.print_summary()

# Export to CSV
checker.export_to_csv('my_site_report.csv')
```

### Command Line Usage

```bash
python link_checker.py
```

Edit the `START_URL` and `MAX_PAGES` variables in the script.

## 📦 Requirements

```
requests>=2.31.0
beautifulsoup4>=4.12.0
```

## 📈 Output Format

The CSV report includes:

| Column | Description |
|--------|-------------|
| url | The checked URL |
| status_code | HTTP status code (200, 404, 500, etc.) |
| redirect_chain | Number of redirects before final destination |
| final_url | Final URL after redirects |
| response_time | Page load time in seconds |
| error | Any connection errors |
| issue_type | Categorized issue (Broken Link, Redirect Chain, etc.) |
| timestamp | When the check was performed |

## 📊 Example Output

```
==================================================
CRAWL SUMMARY
==================================================
Total URLs checked: 50
✓ OK (200):         42
⚠ Redirects:        5
✗ Broken (404):     2
✗ Errors:           1
==================================================
```

## ⚙️ Configuration Options

```python
BrokenLinkChecker(
    start_url="https://example.com",  # Starting point for crawl
    max_pages=100                       # Maximum pages to check
)
```

## 🔍 What It Checks

- **200 OK**: Page is accessible
- **404 Not Found**: Broken link (needs fixing)
- **301/302 Redirects**: Permanent/temporary redirects
- **Redirect Chains**: Multiple redirects (bad for SEO)
- **500 Server Errors**: Server-side issues
- **Timeout/Connection Errors**: Unreachable pages

## 🎓 SEO Impact

**Why This Matters:**
- Broken links waste crawl budget
- 404 errors create poor user experience
- Redirect chains slow down page loads
- Google penalizes sites with too many errors

**Best Practices:**
- Fix all 404 errors
- Limit redirect chains to 1 hop
- Monitor site health weekly
- Update external links regularly

## 🛠️ Advanced Features

### Custom User Agent
The crawler identifies itself as `SEO-Crawler-Bot/1.0` to be transparent with webmasters.

### Rate Limiting
Built-in 0.5-second delay between requests to avoid overwhelming servers.

### Domain Restriction
Only crawls links within the same domain to focus on your site.

## 📝 Future Enhancements

- [ ] Add support for external link checking
- [ ] Integrate with Google Search Console API
- [ ] Add visualization dashboard
- [ ] Support for JavaScript-rendered content
- [ ] Parallel crawling for faster audits
- [ ] Email alerts for critical issues

## 🤝 Contributing

Contributions welcome! Please open an issue or submit a pull request.

## 📄 License

MIT License - feel free to use for personal or commercial projects.

## 👤 Author

**Tristan Plaus**
- GitHub: [@EunjiTan](https://github.com/EunjiTan)
- Email: Plaustristan@gmail.com

---

**Built with ❤️ for SEO professional and web developer**
