# Imports
from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
import random
import time

# Loads the environment variables ensuring they can stay in a separate file for security
load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# Class that defines a Song Object as an object with a song_name and an artist_name
class Song:
    def __init__(self, song_name, artist_name):
        self.song_name = song_name
        self.artist_name = artist_name
    
    def __str__(self):
        return f"{self.song_name} by {self.artist_name}"
    
    def __repr__(self):
        return f"Song(name='{self.song_name}', artist='{self.artist_name}')"
    
    def get_song_name(self):
        return self.song_name
    
    def get_artist_name(self):
        return self.artist_name
    
# Methods Utilizing the Spotify API
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


    
# SongQuiz class that defines a SongQuiz object, keeping track of the songs within the quiz; also, manages how the game runs
class SongQuiz:
    
    def __init__(self):
        self.songs = []
        self.number_of_songs = 0
        
    def add_song(self, track_name):
        searched_song = search_for_track(token, track_name)
        confirmation = input(f"Would you like to add {searched_song} to your quiz? (y/n) ")
        if confirmation.lower() == "y":
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
        random.shuffle(self.songs)
        correct = 0
        question_number = 0
        self.number_of_songs = len(self.songs)
        for song in self.songs:
            question_number += 1
            song_name = song.get_song_name()
            artist_name = song.get_artist_name()
            print(f"Question {question_number}/{self.number_of_songs}:")
            user_answer = input(f"Who is the artist of {song_name}? ")
            if user_answer.lower() == artist_name.lower():
                print("Correct!")
                correct += 1
            else:
                print(f"That's not correct. The answer was {artist_name}.")
        print(f"You finished the quiz! You got {correct}/{self.number_of_songs} right!")
        time.sleep(3.5)
        self.instantiate_quiz()
        
    def instantiate_quiz(self):
        print("\n" * 100)
        print("Welcome to the Song Quiz featuring the Spotify Web API!")
        while True:
            question_addsong = input("Would you like to add a song? (y/n) ")
            if question_addsong.lower() == "y":
                user_search = input("What song would you like to search for? ")
                self.add_song(user_search)
            elif question_addsong.lower() == "n":
                break
            else:
                print("Please enter 'y' or 'n'.")
        question_startquiz = input("Would you like to start the quiz? (y/n) ")
        print("\n" * 100)
        if question_startquiz.lower() == "y":
            self.start_quiz()
        elif question_startquiz.lower() == "n":
            print("Game is over.")
        else:
            print("Please enter 'y' or 'n'.")
        

# Runs the program
token = get_token()
quiz = SongQuiz()
quiz.instantiate_quiz()