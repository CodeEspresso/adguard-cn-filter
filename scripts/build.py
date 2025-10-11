import requests
from datetime import datetime
import os

def fetch_list(url):
    """获取域名列表"""
    try:
        text = requests.get(url, timeout=30).text
        return [line.strip() for line in text.splitlines() if line and not line.startswith('#')]
    except Exception as e:
        print(f"[WARN] 无法获取 {url}: {e}")
        return []

def load_sources(file_path):
    """
    读取 sources 文件，返回 [(url, source_name), ...]
    文件格式:
    https://example.com/list.txt | 来源说明
    """
    sources = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                parts = line.split('|')
                if len(parts) == 2:
                    url, source_name = parts
                    sources.append((url.strip(), source_name.strip()))
    return sources

# 加载黑名单和白名单源
blacklist_sources = load_sources('sources/blacklists.txt')
whitelist_sources = load_sources('sources/whitelists.txt')

# 获取黑名单域名，并记录来源
black_domains = dict()
for url, source_name in blacklist_sources:
    domains = fetch_list(url)
    for d in domains:
        black_domains[d] = source_name  # 记录来源

# 获取白名单域名
white_domains = set()
for url, _ in whitelist_sources:
    white_domains.update(fetch_list(url))

# 去重 & 排除白名单
final_domains = {d: src for d, src in black_domains.items() if d not in white_domains}

# 确保输出目录存在
os.makedirs('output', exist_ok=True)

# 输出文件
output_file = 'output/adguard-cn-complete.txt'
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(f"# AdGuard CN Complete Filter with source info\n")
    f.write(f"# Last update: {datetime.now().isoformat()}\n")
    f.write(f"# Total domains: {len(final_domains)}\n")
    f.write("# Source: https://github.com/CodeEspresso/adguard-cn-filter\n\n")
    for domain, source in sorted(final_domains.items()):
        f.write(f"{domain}  # Source: {source}\n")

print(f"[OK] 已生成 {output_file}，共 {len(final_domains)} 条记录。")
