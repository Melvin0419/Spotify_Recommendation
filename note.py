from dotenv import load_dotenv
import os
import base64
import json
from requests import post,get

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = client_id+":"+client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes),"utf-8")

    url = "https://accounts.spotify.com/api/token"

    headers = {
        "Authorization": "Basic "+ auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {"grant_type": "client_credentials"}

    result = post(url, headers = headers, data = data) # send a post request to the server, return the 
    json_result = json.loads(result.content)
    token = json_result["access_token"]

    return token

def get_auth_header(token):
    return {"Authorization":"Bearer "+token}


# list out 5 artists and select one.
# input: artist name (str)
# output: return a dict contain{"name","url","image_url","id"}


def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=5" # artist name, type*, limit 

    query_url = url + query
    result = get(query_url, headers = headers)
    json_result = json.loads(result.content)["artists"]["items"]

    # Check if any result
    if len(json_result) == 0:
        print("No artist with this name exists...")
        return "No artist with this name exists..."
    
    # list out 5 results and select one 
    print("The results of searching artist: ")
    for i,artist in enumerate(json_result):
        # popularity = artist["popularity"]
        name = artist["name"]
        print(f"{i+1}. {name}")

    # return up to 5 results 
    artists = []
    for artist in json_result:
        artists.append({
            "name" : artist["name"],
            "genres" : artist["genres"],
            "url" : artist["external_urls"]["spotify"],
            "image_url" : artist["images"][1]["url"],
            "id" : artist["id"]
        })
    
    return artists

# list out 5 tracks
# artist:{"name","artists","popularity","id","external_urls"}

def search_for_track(token, track_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={track_name}&type=track&limit=5" # track name, type*, limit 

    query_url = url + query
    result = get(query_url, headers = headers)
    json_result = json.loads(result.content)["tracks"]["items"]

    # Check if any result
    if len(json_result) == 0:
        print("No track with this name exists...")
        return "No track with this name exists..."
    
    # list out 5 results and select one 
    print("The results of searching track: ")
    for i,track in enumerate(json_result):
        name = track["name"]
        artists = ", ".join([ artist["name"] for artist in track["artists"]])
        print(f"{i+1}. {name} - {artists}")

    # return up to 5 results 
    tracks = []
    for track in json_result:
        artists = track["artists"]
        artists_name = "、".join([artist["name"] for artist in artists])
        track_name = track["name"]
        tracks.append({
            "name" :  f"{track_name} - {artists_name}",
            "url" : track["external_urls"]["spotify"],
            "id" : track["id"]
        })
    
    return tracks

# 需要搭配 autocomplete 之類的

def get_genres(token):
    url = "https://api.spotify.com/v1/recommendations/available-genre-seeds"
    headers = get_auth_header(token)
    result = get(url, headers = headers)
    json_result = json.loads(result.content)["genres"]

    # search = input("Search for genres")
    # result = []
    # for i in json_result:
    #     if search in i:
    #         result.append(i)
    # idx = input("Select a genre")
    # genre = result[idx-1]
    # return genre
    
    return json_result

def get_recommedations(token, selections,limit=5 ):

    # Check selections, then create query
    query = []
    for seed in ['artists', 'tracks', 'genres']:
        if len(selections[seed])>0:
            id = ",".join([i["id"] for i in selections[seed]])
            if seed != "genres":
                query.append(f"seed_{seed}={id}")
            else:
                query.append(f"{seed}={id}")

    querys = "&".join(query)

    # send a GET request to endpoint
    url = "https://api.spotify.com/v1/recommendations?"+querys+f"&limit={limit}"
    headers = get_auth_header(token)
    result = get(url, headers = headers)
    json_result = json.loads(result.content)["tracks"]

    
    # print out the selectoin(for user check)
    for seed in ['artists', 'tracks', 'genres']:
        if len(selections[seed])>0:
            print(f"{seed[0].upper()+seed[1:]}:")
            for idx,i in enumerate(selections[seed]):
                print(f'{idx+1}. {i["name"]}')

    print("------------------------------")
    
    # print out recommedations
    print("Your Recommendation:")
    for i,recom in enumerate(json_result):
        track = recom["name"]
        artists = ", ".join([artist["name"] for artist in recom["artists"]])

        print(f"{i+1}. {track} - {artists}")

    return json_result

token = get_token()
print(token)
# selections = {"artists":[],"tracks":[],"genres":[]}

# artist = search_for_artist(token, "vaundy")
# selections["artists"].append(artist)

# track = search_for_track(token, "yorunikakeru")
# selections["tracks"].append(track)
# recoms = get_recommedations(token=token, selections = selections)


