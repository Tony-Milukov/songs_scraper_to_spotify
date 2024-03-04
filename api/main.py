import os
from flask import Flask, request, session
from dotenv import load_dotenv
from spotipy import SpotifyOAuth

apiScope = os.getenv("SPOTIFY_API_SCOPE")

app = Flask(__name__)

load_dotenv()

clientId = os.getenv('SPOTIFY_CLIENT_ID')
clientSecret = os.getenv('SPOTIFY_CLIENT_SECRET')
redirectUrl = os.getenv('SPOTIFY_REDIRECT_URL')

app.secret_key = 'YOUR_SECRET_KEY'


@app.route('/callback')
def callback():
    code = request.args.get('code')
    sp_oauth = SpotifyOAuth(client_id=clientId, client_secret=clientSecret, redirect_uri=redirectUrl,
                            scope=apiScope)

    token_info = sp_oauth.get_access_token(code)

    session['token_info'] = token_info

    return "Successfully logged in, you can close your browser now  ✅"


if __name__ == '__main__':
    app.run(debug=True)
