def map_profile_fields(data, fields):
    profile = {}
    for dst, src in fields.items():
        if callable(src):
            value = src(data)
        else:
            value = data.get(src)

        if value is not None and value != '':
            profile[dst] = value

    return profile

def normalize_userinfo(client, data):
    params = map_profile_fields(data, {
        'sub': 'id',
        'name': 'username',
        'email': 'email',
        'preferred_username': 'username',
        'email_verified': 'verified',
    })
    if 'avatar' in data:
        src = 'https://cdn.discordapp.com/avatars/{}/{}.png'
        params['picture'] = src.format(data['id'], data['avatar'])
    return params


class Discord(object):
    NAME = 'discord'
    OAUTH_CONFIG = {
        'api_base_url': 'https://discordapp.com/api/',
        'access_token_url': 'https://discordapp.com/api/oauth2/token',
        'authorize_url': 'https://discordapp.com/api/oauth2/authorize',
        'userinfo_endpoint': 'https://discordapp.com/api/users/%40me',
        'userinfo_compliance_fix': normalize_userinfo,
        'client_kwargs': {
            'token_endpoint_auth_method': 'client_secret_post',
            'scope': 'identify email'
        },
    }
