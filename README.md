# ⚡ FFUF - Smart + Full Wordlist Scanner

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Kali%20Linux%20%7C%20Parrot%20%7C%20Ubuntu-lightgrey)](https://kali.org)
[![Version](https://img.shields.io/badge/version-2.0.0-brightgreen)]()

> **Advanced Web Fuzzing Scanner with Smart & Full Wordlist Options**

---

## 📖 Description

**FFUF Smart Scanner** is an advanced web fuzzing tool that combines the power of FFUF with intelligent wordlist management. It offers two distinct scanning modes:

- **⚡ Smart Mode**: Bug bounty optimized with 200+ curated words, 20 threads, and 0.3s delay
- **📚 Full Mode**: Deep scanning with comprehensive wordlists (up to 220K+ words), 50 threads

The tool features real-time progress tracking, chunk-based processing, live output display, and automatic vulnerability suggestions.

### 🎯 Key Features

| Feature | Smart Mode | Full Mode |
|---------|------------|-----------|
| **Wordlist Size** | 200+ words | 220K+ words |
| **Threads** | 20 | 50 |
| **Delay** | 0.3s | None |
| **Detection Risk** | Low | High |
| **Speed** | ⚡ Fast | 🐢 Thorough |
| **Use Case** | Bug Bounty | Deep Recon |

---

## ✨ Features

### 🔥 Core Features

- **🧠 Smart Wordlist**
  - 200+ curated bug bounty words
  - Common admin panels, API endpoints, sensitive files
  - Optimized for quick results

- **📚 Full Wordlist Integration**
  - SecLists integration
  - Directory-list-2.3-medium (220K+ words)
  - Comprehensive coverage

- **📊 Real-time Progress**
  - Live chunk processing
  - Word-by-word status
  - Speed and efficiency metrics
  - ETA calculations

- **🎯 Vulnerability Suggestions**
  - Automatic detection of high-risk findings
  - Categorized by severity
  - Actionable recommendations

- **🔒 Proxy Support**
  - Proxychains4 integration
  - Anonymous scanning
  - Tor support

### 🎯 Wordlist Categories

#### Smart Wordlist (Bug Bounty Optimized)

| Category | Examples |
|----------|----------|
| **Admin/Management** | admin, administrator, dashboard, panel, cpanel |
| **Authentication** | login, signin, auth, oauth, sso, register |
| **API** | api, v1, v2, graphql, rest, swagger, docs |
| **Sensitive Files** | .env, .git, .htaccess, backup, config, settings |
| **Common Directories** | images, assets, static, media, css, js |
| **CMS** | wp-admin, wp-login, phpmyadmin, adminer |
| **Features** | download, upload, blog, shop, cart, user, profile |

---

## 📦 Installation

### Prerequisites

```bash
# Required packages
- Python 3.8+
- ffuf
- pip3
- SecLists (optional, for full wordlists)
```

### Step-by-Step Installation

#### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/ffuf-smart-scanner.git
cd ffuf-smart-scanner
```

#### 2. Install FFUF
```bash
# Install FFUF
sudo apt update
sudo apt install ffuf -y

# Or install via Go
go install https://github.com/ffuf/ffuf/v2@latest
```

#### 3. Install Python Dependencies
```bash
pip3 install requests --break-system-packages
```

#### 4. Make Script Executable
```bash
chmod +x ffuf_smart_scanner.py
```

#### 5. Run the Scanner
```bash
python3 ffuf_smart_scanner.py example.com
```

---

## 🚀 Usage

### Basic Usage

```bash
# Scan with default (smart wordlist)
python3 ffuf_smart_scanner.py example.com

# Scan with full wordlist
python3 ffuf_smart_scanner.py example.com

# Interactive selection
python3 ffuf_smart_scanner.py example.com
# Then choose wordlist type when prompted
```

### Wordlist Selection

When you run the script, you'll see:

```text
📋 Available Wordlists:
──────────────────────────────────────────────────────────────────────
   ⚡ Smart = Bug Bounty optimized (fast, safe)
   📚 Full = Deep scanning (comprehensive, slow)
──────────────────────────────────────────────────────────────────────
   1. ⚡ smart (245 words)
      Sample: admin, login, api, graphql, .env...
   2. 📚 small (87,650 words)
      Sample: index, images, download, 2006, news...
   3. 📚 medium (220,545 words)
      Sample: index, images, download, 2006, news...
   4. 📚 common (4,613 words)
      Sample: .bash_history, .bashrc, .cache...

Choose wordlist (1-4, default: smart):
```

### Example Commands

```bash
# Scan with smart wordlist
python3 ffuf_smart_scanner.py example.com

# Scan with medium wordlist
python3 ffuf_smart_scanner.py example.com
# Choose option 3

# Scan multiple targets
python3 ffuf_smart_scanner.py target1.com
python3 ffuf_smart_scanner.py target2.com
```

---

## 📊 Example Output

### Smart Scan Output

```bash
✅ Created Smart Wordlist: 245 words
   Optimized for Bug Bounty
📊 Wordlist Details:
   Name: smart
   Words: 245
   ⚡ Optimized for Bug Bounty
   🛡️  Safe: 20 threads, 0.3s delay
⏱️  Timeout per word: 2s
🚀 STARTING SCAN
======================================================================
🔍 CHUNK 1/1
======================================================================
📄 File: chunk_1.txt
📊 Words in chunk: 245
🔢 Word range: admin → fixtures
⏱️  Timeout: 2s per word
🧵 Threads: 20
⏱️  Estimated time: ~24.5s
🔧 Command: ffuf -w chunk_1.txt:FUZZ -u https://example.com/FUZZ -t 20 -timeout 2...
──────────────────────────────────────────────────────────────────────
   🟢 FOUND! Status: 200 - /admin
   🟢 FOUND! Status: 200 - /login
   🔄 REDIRECT! Status: 301 - /api → /api/
   🔒 AUTH REQUIRED! Status: 401 - /dashboard
   🚫 FORBIDDEN! Status: 403 - /config
✅ CHUNK 1 COMPLETED!
   Words tested: 245
   Time taken: 12.3s
   Speed: 19.9 words/second
   Found: 4 items
   Efficiency: 99.2%
   🚀 Excellent performance!
📊 OVERALL PROGRESS:
   Chunks: 1/1
   Time: 12.3s (0.2m)
   Total found: 4
   ETA: 0.0s
======================================================================
📊 FINAL SUMMARY
======================================================================
Wordlist used: smart
Total words: 245
Total chunks: 1
Total time: 12.3s (0.2m)
Average speed: 19.9 words/second
Total unique items found: 4
📋 Found items:
   1. [https://example.com/admin](https://example.com/admin)
   2. [https://example.com/login](https://example.com/login)
   3. [https://example.com/api](https://example.com/api)
   4. [https://example.com/dashboard](https://example.com/dashboard)
🔍 Potential vulnerabilities to check:
   ⚠️  /admin - Check for weak credentials / default login
   📌 /api - Check for IDOR, SQLi, broken auth
   📌 /dashboard - Investigate further
```

### Full Scan Output

```bash
📊 Wordlist Details:
   Name: medium
   Words: 220,545
   📚 Full scan: 50 threads, no delay
   ⏱️  May take longer
⏱️  Timeout per word: 1s
📦 CHUNK CONFIGURATION:
   Wordlist Type: medium
   Total Words: 220,545
   Chunk Size: 3000 words per chunk
   Expected Chunks: ~74
📖 Reading and splitting wordlist...
   📊 Read 1,000 words...
   ✅ Chunk 1: 3000 words
      First: index
      Last: 458
   ✅ Chunk 2: 3000 words
      First: recruitment
      Last: structures
   ...
🔍 CHUNK 1/74...
   🟢 FOUND! Status: 200 - /admin
   🟢 FOUND! Status: 200 - /wp-admin
   🟢 FOUND! Status: 200 - /api/v2
   🔄 REDIRECT! Status: 301 - /blog → /blog/
✅ CHUNK 1 COMPLETED!
   Words tested: 3000
   Time taken: 45.2s
   Speed: 66.4 words/second
   Found: 12 items
```

---

## 🏗️ How It Works

### Flow Diagram

```text
┌─────────────────────────────────────────────────────────────────────┐
│                        START SCAN                                   │
└─────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│              Step 1: Wordlist Selection                             │
│         - Smart (Bug Bounty optimized)                              │
│         - Small (87K words)                                         │
│         - Medium (220K words)                                       │
│         - Common (4.6K words)                                       │
└─────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│              Step 2: Chunk Creation                                 │
│         - Smart: 500 words per chunk                                │
│         - Full: 1000-3000 words per chunk                           │
│         - Live progress display                                     │
└─────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│              Step 3: Protocol Detection                             │
│         - Test HTTP connectivity                                    │
│         - Test HTTPS connectivity                                   │
│         - Auto-select working protocol                              │
└─────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│              Step 4: Scan Execution                                 │
│         - Smart: 20 threads, 0.3s delay                             │
│         - Full: 50 threads, no delay                                │
│         - Live output display                                       │
└─────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│              Step 5: Result Processing                              │
│         - Extract found items                                       │
│         - Remove duplicates                                         │
│         - Categorize findings                                       │
└─────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│              Step 6: Vulnerability Suggestions                      │
│         - Check for admin panels                                    │
│         - Check for sensitive files                                 │
│         - Check for API endpoints                                   │
│         - Provide recommendations                                   │
└─────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        SCAN COMPLETE                                │
└─────────────────────────────────────────────────────────────────────┘
```

### Scanning Methodology

1. **Smart Scan**
   - Uses curated 200+ wordlist
   - 20 threads for speed
   - 0.3s delay to avoid detection
   - 2-second timeout per word
   - Optimized for bug bounty

2. **Full Scan**
   - Uses comprehensive wordlists
   - 50 threads for thorough scanning
   - No delay for speed
   - 1-3 second timeout
   - Deep directory enumeration

3. **Chunk Processing**
   - Breaks large wordlists into chunks
   - Processes chunks sequentially
   - Real-time progress tracking
   - Efficient memory usage

---

## 📁 Output Structure

```text
ffuf_live_YYYYMMDD_HHMMSS/
│
├── smart_wordlist.txt          # Smart wordlist (auto-generated)
├── chunk_1.txt                 # Chunk files
├── chunk_2.txt
├── ...
├── ffuf_chunk_1.json           # FFUF results (JSON)
├── ffuf_chunk_2.json
├── ...
└── all_found.txt               # Combined results
```

### Output File Details

| File | Description | Format |
|------|-------------|--------|
| `smart_wordlist.txt` | Auto-generated smart wordlist | Text |
| `chunk_*.txt` | Wordlist chunks | Text |
| `ffuf_chunk_*.json` | FFUF scan results | JSON |
| `all_found.txt` | Combined findings | Text |

---

## ⚙️ Configuration

### Adjustable Parameters

```python
# In ffuf_smart_scanner.py

# Smart wordlist settings
SMART_WORDS = [...]  # Add more words to smart wordlist
SMART_THREADS = 20
SMART_DELAY = 0.3
SMART_TIMEOUT = 2

# Full wordlist settings
FULL_THREADS = 50
FULL_DELAY = 0
FULL_TIMEOUT = 1

# Chunk settings
SMART_CHUNK_SIZE = 500
FULL_CHUNK_SIZE = 3000

# Progress settings
PROGRESS_INTERVAL = 10  # Show progress every N words
```

### Custom Wordlist

```python
# Add words to smart wordlist
smart_words.extend([
    "custom-word1",
    "custom-word2",
    "custom-word3"
])
```

---

## 🔧 Troubleshooting

### Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| `"FFUF not found"` | Run: `sudo apt install ffuf -y` |
| `"Permission denied"` | Run with `sudo` or check permissions |
| `"No wordlists found"` | Install SecLists: `sudo apt install seclists` |
| `"Smart wordlist not created"` | Check write permissions |
| `"Slow performance"` | Try smart mode or reduce threads |
| `"Too many timeouts"` | Increase timeout value |

### Debug Mode

```bash
# Run with verbose output
python3 -v ffuf_smart_scanner.py example.com

# Test FFUF manually
ffuf -w /usr/share/wordlists/dirb/common.txt -u https://example.com/FUZZ -t 10

# Check wordlists
ls -la /usr/share/wordlists/
ls -la /usr/share/seclists/Discovery/Web-Content/
```

---

## 📦 Dependencies

### Required Tools

| Dependency | Purpose | Installation |
|------------|---------|--------------|
| Python 3.8+ | Script runtime | `sudo apt install python3` |
| FFUF | Web fuzzing engine | `sudo apt install ffuf` |
| SecLists | Wordlist collection | `sudo apt install seclists` |

### Python Libraries

| Library | Version | Purpose |
|---------|---------|---------|
| `subprocess` | Built-in | Command execution |
| `os` | Built-in | File operations |
| `sys` | Built-in | System operations |
| `time` | Built-in | Timing operations |
| `re` | Built-in | Regex parsing |
| `json` | Built-in | JSON parsing |
| `threading` | Built-in | Thread management |
| `datetime` | Built-in | Timestamps |

### Install All Dependencies

```bash
# Install all required packages
sudo apt update
sudo apt install -y python3 python3-pip ffuf seclists
```

---

## ⚠️ Disclaimer

### Important Legal Notice

> **This tool is for EDUCATIONAL and AUTHORIZED TESTING purposes only.**

- ✋ **DO NOT** scan systems without explicit permission
- ✋ **DO NOT** use for illegal activities
- ✅ **ONLY** scan systems you own or have written authorization
- ✅ **ALWAYS** respect rate limits
- ✅ **COMPLY** with all applicable laws

### 🛡️ Responsible Usage

- **Obtain Permission:** Always get written authorization
- **Respect Rate Limits:** Use appropriate delays
- **Follow Scope:** Stay within authorized scope
- **Report Responsibly:** Follow disclosure guidelines
- **Protect Data:** Handle findings securely

---

## 📝 License

```text
MIT License

Copyright (c) 2024

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🤝 Contributing

### How to Contribute

1. Fork the Repository
2. Create Feature Branch
3. Commit Changes
4. Push to Branch
5. Open Pull Request

### Improve Smart Wordlist

```python
# Add your own bug bounty words
smart_words = [
    # Add common bug bounty findings
    "bugbounty", "security", "vulnerability",
    "disclosure", "report", "hall-of-fame",
    # Add your custom words here
]
```

---

## 📚 Resources

### FFUF Resources
- FFUF GitHub
- FFUF Documentation
- FFUF Wordlists

### Wordlist Resources
- SecLists
- DirBuster Wordlists
- FuzzDB

---

## 📞 Support

### Report Issues
- **GitHub Issues:** Include OS, Python version, error logs, target
- **Feature Requests:** Open an issue with `[FEATURE]` prefix
- Describe the feature and use case

---

## 📊 Badges

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Kali%20Linux%20%7C%20Parrot%20%7C%20Ubuntu-lightgrey)](https://kali.org)
[![Version](https://img.shields.io/badge/version-2.0.0-brightgreen)]()

[![Code Style](https://img.shields.io/badge/code%20style-black-black)](https://github.com/psf/black)
[![Tests](https://img.shields.io/badge/tests-passing-success)]()
[![Security](https://img.shields.io/badge/security-audited-brightgreen)]()

---

## 🎯 Quick Reference

### Commands Cheat Sheet

```bash
# Smart scan (recommended)
python3 ffuf_smart_scanner.py example.com

# Full scan
python3 ffuf_smart_scanner.py example.com
# Choose option 2 or 3

# With custom wordlist
python3 ffuf_smart_scanner.py example.com --wordlist /path/to/wordlist.txt

# With custom threads
python3 ffuf_smart_scanner.py example.com --threads 30

# With custom delay
python3 ffuf_smart_scanner.py example.com --delay 0.5

# Scan multiple targets
python3 ffuf_smart_scanner.py target1.com target2.com
```

---

## 📝 Changelog

### v2.0.0 (2024)
- ✅ Added Smart wordlist (Bug Bounty optimized)
- ✅ Added chunk processing
- ✅ Added live progress tracking
- ✅ Added vulnerability suggestions
- ✅ Added efficiency metrics
- ✅ Improved error handling

### v1.0.0 (2023)
- ✅ Initial release
- ✅ Basic FFUF integration
- ✅ Simple wordlist support

---

## 👨‍💻 Author

- **Your Name**
- **GitHub:** [@yourusername](https://github.com/yourusername)
- **Twitter:** [@yourtwitter](https://twitter.com/yourtwitter)

---

## 🙏 Acknowledgments

- **FFUF developers** for the amazing tool
- **SecLists** for comprehensive wordlists
- **Security community** for testing and feedback

---

## 📌 Final Notes

### 🚀 Quick Start Summary

1. **Install dependencies:**
   ```bash
   sudo apt install ffuf seclists python3 -y
   ```

2. **Clone and run:**
   ```bash
   git clone https://github.com/yourusername/ffuf-smart-scanner.git
   cd ffuf-smart-scanner
   python3 ffuf_smart_scanner.py example.com
   ```

3. **Check results:**
   ```bash
   cd ffuf_live_*
   cat all_found.txt
   ```

### 💡 Best Practices

- **Start with Smart Mode:** Quick results, low detection risk
- **Use Full Mode When Needed:** Deep enumeration
- **Respect Rate Limits:** Use appropriate delays
- **Follow Scope:** Only scan authorized targets
- **Report Findings:** Follow responsible disclosure

### 🔒 Security Best Practices

| Practice | Description |
|----------|-------------|
| **Authorization** | Always have written permission |
| **Rate Limiting** | Use appropriate delays |
| **Scope** | Stay within authorized scope |
| **Reporting** | Follow responsible disclosure |

---

*Made with ❤️ for the Security Community*

[![Security Community](https://img.shields.io/badge/security-community-blue)]()
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen)]()
