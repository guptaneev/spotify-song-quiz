# Imports
from dotenv import load_dotenv
import os
import base64
import json
import random
import time
from requests import post, get

# Load environment variables (e.g., Spotify API credentials)
load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")


class Song:
    """
    Song class to define a song object with name and artist details
    """
    def __init__(self, song_name, artist_name):
        self.song_name = song_name
        self.artist_name = artist_name

    def __str__(self):
        return f"'{self.song_name}' by {self.artist_name}"

    def __repr__(self):
        return f"Song(song_name='{self.song_name}', artist_name='{self.artist_name}')"


# Spotify API Utility Functions
def get_token():
    """
    Retrieves an access token from Spotify's API using client credentials.
    """
    auth_string = f"{CLIENT_ID}:{CLIENT_SECRET}"
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {"grant_type": "client_credentials"}

    response = post(url, headers=headers, data=data)
    response_data = response.json()
    return response_data["access_token"]


def get_auth_header(token):
    """
    Creates the Authorization header for Spotify API requests.
    """
    return {"Authorization": f"Bearer {token}"}


def search_for_artist(token, artist_name):
    """
    Searches for an artist on Spotify by name.
    """
    url = f"https://api.spotify.com/v1/search?q={artist_name}&type=artist&limit=1"
    headers = get_auth_header(token)

    response = get(url, headers=headers)
    artists = response.json().get("artists", {}).get("items", [])

    if not artists:
        print("No artist with this name found.")
        return None
    return artists[0]


def search_for_track(token, track_name):
    """
    Searches for a track on Spotify by name.
    Returns a Song object with the track's name and artist.
    """
    url = f"https://api.spotify.com/v1/search?q={track_name}&type=track&limit=1"
    headers = get_auth_header(token)

    response = get(url, headers=headers)
    tracks = response.json().get("tracks", {}).get("items", [])

    if not tracks:
        print("No song with this name found.")
        return None

    track_data = tracks[0]
    song_name = track_data["name"]
    artist_name = track_data["artists"][0]["name"]
    return Song(song_name, artist_name)


def get_songs_by_artist(token, artist_id):
    """
    Retrieves top tracks for an artist using their Spotify artist ID.
    """
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)

    response = get(url, headers=headers)
    return response.json().get("tracks", [])



class SongQuiz:
    """
    SongQuiz class to manage the quiz and its functionality
    """
    def __init__(self):
        self.songs = []

    def add_song(self, token, track_name):
        """
        Adds a song to the quiz by searching for it on Spotify.
        """
        searched_song = search_for_track(token, track_name)
        if not searched_song:
            return False

        confirmation = input(f"Would you like to add {searched_song} to your quiz? (y/n): ").strip().lower()
        if confirmation == "y":
            if searched_song not in self.songs:
                self.songs.append(searched_song)
                print("Song added!")
                return True
            print("This song is already in the quiz.")
            return False
        print("Song not added.")
        return False

    def start_quiz(self):
        """
        Starts the quiz, asking users to guess the artist for each song.
        """
        if not self.songs:
            print("No songs in the quiz. Please add songs first!")
            time.sleep(3)
            self.instantiate_quiz()

        random.shuffle(self.songs)
        correct_answers = 0
        print("\n" * 100)
        for idx, song in enumerate(self.songs, start=1):
            print(f"Question {idx}/{len(self.songs)}: Who is the artist of '{song.song_name}'?")
            user_answer = input("Your answer: ").strip().lower()

            if user_answer == song.artist_name.lower():
                print("Correct!")
                correct_answers += 1
            else:
                print(f"Wrong! The correct answer is '{song.artist_name}'.")

        print(f"You completed the quiz! You got {correct_answers}/{len(self.songs)} correct!")
        time.sleep(3)
        self.instantiate_quiz()

    def instantiate_quiz(self):
        """
        Initializes the quiz, allowing users to add songs and start the game.
        """
        print("\n" * 100)
        print("Welcome to the Song Quiz powered by Spotify!")

        while True:
            add_song_input = input("Would you like to add a song? (y/n): ").strip().lower()
            if add_song_input == "y":
                track_name = input("Enter the song name to search for: ").strip()
                self.add_song(token, track_name)
            elif add_song_input == "n":
                break
            else:
                print("Please enter 'y' or 'n'.")

        start_quiz_input = input("Would you like to start the quiz? (y/n): ").strip().lower()
        if start_quiz_input == "y":
            self.start_quiz()
        elif start_quiz_input == "n":
            print("Thank you for playing!")
            time.sleep(3)
            self.instantiate_quiz()
        else:
            print("Invalid input. Exiting.")
            time.sleep(3)
            self.instantiate_quiz()


# Main program execution
if __name__ == "__main__":
    token = get_token()
    quiz = SongQuiz()
    quiz.instantiate_quiz()