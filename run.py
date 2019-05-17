import praw
import time
from requests import get

client_id = 'XXXX'
client_secret = 'XXXX'
reddit_user = 'XXXX'
reddit_pass = 'XXXX'
target_sub = 'XXXX'
target_word = '!urbandict'

reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent=f'{target_word} bot (by u/impshum)',
                     username=reddit_user,
                     password=reddit_pass)


start_time = int(time.time())
api = 'http://api.urbandictionary.com/v0/define?term='

for comment in reddit.subreddit(target_sub).stream.comments():
    if start_time < int(comment.created_utc):
        body = comment.body
        if target_word in body:
            query = body.replace(f'{target_word} ', '')
            print(query)
            data = get(f'{api}{query}').json()
            if len(data['list']):
                result = data['list'][0]['definition']
                comment.reply(result)
                print(result)
            else:
                comment.reply(f'Sorry. There was no result for {query}')
                print('No result')
