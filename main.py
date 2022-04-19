from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

clientID =
secret = 

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="playlist-modify-private",redirect_uri="http://example.com",client_id=clientID,client_secret=secret,show_dialog=True,cache_path="token.txt"))
user_id = sp.current_user()["id"]

year_input=input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD:")
url="https://www.billboard.com/charts/hot-100/"+year_input+"/"
response=requests.get(url)

scraped=response.text

soup=BeautifulSoup(scraped,"html.parser")
print (soup)
songs=soup.find_all(name="h3" , class_="c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 "
                                       "lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 "
                                       "u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 "
                                       "u-max-width-230@tablet-only")
allsongs=[]
for texter in songs:
    allsongs.append(texter.getText().strip())

print (allsongs)

song_uris = []
year = year_input.split("-")[0]
for song in allsongs:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")



playlist = sp.user_playlist_create(user=user_id, name=f"{year_input} Billboard 100", public=False)
# print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)