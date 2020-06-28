#coding:utf8
"""
目的：解决 Unicode 编码和字符串转换
"""


def text2unicode(string, to_byte=False):
    """字符串转 Unicode
    
    一种方式直接得到 unicode 表示的非字节型字符串，另一种是需要转换为字节型字符串，需要通过
    to_byte 参数调整，默认为 False 即转换为非字节型字符串。
    Examples:
    >>> string = "这个是一个测试字符串"
    >>> print(text2unicode(string)) # 默认情况是直接得到 16 进制字符串
        \u8FD9\u4E2A\u662F\u4E00\u4E2A\u6D4B\u8BD5\u5B57\u7B26\u4E32
    >>> print("\u8FD9\u4E2A\u662F\u4E00\u4E2A\u6D4B\u8BD5\u5B57\u7B26\u4E32")
        这个是一个测试字符串
    >>> print(text2unicode(string), True) # 转换为字节型字符
        b'\\u8fd9\\u4e2a\\u662f\\u4e00\\u4e2a\\u6d4b\\u8bd5\\u5b57\\u7b26\\u4e32'
    """
    if not to_byte:
        result = ''
        for char in string:
            result += "\\u{:0>4s}".format(hex(ord(char)).upper().replace('0X', ''))
    else:
        result = string.encode("raw_unicode_escape")

    return result



def unicode2text(string):
    """Unicode 转字符

    存在两种情况，传入参数为字节型数据，另一种情况是直接传入 Unicode 字符串。

    Examples:
    >>> string = b'\\u8fd9\\u4e2a\\u662f\\u4e00\\u4e2a\\u6d4b\\u8bd5\\u5b57\\u7b26\\u4e32'
    >>> unicode2text(string) # 字节型数据转换
        '这个是一个测试字符串'
    >>> string = '\\u8fd9\\u4e2a\\u662f\\u4e00\\u4e2a\\u6d4b\\u8bd5\\u5b57\\u7b26\\u4e32'
    >>> unicode2text(string) # 字符串型数据转换
        '这个是一个测试字符串'
    """
    if isinstance(string, str):
        result = string.encode().decode("raw_unicode_escape")
    elif isinstance(string, bytes):
        result = string.decode("raw_unicode_escape")
    else:
        raise TypeError(f"Support unicode string or bytes, but get {type(string)}")

    return result


if __name__ == "__main__":
    text = "这个是一个测试文件"
    text = "这个是一个测试字符串"
    print(text2unicode(text, True))
    print("Inversed without bytes: ", unicode2text(text2unicode(text)))
    print("Inversed with bytes: ", unicode2text(text2unicode(text, True)))