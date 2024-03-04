import os
import webbrowser
from halo import Halo
from dotenv import load_dotenv
import spotipy

load_dotenv()

# get envs
main_spotify_url = os.getenv('SPOTIFY_API_URL')
clientId = os.getenv('SPOTIFY_CLIENT_ID')
clientSecret = os.getenv('SPOTIFY_CLIENT_SECRET')
apiScope = os.getenv("SPOTIFY_API_SCOPE")
spotifyAuthRedirect = os.getenv('SPOTIFY_REDIRECT_URL')


def search_song(song, sp):
    # search in spotify
    search = sp.search(q=song.get("name"), type="track", limit=25)
    # found items array
    items = search.get('tracks').get("items")
    for item in items:
        # current song artist
        artist_name = item.get('artists')[0].get('name').lower()
        # current song name
        song_name = item.get('name').lower()

        # actual song artist
        input_artist = song.get('author').lower()
        # actual song name
        input_song_name = song.get('name').lower()

        # check if (artist name) and (song-name match)
        if (artist_name in input_artist
                or input_artist in artist_name and
                song_name in input_song_name
                or input_song_name in song_name
        ):
            return item.get('uri')


def create_play_list(playlist_name, playlist_description, sp, user_id) -> str:
    playListInfo = sp.user_playlist_create(user_id, playlist_name, True, "", playlist_description)
    return playListInfo


def create_playlist_with_songs(playlist_name, playlist_description, songs):
    token = get_user_token()
    # create spotipy obj from auth token
    sp = spotipy.Spotify(auth=token)
    # get userId from logged in user
    user_id = sp.current_user().get('id')
    songIds = []

    # create new playlist
    playlist = create_play_list(playlist_name, playlist_description, sp, user_id)

    spinner = Halo(text='Searching for songs in spotify', spinner='dots')
    spinner.start()

    # find every song in spotify
    for song in songs:
        # find it
        found = search_song(song, sp)
        if found:
            songIds.append(found)

    spinner.stop()

    spinner = Halo(text='Adding songs to playlist', spinner='dots')
    spinner.start()
    sp.playlist_add_items(playlist.get('id'), songIds)
    spinner.stop()
    return playlist


def get_user_token(scope=apiScope):
    # redirect user to login page ->
    sp_oauth = spotipy.SpotifyOAuth(client_id=clientId, client_secret=clientSecret,
                                    redirect_uri=spotifyAuthRedirect,
                                    scope=scope)
    # open the login link in browser
    webbrowser.open(sp_oauth.get_authorize_url())
    # when user logged in, return access token
    return sp_oauth.get_access_token().get('access_token')

