import time
import sys

from lib.core.settings import NEW_LINE
from lib.reports.base import FileBaseReport
from lib.utils.common import human_size


class PlainTextReport(FileBaseReport):
    """
    纯文本报告生成器类

    继承自FileBaseReport，用于生成纯文本格式的扫描结果报告
    """

    def get_header(self):
        """
        生成报告头部信息

        返回包含程序启动时间和命令行参数的头部字符串

        Returns:
            str: 格式化的头部信息字符串
        """
        # 构造包含启动时间和命令行参数的头部信息
        return f"# Dirsearch started {time.ctime()} as: {chr(32).join(sys.argv)}" + NEW_LINE * 2

    def generate(self, entries):
        """
        生成纯文本格式的报告内容

        遍历所有扫描结果条目，格式化每个条目的状态码、大小和URL信息，
        并处理重定向信息，最终生成完整的报告文本

        Args:
            entries: 扫描结果条目列表，每个条目包含status、length、url和redirect等属性

        Returns:
            str: 完整的纯文本格式报告内容
        """
        # 初始化输出内容，添加报告头部
        output = self.get_header()

        # 遍历所有扫描结果条目并格式化输出
        for entry in entries:
            # 将字节大小转换为人类可读格式
            readable_size = human_size(entry.length)
            # 格式化状态码、大小和URL信息
            output += f"{entry.status}  {readable_size.rjust(6, chr(32))}  {entry.url}"

            # 如果存在重定向，则添加重定向信息
            if entry.redirect:
                output += f"    -> REDIRECTS TO: {entry.redirect}"

            # 添加换行符
            output += NEW_LINE

        return output

