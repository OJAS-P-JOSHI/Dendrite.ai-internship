from flask import Flask, render_template, redirect, url_for, request
from flask_graphql import GraphQLView
from keycloak import KeycloakOpenID
from schema import schema
import stripe

app = Flask(__name__)

keycloak_openid = KeycloakOpenID(
    server_url="http://localhost:8080/auth/",
    client_id="your-client-id",
    realm_name="your-realm",
    client_secret_key="your-client-secret"
)

stripe.api_key = 'your-stripe-secret-key'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return redirect(keycloak_openid.auth_url(redirect_uri="http://localhost:5000/callback"))

@app.route('/callback')
def callback():
    code = request.args.get('code')
    token = keycloak_openid.token(grant_type='authorization_code', code=code, redirect_uri="http://localhost:5000/callback")
    userinfo = keycloak_openid.userinfo(token['access_token'])

    return redirect(url_for('index'))

@app.route('/pro')
def pro():
    return render_template('pro.html')

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True
    )
)

if __name__ == '__main__':
    app.run(debug=True)
