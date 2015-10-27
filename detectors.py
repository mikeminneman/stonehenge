import string

spacechars = ' \r\n\t'
spacebytes = bytes(spacechars, encoding='utf-8')

paddingchars = '\x04\x05\x08\x02\x06\x01'
paddingbytes = bytes(paddingchars, encoding='utf-8')

otherchars = '-'
otherbytes = bytes(otherchars, encoding='utf-8')


def remove_padding(content):
    if type(content) == bytes:
        firstsp = 0
        for i in range(0, len(content)):
            if not (content[i:i + 1] in paddingbytes):
                firstsp = i + 1
        return content[0:firstsp]
    elif type(content) == str:
        firstsp = 0
        for i in range(0, len(content)):
            if not (content[i:i + 1] in paddingchars):
                firstsp = i + 1
        return content[0:firstsp]
    return content


def detect_padding(content):
    if type(content) == bytes:
        firstsp = 0
        for i in range(0, len(content)):
            if not (content[i:i + 1] in paddingbytes):
                firstsp = i + 1
        return firstsp != len(content)
    elif type(content) == str:
        firstsp = 0
        for i in range(0, len(content)):
            if not (content[i:i + 1] in paddingchars):
                firstsp = i + 1
        return firstsp != len(content)
    return False


def remove_spaces(content):  # returns string
    if type(content) == bytes:
        nosp = b''
        for i in range(0, len(content)):
            if not (content[i:i + 1] in spacebytes):
                nosp += content[i:i + 1]
        return nosp
    elif type(content) == str:
        nosp = ''
        for i in range(0, len(content)):
            if not (content[i:i + 1] in spacechars):
                nosp += content[i:i + 1]
        return nosp
    return b''


def detect_spaces(content):  # returns boolean
    if type(content) == bytes:
        nosp = False
        for i in range(0, len(content)):
            if content[i:i + 1] in spacebytes:
                nosp = True
                return nosp
        return nosp
    elif type(content) == str:
        nosp = False
        for i in range(0, len(content)):
            if content[i:i + 1] in spacechars:
                nosp = True
                return nosp
        return nosp
    return False


def remove_other(content):  # returns string
    if type(content) == bytes:
        nosp = b''
        for i in range(0, len(content)):
            if not (content[i:i + 1] in otherbytes):
                nosp += content[i:i + 1]
        return nosp
    elif type(content) == str:
        nosp = ''
        for i in range(0, len(content)):
            if not (content[i:i + 1] in otherchars):
                nosp += content[i:i + 1]
        return nosp
    return b''


def detect_other(content):  # returns boolean
    if type(content) == bytes:
        nosp = False
        for i in range(0, len(content)):
            if content[i:i + 1] in otherbytes:
                nosp = True
                return nosp
        return nosp
    elif type(content) == str:
        nosp = False
        for i in range(0, len(content)):
            if content[i:i + 1] in otherchars:
                nosp = True
                return nosp
        return nosp
    return False


def detect_hex(text):  # returns boolean
    if len(text) % 2 != 0:
        return False
    if type(text) == bytes:
        return all(c in bytes(string.hexdigits, encoding='utf-8') for c in text)
    elif type(text) == str:
        return all(c in string.hexdigits for c in text)
    return False


def detect_hex_w_spaces(text):
    return detect_spaces(text) and detect_hex(remove_spaces(text))


def detect_hex_w_padding(text):
    return detect_padding(text) and detect_hex(remove_spaces(remove_padding(text)))


def detect_hexlike(text):
    if len(text) % 2 != 0:
        return False
    extrachars = '#Vv'
    if type(text) == bytes:
        return not (detect_hex(text)) and all(c in bytes(string.hexdigits + extrachars, encoding='utf-8') for c in text)
    elif type(text) == str:
        return not (detect_hex(text)) and all(c in string.hexdigits + extrachars for c in text)


def detect_hexlike_w_spaces(text):
    return detect_spaces(text) and detect_hexlike(remove_spaces(text))


def detect_binary(text):
    bits = '01'
    if type(text) == bytes:
        return all(c in bytes(bits, encoding='utf-8') for c in text)
    elif type(text) == str:
        return all(c in bits for c in text)
    return False


def detect_binary_w_spaces(content):
    return detect_spaces(content) and detect_binary(remove_spaces(content))


def detect_binary_w_other(content):
    return detect_other(content) and detect_binary(remove_spaces(remove_other(content)))


def detect_base64(text):
    validchars = string.ascii_letters + string.digits + '+/='
    validbytes = bytes(validchars, encoding='utf-8')
    if type(text) == bytes:
        return len(text) % 4 == 0 and all(c in validbytes for c in text)
    elif type(text) == str:
        return len(text) % 4 == 0 and all(c in validchars for c in text)
    return False


def detect_mult4(text):
    return len(text) % 4 == 0 and len(text) > 0


def detect_mult8(text):
    return len(text) % 8 == 0 and len(text) > 0


def detect_ascii(val):  # returns boolean
    try:
        result = str(val, encoding='ascii')
    except UnicodeDecodeError:
        result = ''
    return len(result) > 0


def detect_utf8(val):  # returns boolean
    try:
        result = str(val, encoding='utf-8')
    except UnicodeDecodeError:
        result = ''
    return len(result) > 0


def detect_utf8end(text):
    return not (detect_utf8(text)) and detect_utf8(remove_first8(text))


def get_first8(val):  # returns value
    return val[:8]


def remove_first8(val):  # returns value
    return b"" if len(val) < 8 else val[8:len(val)]


def detect_brackets(content):
    return content[0:6] == b'[3des]'


def remove_brackets(content):
    return content[53:len(content) - 1]
