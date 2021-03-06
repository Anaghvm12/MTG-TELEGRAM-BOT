from __future__ import unicode_literals

import os
import requests
import aiohttp
import yt_dlp
import asyncio
import math
import time

import wget
import aiofiles

from pyrogram import filters, Client
from pyrogram.errors import FloodWait, MessageNotModified
from pyrogram.types import Message
from youtube_search import YoutubeSearch
from youtubesearchpython import SearchVideos
from yt_dlp import YoutubeDL
import youtube_dl
import requests

def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(':'))))


@Client.on_message(filters.command('song') & ~filters.private & ~filters.channel)
def song(client, message):

    user_id = message.from_user.id 
    user_name = message.from_user.first_name 
    rpk = "["+user_name+"](tg://user?id="+str(user_id)+")"

    query = ''
    for i in message.command[1:]:
        query += ' ' + str(i)
    print(query)
    m = message.reply("**๐ป๐ฅ๐๐๐ฝ๐๐๐ ๐ธ๐๐๐ ๐ฒ๐๐๐๐ถ.....**")
    ydl_opts = {"format": "bestaudio[ext=m4a]"}
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        #print(results)
        title = results[0]["title"][:40]       
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f'thumb{title}.jpg'
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, 'wb').write(thumb.content)


        performer = f"[แดแดษขษดแดs แดษข๐ฎ๐ณ]" 
        duration = results[0]["duration"]
        url_suffix = results[0]["url_suffix"]
        views = results[0]["views"]

    except Exception as e:
        m.edit(
            "**๐ฅ๐๐๐๐ฝ ๐ญ๐๐๐๐๐๐ ๐ฏ๐๐พ๐บ๐๐พ ๐ข๐๐๐๐พ๐ผ๐ ๐ณ๐๐พ ๐ฒ๐๐พ๐๐๐๐๐ ๐ฎ๐ฟ ๐ฒ๐พ๐บ๐๐ผ๐ ๐ ๐๐ ๐ฎ๐๐๐พ๐ ๐ฒ๐๐๐**"
        )
        print(str(e))
        return
    m.edit("**๐ฃ๐๐๐๐๐๐บ๐ฝ๐๐๐ ๐ธ๐๐๐ ๐ฒ๐๐๐๐ธ๐ถ**")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep = f'<b>๐ธ ๐ณ๐๐๐๐พ :</b> <a href="{link}">{title}</a>\n<b>๐งญ ๐ฃ๐๐๐บ๐๐๐๐ :</b> <code>{duration}</code>\n<b>๐ง ๐ต๐๐พ๐๐ :</b> <code>{views}</code>\n <b>๐ค ๐ฑ๐พ๐๐๐พ๐๐๐พ๐ฝ ๐ก๐ ::</b> {message.from_user.mention()} \n <b>๐บ ๐ด๐๐๐๐บ๐ฝ๐พ๐ฝ ๐ก๐ : @Universal_MoviesZ</b> ๐'
        secmul, dur, dur_arr = 1, 0, duration.split(':')
        for i in range(len(dur_arr)-1, -1, -1):
            dur += (int(dur_arr[i]) * secmul)
            secmul *= 60
        message.reply_audio(audio_file, caption=rep, parse_mode='HTML',quote=False, title=title, duration=dur, performer=performer, thumb=thumb_name)
        m.delete()
    except Exception as e:
        m.edit("**๐ซ ๐ค๐๐๐๐ ๐ซ**")
        print(e)

    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)

def get_text(message: Message) -> [None,str]:
    text_to_return = message.text
    if message.text is None:
        return None
    if " " not in text_to_return:
        return None
    try:
        return message.text.split(None, 1)[1]
    except IndexError:
        return None


@Client.on_message(filters.command(["video", "mp4"]))
async def vsong(client, message: Message):
    urlissed = get_text(message)

    pablo = await client.send_message(
        message.chat.id, f"**๐ฅ๐๐๐ฝ๐๐๐ ๐ธ๐๐๐ ๐ต๐๐ฝ๐พ๐..** `{urlissed}`"
    )
    if not urlissed:
        await pablo.edit("Invalid Command Syntax Please Check help Menu To Know More!")
        return

    search = SearchVideos(f"{urlissed}", offset=1, mode="dict", max_results=1)
    mi = search.result()
    mio = mi["search_result"]
    mo = mio[0]["link"]
    thum = mio[0]["title"]
    fridayz = mio[0]["id"]
    mio[0]["channel"]
    kekme = f"https://img.youtube.com/vi/{fridayz}/hqdefault.jpg"
    await asyncio.sleep(0.6)
    url = mo
    sedlyf = wget.download(kekme)
    opts = {
        "format": "best",
        "addmetadata": True,
        "key": "FFmpegMetadata",
        "prefer_ffmpeg": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
        "postprocessors": [{"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}],
        "outtmpl": "%(id)s.mp4",
        "logtostderr": False,
        "quiet": True,
    }
    try:
        with YoutubeDL(opts) as ytdl:
            ytdl_data = ytdl.extract_info(url, download=True)
    except Exception as e:
        await event.edit(event, f"**๐ฃ๐๐๐๐๐๐บ๐ฝ ๐ฅail๐ฝ ๐ฏ๐๐พ๐บ๐๐พ ๐ณ๐๐ ๐ ๐๐บ๐๐..** \n**Error :** `{str(e)}`")
        return
    c_time = time.time()
    file_stark = f"{ytdl_data['id']}.mp4"
    capy = f"""
**๐๐ธ๐๐ป๐ด :** [{thum}]({mo})
**๐๐ด๐๐๐ด๐๐๐ด๐ณ ๐ฑ๐ :** {message.from_user.mention}
"""
    await client.send_video(
        message.chat.id,
        video=open(file_stark, "rb"),
        duration=int(ytdl_data["duration"]),
        file_name=str(ytdl_data["title"]),
        thumb=sedlyf,
        caption=capy,
        supports_streaming=True,        
        reply_to_message_id=message.message_id 
    )
    await pablo.delete()
    for files in (sedlyf, file_stark):
        if files and os.path.exists(files):
            os.remove(files)
