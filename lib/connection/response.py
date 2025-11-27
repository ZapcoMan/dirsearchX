from lib.core.settings import (
    DEFAULT_ENCODING, ITER_CHUNK_SIZE,
    MAX_RESPONSE_SIZE, UNKNOWN,
)
from lib.parse.url import clean_path, parse_path
from lib.utils.common import is_binary


class Response:
    """
    响应类，用于封装HTTP响应信息

    Args:
        response: 原始HTTP响应对象

    Attributes:
        url: 响应的完整URL
        full_path: 解析后的完整路径
        path: 清理后的路径
        status: HTTP状态码
        headers: 响应头字典
        redirect: 重定向地址
        history: 重定向历史URL列表
        content: 解码后的文本内容
        body: 原始二进制内容
    """

    def __init__(self, response):
        # 初始化基本响应信息
        self.url = response.url
        self.full_path = parse_path(response.url)
        self.path = clean_path(self.full_path)
        self.status = response.status_code
        self.headers = response.headers
        self.redirect = self.headers.get("location") or ""
        self.history = [res.url for res in response.history]
        self.content = ""
        self.body = b""

        # 分块读取响应内容，避免内存溢出
        for chunk in response.iter_content(chunk_size=ITER_CHUNK_SIZE):
            self.body += chunk

            # 当达到最大响应大小或检测到二进制内容时停止读取
            if len(self.body) >= MAX_RESPONSE_SIZE or (
                "content-length" in self.headers and is_binary(self.body)
            ):
                break

        # 如果不是二进制内容，则解码为文本
        if not is_binary(self.body):
            self.content = self.body.decode(
                response.encoding or DEFAULT_ENCODING, errors="ignore"
            )

    @property
    def type(self):
        """
        获取响应的内容类型

        Returns:
            str: 内容类型字符串，如果无法获取则返回UNKNOWN
        """
        if "content-type" in self.headers:
            return self.headers.get("content-type").split(";")[0]

        return UNKNOWN

    @property
    def length(self):
        """
        获取响应内容长度

        Returns:
            int: 响应内容长度，优先从header获取，失败则返回body的实际长度
        """
        try:
            return int(self.headers.get("content-length"))
        except TypeError:
            return len(self.body)

    def __hash__(self):
        """
        计算响应对象的哈希值

        Returns:
            int: 基于响应body的哈希值
        """
        return hash(self.body)

    def __eq__(self, other):
        """
        比较两个响应对象是否相等

        Args:
            other: 另一个Response对象

        Returns:
            bool: 如果状态码、body内容和重定向地址都相同则返回True
        """
        return (self.status, self.body, self.redirect) == (
            other.status,
            other.body,
            other.redirect,
        )

