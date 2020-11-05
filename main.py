from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth


date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
response = requests.get("https://www.billboard.com/charts/hot-100/" + date)
soup = BeautifulSoup(response.text, 'html.parser')
song_names_Span = soup.find_all("span", class_="chart-element__information__song")
song_names = [song.getText() for song in song_names_Span]

Authentication spotify
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id= #,
        client_secret= #,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]
print(user_id)

#Search for songs by title
song_uris = []
year = date.split("-")[0]
for song in song_names:
    resulting = sp.search(q=f"track:{song} year:{year}", type="track")
    print(resulting)
    try:
        uri = resulting["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify's library. It will be skipped.")

#new private playlist
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
print(playlist)

#Add songs
sp.user_playlist_add_tracks(user=user_id, playlist_id=playlist["id"], tracks=song_uris)


