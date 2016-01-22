import sys, os
from requests_oauthlib import OAuth1
import requests
import json

def main():
    url = input("Enter your API URL: ")
    username= input("Enter your Username: ")
    password = input("Enter your Password: ")

    print("Attempting to retrieve from API located at %s, on behalf of user: %s" % (url, username))
    request_api(url, username, password)

def request_api(URL, username, password):

    # Specify API's URL location and authentication params using OAuth1
    # URL='http://phillip.lisovicz.com/api/foobars'
    # auth = OAuth1('phillip.lisovicz@gmail.com', 'samplepassword')
    # PARAMS = {}
    
    PARAMS={}
    auth = OAuth1(username, password)
    try:
        r = requests.get(URL, params=PARAMS , allow_redirects=True, auth=auth)

        # If we want to view raw response
        # print(r.text)

        # Let's view the response in a more pleasant manner
        response =json.loads(r.text)
        print(json.dumps(response,indent=4))
     
    except requests.exceptions.RequestException as e:
        # If fails, view Exception that is raised
        print e



if __name__ == '__main__':
    main()


