import json
import re
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

    def get_category_urls(self):
        categories = {
            "首页": f"{self.base_url}",
            "新闻": f"{self.base_url}/news.html",
            "蒙古": f"{self.base_url}/news/nmgnews/index.html",
            "国内": f"{self.base_url}/news/guonei/",
            "国际": f"{self.base_url}/news/guoji/",
            "旅游": f"{self.base_url}/tourist/index.html",

        }
        return categories
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
                    news_list.append({"title": self._clean_content(title), "url": full_url})
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

    def _clean_content(self,content):
        if not content:
            return ""
        content = re.sub(r'\s+'," ",content)
        content = re.sub(r'\n\s*\n','',content)
        content = content.strip()
        return content

    def extract_all(self,categories_):
        news_list = []
        try:
            for title_,url_ in  categories_.items():
                print(f"{title_} | {url_} 开始提取")
                result = self.extract_news_list(self.get_html(url_))
                news_list.append(result)
                print(f"{title_} | {url_} 成功提取到 {len(result)}条数据")
        except Exception as e:
            print(f"【提取错误】{type(e).__name__}] | {e}")
            return []
        return news_list

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
    all_data=spider.extract_all(spider.get_category_urls())
    spider.save_data_json(all_data,"test_all.json")
