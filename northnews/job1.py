from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup, MarkupResemblesLocatorWarning
import time
import warnings

warnings.filterwarnings("ignore", category=MarkupResemblesLocatorWarning)


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

    @staticmethod
    def get_html_title(html: str) -> str | None:
        """从 HTML 中提取 title"""
        if not html:
            return None

        soup = BeautifulSoup(html, "html.parser")
        title_tag = soup.find("title")
        if title_tag and title_tag.text:
            return title_tag.text.strip()
        return None

    @staticmethod
    def get_top_str(html: str, number: int = 500) -> str | None:
        """返回 HTML 前 N 个字符"""
        if not html:
            return None
        return html[:number]


if __name__ == "__main__":
    spider = NorthNewsSpider(delay=1.5)

    list_page = "http://www.northnews.cn/news/nmgnews/index.html"
    html = spider.get_html(list_page)

    print("Title:", spider.get_html_title(html))
    print("Top HTML:", spider.get_top_str(html))