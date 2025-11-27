from lib.core.settings import NEW_LINE
from lib.reports.base import FileBaseReport
from lib.utils.common import escape_csv


class CSVReport(FileBaseReport):
    """
    CSV报告生成器类

    继承自FileBaseReport，用于生成CSV格式的扫描结果报告
    """

    def get_header(self):
        """
        获取CSV文件头部信息

        返回值:
            str: 包含列名的CSV头部字符串，以换行符结尾
        """
        return "URL,Status,Size,Content Type,Redirection" + NEW_LINE

    def generate(self, entries):
        """
        生成CSV格式的报告内容

        参数:
            entries: 扫描结果条目列表，每个条目应包含url、status、length、type和redirect属性

        返回值:
            str: 完整的CSV格式报告字符串
        """
        output = self.get_header()

        # 遍历所有扫描结果条目，生成CSV行数据
        for entry in entries:
            output += f"{entry.url},{entry.status},{entry.length},{entry.type},"

            # 如果存在重定向信息，则对其进行CSV转义处理后添加到输出
            if entry.redirect:
                output += f'"{escape_csv(entry.redirect)}"'

            output += NEW_LINE

        return output

