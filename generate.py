#!/usr/bin/env python3

import requests
import os
import sys
import json
from dotenv import load_dotenv
from TTS.api import TTS
from pydub import AudioSegment

tts_engine = TTS(model_name="tts_models/en/vctk/vits", progress_bar=False, gpu=False)

#get auth/ key values
load_dotenv()
SECRET_KEY = os.getenv("REDDIT_SECRET_KEY")
PUBLIC_KEY = os.getenv("REDDIT_PUBLIC_KEY")
username = os.getenv("REDDIT_USERNAME")
pswd = os.getenv("REDDIT_PASSWORD")
auth = requests.auth.HTTPBasicAuth(PUBLIC_KEY, SECRET_KEY)

#generate token
data = {'grant_type': 'password', 
    'username': username,
    'password': pswd}
headers={'User-Agent': 'top-post by playful-yak'}
response = requests.post('https://www.reddit.com/api/v1/access_token', auth=auth, data=data, headers=headers)

TOKEN = response.json()['access_token']


def topPost(sub, after=0):
    headers = {'Authorization': f'bearer {TOKEN}', 'User-Agent': 'top-post'}
    base = 'https://oauth.reddit.com'
    params = {'t': 'day', 'limit': after+1}

    res = requests.get(base + f'/r/{sub}/top', params=params, headers=headers)

    return res.json()['data']['children'][after]

def delifExist(file):
    if os.path.exists(file):
        os.remove(file)

def genSegment(tts, text):
    tts_engine.tts_to_file(text=text, file_path="data/seg.wav", speaker='p230')
    seg = AudioSegment.from_wav('data/seg.wav')
    tts += seg
    content = ({ 
            'text': text, 
            'time': seg.duration_seconds
            })
    delifExist("data/seg.wav")

    return (content, tts)

def createPostFiles(sub):
    delifExist("data/tts.mp3")
    delifExist("data/post.json")

    for n in range(100):
        r = topPost(sub, after=n)
        if not r['data']['media_embed'] and r['data']['selftext']:
            break

    title = r['data']['title']
    text = r['data']['selftext']
    temp_text = ''
    full_post = {'title': [], 'content': []}
    full_tts = AudioSegment.empty()

    full_post['title'], full_tts = genSegment(full_tts, title)

    for i in range(len(text)):
        temp_text = (temp_text + text[i]).strip('\n')
        if ((text[i] == '.' or text[i] == ',' or text[i] == '?' or text[i] == '!') and len(temp_text) > 5) or (i == len(text) - 1 and len(temp_text) > 0):
            try:
                seg = genSegment(full_tts, temp_text)
                full_post['content'].append(seg[0])
                full_tts = seg[1]
            except:
                pass
            temp_text = ''

        #tts.mp3
        full_tts.export('data/tts.wav', format="wav")
        audio = AudioSegment.from_wav("data/tts.wav")
        audio.export("data/tts.mp3", format="mp3")
        delifExist("data/tts.wav")

        #post.json
        f = open('data/post.json', 'w')
        f.write(json.dumps(full_post))
        f.close()

subreddit = str(sys.argv[1])
createPostFiles(subreddit)
