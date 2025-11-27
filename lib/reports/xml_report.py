import time
import sys

from xml.dom import minidom
from xml.etree import ElementTree as ET

from lib.core.settings import DEFAULT_ENCODING
from lib.reports.base import FileBaseReport


class XMLReport(FileBaseReport):
    """
    XML报告生成器类

    该类继承自FileBaseReport，用于将扫描结果生成XML格式的报告
    """

    def generate(self, entries):
        """
        生成XML格式的扫描报告

        Args:
            entries: 扫描结果条目列表，每个条目包含url、status、length、type和redirect等信息

        Returns:
            str: 格式化后的XML字符串，包含所有扫描结果信息
        """
        # 创建根元素，包含命令行参数和扫描时间属性
        tree = ET.Element("dirsearchscan", args=" ".join(sys.argv), time=time.ctime())

        # 遍历所有扫描结果条目，为每个条目创建XML节点
        for entry in entries:
            # 创建目标节点，包含URL属性
            target = ET.SubElement(tree, "target", url=entry.url)
            # 添加状态码子节点
            ET.SubElement(target, "status").text = str(entry.status)
            # 添加内容长度子节点
            ET.SubElement(target, "contentLength").text = str(entry.length)
            # 添加内容类型子节点
            ET.SubElement(target, "contentType").text = entry.type
            # 如果存在重定向信息，则添加重定向子节点
            if entry.redirect:
                ET.SubElement(target, "redirect").text = entry.redirect

        # 将XML树转换为字符串
        output = ET.tostring(tree, encoding=DEFAULT_ENCODING, method="xml")
        # 美化XML输出格式
        return minidom.parseString(output).toprettyxml()

