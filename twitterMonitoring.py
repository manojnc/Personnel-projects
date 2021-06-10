import tweepy
import twilio
from twilio.rest import Client

class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        print(status.text)
        if status.text.startswith("RT @"):
            try:
                full_text=status.retweeted_status.extended_tweet["full_text"]
            except AttributeError:
                full_text = status.retweeted_status.text
            print("retweet got executed" + " " + full_text)
        else:
            try:
                full_text=status.extended_tweet["full_text"]
            except AttributeError:
                full_text = status.text
            print("tweet got executed" + " " + full_text)
        track = ['b1', 'b2', 'h1-b', 'chennai', 'B1/B2','resume','appointments']
        for i in track:
            if i in full_text.lower():
                print("keyword found" +" " + full_text)
                client = get_twilio_obj()
                send_whatsapp_msg(client, full_text)
                #make_call(client)
                break

def get_twilio_obj():
    TWILIO_ACCOUNT_SID = ''
    TWILIO_AUTH_TOKEN = ''
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    return client

def send_whatsapp_msg(client,text):
    from_whatsapp_number = 'whatsapp:+1{fromNum}'
    to_whatsapp_number = 'whatsapp:+1{num}'
    msg = client.messages.create(body=text,
                                 from_=from_whatsapp_number,
                                 to=to_whatsapp_number)
    return

def make_call(client):

    call = client.calls.create(
    url='http://demo.twilio.com/docs/voice.xml',
    to='+1{}',
    from_='+1{}')
    return


def main():
    auth = tweepy.OAuthHandler("twitterCreds", "twitterCreds")
    auth.set_access_token("twitterCreds",
                          "twitterCreds")
    api = tweepy.API(auth, wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True)

    try:
        api.verify_credentials()
        print("Authentication OK")
    except:
        print("Error during authentication")
    try:
        myStreamListener = MyStreamListener()
        myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
        myStream.filter(follow=['41533816','204661628','94702211','1352755439654461440'],is_async=True)
    except ReadTimeoutError:
        main()
    except Exception as e:
        client = get_twilio_obj()
        send_whatsapp_msg(client, str(e))
    return

if  __name__ == "__main__":
    main()

#myStream.filter(follow=['1352755439654461440'],track=['b1','b2','B1','B2','h1b'], is_async=True)

#myStream.filter(languages=['en'], track=['b1','b2','B1','B2','h1b','chennai','B1/B2'], is_async=True)