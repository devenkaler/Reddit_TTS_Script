from moviepy.editor import *
import os
import json
import random
import sys
from moviepy.video.tools.subtitles import SubtitlesClip

clip = TextClip("test", font ="Arial-Bold", fontsize = 50, color ="green") 

sample = str(sys.argv[1])

if os.path.exists("final.mp4"):
        os.remove("final.mp4")
if os.path.exists("sub_clip.mp4"):
        os.remove("sub_clip.mp4")

#get audio length/ subtitles
post_data = open('data/post.json', 'r').read()
post_data = json.loads(post_data)

subtitles = []
audio_len = post_data['title']['time']
subtitles.append(((0, audio_len), post_data['title']['text']))
for c in post_data['content']:
    subtitles.append(((audio_len, audio_len+c['time']), c['text']))
    audio_len += c['time']

#get video length
video = VideoFileClip(sample)
video_len = video.duration

#set video length/ add audio
start_time = random.randrange(5, int(video_len-audio_len))
end_time = start_time+audio_len

video = video.subclip(start_time, end_time)
audio = AudioFileClip("data/tts.mp3")
video.audio = audio

generator = lambda txt: TextClip(txt, font='Ubuntu-Bold', fontsize=50, method='caption',
                                 size=(900, 0), color="white", stroke_color="black", stroke_width=3.5)

sub_clip = SubtitlesClip(subtitles, generator)

final = CompositeVideoClip([video, sub_clip.set_pos(('center','center'))])

final.write_videofile("final.mp4")