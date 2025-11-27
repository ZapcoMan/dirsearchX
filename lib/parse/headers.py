from email.parser import BytesParser

from lib.core.settings import NEW_LINE
from lib.core.structures import CaseInsensitiveDict


class HeadersParser:
    """
    HTTP头部解析器类，用于在字符串格式和字典格式之间转换HTTP头部信息

    Args:
        headers (str or dict): HTTP头部信息，可以是字符串格式或字典格式

    Attributes:
        str (str): 字符串格式的HTTP头部信息
        dict (dict): 字典格式的HTTP头部信息
        headers (CaseInsensitiveDict): 大小写不敏感的字典格式头部信息
    """
    def __init__(self, headers):
        self.str = self.dict = headers

        if isinstance(headers, str):
            self.dict = self.str_to_dict(headers)
        elif isinstance(headers, dict):
            self.str = self.dict_to_str(headers)
            self.dict = self.str_to_dict(self.str)

        self.headers = CaseInsensitiveDict(self.dict)

    def get(self, key):
        """
        获取指定键的头部值

        Args:
            key (str): 头部键名

        Returns:
            str: 对应的头部值
        """
        return self.headers[key]

    @staticmethod
    def str_to_dict(headers):
        """
        将字符串格式的HTTP头部转换为字典格式

        Args:
            headers (str): 字符串格式的HTTP头部信息

        Returns:
            dict: 字典格式的HTTP头部信息
        """
        if not headers:
            return {}

        return dict(BytesParser().parsebytes(headers.encode()))

    @staticmethod
    def dict_to_str(headers):
        """
        将字典格式的HTTP头部转换为字符串格式

        Args:
            headers (dict): 字典格式的HTTP头部信息

        Returns:
            str: 字符串格式的HTTP头部信息，各头部项用换行符分隔
        """
        if not headers:
            return

        return NEW_LINE.join(f"{key}: {value}" for key, value in headers.items())

    def __iter__(self):
        """
        返回头部信息的迭代器

        Returns:
            iterator: 头部信息键值对的迭代器
        """
        return iter(self.headers.items())

    def __str__(self):
        """
        返回字符串格式的HTTP头部信息

        Returns:
            str: 字符串格式的HTTP头部信息
        """
        return self.str

