import pandas as pd
import pynput.keyboard
import spotipy
from requests import HTTPError, ReadTimeout
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
from pynput import keyboard
import os
import datetime
import time
import requests
from ml_part1 import Predictor


# ---------------------------------------------Spotify Work ----------------------------------------------------#
class Spotify_work:
    def __init__(self):
        self.client_id = os.environ["client-id"]
        self.client_secret = os.environ["client-secret"]
        self.scope = "user-follow-modify playlist-read-private user-follow-read user-library-read user-library-modify " \
                     "playlist-modify-private user-read-currently-playing"
        self.redirect_uri = 'http://localhost:8080'

        self.credentials = SpotifyClientCredentials(client_id=self.client_id, client_secret=self.client_secret)

        self.authorization = SpotifyOAuth(client_id=self.credentials.client_id,
                                          client_secret=self.credentials.client_secret,
                                          scope=self.scope, redirect_uri=self.redirect_uri, cache_path=".cache")

        self.Client = spotipy.client.Spotify(auth=self.authorization.get_cached_token()["access_token"],
                                             requests_timeout=15, retries=15)

        self.genres = ["pop", "rock", "indie", "electronic", "hip-hop", "classical", "jazz", "punk", "lofi", "grunge",
                       "R&B", "post punk", "britpop", "alt dance", "rap", "trap", "EDM", "psytrance", "dance", "house",
                       "metal", "soft rock", "alt rock", "classic rock", "country", "alternative", "blues",
                       "deep-house",
                       "techno", "dubstep", "funk", "garage", "heavy-metal", "industrial", "new-age", "minimal techno",
                       "post-dubstep", "progressive house", "psychedelic rock"]

        # code = self.authorization.get_authorization_code()
        # self.authorization.get_access_token(code=code)

        self.playlist_urls = [["https://open.spotify.com/playlist/6mtYuOxzl58vSGnEDtZ9uB?si=297cbd179df248c0", "pop"],
                              ["https://open.spotify.com/playlist/6mtYuOxzl58vSGnEDtZ9uB?si=1fa9f3f7044948f0", "pop"],
                              ["https://open.spotify.com/playlist/3Da3yokTjSupbEd7QSE3Kg?si=69261219c8264428", "rock"],
                              ["https://open.spotify.com/playlist/37i9dQZF1DWXRqgorJj26U?si=086e8ac764e44250", "rock"],
                              ["https://open.spotify.com/playlist/0sGYJV5EvhteqK6l9xZY55?si=0e6d52452e0e4789", "indie"],
                              ["https://open.spotify.com/playlist/3FixUcICt6cDhoqX5HCL9Y?si=7b7c6c4dc3ee4066", "indie"],
                              ["https://open.spotify.com/playlist/5OuwluOQwdzeTMc3ZqTHcI?si=3b9bd684966942d2",
                               "electronic"],
                              ["https://open.spotify.com/playlist/37WLg2xRZcHw5DJSlnYLr9?si=dd03f021bb4a474d",
                               "electronic"],
                              ["https://open.spotify.com/playlist/0weizyV5WNZP3tvfXWVfmg?si=302388b42ba94d91",
                               "hip-hop"],
                              ["https://open.spotify.com/playlist/3RcRK9HGTAm9eLW1LepWKZ?si=3ca06718948c4522",
                               "hip-hop"],
                              ["https://open.spotify.com/playlist/1h0CEZCm6IbFTbxThn6Xcs?si=a4c10fe5a3714770",
                               "classic"],
                              ["https://open.spotify.com/playlist/7v9uKvGwd9pwloVMziYPAg?si=66ebc4efaf4b4074",
                               "classic"],
                              ["https://open.spotify.com/playlist/4xKFUXoma8EepzgxKguJUi?si=3167c46d7a594d28", "jazz"],
                              ["https://open.spotify.com/playlist/37i9dQZF1DXbITWG1ZJKYt?si=a50c46ae436140e8", "jazz"],
                              ["https://open.spotify.com/playlist/0KwmgNbTWLzyiXfMcktfao?si=bf02fa1220944cf6", "punk"],
                              ["https://open.spotify.com/playlist/5Tlr1XQHpIjyVRpsVHpDig?si=f8dfe915671940c3", "punk"],
                              ["https://open.spotify.com/playlist/1lbjVb7UpHAwv2fxNfM2Wz?si=a75f87ba735449da", "lofi"],
                              ["https://open.spotify.com/playlist/4VN7J0uq62foOhZndwOegy?si=12120a31f0684b2a", "lofi"],
                              ["https://open.spotify.com/playlist/3yPIwFAm6vLZn8JbyyjXaP?si=ce4a6111c123408b",
                               "grunge"],
                              ["https://open.spotify.com/playlist/1DRQljCHFVHNnRtTnJxOBk?si=1d717283fa8d46eb",
                               "grunge"],
                              ["https://open.spotify.com/playlist/6bJqBjXDDXJnOp2qhsn7Zg?si=d70aa43d50c0493a", "R&B"],
                              ["https://open.spotify.com/playlist/37i9dQZF1DX04mASjTsvf0?si=d2b65ca7eb4d4733", "R&B"],
                              ["https://open.spotify.com/playlist/64vg1OW5TiOYb6uzb5Y9XL?si=7b2b8fab86f44ad9",
                               "post punk"],
                              ["https://open.spotify.com/playlist/2gNTpZxVxW4KLyceVYFgms?si=d773faa7a4aa4f82",
                               "post punk"],
                              ["https://open.spotify.com/playlist/1fDwuEZMWYaOBXmfW6PkdL?si=9f2a3cd15e3748e9",
                               "alt dance"],
                              ["https://open.spotify.com/playlist/7IXixBCW4WCjtMM2smuZDA?si=4676eee690bf4778",
                               "alt dance"],
                              ["https://open.spotify.com/playlist/1rlBSxR4WryLssBr4kiZ77?si=2948243866d7497d",
                               "britpop"],
                              ["https://open.spotify.com/playlist/3KDPy7xcUQklhjuOycL6i6?si=7290f18b1f084288",
                               "britpop"],
                              ["https://open.spotify.com/playlist/7t89lEGvzSeexFTuJAgc3f?si=0adb6e0364234b67", "rap"],
                              ["https://open.spotify.com/playlist/12b6xARXdJqkqGPVDMgGHI?si=3dac7c2c6d6c4568", "rap"],
                              ["https://open.spotify.com/playlist/4iwWGCoTnhe5LiIrFXzyFQ?si=62952442d9f14dfb", "trap"],
                              ["https://open.spotify.com/playlist/1nmZw1vdNDCDh5burxzGdO?si=d30ca629d6954efe", "trap"],
                              ["https://open.spotify.com/playlist/0ftBbYPc1Oyz7WGokBtBr3?si=06eedfa484c34630", "EDM"],
                              ["https://open.spotify.com/playlist/2e3dcRuo9uDH6qD3NOGKAL?si=314f7c3e557743f3", "EDM"],
                              ["https://open.spotify.com/playlist/3PxIBhkmDMzEyhUTCTo30L?si=7ff08e3b67814f82",
                               "psytrance"],
                              ["https://open.spotify.com/playlist/75PxWthUYPOskOU1EjGrFX?si=eaadc65ddc3e4c28",
                               "psytrance"],
                              ["https://open.spotify.com/playlist/2Qfd2JyaZj9X0m3xKrJI6Z?si=4b7966705a0242f0", "dance"],
                              ["https://open.spotify.com/playlist/37i9dQZF1EQp9BVPsNVof1?si=3b1febfd22ea40db", "dance"],
                              ["https://open.spotify.com/playlist/37i9dQZF1DXaXB8fQg7xif?si=901a4e4762fc41cc", "dance"],
                              ["https://open.spotify.com/playlist/0FftsKlbP6bIikIEPsOrUs?si=41dbe2249b494c63", "house"],
                              ["https://open.spotify.com/playlist/4zYkenA32al0vgwQnf014d?si=76f18d10603b41e2", "house"],
                              ["https://open.spotify.com/playlist/27gN69ebwiJRtXEboL12Ih?si=99dffff4f8854ef0", "metal"],
                              ["https://open.spotify.com/playlist/37i9dQZF1DX08jcQJXDnEQ?si=4b8ec44305a94bb5", "metal"],
                              ["https://open.spotify.com/playlist/4orkpXnOcQb9hVw7OEsVV4?si=905c84a24aae4d9f",
                               "soft rock"],
                              ["https://open.spotify.com/playlist/4V6mc8koErhrWy9qcK70l2?si=6e01f4779cc74d72",
                               "soft rock"],
                              ["https://open.spotify.com/playlist/2zn5Uz49wyfb5RvIPxgify?si=a521a93f21474174",
                               "alt rock"],
                              ["https://open.spotify.com/playlist/26rnYeROYMTFXX6ttPB7ts?si=271173dc15714e1c",
                               "alt rock"],
                              ["https://open.spotify.com/playlist/70WhjhytLx0Ph8Wl2TMOVY?si=58460e70cc664156",
                               "classic rock"],
                              ["https://open.spotify.com/playlist/6Qc8Qk87qjc5vXuSOwjNH7?si=f9f98a19b5484e7a",
                               "classic rock"],
                              ["https://open.spotify.com/playlist/4M2JXLFKSvweWiN7UXPotW?si=12d73505e9dd44af",
                               "country"],
                              ["https://open.spotify.com/playlist/37i9dQZF1DWZBCPUIUs2iR?si=670c84576acb4cb8",
                               "country"]]

    def refresh(self):
        token_info = self.authorization.refresh_access_token(self.authorization.get_cached_token()['refresh_token'])
        token = token_info["access_token"]
        self.Client = spotipy.client.Spotify(auth=token, requests_timeout=15, retries=15)

    def get_saved_ids(self):
        try:
            saved_ids = []
            results = self.Client.current_user_saved_tracks()
            tracks = results["items"]
            while results["next"]:
                results = self.Client.next(results)
                tracks.extend(results["items"])
            for item in tracks:
                saved_ids.append(item["track"]["id"])
            return saved_ids
        except spotipy.exceptions.SpotifyException or HTTPError or TypeError:
            self.refresh()
            self.get_saved_ids()
        finally:
            print("Done")

    def get_playlist_tracks(self, playlist_id):
        try:
            results = self.Client.playlist_items(playlist_id)
            tracks = results['items']
            while results['next']:
                results = self.Client.next(results)
                tracks.extend(results['items'])
            return tracks
        except spotipy.exceptions.SpotifyException:
            self.refresh()
            self.get_playlist_tracks(playlist_id)
        except HTTPError:
            self.refresh()
            self.get_playlist_tracks(playlist_id)
        except TypeError:
            self.refresh()
            self.get_playlist_tracks(playlist_id)

    def save_songs_from_weeklymix(self):
        u_playlists = self.get_user_playlists()
        to_add = ""
        from_add = ""
        for playlist in u_playlists:
            if playlist["name"] == '"Discover Weekly " Mix':
                to_add = playlist["id"]
            elif playlist["name"] == 'Discover Weekly':
                from_add = playlist["id"]
        saved_ids = self.get_saved_ids()
        saved_p = []
        try:
            for track in self.get_playlist_tracks(to_add):
                saved_p.append(track["track"]["id"])

            for track in self.get_playlist_tracks(from_add):
                id = track["track"]["id"]
                if id in saved_ids and id not in saved_p:
                    self.Client.playlist_add_items(playlist_id=to_add, items=[id])
                    print("Saved in Weeklymix")
                else:
                    print("Not saved in Weeklymix")
        except spotipy.exceptions.SpotifyException or HTTPError or TypeError:
            self.refresh()
            self.save_songs_from_weeklymix()

    def like_current_song1(self):
        try:
            current_ids = []
            results = self.Client.current_user_saved_tracks()
            tracks = results["items"]
            for item in tracks:
                current_ids.append(item["track"]["id"])

            current = self.Client.currently_playing()
            id = ""
            if current is not None:
                id = current["item"]["id"]
            else:
                print("Nothing playing currently")

            if id not in current_ids:
                self.Client.current_user_saved_tracks_add(tracks=[id])
                print(f"Saved '{current['item']['name']}'")
            else:
                print(f"Already saved '{current['item']['name']}'")

        except spotipy.exceptions.SpotifyException or HTTPError or TypeError:
            self.refresh()
            self.like_current_song1()

    def follow_artists_playlist(self):
        try:
            songs = self.get_playlist_tracks(
                "https://open.spotify.com/playlist/0GWuhvuM9Pw7eARn8I7F3m?si=5b69455ae6fe446d")
            for song in songs:
                for artist in song["track"]["album"]["artists"]:
                    self.Client.user_follow_artists(ids=[artist["id"]])
        except spotipy.exceptions.SpotifyException or HTTPError or TypeError:
            self.refresh()
            self.follow_artists_playlist()

    def get_user_playlists(self):
        try:
            results = self.Client.current_user_playlists()
            playlists = results["items"]
            while results["next"]:
                results = self.Client.next(results)
                playlists.extend(results["items"])
            return playlists
        except spotipy.exceptions.SpotifyException or HTTPError or TypeError:
            self.refresh()
            self.get_user_playlists()

    def like_current_song(self):
        global saved_ids
        try:
            id = ""
            if self.Client.currently_playing() is not None:
                id = self.Client.currently_playing()["item"]["id"]
            else:
                print("Nothing playing currently")

            if id and id not in saved_ids:
                self.Client.current_user_saved_tracks_add(tracks=[id])
                print("Saved")
                track = self.Client.track(track_id=id)["id"]
                saved_ids.append(track)
            else:
                print("Already liked")
        except spotipy.exceptions.SpotifyException or HTTPError or TypeError:
            self.refresh()
            self.like_current_song()

    def get_info_1song(self, song_id):
        try:
            id = self.Client.track(song_id)["id"]
            audio_ft = self.Client.audio_features(id)
            danceability = audio_ft[0]["danceability"]
            energy = audio_ft[0]["energy"]
            loudness = audio_ft[0]["loudness"]
            speechiness = audio_ft[0]["speechiness"]
            acousticness = audio_ft[0]["acousticness"]
            instrumentalness = audio_ft[0]["instrumentalness"]
            liveness = audio_ft[0]["liveness"]
            valence = audio_ft[0]["valence"]
            tempo = audio_ft[0]["tempo"]
            key = audio_ft[0]["key"]
            mode = audio_ft[0]["mode"]
            time_signature = audio_ft[0]["time_signature"]

            return [danceability, energy, loudness, speechiness, acousticness, instrumentalness,
                    liveness, valence, tempo, key, mode, time_signature]

        except spotipy.exceptions.SpotifyException:
            self.refresh()
            self.get_info_1song(song_id)
        except HTTPError:
            self.refresh()
            self.get_info_1song(song_id)
        except TypeError:
            self.refresh()
            self.get_info_1song(song_id)

    def save_info(self, songs: list, ret: dict, genre: str):
        for id in songs:
            danceability = id["danceability"]
            energy = id["energy"]
            loudness = id["loudness"]
            speechiness = id["speechiness"]
            acousticness = id["acousticness"]
            instrumentalness = id["instrumentalness"]
            liveness = id["liveness"]
            valence = id["valence"]
            tempo = id["tempo"]
            key = id["key"]
            mode = id["mode"]
            time_signature = id["time_signature"]
            ret[f"{id['id']}"] = {"danceability": danceability, "energy": energy, "loudness": loudness,
                                  "speechiness": speechiness, "acousticness": acousticness,
                                  "instrumentalness": instrumentalness,
                                  "liveness": liveness, "valence": valence, "tempo": tempo, "key": key, "mode": mode,
                                  "time signature": time_signature, "genre": genre}

    def get_info(self, songs_id: list, ret, genre: str):
        try:
            print(f"Trying info : {genre}")
            if songs_id is not None:
                if len(songs_id) > 100:
                    for n in range(100, len(songs_id) - 1, 100):
                        if n + 100 > len(songs_id) - 1:
                            audio_ft = self.Client.audio_features(songs_id[n:len(songs_id) - 1])
                        else:
                            audio_ft = self.Client.audio_features(songs_id[n - 100:n])

                        self.save_info(audio_ft, ret, genre)
                else:
                    audio_ft = self.Client.audio_features(songs_id)
                    self.save_info(audio_ft, ret, genre)

                print(f"Got info : {genre}")

        except spotipy.exceptions.SpotifyException:
            print("spotiException")
            self.refresh()
            self.get_info(songs_id, ret, genre)
        except HTTPError:
            print("httpError")
            self.get_info(songs_id, ret, genre)
        except TypeError:
            print("TypeError")

    def get_playlist_ids(self, playlist_url):
        saved_ids = []
        try:
            results = self.Client.playlist_items(playlist_id=playlist_url)
            tracks = results["items"]
        except spotipy.exceptions.SpotifyException:
            print("Spoty exception")
            self.refresh()
            self.get_playlist_ids(playlist_url)
        except HTTPError:
            print("Http error")
            self.get_playlist_ids(playlist_url)
        except TypeError:
            print("type error")
        except ReadTimeout:
            print("timeout")
            self.get_playlist_ids(playlist_url)
        else:
            try:
                while results["next"]:
                    results = self.Client.next(results)
                    tracks.extend(results["items"])
                for item in tracks:
                    if item["track"]["id"] is not None:
                        saved_ids.append(item["track"]["id"])
            except spotipy.exceptions.SpotifyException:
                print("Spoty exception")
                self.refresh()
                self.get_playlist_ids(playlist_url)
            except HTTPError:
                print("Http error")
                self.get_playlist_ids(playlist_url)
            except TypeError:
                print("type error")
            except ReadTimeout:
                print("Spotipy timed out... retrying")
                self.get_playlist_ids(playlist_url)
            else:
                print("returned")
                return saved_ids

    def gen_csv(self, list_to_use: list = None):
        songs_info = {}
        if list_to_use is None:
            for play_list in self.playlist_urls:
                try:
                    playlist = self.get_playlist_ids(play_list[0])
                except ReadTimeout:
                    print("Spotipy timed out... retrying")
                    playlist = self.get_playlist_ids(play_list[0])

                genre = play_list[1]
                if playlist is not None:
                    self.get_info(playlist, songs_info, genre)

        else:
            for play_list in list_to_use:
                try:
                    print(f"Trying: {play_list[0]}")
                    playlist = play_list[0]
                    genre = play_list[1]
                    print(f"Done: {play_list[0]}")
                except ReadTimeout:
                    print("Spotipy timed out... retrying")
                    print(f"Trying: {play_list[0]}")
                    playlist = play_list[0]
                    genre = play_list[1]
                    print(f"Done: {play_list[0]}")
                finally:
                    if playlist is not None:
                        self.get_info(playlist, songs_info, genre)
                    time.sleep(10)

        df_songs = pd.DataFrame.from_dict(data=songs_info, orient="index")
        name = input("Name for the csv: ")
        df_songs.to_csv(f"{name}.csv")
        print("Finnaly Done")
        songs_df = pd.read_csv(f"{name}.csv")
        print(songs_df.sample())
        print(f"Len : {len(songs_df)}")

    def get_genres(self, artist):
        try:
            genres = []
            for genre in self.Client.artist(artist)["genres"]:
                genres.append(genre)
            return genres
        except spotipy.exceptions.SpotifyException or HTTPError or TypeError or requests.exceptions.ReadTimeout:
            self.refresh()
            self.get_genres(artist)

    def get_genre_playlist(self, genre: str):
        playlist_ids = []
        try:
            result = self.Client.search(q=genre, type="playlist", limit=50)
        except HTTPError:
            print("No playlist for this genre was found HTTp error")
            self.refresh()
        except spotipy.exceptions.SpotifyException:
            print("No playlist for this genre was found SpotiException")
            self.refresh()
            self.get_genre_playlist(genre)
        except ConnectionError:
            print("Ups.. Connection error")
            self.refresh()

        else:
            playlist_items = result["playlists"]["items"]
            try:
                while result["playlists"]["next"] is not None:
                    result = self.Client.next(result["playlists"])
            except HTTPError:
                print("Not found")
            except spotipy.exceptions.SpotifyException:
                print("Not found")
                self.refresh()
            finally:
                playlist_items.extend(result["playlists"]["items"])

                for item in playlist_items:
                    print(f'added {item["name"]}')
                    if item is not None:
                        playlist_ids.append(item["id"])
                    if len(playlist_ids) >= 13:
                        return playlist_ids

    def csv_from_spotigenres(self):
        playlists = []
        for genre in self.genres:
            playlist_ids = self.get_genre_playlist(genre)
            if playlist_ids is not None:
                for playlist in playlist_ids:
                    if playlist is not None:
                        time.sleep(15)
                        playlists.append([self.get_playlist_ids(playlist), genre])
            print(f"done with {genre}")

        self.gen_csv(playlists)


spoti = Spotify_work()
spoti.csv_from_spotigenres()
# print(spoti.get_playlist_ids("https://open.spotify.com/playlist/37i9dQZF1EIZvbvrhfHXQ5?si=ae2210499fd94152"))
# predictor = Predictor(spoti.get_info_1song("https://open.spotify.com/track/4l1F6QTzTtrf7CRbamAw4G?si=2c940c8a40be448c"),
#                      spoti.genres)
# predictor.predict_all_genres()

# predict(get_info_1song("https://open.spotify.com/track/1cUIk99uflLAjSqA2XSC9H?si=bb34d4c0babb4298"))

# if int(datetime.datetime.now().weekday()) == 6:
#    save_songs_from_weeklymix()

# -----------------------------------------HOTKEY----------------------------------------------------#
# hotkey = keyboard.HotKey(keyboard.HotKey.parse('<alt>+<ctrl>+l'), like_current_song1)


# def for_canonical(f):
#    return lambda k: f(h.canonical(k))


# with keyboard.Listener(on_press=for_canonical(hotkey.press)) as h:
#    h.join()
