from flask import Flask, jsonify
from authlib.integrations.flask_client import OAuth
from lab_6.loginpass import create_flask_blueprint
from lab_6.loginpass import GitHub,Discord

class Google(object):
    NAME = 'google'
    OAUTH_CONFIG = {
        'api_base_url': 'https://www.googleapis.com/',
        'server_metadata_url': 'https://accounts.google.com/.well-known/openid-configuration',
        'client_kwargs': {'scope': 'openid email profile'},
    }

app = Flask(__name__)
app.config.from_pyfile('config.example.py')
oauth = OAuth(app)
backends = [Discord, GitHub, Google]


@app.route('/')
def index():
    tpl = '<li><a href="/login/{}">{}</a></li>'
    lis = [tpl.format(b.NAME, b.NAME) for b in backends]
    return '<ul>{}</ul>'.format(''.join(lis))


def handle_authorize(remote, token, user_info):
    return jsonify(user_info)


bp = create_flask_blueprint(backends, oauth, handle_authorize)
app.register_blueprint(bp, url_prefix='')

app.run()