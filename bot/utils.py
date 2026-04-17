import secrets

def generate_invite_code():
    alf = '0123456789'
    code = ''
    for i in range(12):
        code += secrets.choice(alf)
    return code

print(generate_invite_code())