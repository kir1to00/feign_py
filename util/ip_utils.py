import socket


def get_local_ip():
    try:
        # 创建一个UDP套接字
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # 连接到一个外部地址（不发送数据）
        sock.connect(("8.8.8.8", 80))
        # 获取本地IP地址
        local_ip = sock.getsockname()[0]
        # 关闭套接字
        sock.close()
        return local_ip
    except Exception as e:
        print(f"Error getting local IP: {e}")
        return None


def ip_to_long(ip: str) -> int:
    try:
        ip_parts = [int(part) for part in ip.split('.')]

        if len(ip_parts) != 4 or any(not (0 <= part <= 255) for part in ip_parts):
            raise ValueError("Invalid IPv4 address format")

        result = 0
        for i, part in enumerate(ip_parts):
            result = (result << 8) | part

        return result
    except (AttributeError, ValueError) as e:
        raise ValueError(f"Invalid IPv4 address '{ip}': {e}")


def long_to_ip(num: int) -> str:
    if not 0 <= num <= 0xFFFFFFFF:
        raise ValueError("Input number out of IPv4 address range")

    ip_parts = []
    for i in reversed(range(4)):
        part, num = divmod(num, 256 ** i)
        ip_parts.append(str(part))

    return '.'.join(ip_parts)
