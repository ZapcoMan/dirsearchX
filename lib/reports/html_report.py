import os
import sys
import time

from jinja2 import Environment, FileSystemLoader

from lib.reports.base import FileBaseReport
from lib.utils.common import human_size


class HTMLReport(FileBaseReport):
    """
    HTML报告生成器类

    该类继承自FileBaseReport，用于生成HTML格式的扫描结果报告
    """

    def generate(self, entries):
        """
        生成HTML格式的报告

        Args:
            entries: 扫描结果条目列表，每个条目包含URL、状态码、内容长度等信息

        Returns:
            str: 渲染后的HTML报告字符串
        """
        # 配置Jinja2模板环境，加载报告模板
        file_loader = FileSystemLoader(
            os.path.dirname(os.path.realpath(__file__)) + "/templates/"
        )
        env = Environment(loader=file_loader)
        template = env.get_template("html_report_template.html")

        # 准备报告元数据，包括命令行参数和生成时间
        metadata = {"command": " ".join(sys.argv), "date": time.ctime()}
        results = []

        # 处理每个扫描结果条目，根据状态码设置相应的CSS样式类
        for entry in entries:
            status_color_class = ""
            if entry.status >= 200 and entry.status <= 299:
                status_color_class = "text-success"
            elif entry.status >= 300 and entry.status <= 399:
                status_color_class = "text-warning"
            elif entry.status >= 400 and entry.status <= 599:
                status_color_class = "text-danger"

            # 将处理后的结果添加到结果列表中
            results.append(
                {
                    "url": entry.url,
                    "status": entry.status,
                    "statusColorClass": status_color_class,
                    "contentLength": human_size(entry.length),
                    "contentType": entry.type,
                    "redirect": entry.redirect,
                }
            )

        # 使用模板渲染最终的HTML报告
        return template.render(metadata=metadata, results=results)

