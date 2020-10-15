
def create_flask_blueprint(backends, oauth, handle_authorize):

    from flask import Blueprint, request, url_for, current_app, abort

    for b in backends:
        register_to(oauth, b)

    bp = Blueprint('lab_6', __name__)

    @bp.route('/auth/<name>', methods=('GET', 'POST'))
    def auth(name):
        remote = oauth.create_client(name)
        if remote is None:
            abort(404)

        id_token = request.values.get('id_token')
        if request.values.get('code'):
            token = remote.authorize_access_token()
            if id_token:
                token['id_token'] = id_token
        elif id_token:
            token = {'id_token': id_token}
        elif request.values.get('oauth_verifier'):
            # OAuth 1
            token = remote.authorize_access_token()
        else:
            # handle failed
            return handle_authorize(remote, None, None)
        if 'id_token' in token:
            user_info = remote.parse_id_token(token)
        else:
            remote.token = token
            user_info = remote.userinfo(token=token)
        return handle_authorize(remote, token, user_info)

    @bp.route('/login/<name>')
    def login(name):
        remote = oauth.create_client(name)
        if remote is None:
            abort(404)

        redirect_uri = url_for('.auth', name=name, _external=True)
        conf_key = '{}_AUTHORIZE_PARAMS'.format(name.upper())
        params = current_app.config.get(conf_key, {})
        return remote.authorize_redirect(redirect_uri, **params)

    return bp


def register_to(oauth, backend_cls):
    from authlib.integrations.flask_client import FlaskRemoteApp

    class RemoteApp(backend_cls, FlaskRemoteApp):
        OAUTH_APP_CONFIG = backend_cls.OAUTH_CONFIG

    oauth.register(RemoteApp.NAME, overwrite=True, client_cls=RemoteApp)
