def password_verification(data, passwd):
    errors = {}
    if data[0][2] != str(passwd):
        errors['passwd'] = 'Incorrect login or password'
        return errors

