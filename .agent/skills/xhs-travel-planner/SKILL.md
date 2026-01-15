---
name: xhs-travel-planner
description: "小红书旅行规划助手。爬取小红书搜索结果，按类别（交通、住宿、饮食、优惠等）筛选内容，生成思维导图。当用户需要从小红书收集旅行攻略信息时使用。"
---

# 小红书旅行规划助手

## 核心功能

1. **搜索爬取**: 使用 Patchright 自动搜索指定目的地
2. **内容筛选**: 按关键词分类（交通、住宿、餐饮、优惠、学生票等）
3. **思维导图**: 生成 Mermaid 格式的结构化导图

## 使用前提

- 首次使用需手动登录小红书（cookies 会被保存复用）
- 建议每次爬取 ≤ 50 篇笔记
- 确保 `patchright` 已安装

## 快速开始

### 1. 首次登录（保存 cookies）
```bash
python .agent/skills/xhs-travel-planner/scripts/scraper.py --login
```

### 2. 搜索并爬取
```bash
python .agent/skills/xhs-travel-planner/scripts/scraper.py --query "黄山" --limit 30
```

### 3. 分析并生成思维导图
```bash
python .agent/skills/xhs-travel-planner/scripts/analyzer.py --input xhs_results.json
python .agent/skills/xhs-travel-planner/scripts/visualizer.py --input analyzed.json
```

## 反检测措施

- Cookie 复用（避免反复登录）
- 请求间隔 3-8 秒随机延迟
- 每 10 篇休息 30 秒
- 遇到 CAPTCHA 自动暂停

## 关键词配置

编辑 `references/keywords.json` 自定义分类关键词。
