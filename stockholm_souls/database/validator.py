def password_verification(data, passwd):
    errors = {}
    if data[0][2] != str(passwd):
        errors['login'] = 'Incorrect login or password'
        return errors


def password_checker(passwd, c_passwd):
    errors = {}
    if passwd != c_passwd:
        errors['passwd'] = "Password mismatch"
    elif len(passwd) < 8:
        errors['passwd'] = "Password is short"
    return errors