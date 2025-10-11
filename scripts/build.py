import requests
from datetime import datetime
import os

def fetch_list(url):
    try:
        text = requests.get(url, timeout=30).text
        return [line.strip() for line in text.splitlines() if line and not line.startswith('#')]
    except Exception as e:
        print(f"[WARN] 无法获取 {url}: {e}")
        return []

def load_sources(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        urls = []
        for line in f:
            if line.strip() and not line.startswith('#'):
                parts = line.split('|')[0].strip()
                urls.append(parts)
        return urls

blacklist_sources = load_sources('sources/blacklists.txt')
whitelist_sources = load_sources('sources/whitelists.txt')

black_domains = set()
for url in blacklist_sources:
    black_domains.update(fetch_list(url))

white_domains = set()
for url in whitelist_sources:
    white_domains.update(fetch_list(url))

# 去重 & 排除白名单
final_domains = sorted(black_domains - white_domains)

# 确保输出目录存在
os.makedirs('output', exist_ok=True)

# 输出
with open('output/adguard-cn-complete.txt', 'w', encoding='utf-8') as f:
    f.write(f"# AdGuard CN Complete Filter\n")
    f.write(f"# Last update: {datetime.now().isoformat()}\n")
    f.write(f"# Total domains: {len(final_domains)}\n")
    f.write("# Source: https://github.com/CodeEspresso/adguard-cn-filter\n\n")
    for d in final_domains:
        f.write(d + "\n")

print(f"[OK] 已生成 adguard-cn-complete.txt，共 {len(final_domains)} 条记录。")
