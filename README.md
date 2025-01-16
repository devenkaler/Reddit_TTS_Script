# Reddit_TTS_Script

(Linux script) creates a mp4 file containing the top post for that day of the specified subreddit with text to speech and subtitles

# Dependencies

TTS
```pip install TTS```


pydub
```pip install pydub```


moviepy
```pip install moviepy```


espeak
```apt-get install espeak```

# Use

To generate mp4, 


```./run.sh [subreddit] [mp4 file]``` 

Produces file data/post.json with some relavent post data
Produces file data/tts.mp3 with text to speech from the post

requires both parameters, subreddit must be real

Must create .env file with: SECERET KEY, PUBLIC_KEY, username, password by creating a new reddit application through https://business.reddithelp.com/s/article/Create-a-Reddit-Application
