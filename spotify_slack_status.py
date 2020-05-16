import spotipy
import spotipy.util as util
import time

from update_status import update_status

# Spotify App credentials
CLIENT_ID = ''
CLIENT_SECRET = ''
# Slack Credentials
slack_token = ''
# The second blank is filled in during the function call
slack_url = 'https://slack.com/api/users.profile.set?token={}&profile={}'.format(slack_token)

# This gets the user's authorization token
# Parameters are username, scope, client id, client secret and redirect url
# The CLIENT_ID, CLIENT_SECRET and REDIRECT_URL need to be setup in Spotify Developer Dashboard.
token = util.prompt_for_user_token(
    'YOU_SPOTIFY_USERNAME_HERE',
    'user-read-playback-state',
    CLIENT_ID,
    CLIENT_SECRET,
    'http://localhost:9090')


spotify = spotipy.Spotify(auth=token)

while True:
    sleep_time, spotify = update_status(spotify, slack_url)
    time.sleep(sleep_time)

