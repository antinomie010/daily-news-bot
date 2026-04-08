# -*- coding: utf-8 -*-
"""
飞书每日早报配置文件
"""

# ============== 飞书配置 ==============
# TODO: 请替换为你自己的飞书群机器人 Webhook URL
# 创建方式：飞书群 -> 设置 -> 群机器人 -> 添加机器人 -> 自定义机器人
WEBHOOK_URL = "https://open.feishu.cn/open-apis/bot/v2/hook/ed009cbe-5b14-4728-9c32-3280f3cc644e"

# ============== 代理配置 ==============
# 如果无法访问海外媒体，请配置代理
# PROXY = {
#     "http": "http://127.0.0.1:7890",
#     "https": "http://127.0.0.1:7890",
# }
PROXY = None  # 不使用代理

# ============== 新闻源配置 ==============
SOURCES = {
    # 国内科技/AI媒体
    "36kr": {
        "name": "36氪",
        "url": "https://36kr.com/feed",
        "type": "rss",
        "enabled": True,
    },
    "huxiu": {
        "name": "虎嗅",
        "url": "https://www.huxiu.com/rss/",
        "type": "rss",
        "enabled": True,
    },
    "qbitai": {
        "name": "量子位",
        "url": "https://www.qbitai.com/feed",
        "type": "rss",
        "enabled": True,
    },
    "jiqizhixin": {
        "name": "机器之心",
        "url": "https://rs.jiqizhixin.com/nlp/daily_rss",
        "type": "rss",
        "enabled": True,
    },
    "ifeng": {
        "name": "凤凰科技",
        "url": "https://tech.ifeng.com/rss/",
        "type": "rss",
        "enabled": True,
    },
    "ithome": {
        "name": "IT之家",
        "url": "https://www.ithome.com/rss/",
        "type": "rss",
        "enabled": True,
    },
    "lieyunwang": {
        "name": "猎云网",
        "url": "https://www.lieyunpro.com/feed",
        "type": "rss",
        "enabled": True,
    },
    "tmtpost": {
        "name": "钛媒体",
        "url": "https://www.tmtpost.com/rss",
        "type": "rss",
        "enabled": True,
    },
    "geekpark": {
        "name": "极客公园",
        "url": "https://www.geekpark.net/rss",
        "type": "rss",
        "enabled": True,
    },
    # 国内综合新闻
    "thepaper": {
        "name": "澎湃新闻",
        "url": "https://www.thepaper.cn/rss",
        "type": "rss",
        "enabled": True,
    },
    "sina": {
        "name": "新浪科技",
        "url": "https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2519&k=&num=20&page=1",
        "type": "rss",
        "enabled": True,
    },
}

# ============== 关键词配置 ==============
# 匹配的关键词会获得更高权重
KEYWORDS = [
    # AI相关
    "AI", "人工智能", "大模型", "GPT", "ChatGPT", "LLM", "AGI",
    "OpenAI", "Anthropic", "Google", "Meta", "微软", "英伟达",
    "神经网络", "深度学习", "机器学习", "AIGC", "生成式AI",
    "文心一言", "通义千问", "Kimi", "智谱", "百川",
    # 科技行业
    "发布", "融资", "投资", "收购", "上市", "财报",
    "技术突破", "产品", "芯片", "算力", "自动驾驶",
    # 互联网
    "互联网", "电商", "社交", "平台", "数字化", "云服务",
]

# 排除的关键词（包含这些词的新闻可能不太适合早报）
EXCLUDE_KEYWORDS = [
    "广告", "推广", "优惠券", "抽奖", "赌博", "色情",
]

# ============== 早报配置 ==============
# 早报标题
REPORT_TITLE = "📰 每日早报"

# 最多收录条数
MAX_ITEMS = 10

# 日期格式
DATE_FORMAT = "%Y年%m月%d日"

# ============== HTTP配置 ==============
REQUEST_TIMEOUT = 30
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"