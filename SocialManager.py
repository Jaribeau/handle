#SocialManager

import facebook
from TwitterAPI import TwitterAPI
import getpass

class SocialManager:
    def __init__(self):
        self.fb_appID = "176920796159563"
        self.fb_app_secret = "ffc0d23e13dc6617f76140bbcf531cf6"
        self.fb_userToken = "EAACg0btpGMwBAArWP09Y5J7kIkZB2adkMx0V1fmEmXmnaEaGZBlD9ZBBxe5lM5ghupkaq9q4VaDFDuuJ6bnx1GqBk4ifpjZCaMlmdAcbmyb7bHpke8IHo0f6LwGSnCZA3A65pjLch1Q17V9v1lIh02qPDhZAbRDZAoZD"

        self.tw_consumer_key = "HCkDa7pZd82ec73DBN0VMyoVV"
        self.tw_consumer_secret = "3H1u52aXZyVGGv3FqPBYPzHVRrmbQwhtiMV2EqJTv3syfuKq00"
        self.tw_access_token_key = "847601801939505164-viihnSuuCJGLCUvPHyshsDUX8XEUHZd"
        self.tw_access_token_secret = "JM92HuYVPrbNm6MAJlhJVUhPtYe0zUJ2jBh6Y4xaecrtE"

    # Called by GameServer
    def post(self, score):
        try:
            self.fb_graph = facebook.GraphAPI(access_token=self.fb_userToken)
            self.fb_graph.put_wall_post(message="just scored " + str(score) + " on Handle! Beat my score if you can!")
        except:
            print("facebook.GraphAPIError: (#200) The user hasn't authorized the application to perform this action")

        try:
            self.tw_api = TwitterAPI(self.tw_consumer_key, self.tw_consumer_secret, self.tw_access_token_key, self.tw_access_token_secret)
        except:
            print("Could not connect to Twitter")

        #search for pizza
        #r = api.request('search/tweets', {'q':'pizza'})
        #for item in r:
        #        print(item)

        # tweet
        self.tw_post = self.tw_api.request('statuses/update', {'status':'Just scored ' + str(score) + ' in Handle! Beat my score if you can!'})
        print(self.tw_post.status_code)\


    def reauthenticate(self):
        self.username = input("Username: ")
        self.password = getpass("Password: ")

        self.fb_graph.reauthenticate(self.username, self.password)

        self.tw_api.threeLegAuthenticate(self.username, self.password)