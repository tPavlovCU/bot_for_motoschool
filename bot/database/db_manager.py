users = {
    'Timofeeeey': {
        'role': 'user',
        'name': None
    }
}


def get_role(username):
    if username in users:
        return users[username]['role']
    else:
        return None


def get_bd():
    return users


def add_in_bd(username, role='user', name=None):
    if username in users:
        users[username]['role'] = role
        return 'was in bd'
    else:
        users[username] = {}
        users[username]['role'] = role
        users[username]['name'] = name
        return 'added in_bd'
