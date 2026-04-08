# -*- coding: utf-8 -*-
"""
飞书每日早报 - 新闻爬虫主程序
从各大媒体网站/RSS获取前一天的新闻，筛选后发送飞书
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import feedparser
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import re
import json
import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import (
    SOURCES, KEYWORDS, EXCLUDE_KEYWORDS,
    MAX_ITEMS, DATE_FORMAT, REQUEST_TIMEOUT,
    USER_AGENT, PROXY, WEBHOOK_URL, REPORT_TITLE
)


def get_yesterday_date():
    """获取昨天的日期字符串"""
    yesterday = datetime.now() - timedelta(days=1)
    return yesterday.strftime("%Y-%m-%d")


def parse_date(date_str):
    """解析各种格式的日期字符串"""
    if not date_str:
        return None

    date_formats = [
        "%Y-%m-%d",
        "%Y年%m月%d日",
        "%Y/%m/%d",
        "%d %b %Y",
        "%a, %d %b %Y %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S",
    ]

    for fmt in date_formats:
        try:
            return datetime.strptime(date_str.strip()[:len("%Y-%m-%d")+5], fmt)
        except (ValueError, TypeError):
            continue

    # 尝试解析相对时间
    now = datetime.now()
    if "今天" in date_str or "today" in date_str.lower():
        return now
    if "昨天" in date_str or "yesterday" in date_str.lower():
        return now - timedelta(days=1)

    return None


def is_from_recent_days(date_obj, days=2):
    """检查日期是否在最近几天内"""
    if not date_obj:
        return False
    now = datetime.now()
    delta = now - date_obj
    return delta.days >= 0 and delta.days < days


def calculate_score(title, summary, keywords, exclude_keywords):
    """计算新闻的关键词匹配得分"""
    text = (title + " " + summary).lower()
    score = 0

    for keyword in keywords:
        if keyword.lower() in text:
            score += 1

    for keyword in exclude_keywords:
        if keyword.lower() in text:
            score -= 5

    return score


def fetch_rss_feed(source_name, source_config):
    """获取RSS订阅源内容"""
    url = source_config["url"]
    news_list = []

    try:
        headers = {"User-Agent": USER_AGENT}
        proxies = PROXY

        response = requests.get(
            url,
            headers=headers,
            proxies=proxies,
            timeout=REQUEST_TIMEOUT
        )
        response.encoding = response.apparent_encoding or 'utf-8'

        feed = feedparser.parse(response.text)

        for entry in feed.entries:
            title = entry.get("title", "").strip()
            link = entry.get("link", "").strip()
            summary = entry.get("summary", "").strip()
            published = entry.get("published", "")

            # 清理summary中的HTML标签
            if summary:
                soup = BeautifulSoup(summary, 'html.parser')
                summary = soup.get_text()[:200]

            # 解析日期
            date_obj = parse_date(published)

            # 跳过日期不在最近2天的新闻（除非无法确定日期）
            if date_obj and not is_from_recent_days(date_obj, days=2):
                continue

            # 计算得分
            score = calculate_score(title, summary, KEYWORDS, EXCLUDE_KEYWORDS)

            news_list.append({
                "title": title,
                "link": link,
                "summary": summary,
                "source": source_config["name"],
                "date": published,
                "score": score
            })

    except Exception as e:
        print(f"  [警告] 获取 {source_name} 失败: {e}")

    return news_list


def select_top_news(all_news, max_items=10):
    """选择得分最高的新闻"""
    # 按得分排序
    sorted_news = sorted(all_news, key=lambda x: x["score"], reverse=True)

    # 去重（基于标题相似度）
    selected = []
    for news in sorted_news:
        is_duplicate = False
        for selected_news in selected:
            # 简单的标题相似度检测
            if (news["title"][:20] in selected_news["title"] or
                selected_news["title"][:20] in news["title"]):
                is_duplicate = True
                break

        if not is_duplicate:
            selected.append(news)

        if len(selected) >= max_items:
            break

    return selected


def format_report(news_list, title=REPORT_TITLE):
    """格式化早报内容"""
    yesterday = datetime.now() - timedelta(days=1)
    date_str = yesterday.strftime(DATE_FORMAT)

    report = f"{title} | {date_str}\n"
    report += "=" * 40 + "\n\n"

    if not news_list:
        report += "昨日暂无精选资讯\n"
        return report

    for i, news in enumerate(news_list, 1):
        report += f"{i}. [{news['source']}] {news['title']}\n"
        if news.get('summary'):
            report += f"   {news['summary'][:100]}...\n"
        report += f"   🔗 {news['link']}\n\n"

    report += "-" * 40 + "\n"
    report += f"⚡ 共收录 {len(news_list)} 条精选资讯"

    return report


def main():
    """主函数"""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始获取新闻...")

    all_news = []

    # 获取每个启用的源
    for source_name, source_config in SOURCES.items():
        if not source_config.get("enabled", True):
            continue

        print(f"正在获取: {source_config['name']}...")
        news_list = fetch_rss_feed(source_name, source_config)
        all_news.extend(news_list)
        print(f"  获取到 {len(news_list)} 条昨日新闻")

    print(f"\n共获取 {len(all_news)} 条新闻，开始筛选...")

    # 筛选精选新闻
    selected_news = select_top_news(all_news, MAX_ITEMS)

    print(f"筛选完成，精选 {len(selected_news)} 条新闻")

    # 格式化早报
    report = format_report(selected_news)

    print("\n" + "=" * 40)
    print("早报预览:")
    print("=" * 40)
    print(report)

    # 保存到文件（供后续发送）
    output_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "daily_report.txt"
    )
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"\n早报已保存到: {output_file}")

    return report, selected_news


if __name__ == "__main__":
    main()