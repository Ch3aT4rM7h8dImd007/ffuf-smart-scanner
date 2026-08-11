#!/usr/bin/env python3
"""
FFUF - LIVE DEBUG SCANNER WITH SMART + FULL WORDLIST
Shows everything in real-time!
Choose between Smart (fast) or Full (deep) scan
"""

import subprocess
import os
import sys
import time
import re
import json
import threading
from datetime import datetime

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

class FFUFLiveScanner:
    def __init__(self, target):
        self.target = target
        self.clean_target = self.clean_url(target)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.results_dir = f"ffuf_live_{self.timestamp}"
        self.found_items = []
        self.total_words = 0
        self.processed_words = 0
        self.lock = threading.Lock()
        os.makedirs(self.results_dir, exist_ok=True)
        
    def clean_url(self, url):
        url = re.sub(r'^https?://', '', url)
        url = re.sub(r'^www\.', '', url)
        url = url.split('/')[0]
        return url

    def create_smart_wordlist(self):
        """Create smart wordlist for bug bounty"""
        smart_words = [
            # Admin/Management
            "admin", "administrator", "adminpanel", "dashboard", "panel",
            "cpanel", "webmail", "plesk", "control", "manage", "manager",
            
            # Authentication
            "login", "signin", "auth", "oauth", "sso", "register", 
            "signup", "forgot", "reset", "verify", "password", "credentials",
            
            # API
            "api", "v1", "v2", "v3", "graphql", "rest", "soap",
            "swagger", "docs", "redoc", "openapi", "postman", "insomnia",
            
            # Sensitive Files
            ".env", ".git", ".svn", ".hg", ".htaccess", ".htpasswd",
            "backup", "backups", "config", "configuration", "settings",
            "secret", "private", "conf", "credentials", "security",
            
            # Common Directories
            "images", "img", "assets", "static", "media", "public",
            "css", "js", "javascript", "fonts", "icons", "styles",
            
            # Development/Testing
            "dev", "development", "test", "testing", "staging",
            "debug", "phpinfo", "info", "status", "health", "ping",
            "monitoring", "metrics", "stats", "analytics",
            
            # Bug Bounty Targets
            "robots.txt", "sitemap.xml", "crossdomain.xml", "security.txt",
            "bugbounty", "responsible-disclosure", "vulnerability",
            
            # CMS
            "wp-admin", "wp-login", "wp-content", "wp-includes", "wp-json",
            "phpmyadmin", "mysql", "database", "db", "sql", "adminer",
            
            # Features
            "download", "uploads", "files", "documents", "archive",
            "blog", "news", "articles", "posts", "comments",
            "shop", "store", "cart", "checkout", "payment", "order",
            "user", "profile", "account", "settings", "preferences",
            "search", "results", "find", "explore", "discover",
            "help", "support", "faq", "contact", "about", "team",
            "privacy", "terms", "policy", "legal", "disclaimer",
            
            # Additional
            "internal", "private", "beta", "alpha", "experimental",
            "old", "new", "temp", "tmp", "cache", "logs", "log",
            "error", "errors", "debug", "trace", "dump",
            
            # Technology specific
            "node_modules", "vendor", "third-party", "lib", "includes",
            "src", "dist", "build", "compiled", "generated",
            
            # Common vulnerabilities
            "cgi-bin", "cgi", "pl", "perl", "shell", "cmd",
            "exec", "system", "command", "terminal", "console",
            
            # Data
            "data", "dataset", "database", "dump", "export",
            "import", "migration", "seed", "fixture", "fixtures"
        ]
        
        # Save smart wordlist
        wordlist_path = f"{self.results_dir}/smart_wordlist.txt"
        with open(wordlist_path, 'w') as f:
            for word in smart_words:
                f.write(f"{word}\n")
        
        print(f"{Colors.GREEN}✅ Created Smart Wordlist: {len(smart_words)} words{Colors.RESET}")
        print(f"{Colors.BLUE}   Optimized for Bug Bounty{Colors.RESET}")
        
        return wordlist_path, len(smart_words)

    def get_wordlist_with_details(self):
        """Get wordlist with size and details"""
        wordlists = {
            'smart': self.create_smart_wordlist(),  # Smart wordlist (bug bounty optimized)
            'small': "/usr/share/seclists/Discovery/Web-Content/directory-list-2.3-small.txt",
            'medium': "/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt",
            'common': "/usr/share/wordlists/dirb/common.txt",
        }
        
        available = {}
        
        # Add smart wordlist first
        smart_path, smart_count = wordlists['smart']
        available['smart'] = {'path': smart_path, 'count': smart_count, 'words': ['admin', 'login', 'api', 'graphql', '.env']}
        print(f"{Colors.GREEN}✅ Smart: {smart_count} words{Colors.RESET}")
        
        # Add other wordlists
        for name, path in wordlists.items():
            if name == 'smart':
                continue
            if os.path.exists(path):
                try:
                    with open(path, 'r') as f:
                        words = [line.strip() for line in f if line.strip() and not line.startswith('#')]
                        count = len(words)
                    available[name] = {'path': path, 'count': count, 'words': words[:10]}
                    print(f"{Colors.GREEN}✅ Found: {name} - {count:,} words{Colors.RESET}")
                except:
                    pass
        
        if not available:
            fallback = f"{self.results_dir}/fallback.txt"
            words = ["admin", "login", "test", "dev", "api", "blog", "shop"]
            with open(fallback, 'w') as f:
                for w in words:
                    f.write(f"{w}\n")
            available['fallback'] = {'path': fallback, 'count': len(words), 'words': words}
            print(f"{Colors.YELLOW}⚠️ Created fallback wordlist{Colors.RESET}")
        
        return available

    def split_wordlist_with_live_preview(self, wordlist_path, word_count, wordlist_name):
        """Split wordlist and show live progress"""
        # Calculate chunk size based on wordlist type
        if wordlist_name == 'smart':
            chunk_size = 500  # Smart wordlist er jonno choto chunk
        elif word_count > 150000:
            chunk_size = 3000
        elif word_count > 100000:
            chunk_size = 2500
        elif word_count > 50000:
            chunk_size = 2000
        elif word_count > 10000:
            chunk_size = 1500
        else:
            chunk_size = 1000
        
        print(f"\n{Colors.CYAN}📦 CHUNK CONFIGURATION:{Colors.RESET}")
        print(f"{Colors.YELLOW}   Wordlist Type: {wordlist_name}{Colors.RESET}")
        print(f"{Colors.YELLOW}   Total Words: {word_count:,}{Colors.RESET}")
        print(f"{Colors.YELLOW}   Chunk Size: {chunk_size} words per chunk{Colors.RESET}")
        print(f"{Colors.YELLOW}   Expected Chunks: ~{word_count // chunk_size + 1}{Colors.RESET}")
        print(f"{Colors.BLUE}{'─'*70}{Colors.RESET}")
        
        chunks = []
        current_chunk = []
        chunk_num = 1
        processed = 0
        
        print(f"{Colors.CYAN}📖 Reading and splitting wordlist...{Colors.RESET}")
        start_time = time.time()
        
        with open(wordlist_path, 'r') as f:
            for line in f:
                word = line.strip()
                if word and not word.startswith('#'):
                    current_chunk.append(word)
                    processed += 1
                    
                    # Show progress every 1000 words
                    if processed % 1000 == 0:
                        print(f"{Colors.BLUE}   📊 Read {processed:,} words...{Colors.RESET}")
                    
                    if len(current_chunk) >= chunk_size:
                        chunk_file = f"{self.results_dir}/chunk_{chunk_num}.txt"
                        with open(chunk_file, 'w') as cf:
                            cf.write('\n'.join(current_chunk))
                        chunks.append({
                            'file': chunk_file,
                            'num': chunk_num,
                            'size': len(current_chunk),
                            'first_word': current_chunk[0] if current_chunk else 'N/A',
                            'last_word': current_chunk[-1] if current_chunk else 'N/A'
                        })
                        
                        # Live chunk creation info
                        print(f"{Colors.GREEN}   ✅ Chunk {chunk_num}: {len(current_chunk)} words{Colors.RESET}")
                        print(f"{Colors.BLUE}      First: {current_chunk[0]}{Colors.RESET}")
                        print(f"{Colors.BLUE}      Last: {current_chunk[-1]}{Colors.RESET}")
                        
                        current_chunk = []
                        chunk_num += 1
        
        # Save remaining words
        if current_chunk:
            chunk_file = f"{self.results_dir}/chunk_{chunk_num}.txt"
            with open(chunk_file, 'w') as cf:
                cf.write('\n'.join(current_chunk))
            chunks.append({
                'file': chunk_file,
                'num': chunk_num,
                'size': len(current_chunk),
                'first_word': current_chunk[0] if current_chunk else 'N/A',
                'last_word': current_chunk[-1] if current_chunk else 'N/A'
            })
            print(f"{Colors.GREEN}   ✅ Chunk {chunk_num}: {len(current_chunk)} words (final){Colors.RESET}")
        
        elapsed = time.time() - start_time
        print(f"{Colors.CYAN}⏱️  Wordlist split completed in {elapsed:.1f}s{Colors.RESET}")
        print(f"{Colors.GREEN}📊 Total chunks created: {len(chunks)}{Colors.RESET}")
        
        return chunks

    def scan_chunk_with_live_stats(self, chunk_info, chunk_num, total_chunks, protocol, timeout, wordlist_name):
        """Scan chunk with live stats display"""
        chunk_file = chunk_info['file']
        chunk_size = chunk_info['size']
        
        print(f"\n{Colors.MAGENTA}{'='*70}{Colors.RESET}")
        print(f"{Colors.BOLD}🔍 CHUNK {chunk_num}/{total_chunks}{Colors.RESET}")
        print(f"{Colors.MAGENTA}{'='*70}{Colors.RESET}")
        print(f"{Colors.CYAN}📄 File: {os.path.basename(chunk_file)}{Colors.RESET}")
        print(f"{Colors.CYAN}📊 Words in chunk: {chunk_size}{Colors.RESET}")
        print(f"{Colors.CYAN}🔢 Word range: {chunk_info['first_word']} → {chunk_info['last_word']}{Colors.RESET}")
        print(f"{Colors.CYAN}⏱️  Timeout: {timeout}s per word{Colors.RESET}")
        
        # Adjust threads based on wordlist type
        if wordlist_name == 'smart':
            threads = 20  # Smart wordlist er jonno kom thread (safe)
        else:
            threads = 50  # Full wordlist er jonno beshi thread (fast)
        
        print(f"{Colors.CYAN}🧵 Threads: {threads}{Colors.RESET}")
        
        # Calculate estimated time
        estimated_time = (chunk_size / threads) * timeout
        print(f"{Colors.YELLOW}⏱️  Estimated time: ~{estimated_time:.1f}s{Colors.RESET}")
        
        output_file = f"{self.results_dir}/ffuf_chunk_{chunk_num}.json"
        
        # FFUF command with adjustable threads
        cmd = (f"ffuf -w {chunk_file}:FUZZ "
               f"-u {protocol}://{self.clean_target}/FUZZ "
               f"-o {output_file} "
               f"-of json "
               f"-t {threads} "
               f"-timeout {timeout} "
               f"-ac -c -s "
               f"-fc 404,403,500 "
               f"-H 'User-Agent: Mozilla/5.0'")
        
        # Add delay for smart wordlist (avoid detection)
        if wordlist_name == 'smart':
            cmd += " -p 0.3"  # 0.3 second delay
        
        print(f"{Colors.YELLOW}🔧 Command: {cmd[:100]}...{Colors.RESET}")
        print(f"{Colors.BLUE}{'─'*70}{Colors.RESET}")
        
        start = time.time()
        found_in_chunk = 0
        words_tested = 0
        last_update = time.time()
        
        try:
            process = subprocess.Popen(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # Live output reading
            while True:
                line = process.stdout.readline()
                if line == '' and process.poll() is not None:
                    break
                if line:
                    line = line.rstrip()
                    
                    # Count words being tested
                    if 'Progress' in line:
                        # Extract progress percentage
                        match = re.search(r'Progress:\s*\[(\d+)/(\d+)\]', line)
                        if match:
                            current = int(match.group(1))
                            total = int(match.group(2))
                            words_tested = current
                            progress_pct = (current / total) * 100
                            
                            # Update every 10%
                            if int(progress_pct) % 10 == 0:
                                elapsed = time.time() - start
                                print(f"{Colors.CYAN}   📈 Progress: {progress_pct:.1f}% ({current}/{total}) - Time: {elapsed:.1f}s{Colors.RESET}")
                    
                    # Show found items with colors
                    if 'Status: 200' in line:
                        print(f"{Colors.GREEN}   🟢 FOUND! {line}{Colors.RESET}")
                        match = re.search(r'FUZZ\s+->\s+([^\s]+)', line)
                        if match:
                            self.found_items.append(match.group(1))
                            found_in_chunk += 1
                    elif 'Status: 301' in line or 'Status: 302' in line:
                        print(f"{Colors.YELLOW}   🔄 REDIRECT! {line}{Colors.RESET}")
                        match = re.search(r'FUZZ\s+->\s+([^\s]+)', line)
                        if match:
                            self.found_items.append(match.group(1))
                            found_in_chunk += 1
                    elif 'Status: 401' in line:
                        print(f"{Colors.MAGENTA}   🔒 AUTH REQUIRED! {line}{Colors.RESET}")
                    elif 'Status: 403' in line:
                        print(f"{Colors.YELLOW}   🚫 FORBIDDEN! {line}{Colors.RESET}")
                    elif 'ERROR' in line or 'error' in line.lower():
                        print(f"{Colors.RED}   ❌ {line}{Colors.RESET}")
            
            process.wait()
            elapsed = time.time() - start
            
            # Live stats
            print(f"{Colors.BLUE}{'─'*70}{Colors.RESET}")
            print(f"{Colors.GREEN}✅ CHUNK {chunk_num} COMPLETED!{Colors.RESET}")
            print(f"{Colors.CYAN}   Words tested: {chunk_size}{Colors.RESET}")
            print(f"{Colors.CYAN}   Time taken: {elapsed:.1f}s{Colors.RESET}")
            print(f"{Colors.CYAN}   Speed: {chunk_size/elapsed:.1f} words/second{Colors.RESET}")
            print(f"{Colors.GREEN}   Found: {found_in_chunk} items{Colors.RESET}")
            
            # Real-time performance analysis
            if elapsed > 0:
                efficiency = (chunk_size / threads) / elapsed * 100
                print(f"{Colors.CYAN}   Efficiency: {efficiency:.1f}%{Colors.RESET}")
                if efficiency > 80:
                    print(f"{Colors.GREEN}   🚀 Excellent performance!{Colors.RESET}")
                elif efficiency > 50:
                    print(f"{Colors.YELLOW}   ⚡ Good performance{Colors.RESET}")
                else:
                    print(f"{Colors.RED}   🐌 Network may be slow{Colors.RESET}")
            
            return found_in_chunk
            
        except Exception as e:
            print(f"{Colors.RED}❌ Chunk {chunk_num} error: {str(e)[:50]}{Colors.RESET}")
            return 0

    def test_protocol(self):
        """Test which protocol works"""
        try:
            import requests
            try:
                response = requests.get(f"https://{self.clean_target}", timeout=5)
                if response.status_code < 400:
                    print(f"{Colors.GREEN}✅ HTTPS works{Colors.RESET}")
                    return 'https'
            except:
                pass
            
            try:
                response = requests.get(f"http://{self.clean_target}", timeout=5)
                if response.status_code < 400:
                    print(f"{Colors.GREEN}✅ HTTP works{Colors.RESET}")
                    return 'http'
            except:
                pass
            
            print(f"{Colors.YELLOW}⚠️ Testing both protocols{Colors.RESET}")
            return 'both'
        except:
            return 'both'

    def run_live_scan(self):
        """Main scan with live output"""
        print(f"""
{Colors.BOLD}{Colors.MAGENTA}
╔═══════════════════════════════════════════════════════════════════╗
║           FFUF - SMART + FULL WORDLIST SCANNER                  ║
║           Choose your wordlist based on needs                   ║
║           Smart = Fast & Safe | Full = Deep & Complete         ║
╚═══════════════════════════════════════════════════════════════════╝
{Colors.RESET}
        """)

        # Step 1: Get wordlists
        print(f"{Colors.CYAN}📥 Scanning for wordlists...{Colors.RESET}")
        available_wordlists = self.get_wordlist_with_details()
        
        if not available_wordlists:
            print(f"{Colors.RED}❌ No wordlists found{Colors.RESET}")
            return

        # Step 2: Choose wordlist with description
        print(f"\n{Colors.CYAN}📋 Available Wordlists:{Colors.RESET}")
        print(f"{Colors.BLUE}{'─'*70}{Colors.RESET}")
        print(f"{Colors.YELLOW}   ⚡ Smart = Bug Bounty optimized (fast, safe){Colors.RESET}")
        print(f"{Colors.YELLOW}   📚 Full = Deep scanning (comprehensive, slow){Colors.RESET}")
        print(f"{Colors.BLUE}{'─'*70}{Colors.RESET}")
        
        wordlist_names = list(available_wordlists.keys())
        for i, name in enumerate(wordlist_names, 1):
            info = available_wordlists[name]
            emoji = "⚡" if name == 'smart' else "📚"
            print(f"{Colors.WHITE}   {i}. {emoji} {name} ({info['count']:,} words){Colors.RESET}")
            if 'words' in info:
                sample = ', '.join(info['words'][:5])
                print(f"{Colors.BLUE}      Sample: {sample}...{Colors.RESET}")
        
        choice = input(f"\n{Colors.CYAN}Choose wordlist (1-{len(wordlist_names)}, default: smart): {Colors.RESET}").strip()
        
        # Step 3: Select
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(wordlist_names):
                name = wordlist_names[idx]
                selected = available_wordlists[name]
                print(f"{Colors.GREEN}✅ Selected: {name}{Colors.RESET}")
            else:
                selected = available_wordlists['smart']
                name = 'smart'
                print(f"{Colors.GREEN}✅ Using Smart wordlist (Bug Bounty optimized){Colors.RESET}")
        except:
            selected = available_wordlists['smart']
            name = 'smart'
            print(f"{Colors.GREEN}✅ Using Smart wordlist (Bug Bounty optimized){Colors.RESET}")

        wordlist_path = selected['path']
        word_count = selected['count']
        
        # Show wordlist details
        print(f"\n{Colors.CYAN}📊 Wordlist Details:{Colors.RESET}")
        print(f"{Colors.YELLOW}   Name: {name}{Colors.RESET}")
        print(f"{Colors.YELLOW}   Words: {word_count:,}{Colors.RESET}")
        if name == 'smart':
            print(f"{Colors.GREEN}   ⚡ Optimized for Bug Bounty{Colors.RESET}")
            print(f"{Colors.GREEN}   🛡️  Safe: 20 threads, 0.3s delay{Colors.RESET}")
        else:
            print(f"{Colors.YELLOW}   📚 Full scan: 50 threads, no delay{Colors.RESET}")
            print(f"{Colors.YELLOW}   ⏱️  May take longer{Colors.RESET}")
        
        # Step 4: Test protocol
        protocol = self.test_protocol()
        if protocol == 'both':
            protocols = ['https', 'http']
        else:
            protocols = [protocol]

        # Step 5: Split wordlist with live preview
        chunks = self.split_wordlist_with_live_preview(wordlist_path, word_count, name)
        
        if not chunks:
            print(f"{Colors.RED}❌ No chunks created{Colors.RESET}")
            return

        # Step 6: Calculate timeout based on wordlist type
        if name == 'smart':
            timeout = 2  # Smart wordlist er jonno 2 second
        elif word_count > 100000:
            timeout = 1
        elif word_count > 50000:
            timeout = 2
        else:
            timeout = 3
        
        print(f"\n{Colors.CYAN}⏱️  Timeout per word: {timeout}s{Colors.RESET}")
        
        # Step 7: Scan with live stats
        total_start = time.time()
        total_found = 0
        
        print(f"\n{Colors.MAGENTA}{'='*70}{Colors.RESET}")
        print(f"{Colors.BOLD}🚀 STARTING SCAN{Colors.RESET}")
        print(f"{Colors.MAGENTA}{'='*70}{Colors.RESET}")
        
        for protocol in protocols:
            for i, chunk_info in enumerate(chunks, 1):
                found = self.scan_chunk_with_live_stats(
                    chunk_info, i, len(chunks), 
                    protocol, timeout, name
                )
                total_found += found
                
                elapsed = time.time() - total_start
                print(f"\n{Colors.CYAN}📊 OVERALL PROGRESS:{Colors.RESET}")
                print(f"{Colors.YELLOW}   Chunks: {i}/{len(chunks)}{Colors.RESET}")
                print(f"{Colors.YELLOW}   Time: {elapsed:.1f}s ({elapsed/60:.1f}m){Colors.RESET}")
                print(f"{Colors.GREEN}   Total found: {total_found}{Colors.RESET}")
                
                # Estimate remaining time
                if i > 0:
                    avg_time_per_chunk = elapsed / i
                    remaining_chunks = len(chunks) - i
                    eta = avg_time_per_chunk * remaining_chunks
                    print(f"{Colors.CYAN}   ETA: {eta:.1f}s (~{eta/60:.1f}m){Colors.RESET}")
                
                print(f"{Colors.BLUE}{'─'*70}{Colors.RESET}")
                time.sleep(0.5)

        # Step 8: Final summary
        total_elapsed = time.time() - total_start
        self.found_items = list(set(self.found_items))
        
        print(f"\n{Colors.MAGENTA}{'='*70}{Colors.RESET}")
        print(f"{Colors.BOLD}📊 FINAL SUMMARY{Colors.RESET}")
        print(f"{Colors.MAGENTA}{'='*70}{Colors.RESET}")
        print(f"{Colors.CYAN}Wordlist used: {name}{Colors.RESET}")
        print(f"{Colors.CYAN}Total words: {word_count:,}{Colors.RESET}")
        print(f"{Colors.CYAN}Total chunks: {len(chunks)}{Colors.RESET}")
        print(f"{Colors.CYAN}Total time: {total_elapsed:.1f}s ({total_elapsed/60:.1f}m){Colors.RESET}")
        print(f"{Colors.CYAN}Average speed: {word_count/total_elapsed:.1f} words/second{Colors.RESET}")
        print(f"{Colors.GREEN}Total unique items found: {len(self.found_items)}{Colors.RESET}")
        
        if self.found_items:
            with open(f"{self.results_dir}/all_found.txt", 'w') as f:
                for item in sorted(self.found_items):
                    f.write(f"{item}\n")
            print(f"{Colors.CYAN}📁 Results: {self.results_dir}/all_found.txt{Colors.RESET}")
            
            print(f"\n{Colors.GREEN}📋 Found items:{Colors.RESET}")
            for i, item in enumerate(sorted(self.found_items)[:20], 1):
                print(f"{Colors.GREEN}   {i}. {item}{Colors.RESET}")
            if len(self.found_items) > 20:
                print(f"{Colors.YELLOW}   ... and {len(self.found_items)-20} more{Colors.RESET}")
            
            # Vulnerability suggestions
            print(f"\n{Colors.YELLOW}🔍 Potential vulnerabilities to check:{Colors.RESET}")
            for item in sorted(self.found_items)[:10]:
                if 'admin' in item.lower() or 'login' in item.lower():
                    print(f"{Colors.RED}   ⚠️  {item} - Check for weak credentials / default login{Colors.RESET}")
                elif '.env' in item or '.git' in item:
                    print(f"{Colors.RED}   ⚠️  {item} - Sensitive file exposure! Check for secrets{Colors.RESET}")
                elif 'api' in item.lower() or 'graphql' in item.lower():
                    print(f"{Colors.YELLOW}   📌 {item} - Check for IDOR, SQLi, broken auth{Colors.RESET}")
                elif 'swagger' in item.lower() or 'docs' in item.lower():
                    print(f"{Colors.YELLOW}   📌 {item} - Check for exposed API documentation{Colors.RESET}")
                elif 'backup' in item.lower() or 'backups' in item.lower():
                    print(f"{Colors.YELLOW}   📌 {item} - Check for backup files containing sensitive data{Colors.RESET}")
                elif 'config' in item.lower() or 'settings' in item.lower():
                    print(f"{Colors.YELLOW}   📌 {item} - Check for configuration exposure{Colors.RESET}")
                else:
                    print(f"{Colors.BLUE}   📌 {item} - Investigate further{Colors.RESET}")
        else:
            print(f"{Colors.YELLOW}⚠️ No items found{Colors.RESET}")
            print(f"{Colors.YELLOW}💡 Try Smart wordlist for faster results{Colors.RESET}")
            print(f"{Colors.YELLOW}💡 Or Full wordlist for deeper scanning{Colors.RESET}")

def main():
    if len(sys.argv) < 2:
        print(f"{Colors.YELLOW}Usage: python3 {sys.argv[0]} <target>{Colors.RESET}")
        print(f"{Colors.YELLOW}Example: python3 {sys.argv[0]} foodnetwork.com{Colors.RESET}")
        sys.exit(1)
    
    target = sys.argv[1]
    scanner = FFUFLiveScanner(target)
    scanner.run_live_scan()

if __name__ == "__main__":
    main()