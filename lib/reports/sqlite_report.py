import sqlite3
import time

from lib.core.decorators import locked
from lib.reports.base import FileBaseReport


class SQLiteReport(FileBaseReport):
    """
    SQLite报告生成器类

    该类用于将扫描结果保存到SQLite数据库中，每个主机创建一个独立的数据表
    """

    def generate(self, entries):
        """
        生成SQL命令列表用于创建表和插入数据

        Args:
            entries: 包含扫描结果条目的列表，每个条目应包含url、status、length、type、redirect等属性

        Returns:
            list: 包含SQL命令及其参数的列表，每个元素为一个包含命令和可选参数的列表
        """
        commands = []
        created_tables = []

        for entry in entries:
            # 从URL中提取主机名作为表名
            host = entry.url.split("/")[2]
            if host not in created_tables:
                # 如果该主机的表还未创建，则先删除可能存在的同名表，然后创建新表
                commands.append([f"DROP TABLE IF EXISTS `{host}`"])
                commands.append(
                    [
                        f"""CREATE TABLE `{host}`
                        ([time] TEXT, [url] TEXT, [status_code] INTEGER, [content_length] INTEGER, [content_type] TEXT, [redirect] TEXT)"""
                    ]
                )
                created_tables.append(host)

            # 为当前条目生成插入语句，使用参数化查询防止SQL注入
            commands.append(
                [
                    f"""INSERT INTO `{host}` (time, url, status_code, content_length, content_type, redirect)
                    VALUES
                    (?, ?, ?, ?, ?, ?)""",
                    (
                        time.ctime(),
                        entry.url,
                        entry.status,
                        entry.length,
                        entry.type,
                        entry.redirect,
                    ),
                ]
            )

        return commands

    def open(self):
        """
        打开SQLite数据库连接并创建游标对象
        """
        self.file = sqlite3.connect(self.output, check_same_thread=False)
        self.cursor = self.file.cursor()

    @locked
    def save(self):
        """
        执行所有SQL命令并将结果保存到数据库中
        使用装饰器确保线程安全
        """
        for command in self.generate():
            self.cursor.execute(*command)

        self.file.commit()

