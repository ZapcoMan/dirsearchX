import re

from lib.core.data import options
from lib.core.decorators import locked
from lib.core.settings import (
    SCRIPT_PATH,
    EXTENSION_TAG,
    EXCLUDE_OVERWRITE_EXTENSIONS,
    EXTENSION_RECOGNITION_REGEX,
)
from lib.core.structures import OrderedSet
from lib.parse.url import clean_path
from lib.utils.common import lstrip_once
from lib.utils.file import FileUtils


def get_blacklists():
    """
    获取用于状态码过滤的忽略路径列表（黑名单）。

    根据指定的状态码（400、403、500），读取对应的黑名单文件，
    并构建一个字典结构存储这些黑名单内容。

    返回:
        dict: 键是状态码(int)，值是Dictionary对象，表示该状态码对应的黑名单路径集合。
    """
    blacklists = {}

    for status in [400, 403, 500]:
        blacklist_file_name = FileUtils.build_path(SCRIPT_PATH, "db")
        blacklist_file_name = FileUtils.build_path(
            blacklist_file_name, f"{status}_blacklist.txt"
        )

        if not FileUtils.can_read(blacklist_file_name):
            # 跳过无法读取的文件
            continue

        blacklists[status] = Dictionary(
            files=[blacklist_file_name],
            is_blacklist=True,
        )

    return blacklists


class Dictionary:
    """
    字典类，用于处理和生成扫描路径词典。

    支持经典模式与强制扩展模式两种方式来处理路径词典，并支持前缀、后缀等附加功能。
    """

    def __init__(self, **kwargs):
        """
        初始化Dictionary实例。

        参数:
            **kwargs: 可变关键字参数，传递给generate方法以生成路径项。
        """
        self._index = 0
        self._items = self.generate(**kwargs)

    @property
    def index(self):
        """
        当前迭代器索引位置。

        返回:
            int: 当前索引值。
        """
        return self._index

    @locked
    def __next__(self):
        """
        实现迭代器协议中的下一个元素获取逻辑。

        返回:
            str: 下一个路径字符串。

        异常:
            StopIteration: 当没有更多元素时抛出。
        """
        try:
            path = self._items[self._index]
        except IndexError:
            raise StopIteration

        self._index += 1

        return path

    def __contains__(self, item):
        """
        判断某个路径是否存在于当前词典中。

        参数:
            item (str): 待检查的路径字符串。

        返回:
            bool: 存在则返回True，否则False。
        """
        return item in self._items

    def __getstate__(self):
        """
        序列化对象状态。

        返回:
            tuple: 包含_items和_index的元组。
        """
        return (self._items, self._index)

    def __setstate__(self, state):
        """
        反序列化恢复对象状态。

        参数:
            state (tuple): 包含_items和_index的元组。
        """
        self._items, self._index = state

    def __iter__(self):
        """
        返回可迭代对象自身。

        返回:
            iter: 自身迭代器。
        """
        return iter(self._items)

    def __len__(self):
        """
        获取词典长度。

        返回:
            int: 词典中路径的数量。
        """
        return len(self._items)

    def generate(self, files=[], is_blacklist=False):
        """
        根据输入文件生成路径词典列表。

        处理包括替换%EXT%标签、追加扩展名、应用大小写转换等功能。

        参数:
            files (list): 文件路径列表，默认为空列表。
            is_blacklist (bool): 是否为黑名单模式，默认为False。

        返回:
            list: 经过处理后的路径字符串列表。
        """

        wordlist = OrderedSet()
        re_ext_tag = re.compile(EXTENSION_TAG, re.IGNORECASE)

        for dict_file in files:
            for line in FileUtils.get_lines(dict_file):
                # 移除开头的"/"以便后续处理前缀
                line = lstrip_once(line, "/")

                if options["remove_extensions"]:
                    line = line.split(".")[0]

                if not self.is_valid(line):
                    continue

                # 经典dirsearch词典处理（含有%EXT%关键字）
                if EXTENSION_TAG in line.lower():
                    for extension in options["extensions"]:
                        newline = re_ext_tag.sub(extension, line)
                        wordlist.add(newline)
                else:
                    wordlist.add(line)

                    # 黑名单不应使用“强制扩展”或“覆盖扩展”，避免误判
                    if is_blacklist:
                        continue

                    # 若启用强制扩展且路径不是目录或已有扩展名，则追加扩展名
                    if (
                        options["force_extensions"]
                        and "." not in line
                        and not line.endswith("/")
                    ):
                        wordlist.add(line + "/")

                        for extension in options["extensions"]:
                            wordlist.add(f"{line}.{extension}")
                    # 覆盖未知扩展名为选定扩展名（保留原始路径）
                    elif (
                        options["overwrite_extensions"]
                        and not line.endswith(options["extensions"] + EXCLUDE_OVERWRITE_EXTENSIONS)
                        # 含有查询参数的路径通常用于漏洞利用，跳过此类路径
                        and "?" not in line
                        and "#" not in line
                        and re.search(EXTENSION_RECOGNITION_REGEX, line)
                    ):
                        base = line.split(".")[0]

                        for extension in options["extensions"]:
                            wordlist.add(f"{base}.{extension}")

        if not is_blacklist:
            # 添加前缀和后缀
            altered_wordlist = OrderedSet()

            for path in wordlist:
                for pref in options["prefixes"]:
                    if (
                        not path.startswith(("/", pref))
                    ):
                        altered_wordlist.add(pref + path)
                for suff in options["suffixes"]:
                    if (
                        not path.endswith(("/", suff))
                        # 对URL片段添加后缀无意义
                        and "?" not in path
                        and "#" not in path
                    ):
                        altered_wordlist.add(path + suff)

            if altered_wordlist:
                wordlist = altered_wordlist

        if options["lowercase"]:
            return list(map(str.lower, wordlist))
        elif options["uppercase"]:
            return list(map(str.upper, wordlist))
        elif options["capitalization"]:
            return list(map(str.capitalize, wordlist))
        else:
            return list(wordlist)

    def is_valid(self, path):
        """
        检查路径是否有效。

        排除注释行、空行以及被排除的扩展名结尾的路径。

        参数:
            path (str): 待验证的路径字符串。

        返回:
            bool: 有效返回True，无效返回False。
        """
        # 忽略注释和空行
        if not path or path.startswith("#"):
            return False

        # 忽略具有排除扩展名的路径
        cleaned_path = clean_path(path)
        if cleaned_path.endswith(
            tuple(f".{extension}" for extension in options["exclude_extensions"])
        ):
            return False

        return True

    def reset(self):
        """
        重置内部索引计数器到初始状态。
        """
        self._index = 0

