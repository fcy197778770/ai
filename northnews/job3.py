import json
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup, MarkupResemblesLocatorWarning
import time
import warnings

warnings.filterwarnings("ignore", category=MarkupResemblesLocatorWarning)

# 获取不同分类的页面
class NorthNewsSpider:
    def __init__(
        self,
        base_url: str = "http://www.northnews.cn",
        delay: float = 0.5
    ):
        self.base_url = base_url
        self.delay = delay

        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Referer": self.base_url,
        })

    def get_html(self, url: str) -> str | None:
        """请求页面，返回 HTML 文本"""
        try:
            time.sleep(self.delay)
            resp = self.session.get(url, timeout=15)
            resp.raise_for_status()
            resp.encoding = resp.apparent_encoding
            return resp.text

        except requests.exceptions.Timeout as e:
            print(f"【Timeout】{url} | {e}")
        except requests.exceptions.ConnectionError as e:
            print(f"【ConnectionError】{url} | {e}")
        except requests.exceptions.RequestException as e:
            print(f"【RequestException】{url} | {e}")
        except Exception as e:
            print(f"【未知错误】{url} | {type(e).__name__} | {e}")

        return None

    def extract_news_list(self,soup):
        try:
            news_list = []
            soup = BeautifulSoup(soup, "html.parser")
            items = soup.find_all("a",href=True)
            for a in items:
                title = a.get_text(strip=True)
                href = a.get("href")
                if not href or not title:
                    continue
                # 过滤长度小于6的
                if href.endswith(".html") and len(title) > 6:
                    full_url = urljoin(self.base_url, href)
                    news_list.append({"title": title, "url": full_url})
                else:
                    continue

            # 去重
            unique_list = []
            seen = set()
            for news in news_list:
                if news["url"] not in seen:
                    seen.add(news["url"])
                    unique_list.append(news)
            return unique_list
        except Exception as e:
            print(f"【提取错误】{type(e).__name__}] | {e}")
            return []

    def save_data_json(self,data,filename):
        if data is None:
            return False
        try:
            with open(filename,"w",encoding="utf-8") as f:
                json.dump(data,f,ensure_ascii=False,indent=2,sort_keys=True)
                print(f"data saved {filename} successfully")
                return True
        except Exception as e:
            print(f"save data error {type(e).__name__} | {e}")
            return False

    def read_data_json(self,filename):
        try:
            with open(filename,"r",encoding="utf-8") as f:
                data = json.load(f)
                print(f"data loaded from {filename} successfully")
                return data
        except Exception as e:
            print(f"read data error {type(e).__name__} | {e}")
            return False


if __name__ == "__main__":
    spider = NorthNewsSpider(delay=1.5)
    categories ={
        "首页":"https://www.northnews.cn/",
        "新闻":"https://www.northnews.cn/news.html",
        "蒙古":"https://www.northnews.cn/news/nmgnews/index.html",
        "国内":"https://www.northnews.cn/news/guonei/",
        "国际":"https://www.northnews.cn/news/guoji/",
        "旅游":"https://www.northnews.cn/tourist/index.html",

    }
    all_data = []
    for title,url in  categories.items():
        html = spider.get_html(url)
        list_data = spider.extract_news_list(html)
        all_data.extend(list_data)
        print(f"{title} | {url} | {len(list_data)} | {list_data[:3]}")
        print(url,spider.save_data_json(list_data,f"test_{title}.json"))
        # print(spider.read_data_json("test.json"))
    spider.save_data_json(all_data,"test_all.json")
