# -*- coding: utf-8 -*-
"""
飞书每日早报 - 发送脚本
将格式化后的早报内容发送到飞书群
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import requests
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import WEBHOOK_URL


def send_text_message(text):
    """发送文本消息到飞书群"""
    url = WEBHOOK_URL

    payload = {
        "msg_type": "text",
        "content": {
            "text": text
        }
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        result = response.json()

        if result.get("code") == 0 or result.get("StatusCode") == 0:
            print("[成功] 消息已发送到飞书群")
            return True
        else:
            print(f"[失败] 发送失败: {result}")
            return False

    except Exception as e:
        print(f"[错误] 发送失败: {e}")
        return False


def send_rich_text_message(news_list, title):
    """发送富文本消息（卡片形式）到飞书群"""
    url = WEBHOOK_URL

    # 构建富文本内容
    content = []

    for i, news in enumerate(news_list, 1):
        item = [
            {"tag": "text", "text": f"{i}. "},
            {"tag": "a", "text": f"{news['title']}", "href": news['link']},
            {"tag": "text", "text": f"\n{news.get('summary', '')[:80]}...\n"}
        ]
        content.append(item)

    payload = {
        "msg_type": "post",
        "content": {
            "post": {
                "zh_cn": {
                    "title": title,
                    "content": [[
                        {"tag": "text", "text": f"📰 {title}\n\n"}
                    ]] + [[
                        {"tag": "text", "text": f"{i}. "},
                        {"tag": "a", "text": f"{news['title']}", "href": news['link']},
                        {"tag": "text", "text": f"\n📌 {news.get('summary', '')[:60]}...\n\n"}
                    ] for i, news in enumerate(news_list, 1)]
                }
            }
        }
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        result = response.json()

        if result.get("code") == 0 or result.get("StatusCode") == 0:
            print("[成功] 富文本消息已发送到飞书群")
            return True
        else:
            print(f"[失败] 发送失败: {result}")
            return False

    except Exception as e:
        print(f"[错误] 发送失败: {e}")
        return False


def send_from_file():
    """从文件读取早报内容并发送"""
    report_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "daily_report.txt"
    )

    if not os.path.exists(report_file):
        print(f"[错误] 早报文件不存在: {report_file}")
        return False

    with open(report_file, "r", encoding="utf-8") as f:
        content = f.read()

    return send_text_message(content)


def main():
    """主函数"""
    print("正在发送早报到飞书群...")

    # 从文件读取并发送
    success = send_from_file()

    if success:
        print("✅ 早报发送成功！")
    else:
        print("❌ 早报发送失败，请检查 Webhook 配置")

    return success


if __name__ == "__main__":
    main()