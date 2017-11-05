import socket
import ssl


def parsed_url(url):
    """
    解析 url 返回 (protocol host port path)
    """
    # 检查协议
    protocol = 'http'
    if url[:7] == 'http://':
        u = url.split('://')[1]
    elif url[:8] == 'https://':
        protocol = 'https'
        u = url.split('://')[1]
    else:
        # '://' 定位 然后取第一个 / 的位置来切片
        u = url

    # 检查默认 path
    i = u.find('/')
    if i == -1:
        host = u
        path = '/'
    else:
        host = u[:i]
        path = u[i:]

    # 检查端口
    port_dict = {
        'http': 80,
        'https': 443,
    }

    # 默认端口
    port = port_dict[protocol]
    if host.find(':') != -1:
        h = host.split(':')
        host = h[0]
        port = int(h[1])

    return protocol, host, port, path


def socket_by_protocol(protocol):
    """
    根据协议返回一个 socket 实例
    """
    if protocol == 'http':
        s = socket.socket()
    else:
        # HTTPS 协议需要使用 ssl.wrap_socket 包装一下原始的 socket
        s = ssl.wrap_socket(socket.socket())
    return s


def response_by_socket(s):
    """
    参数是一个 socket 实例
    返回这个 socket 读取的所有数据
    """
    response = b''
    buffer_size = 1024
    while True:
        r = s.recv(buffer_size)
        if len(r) == 0:
            break
        response += r
    return response


def parsed_response(r):
    """
    把 response 解析出 状态码 headers body 返回
    状态码是 int
    headers 是 dict
    body 是 str
    """
    header, body = r.split('\r\n\r\n', 1)
    h = header.split('\r\n')
    status_code = h[0].split()[1]
    status_code = int(status_code)

    headers = {}
    for line in h[1:]:
        k, v = line.split(': ')
        headers[k] = v
    return status_code, headers, body


def path_with_query(path, query):
    """
    path 是一个字符串
    query 是一个字典

    返回一个拼接后的 url
    详情请看下方测试函数
    """
    all_query = ''
    length = len(query) - 1
    for j, i in enumerate(query):
        all_query = i + '=' + str(query[i])
        while j < length:
            all_query += '&'
    answer = path + '?' + all_query
    return answer


def test_path_with_query():
    path = '/'
    query = {
        'name': 'gua',
        'height': 169,
    }
    expected = [
        '/?name=gua&height=169',
        '/?height=169&name=gua',
    ]
    e = 'xxx'
    assert path_with_query(path, query) in expected, e


# test_path_with_query()


def get(url, query):
    """
    用 GET 请求 url 并返回响应
    """
    protocol, host, port, path = parsed_url(url)
    path = path_with_query(path, query)

    s = socket_by_protocol(protocol)
    s.connect((host, port))

    request = 'GET {} HTTP/1.1\r\nhost: {}\r\nConnection: close\r\n\r\n'.format(path, host)
    encoding = 'utf-8'
    s.send(request.encode(encoding))

    response = response_by_socket(s)
    r = response.decode(encoding)

    status_code, headers, body = parsed_response(r)
    if status_code == 301:
        url = headers['Location']
        return get(url, query)
    return status_code, headers, body


def header_from_dict(headers):
    """
    headers 是一个字典
    返回如下 str
    'Content-Type: text/html\r\nContent-Length: 127\r\n'
    """
    header = ''
    for j in headers:
        header += j + ':' + ' ' + str(headers[j]) + '\r\n'
    return header


headers = {
    'Content-Type': 'text/html',
    'Content-Length': 127,
}
header_from_dict(headers)


def test_header_from_dict():
    headers = {
        'Content-Type': 'text/html',
        'Content-Length': 127,
    }
    expected = [
        'Content-Type: text/html\r\nContent-Length: 127\r\n',
        'Content-Length: 127\r\nContent-Type: text/html\r\n',
    ]
    e = 'xxx'
    assert header_from_dict(headers) in expected, e


test_header_from_dict()


def find_between(body, ciuu):
    a = body.split('div class="hd"')
    j = 25 * ciuu
    for one_movie in a[1:]:
        b = one_movie.split('</span>', 1)
        c = b[0]
        movie_name = c.split('<span class="title">')[1]
        d = b[1]
        e = d.split('<span class="rating_num" property="v:average">')[1]
        f = e.split('</span>', 1)
        movie_num = f[0]
        g = f[1].split('<span>')[1]
        h = g.split('</span>', 1)
        movie_pyjw = h[0]
        i = h[1]
        if i.find('<span class="inq">') != -1:
            i = h[1].split('<span class="inq">')[1]
            movie_mcuu = i.split('</span>', 1)[0]
        else:
            movie_mcuu = 'has no quote'
        j += 1
        k = '第{}名\r\n电影名:{}\r\n分数:{}\r\n评价人数:{}\r\n一句话点评:{}\r\n'.format(j, movie_name, movie_num, movie_pyjw,
                                                                        movie_mcuu)
        print(k)

    pass


def yoyoyo():
    for i in range(10):
        l = [
            {'start': 0},
            {'start': 25},
            {'start': 50},
            {'start': 75},
            {'start': 100},
            {'start': 125},
            {'start': 150},
            {'start': 175},
            {'start': 200},
            {'start': 225},
        ]
        query = l[i]
        # 这里因为是http协议, 在get函数里会被递归一次, 所以还有问题, 若干年后如果记得的话回来优化一下把...
        url = 'http://movie.douban.com/top250'
        status_code, headers, body = get(url, query)
        find_between(body, i)


def main():
    yoyoyo()


if __name__ == '__main__':
    main()
