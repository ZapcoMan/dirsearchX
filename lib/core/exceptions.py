class FailedDependenciesInstallation(Exception):
    """
    自定义异常类，用于表示依赖安装失败的情况

    这个异常类继承自Python内置的Exception类，专门用于处理依赖包安装过程中出现的错误情况。
    当系统无法成功安装所需的依赖包时，会抛出此异常。
    """
    pass


class InvalidRawRequest(Exception):
    """
    自定义异常类，用于表示原始请求无效的情况

    这个异常类继承自Python内置的Exception类，专门用于处理接收到的原始HTTP请求格式不正确
    或者内容无效的错误情况。当解析或验证原始请求数据失败时会抛出此异常。
    """
    pass


class InvalidURLException(Exception):
    """
    自定义异常类，用于表示URL地址无效的情况

    这个异常类继承自Python内置的Exception类，专门用于处理URL格式错误、无法解析或者
    不符合预期格式的URL地址。当系统遇到无法处理的URL时会抛出此异常。
    """
    pass


class RequestException(Exception):
    """
    自定义异常类，用于表示请求处理过程中的通用错误

    这个异常类继承自Python内置的Exception类，作为处理HTTP请求相关错误的基类异常。
    用于捕获和处理在请求发送、接收、解析等过程中发生的各种异常情况。
    """
    pass


class SkipTargetInterrupt(Exception):
    """
    自定义异常类，用于表示跳过当前目标的中断操作

    这个异常类继承自Python内置的Exception类，专门用于在程序执行过程中需要跳过当前处理目标
    并继续处理下一个目标的场景。通过抛出此异常来实现流程控制中的跳过操作。
    """
    pass


class QuitInterrupt(Exception):
    """
    自定义异常类，用于表示退出程序的中断操作

    这个异常类继承自Python内置的Exception类，专门用于在程序执行过程中需要立即终止程序运行
    的场景。通过抛出此异常来实现优雅的程序退出机制。
    """
    pass


class UnpicklingError(Exception):
    """
    自定义异常类，用于表示反序列化过程中的错误

    这个异常类继承自Python内置的Exception类，专门用于处理pickle模块在反序列化对象时发生
    的各种错误。当从字节流恢复Python对象的过程中出现问题时会抛出此异常。
    """
    pass

