import hashlib


def make_password(passwd_str):
    return hashlib.md5(("9@^"+passwd_str+'$&').encode()).hexdigest()


def check_password(passwd_str, encrypted_str):
    return make_password(passwd_str) == encrypted_str

