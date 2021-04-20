#!/usr/bin/env python 3


import requests
from secrets import client_id, client_secret

def get_authorization():
    query = "https://accounts.spotify.com/authorize"
    scope = "user-read-recently-played"
    #redirect_uri = "https:%2F%2Fwww.builtinseattle.com%2F"
    redirect_uri = "http://localhost/callback"
    parameters = {
        "client_id": client_id, 
        "scope": scope, 
        "response_type": "code",
        "redirect_uri": redirect_uri
        }
    response = requests.get(query, params = parameters)

    return(response.url)

    
def get_token(code):
    query = "https://accounts.spotify.com/api/token"
    scope = "user-read-recently-played"
    redirect_uri = "http://localhost/callback"
    grant_type = "authorization_code"
    code = code

    response = requests.post(
        query,
        data = {
            "grant_type": grant_type,
            "code": code,
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uri": redirect_uri
        }
    )

    response_json = response.json()
    #print("This is the access token: " + response_json["access_token"])
    return(response_json)
    

if __name__ == "__main__":
    code = get_authorization()
    get_token(code)
 