import ssl
import socket

from lib.core.settings import SOCKET_TIMEOUT


def detect_scheme(host, port):
    """
    检测指定主机和端口使用的协议是HTTP还是HTTPS

    :param host: 主机名或IP地址
    :param port: 端口号
    :return: "https" 如果支持SSL连接，否则返回"http"
    :raises ValueError: 当端口为空时抛出异常
    """
    if not port:
        raise ValueError

    # 创建socket连接并设置超时时间
    s = socket.socket()
    s.settimeout(SOCKET_TIMEOUT)
    conn = ssl.SSLContext().wrap_socket(s)

    try:
        # 尝试建立SSL连接来检测是否支持HTTPS
        conn.connect((host, port))
        conn.close()
        return "https"
    except Exception:
        # SSL连接失败，返回HTTP协议
        return "http"

