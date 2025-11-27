import configparser


class ConfigParser(configparser.ConfigParser):
    """
    安全配置解析器类，扩展了标准ConfigParser功能，提供带默认值和允许值检查的安全读取方法

    该类继承自configparser.ConfigParser，增加了safe_get系列方法来避免在读取不存在的section或option时抛出异常
    """

    def safe_get(self, section, option, default=None, allowed=None):
        """
        安全地获取配置字符串值

        参数:
            section (str): 配置节名称
            option (str): 配置项名称
            default (any): 当找不到配置项时返回的默认值，默认为None
            allowed (list/tuple/set): 允许的值列表，如果设置且实际值不在其中则返回默认值，默认为None

        返回:
            any: 获取到的配置值或默认值
        """
        try:
            result = super().get(section, option)

            # 如果设置了允许值检查，则验证结果是否在允许范围内
            if allowed is not None:
                return result if result in allowed else default

            return result
        except (configparser.NoSectionError, configparser.NoOptionError):
            # 捕获节或选项不存在的异常，返回默认值
            return default

    def safe_getfloat(self, section, option, default=0, allowed=None):
        """
        安全地获取配置浮点数值

        参数:
            section (str): 配置节名称
            option (str): 配置项名称
            default (float): 当找不到配置项时返回的默认值，默认为0
            allowed (list/tuple/set): 允许的值列表，如果设置且实际值不在其中则返回默认值，默认为None

        返回:
            float: 获取到的配置浮点数值或默认值
        """
        try:
            result = super().getfloat(section, option)

            # 如果设置了允许值检查，则验证结果是否在允许范围内
            if allowed is not None:
                return result if result in allowed else default

            return result
        except (configparser.NoSectionError, configparser.NoOptionError):
            # 捕获节或选项不存在的异常，返回默认值
            return default

    def safe_getboolean(self, section, option, default=False, allowed=None):
        """
        安全地获取配置布尔值

        参数:
            section (str): 配置节名称
            option (str): 配置项名称
            default (bool): 当找不到配置项时返回的默认值，默认为False
            allowed (list/tuple/set): 允许的值列表，如果设置且实际值不在其中则返回默认值，默认为None

        返回:
            bool: 获取到的配置布尔值或默认值
        """
        try:
            result = super().getboolean(section, option)

            # 如果设置了允许值检查，则验证结果是否在允许范围内
            if allowed is not None:
                return result if result in allowed else default

            return result
        except (configparser.NoSectionError, configparser.NoOptionError):
            # 捕获节或选项不存在的异常，返回默认值
            return default

    def safe_getint(self, section, option, default=0, allowed=None):
        """
        安全地获取配置整数值

        参数:
            section (str): 配置节名称
            option (str): 配置项名称
            default (int): 当找不到配置项时返回的默认值，默认为0
            allowed (list/tuple/set): 允许的值列表，如果设置且实际值不在其中则返回默认值，默认为None

        返回:
            int: 获取到的配置整数值或默认值
        """
        try:
            result = super().getint(section, option)

            # 如果设置了允许值检查，则验证结果是否在允许范围内
            if allowed is not None:
                return result if result in allowed else default

            return result
        except (configparser.NoSectionError, configparser.NoOptionError):
            # 捕获节或选项不存在的异常，返回默认值
            return default

