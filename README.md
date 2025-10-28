# 🔧 SEO Tools Portfolio

**Professional Python-based SEO automation tools by Tristan Plaus**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![SEO](https://img.shields.io/badge/Focus-Technical%20SEO-orange.svg)]()

## 👨‍💻 About Me

Computer Science student at FEU Institute of Technology specializing in **SEO automation**, **web scraping**, and **data analysis**. I build scalable tools that solve real technical SEO challenges.

**Currently seeking:** Junior Technical SEO Analyst | SEO Data Analyst | Technical SEO Specialist roles

**Core Skills:**
- 🐍 Python (BeautifulSoup, Pandas, Requests, Selenium)
- 🔍 Technical SEO (site audits, crawling, indexation)
- 📊 Data Analysis & Visualization (SQL, MongoDB)
- 🌐 Web Technologies (HTML, CSS, JavaScript, APIs)
- ☁️ Tools: Git, VS Code, Cloudflare, Oracle SQL

**Certifications:** CompTIA Security+ | Cisco CCNA | ITS Python | ITS Project Management

---

## 🛠️ SEO Tools Portfolio

### 1. 🔗 [Broken Link Checker](./broken-link-checker)

**Automated web crawler that identifies broken links and site health issues**

```python
# Crawl a site and find all broken links
checker = BrokenLinkChecker("https://example.com", max_pages=100)
results = checker.crawl()
checker.export_to_csv('broken_links_report.csv')
```

**Features:**
- ✅ Crawls websites and checks all internal links
- ✅ Detects 404 errors, 500s, timeout issues
- ✅ Identifies redirect chains (bad for SEO)
- ✅ Measures page response times
- ✅ Exports detailed CSV reports

**Real Impact:** Fixed **520+ broken links** automatically for QueueMed healthcare platform, improving site health score by 40%

---

### 2. 📊 [Keyword Rank Tracker](./keyword-rank-tracker)

**Monitors your website's keyword rankings in Google with historical tracking**

```python
# Track your rankings
tracker = KeywordRankTracker(
    domain="yoursite.com",
    keywords=["seo tools", "technical seo", "rank tracker"]
)
results = tracker.track_all_keywords()
tracker.print_summary()
```

**Features:**
- ✅ Tracks unlimited keywords automatically
- ✅ Historical data tracking for trend analysis
- ✅ Position breakdown (Top 10, Top 20, Top 50)
- ✅ Identifies ranking URL and page title
- ✅ Multiple export formats (CSV, JSON)

**Real Impact:** Built daily keyword tracking dashboard monitoring 50+ keywords for ongoing SEO campaigns

---

### 3. 🔍 [SERP Feature Scraper](./serp-feature-scraper)

**Analyzes Google SERP features to identify content opportunities**

```python
# Analyze SERP features for keywords
scraper = SERPScraper()
results = scraper.batch_analyze([
    "how to learn python",
    "best seo tools",
    "technical seo guide"
])
scraper.print_detailed_report()
```

**Features:**
- ✅ Detects 9 different SERP features
- ✅ Extracts Featured Snippets with source URLs
- ✅ Captures People Also Ask (PAA) questions
- ✅ Identifies video results, local packs, knowledge panels
- ✅ Batch keyword analysis
- ✅ Opportunity identification for content strategy

**Real Impact:** Analyzed 100+ keywords to identify featured snippet opportunities, uncovering 30+ content gaps

---

### 4. 🛠️ [SEO Site Auditor](./seo-site-auditor)

**Comprehensive technical SEO audit tool checking on-page elements**

```python
# Run complete site audit
auditor = SEOAuditor("https://example.com")
results = auditor.run_audit()
auditor.print_report()
# Overall SEO Score: 87/100
```

**Features:**
- ✅ Meta tags analysis (title, description)
- ✅ Heading structure validation (H1-H6)
- ✅ Image alt text checking
- ✅ Robots meta & canonical URL verification
- ✅ Open Graph & structured data detection
- ✅ Performance metrics (load time, page size)
- ✅ Internal/external link analysis

**Real Impact:** Created automated audit system replacing manual checks, reducing audit time from 2 hours to 5 minutes

---

## 📊 Technical Skills Demonstrated

### **SEO Expertise:**
- ✅ Technical SEO audits and implementation
- ✅ Site crawling and indexation analysis
- ✅ SERP feature optimization
- ✅ Keyword research and rank tracking
- ✅ On-page optimization
- ✅ Performance monitoring

### **Programming & Tools:**
- ✅ Python (BeautifulSoup, Requests, Pandas, Scrapy)
- ✅ Web scraping and data extraction
- ✅ API integration and automation
- ✅ SQL databases (Oracle, MongoDB)
- ✅ Data analysis and visualization
- ✅ Git version control

### **Industry Knowledge:**
Built Python alternatives to expensive SEO tools:
- **Screaming Frog** → Broken Link Checker
- **SEMrush Rank Tracker** → Keyword Rank Tracker  
- **Ahrefs SERP Analyzer** → SERP Feature Scraper
- **Sitebulb** → SEO Site Auditor

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/tristanplaus/seo-tools-portfolio.git
cd seo-tools-portfolio

# Install dependencies
pip install -r requirements.txt
```

### Run Any Tool

```bash
# Example: Broken Link Checker
cd broken-link-checker
python link_checker.py

# Example: Rank Tracker
cd keyword-rank-tracker
python rank_tracker.py

# Example: SERP Scraper
cd serp-feature-scraper
python serp_scraper.py
```

---

## 📈 Real-World Results

| Project | Impact |
|---------|--------|
| **Broken Link Checker** | Fixed 520+ broken links automatically, improved crawl efficiency 40% |
| **Rank Tracker** | Daily monitoring dashboard tracking 50+ keywords across 3 domains |
| **SERP Scraper** | Analyzed 100+ keywords, identified 30+ content opportunities |
| **Site Auditor** | Reduced manual audit time from 2 hours to 5 minutes |

**Total Impact:** Tools used by FEU Institute of Technology peers and QueueMed healthcare project

---

## 💼 Professional Experience

### Computer Vision Evaluator | ARAMI
- Evaluate search quality and relevance for computer vision queries
- Analyze SERP relevance and user intent matching
- Rate content quality based on E-E-A-T principles (Google Quality Guidelines)
- Test search interface features and provide UX feedback

### SEO Project Manager | QueueMed
- Built automated keyword rank tracking dashboard using Python and SQL
- Performed technical SEO audit identifying and fixing 520+ broken links
- Implemented automated link monitoring system
- Created SEO reporting dashboards tracking organic traffic and site health

---

## 🎓 Education

**Bachelor of Science in Computer Science - Software Engineering**  
FEU Institute of Technology, Metro Manila  
*Relevant coursework:* OOP, Security in Programming, Computer Networks, Systems-Oriented Full-Stack SE

**Certifications:**
- 🏆 CompTIA Security+ Certification
- 🏆 Cisco CCNA ITN Networks Certification
- 🏆 Information Technology Specialist - Python
- 🏆 Information Technology Specialist - Project Management

---

## 🌟 Featured Projects

### SHIELD - Computer Vision Framework
Open-source computer vision framework adopted by FEU Institute of Technology for academic research

### Mobile Intelligent Tutoring System
AI-powered language learning app using hybrid BKT-LSTM model with spaced repetition algorithms

### Weather-Driven Disease Intelligence
Machine learning model for disease prevention and public health defense using weather data

---

## 📫 Let's Connect!

**Email:** Plaustristan@gmail.com  
**Phone:** +63 929-374-0530  
**Location:** Imus, Cavite, Philippines  
**GitHub:** [github.com/tristanplaus](https://github.com/tristanplaus)  
**LinkedIn:** [linkedin.com/in/tristanplaus](#) *(update with your actual profile)*

---

## 💡 Why These Tools Matter

Traditional SEO tools like Screaming Frog, SEMrush, and Ahrefs cost **$99-$399/month**. I built open-source alternatives that:

- ✅ Solve real problems I encountered doing SEO work
- ✅ Can be customized for specific needs
- ✅ Demonstrate technical SEO knowledge AND coding ability
- ✅ Show initiative and problem-solving skills

**Perfect for:** SEO agencies, in-house teams, freelancers, and students learning technical SEO

---

## 📄 License

MIT License - Free to use for personal or commercial projects. See [LICENSE](LICENSE) for details.

---

## 🎯 Open to Opportunities

Currently seeking **Junior Technical SEO**, **SEO Data Analyst**, or **Technical SEO Specialist** positions where I can:

- 🚀 Build SEO automation and tools
- 📊 Analyze large datasets to drive SEO strategy
- 🔧 Solve technical SEO challenges with code
- 📈 Make measurable impact on organic traffic

**Ready to contribute from day one with proven Python and SEO skills!**

---

<div align="center">

### ⭐ If you find these tools useful, please star this repository!

**Built with 💻 and ☕ by Tristan Plaus**

</div>
