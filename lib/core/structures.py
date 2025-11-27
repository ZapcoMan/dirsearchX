class CaseInsensitiveDict(dict):
    """
    一个大小写不敏感的字典类，继承自dict
    所有字符串键都会被自动转换为小写形式进行存储和查找
    """

    def __init__(self, *args, **kwargs):
        """
        初始化CaseInsensitiveDict实例

        Args:
            *args: 位置参数，传递给父类dict的构造函数
            **kwargs: 关键字参数，传递给父类dict的构造函数
        """
        super().__init__(*args, **kwargs)
        self._convert_keys()

    def __setitem__(self, key, value):
        """
        设置字典项，将字符串键转换为小写后存储

        Args:
            key: 字典的键，如果是字符串则会被转换为小写
            value: 字典的值
        """
        if isinstance(key, str):
            key = key.lower()

        super().__setitem__(key.lower(), value)

    def __getitem__(self, key):
        """
        获取字典项，将字符串键转换为小写后查找

        Args:
            key: 要查找的键，如果是字符串则会被转换为小写

        Returns:
            与键关联的值
        """
        if isinstance(key, str):
            key = key.lower()

        return super().__getitem__(key.lower())

    def _convert_keys(self):
        """
        将现有所有键转换为小写形式
        遍历当前字典的所有键，将其转换为小写并重新设置
        """
        for key in list(self.keys()):
            value = super().pop(key)
            self.__setitem__(key, value)


class OrderedSet():
    """
    有序集合类，保持元素插入顺序且不允许重复元素
    内部使用字典实现，利用字典键的唯一性和Python 3.7+字典保持插入顺序的特性
    """

    def __init__(self, items=[]):
        """
        初始化OrderedSet实例

        Args:
            items: 可选的初始元素列表，默认为空列表
        """
        self._data = dict()

        for item in items:
            self._data[item] = None

    def __contains__(self, item):
        """
        检查元素是否在集合中

        Args:
            item: 要检查的元素

        Returns:
            bool: 元素存在返回True，否则返回False
        """
        return item in self._data

    def __eq__(self, other):
        """
        比较两个OrderedSet是否相等

        Args:
            other: 另一个OrderedSet对象

        Returns:
            bool: 键序列相同返回True，否则返回False
        """
        return self._data.keys() == other._data.keys()

    def __iter__(self):
        """
        返回集合的迭代器

        Returns:
            iterator: 集合元素的迭代器
        """
        return iter(list(self._data))

    def __len__(self):
        """
        返回集合中元素的数量

        Returns:
            int: 集合中元素的个数
        """
        return len(self._data)

    def add(self, item):
        """
        向集合中添加元素

        Args:
            item: 要添加的元素
        """
        self._data[item] = None

    def clear(self):
        """
        清空集合中的所有元素
        """
        self._data.clear()

    def discard(self, item):
        """
        移除集合中的指定元素，如果元素不存在不抛出异常

        Args:
            item: 要移除的元素
        """
        self._data.pop(item, None)

    def pop(self):
        """
        移除并返回集合中的最后一个元素
        """
        self._data.popitem()

    def remove(self, item):
        """
        移除集合中的指定元素，如果元素不存在会抛出KeyError异常

        Args:
            item: 要移除的元素

        Raises:
            KeyError: 当要移除的元素不存在时抛出
        """
        del self._data[item]

    def update(self, items):
        """
        将多个元素添加到集合中

        Args:
            items: 要添加的元素序列
        """
        for item in items:
            self.add(item)

