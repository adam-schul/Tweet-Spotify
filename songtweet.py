import spotipy
import tweepy
from spotipy.oauth2 import SpotifyOAuth
import spotipy.util as util
import requests
import json
import time
import sys

loops_completed = 0
loops = 12

# Twitter personal details
consumer_key = "pZP7kFlAFKpegNSDIr5sLqUcr"
consumer_secret = "KLiAeezYG70EKe9uKKEdBXFISC5sfXk4215L3n7PtQGSg341pd"
access_token = "1114306019134398464-lgWL8QFlHnxOjJ5X2GrQ72rgBI3LOk"
access_token_secret = "sPhDeWSWwLmwtk7JM960YDFu7uV63IO72Qq379byc3mOD"

# Spotify personal details
username = 'ctbh8bkg6z5f5ovxe483osd75'
client_id = 'b6ad6fce25ea486d8c25aa0c77387232'
client_secret = '0fb16d2dc0814a138418b12085fe9efe'
scope = 'user-read-currently-playing'
redirect_uri = 'http://localhost:7777/callback'

try:
    for i in range(loops):
        # Authentication of consumer key and secret
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

        # Authenticate Twitter with token
        auth.set_access_token(access_token, access_token_secret)

        api = tweepy.API(auth, wait_on_rate_limit=True)

        # Authenticate Spotify with token
        token = util.prompt_for_user_token(username=username,
                                           scope=scope,
                                           client_id=client_id,
                                           client_secret=client_secret,
                                           redirect_uri=redirect_uri)

        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + token
        }

        params = (
            ('market', 'US'),
        )

        # Get the json file of the song I'm currently playing, then store that in the 'json' variable
        response = requests.get('https://api.spotify.com/v1/me/player/currently-playing', headers=headers,
                                params=params, timeout=5)

        json = response.json()

        # Find the name of the song and the name of the artist in the json file, then store these in variables
        track_name = json['item']['name']
        artist_name = json['item']['album']['artists'][0]['name']

        # Execute the tweet
        api.update_status(status='Adam is listening to "' + track_name + '" by ' + artist_name + '.')

        print('Adam is listening to "' + track_name + '" by ' + artist_name + '.')

        # Print progress
        loops_completed = loops_completed + 1
        print(str(loops_completed) + '/' + str(loops) + ' loops completed.')

        # Delay 5 minutes
        time.sleep(300)

except KeyboardInterrupt:
    sys.exit()
