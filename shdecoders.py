import binascii

from solve import *


# Legacy

def unhex(post_content):
    try:
        post_nospace = remove_spaces(post_content)
        post_unhex = hex2num(post_nospace)
        post_utf8 = decode_utf8(post_unhex)
    except:
        post_utf8 = ""
    return post_utf8


def unb64(post_base64):
    post_unb64 = decode_b64(post_base64)
    return post_unb64


def unb64codec(post_b64, codec):
    try:
        post_unb64_text = post_b64.decode(codec)
    except:
        post_unb64_text = ""
        pass
    return post_unb64_text


def b64(post_content):
    try:
        post_nospace = remove_spaces(post_content)
        post_unhex = hex2num(post_nospace)
        base64_bin = encode_b64(post_unhex)
        base64_utf8 = decode_utf8(base64_bin)
    except:
        base64_utf8 = ''
    return base64_utf8


def des3decrypt(post_content, key_hex):
    try:
        post_nospace = remove_spaces(post_content)
        post_unhex_noascii = hex2num(post_nospace)
        ct = post_unhex_noascii
        key = hex2num(key_hex)
        pt = decode_des3_ecb(ct, key)
    except:
        pt = ""
        pass
    return pt


def des3decryptcbc(post_content, key, iv):
    try:
        post_nospace = post_content.replace(" ", "")
        post_unhex_noascii = binascii.unhexlify(post_nospace)
        ct = post_unhex_noascii
        key_unhex = binascii.unhexlify(key)
        iv_unhex = binascii.unhexlify(iv)
        obj = DES3.new(key_unhex, DES3.MODE_CBC, iv_unhex)
        pt = obj.decrypt(ct)
    except:
        pt = ""
        pass
    return pt
