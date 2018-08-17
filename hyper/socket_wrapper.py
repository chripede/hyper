# -*- coding: utf-8 -*-
import socket
import socks


def create_connection_with_options(address, timeout=socket._GLOBAL_DEFAULT_TIMEOUT,
                                   socks5_proxy_host=None, socks5_proxy_port=None):
    host, port = address
    err = None
    for res in socket.getaddrinfo(host, port, 0, socket.SOCK_STREAM):
        af, socktype, proto, canonname, sa = res
        sock = None
        try:
            if socks5_proxy_host:
                sock = socks.socksocket(af, socktype, proto)
                sock.set_proxy(socks.SOCKS5, socks5_proxy_host, socks5_proxy_port)
            else:
                sock = socket.socket(af, socktype, proto)

            if timeout is not socket._GLOBAL_DEFAULT_TIMEOUT:
                sock.settimeout(timeout)
            sock.connect(sa)
            return sock

        except IOError as _:
            err = _
            if sock is not None:
                sock.close()

    if err is not None:
        raise err
    else:
        raise IOError("getaddrinfo returns an empty list")
