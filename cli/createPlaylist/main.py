def createPlaylist():
    from spotifyApi.main import create_playlist_with_songs
    from utilities.inputs import getDate
    from webParser.main import get_songs_per_date

    # user input
    print("\n")
    selected_date = getDate()
    playlist_name = input("Playlist Name: ")
    playlist_descr = input("Description: ")
    print("\n")

    # get songs per date
    songs = get_songs_per_date(selected_date)

    # create playlist with that songs
    playlist = create_playlist_with_songs(playlist_name, playlist_descr, songs)

    print("Yor playlist url: ", playlist.get("external_urls").get("spotify"), " ✅")