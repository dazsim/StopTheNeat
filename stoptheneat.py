import tweepy
from os import environ


auth = tweepy.OAuthHandler(environ['CONSUMER_KEY'], environ['CONSUMER_SECRET'])
auth.set_access_token(environ['ACCESS_TOKEN'], environ['ACCESS_TOKEN_SECRET'])

api = tweepy.API(auth)

for follower in tweepy.Cursor(api.followers).items():
    follower.follow()


class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        if not hasattr(status, 'retweeted_status'):
            print(f"{status.user.name} - {status.text}")
            if " neat" in status.text.lower():
                api.update_with_media('stop.gif', in_reply_to_status_id=status.id, auto_populate_reply_metadata=True)
            if "#unfollowme" in status.text.lower():
                if status.user.id == 1019126612279914496:
                    return
                api.destroy_friendship(status.user.id)

    def on_event(self, event):
        if event.event == 'follow':
            source_user = event.source
            if source_user['id'] == 1019126612279914496:
                return
            api.create_friendship(source_user['id'])


stream_listener = MyStreamListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
stream.userstream(encoding='utf8')
