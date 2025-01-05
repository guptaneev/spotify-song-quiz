from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")


class Song:
    
    def __init__(self, song_name, artist_name):
        self.song_name = song_name
        self.artist_name = artist_name
    
    def toString(self):
        return f"{self.song_name} by {self.artist_name}"
    
    
    
    
    
def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token
 
def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def search_for_artist(token, artist_name):
    url = f"https://api.spotify.com/v1/search?q={artist_name}&type=artist&limit=1"
    headers = get_auth_header(token)
    
    query_url = url
    result = get(query_url, headers = headers)
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result) == 0:
        print("No artist with this name exists!")
        return None
    return json_result[0]

def search_for_track(token, track_name):
    url = f"https://api.spotify.com/v1/search?q={track_name}&type=track&limit=1"
    headers = get_auth_header(token)
    
    query_url = url
    result = get(query_url, headers = headers)
    json_result = json.loads(result.content)
    if len(json_result) == 0:
        print("No song with this genre exists!")
        return None
    artist_name = json_result["tracks"]["items"][0]["album"]["artists"][0]["name"]
    song_name = json_result["tracks"]["items"][0]["name"]
    return Song(song_name, artist_name)

def get_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    result = get(url, headers = headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result


    
    
class SongQuiz:
    
    def __init__(self):
        self.number_of_songs = 0
        self.songs = []
        
    def add_song(self, track_name):
        searched_song = search_for_track(token, track_name)
        confirmation = input(f"Would you like to add {searched_song.toString()} to your quiz? (y/n) ")
        if confirmation == "y":
            if searched_song not in self.songs:
                self.songs.append(searched_song)
                print("Song added!")
                return True
            print("Song already added!")
            return False
        else:
            print("Song not added!")
            return False
        
    def start_quiz(self):
        
        

search_song_input = str(input("What song would you like to search for? "))
token = get_token()
result = search_for_track(token, search_song_input)
print(f"You searched for: {result[0]} by {result[1]}")