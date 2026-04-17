import secrets

def generate_instructor_invite_code():
    alf = '0123456789'
    code = '0'
    for i in range(11):
        code += secrets.choice(alf)
    return code

def generate_admin_invite_code():
    alf = '0123456789'
    code = '1'
    for i in range(11):
        code += secrets.choice(alf)
    return code
