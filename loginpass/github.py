def normalize_userinfo(client, data):
    params = {
        'sub': str(data['id']),
        'name': data['name'],
        'email': data.get('email'),
        'preferred_username': data['login'],
        'profile': data['html_url'],
        'picture': data['avatar_url'],
        'website': data.get('blog'),
    }
    if params.get('email') is None:
        resp = client.get('user/emails')
        resp.raise_for_status()
        data = resp.json()
        params["email"] = next(email['email'] for email in data if email['primary'])
    return params


class GitHub(object):
    NAME = 'github'
    OAUTH_CONFIG = {
        'api_base_url': 'https://api.github.com/',
        'access_token_url': 'https://github.com/login/oauth/access_token',
        'authorize_url': 'https://github.com/login/oauth/authorize',
        'client_kwargs': {'scope': 'user:email'},
        'userinfo_endpoint': 'https://api.github.com/user',
        'userinfo_compliance_fix': normalize_userinfo,
    }
