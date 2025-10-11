# 🇨🇳 AdGuard CN Complete Filter

一个专为中国网络环境优化的广告、追踪与恶意域名屏蔽列表。  
自动每日更新，自动整合黑白名单并去重。

## 📦 订阅地址（用于 AdGuard Home）
```
https://raw.githubusercontent.com/CodeEspresso/adguard-cn-filter/main/output/adguard-cn-complete.txt
```

## 📋 特点
- 基于 Anti-AD、AdGuard DNS、Hagezi 专业版规则；
- 自动整合国内 CDN 白名单（如腾讯云、阿里云、百度等）；
- 去重并清理冲突，减少误杀；
- 每日凌晨自动更新。

## ⚙️ 目录结构
```
sources/blacklists.txt   # 黑名单来源
sources/whitelists.txt   # 白名单来源
scripts/build.py         # 构建脚本
output/adguard-cn-complete.txt  # 最终文件
.github/workflows/build.yml     # 自动更新任务
```

---
作者：CodeEspresso  
自动化生成版本。
