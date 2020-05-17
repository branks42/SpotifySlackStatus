import requests
import json
import spotipy
import spotipy.util as util


def update_status(spotify, slack_url, client_id, client_secret):
    """
    Update the requesting user's Slack status.

    Parameters
    ----------
    spotify: class
        Spotipy class
    slack_url : str
        Url to post the new status

    Returns
    -------
    The time to sleep (Length of current track - progress in song + 5 seconds)
    """
    try:
        current_song = spotify.current_playback()
    except spotipy.exceptions.SpotifyException:
        # Spotify Authentication error, authorization resets after an hour
        token = util.prompt_for_user_token(
            'YOUR_SPOTIFY_USERNAME_HERE',
            'user-read-playback-state',
            client_id,
            client_secret,
            'http://localhost:9090')
        spotify = spotipy.Spotify(auth=token)
        current_song = spotify.current_playback()

    song_info = "{} - {}".format(current_song['item']['artists'][0]['name'],
                                 current_song['item']['name'])

    print("Changing Slack Status to {} \n".format(song_info))

    # Change the status
    sleep_time = (current_song['item']['duration_ms'] - current_song['progress_ms']) / 1000
    print("Gonna sleep for {} seconds...\n".format(sleep_time))
    
    slack_status = {"status_text": song_info, "status_emoji": ":spotify:"}
    response = requests.post(slack_url.format(json.dumps(slack_status)))

    return sleep_time + 5, spotify
