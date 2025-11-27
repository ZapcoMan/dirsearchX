import re

from bs4 import BeautifulSoup
from functools import lru_cache

from lib.core.settings import (
    CRAWL_ATTRIBUTES, CRAWL_TAGS,
    MEDIA_EXTENSIONS, ROBOTS_TXT_REGEX,
    URI_REGEX,
)
from lib.parse.url import clean_path, parse_path
from lib.utils.common import merge_path


def _filter(paths):
    """
    过滤路径集合，移除以媒体扩展名结尾的路径，并清理路径格式。

    :param paths: 原始路径集合
    :return: 清理并过滤后的路径集合
    """
    return {clean_path(path, keep_queries=True) for path in paths if not path.endswith(MEDIA_EXTENSIONS)}


class Crawler:
    """
    网页爬虫类，用于从不同类型的响应中提取URL路径。
    """

    @classmethod
    def crawl(cls, response):
        """
        根据响应的内容类型选择合适的爬取方法。

        :param response: 包含URL、headers和content的响应对象
        :return: 提取到的路径集合
        """
        # 构造作用域基础URL（协议+域名）
        scope = "/".join(response.url.split("/")[:3]) + "/"

        # 判断内容类型并调用相应的解析方法
        if "text/html" in response.headers.get("content-type", ""):
            return cls.html_crawl(response.url, scope, response.content)
        elif response.path == "robots.txt":
            return cls.robots_crawl(response.url, scope, response.content)
        else:
            return cls.text_crawl(response.url, scope, response.content)

    @staticmethod
    @lru_cache(maxsize=None)
    def text_crawl(url, scope, content):
        """
        从纯文本内容中通过正则表达式提取符合作用域的路径。

        :param url: 当前页面的完整URL
        :param scope: 作用域基础URL
        :param content: 页面内容（字节串）
        :return: 提取并过滤后的路径集合
        """
        results = []
        # 构建匹配当前域下路径的正则表达式
        regex = re.escape(scope) + "[a-zA-Z0-9-._~!$&*+,;=:@?%]+"

        # 查找所有匹配项并去掉作用域部分
        for match in re.findall(regex, content):
            results.append(match[len(scope):])

        return _filter(results)

    @staticmethod
    @lru_cache(maxsize=None)
    def html_crawl(url, scope, content):
        """
        从HTML内容中解析出链接地址。

        :param url: 当前页面的完整URL
        :param scope: 作用域基础URL
        :param content: HTML内容（字节串）
        :return: 提取并过滤后的路径集合
        """
        results = []
        soup = BeautifulSoup(content, 'html.parser')

        # 遍历需要爬取的标签
        for tag in CRAWL_TAGS:
            for found in soup.find_all(tag):
                # 获取指定属性中的值
                for attr in CRAWL_ATTRIBUTES:
                    value = found.get(attr)

                    if not value:
                        continue

                    # 处理绝对路径、相对路径及站内链接
                    if value.startswith("/"):
                        results.append(value[1:])
                    elif value.startswith(scope):
                        results.append(value[len(scope):])
                    elif not re.search(URI_REGEX, value):
                        new_url = merge_path(url, value)
                        results.append(parse_path(new_url))

        return _filter(results)

    @staticmethod
    @lru_cache(maxsize=None)
    def robots_crawl(url, scope, content):
        """
        从robots.txt文件中提取Disallow和Allow规则中的路径。

        :param url: robots.txt的完整URL
        :param scope: 作用域基础URL
        :param content: robots.txt的内容（字节串）
        :return: 提取并过滤后的路径集合
        """
        return _filter(re.findall(ROBOTS_TXT_REGEX, content))

