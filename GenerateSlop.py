import moviepy
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from PIL import Image, ImageDraw, ImageFont

import whisper_timestamped as whisper
import torch

import edge_tts, asyncio
import random

import pandas as pd
import os
import shutil
import multiprocessing

voice_list = ["en-US-AndrewMultilingualNeural", "en-US-AndrewNeural", "en-US-AriaNeural", "en-US-AvaMultilingualNeural", "en-US-AvaMultilingualNeural",
              "en-US-AvaNeural", "en-US-BrianMultilingualNeural", "en-US-EmmaMultilingualNeural", "en-US-EmmaNeural", "en-US-EricNeural",
              "en-US-GuyNeural", "en-US-JennyNeural", "en-US-MichelleNeural"]

whisper_model = whisper.load_model("base", device="cuda" if torch.cuda.is_available() else "cpu")

def wrap_text(text, font, max_width, draw):
    font = ImageFont.truetype("arial.ttf", 80)
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + (" " if current_line else "") + word
        width = draw.textlength(test_line, font=font)

        if width <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return lines

def create_text_image(text, font_path, font_size, max_width, color=(255, 255, 255), stroke_width=2, stroke_fill=(0, 0, 0), line_spacing=10):
    font = ImageFont.truetype(font_path, font_size)

    dummy_img = Image.new("RGBA", (1, 1))
    draw = ImageDraw.Draw(dummy_img)

    lines = wrap_text(text, font, max_width, draw)

    line_height = font_size + line_spacing
    img_height = line_height * len(lines)

    img = Image.new("RGBA", (max_width, img_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    y = 0
    for line in lines:
        draw.text(
            (0, y),
            line,
            font=font,
            fill=color,
            stroke_width=stroke_width,
            stroke_fill=stroke_fill
        )
        y += line_height

    return img

def GenerateVideo(ThreadFolder:str):
    for i in range(1):
        #edge-tts --list-voices | for list of TTS voices
        voice=random.choice(voice_list)
        async def save_tts(text, to_save):
            tts = edge_tts.Communicate(text, voice=voice)
            await tts.save(f"./TempStuffForBuilding/{ThreadFolder}/{to_save}.mp3")

        reddit_page = random.choice(os.listdir('./RedditLists')).split("_")[0]
        data = pd.read_csv(f"./RedditLists/{reddit_page}").values.tolist()
        story = random.choice(data)
        
        if reddit_page == "AmItheAsshole":
            title = str(story[0]).replace("AITA", "Am I The Asshole").replace("aita", "Am I The Asshole").replace("Aita", "Am I the Asshole") + "... "
            author = str(story[1])
            body = story[2].replace("AITA", "Am I The Asshole")
        else:   
            title = str(story[0])
            author = str(story[1])
            body = story[2]

        identifier = random.randint(0, 1000000)
        asyncio.run(save_tts(title, f"temp_title{identifier}"))
        asyncio.run(save_tts(body, f"temp_body{identifier}"))

        #Base Shit
        base_background_clip = moviepy.VideoFileClip("Footage/VideoBackgroundSloppified.mov")
        
        title_audio_clip = moviepy.AudioFileClip(f"./TempStuffForBuilding/{ThreadFolder}/temp_title{identifier}.mp3")
        title_audio_clip = title_audio_clip.with_end(title_audio_clip.duration)
        body_audio_clip = moviepy.AudioFileClip(f"./TempStuffForBuilding/{ThreadFolder}/temp_body{identifier}.mp3")
        body_audio_clip = body_audio_clip.with_start(title_audio_clip.duration)
        
        if title_audio_clip.duration + body_audio_clip.duration > 180: continue
        
        jesus = moviepy.VideoFileClip("./Footage/Jesus 67.mov", has_mask=True).with_duration(title_audio_clip.duration + body_audio_clip.duration + .2)
        jesus = jesus.with_position((-180, -570))
        
        #Background Music
        music_choice = str(random.choice(os.listdir("./Footage/Music")))
        music_file = moviepy.AudioFileClip(f"./Footage/Music/{music_choice}").with_volume_scaled(.05).with_duration(title_audio_clip.duration + body_audio_clip.duration)
        
        base_audio_clip = moviepy.CompositeAudioClip([title_audio_clip, body_audio_clip, music_file])

        #Length Calcs
        base_audio_length = int(base_audio_clip.duration)
        base_background_length = int(base_background_clip.duration)
        end_cuttoff = base_background_length - base_audio_length - 15
        startpoint = random.randint(5, int(end_cuttoff))

        #Cutting down the background clip
        background_clip_cut = base_background_clip.subclipped(startpoint, startpoint+base_audio_length+1)
        background_clip_cut.audio = base_audio_clip
        
        #Animation Handlers
        def pop_effect(t, clip_duration):
            if t < .15:
                p = t / .15
                return .05 + (1.1 - .05) * (1 - (1 - p) ** 3)

            if t > clip_duration - .15:
                p = (t - (clip_duration - .15)) / .15
                return 1.1 * (1 - p) + .05 * p

            return 1.0
        
        #Initial Card Shit
        card = moviepy.ImageClip("./Footage/RedditCardThingV2.png").with_duration(background_clip_cut.duration)
        subreddit_text = moviepy.TextClip(text=f"r/{reddit_page.split('_')[0]}", font_size=60, size=(720,200), horizontal_align="left", vertical_align="top").with_position((320, 120))
        subreddit_text = subreddit_text.with_duration(background_clip_cut.duration)
        author_text = moviepy.TextClip(text=f"u/{author}", font_size=50, size=(720, 200), color="grey", horizontal_align="left", vertical_align="top").with_position((320, 180))
        author_text = author_text.with_duration(background_clip_cut.duration)
        
        title_text = create_text_image(text=title, font_path="arial.ttf", font_size=75, max_width=625, color=(0, 0, 0), stroke_width=0)
        title_text.save(f"./TempStuffForBuilding/{ThreadFolder}/title_text{identifier}.png")
        title_clip = moviepy.ImageClip(f"./TempStuffForBuilding/{ThreadFolder}/title_text{identifier}.png").with_position((220, 300)).with_duration(background_clip_cut.duration).resized(lambda t: pop_effect(t, title_audio_clip.duration+.2)).with_end(title_audio_clip.duration+.2)
        
        #Caption Generator
        caption_text = whisper.transcribe(whisper_model, f"./TempStuffForBuilding/{ThreadFolder}/temp_body{identifier}.mp3", language="en")
        def build_captions(segments, max_characters):
            captions = []
            current_words = []
            start_time = None
            
            for segment in segments:
                for w in segment['words']:
                    if start_time == None:
                        start_time = w["start"]
                    
                    current_words.append(w)
                    text = " ".join(word["text"] for word in current_words)
                    
                    if len(text) >= max_characters:
                        captions.append({
                            "text": text,
                            "start": start_time,
                            "end": w["end"]
                        })
                        current_words = []
                        start_time = None
            if current_words:
                captions.append({
                    "text": " ".join(word["text"] for word in current_words),
                    "start": start_time,
                    "end": current_words[-1]["end"]
                })
            
            return captions
        
        def make_caption_image(text, start, end):
            clip = create_text_image(text=text, font_path="arial.ttf", font_size=75, max_width=625, color=(0, 0, 0), stroke_width=0)
            clip.save(f"./TempStuffForBuilding/{ThreadFolder}/Caption_{identifier}_{i}.png")
            
            caption_clip = moviepy.ImageClip(f"./TempStuffForBuilding/{ThreadFolder}/Caption_{identifier}_{i}.png").with_position((220, 300)).with_start(start+title_audio_clip.duration+.2).with_end(end+title_audio_clip.duration+.2)
            caption_clip = caption_clip.resized(lambda t: pop_effect(t, caption_clip.duration))
            return caption_clip
            
        captions_to_use = build_captions(caption_text["segments"], 150)
        caption_clips = [make_caption_image(caption["text"], caption["start"], caption["end"]) for caption in captions_to_use]
        
        #Final Shit
        final_clip = moviepy.CompositeVideoClip([background_clip_cut, card, subreddit_text, author_text, title_clip, jesus, *caption_clips])
        final_clip.write_videofile(f"./Output/{voice}_{ThreadFolder}_{i}_{reddit_page}.mp4", fps=30, codec="libx264")

        #Cleanup Shit I Need To Do For Some Reason
        base_background_clip.close()
        background_clip_cut.close()
        card.close()
        author_text.close()
        subreddit_text.close()
        
        for file in os.listdir(f"./TempStuffForBuilding/{ThreadFolder}"):
            os.remove(f"./TempStuffForBuilding/{ThreadFolder}/{file}")

if __name__ == "__main__":
    thread1 = multiprocessing.Process(target=GenerateVideo, args=("Thread1",))
    thread1.start()
    thread2 = multiprocessing.Process(target=GenerateVideo, args=("Thread2",))
    thread2.start()
    thread3 = multiprocessing.Process(target=GenerateVideo, args=("Thread3",))
    thread3.start()
    
    GenerateVideo("Thread4")