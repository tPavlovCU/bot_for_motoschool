    # users = {
    #     'Timofeeeey': {
    #         'role': 'user',
    #         'name': None
    #     },
    #     'Ivan': {
    #         'role': 'instructor',
    #         'name': 'Vanya'
    #     },
    #     'Vladimir': {
    #         'role': 'instructor',
    #         'name': 'Vova'
    #     }
    # }
    #
    #
    # def get_role(username):
    #     if username in users:
    #         return users[username]['role']
    #     else:
    #         return None
    #
    #
    # def get_all_role(role):
    #     result = []
    #     for user in users:
    #         if users[user]['role'] == role:
    #             if users[user]['name'] is not None:
    #                 result.append(f'{users[user]["name"]} (@{user})')
    #             else:
    #                 result.append(f'@{user}')
    #     return result
    #
    #
    # def add_in_bd(username, role='user', name=None):
    #     if username in users:
    #         users[username]['role'] = role
    #         return 'was in bd'
    #     else:
    #         users[username] = {}
    #         users[username]['role'] = role
    #         users[username]['name'] = name
    #         print(users)
    #         return 'added in_bd'
    #
    #
    # def delete_in_bd(username):
    #     if username in users:
    #         del users[username]
    #         return 'deleted in_bd'
    #     else:
    #         return 'username not found'
