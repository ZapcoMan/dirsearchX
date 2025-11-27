from socket import getaddrinfo

_dns_cache = {}


def cache_dns(domain, port, addr):
    """
    缓存DNS解析结果到全局缓存中

    :param domain: 域名
    :param port: 端口号
    :param addr: 地址
    """
    _dns_cache[domain, port] = getaddrinfo(addr, port)


def cached_getaddrinfo(*args, **kwargs):
    """
    socket.getaddrinfo 的替代品，它们是一样的，但功能是这样
    是否缓存答案以提升性能
    """

    # 提取主机名和端口用于缓存键
    host, port = args[:2]
    # 检查缓存中是否已存在该主机和端口的解析结果
    if (host, port) not in _dns_cache:
        _dns_cache[host, port] = getaddrinfo(*args, **kwargs)

    return _dns_cache[host, port]

