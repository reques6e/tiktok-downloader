import os
import asyncio
import random

from yt_dlp import YoutubeDL
from bot.exceptions import (
    TikTokVideoDownloadError, InstagramVideoDownloadError, 
    FileIsNotVideo, UnknownDownloadError
)


DOWNLOAD_DIR = './data'

async def download_video(url: str) -> str:
    """
    Скачивает видео.
    """
    ydl_opts = {
        'format': 'best',
        'outtmpl': f'{DOWNLOAD_DIR}/{random.randint(0000, 9999)}-%(title)s.%(ext)s',
        'quiet': True,
        'merge_output_format': 'mp4',
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }],
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = await asyncio.to_thread(ydl.extract_info, url, download=False)
            
            if not info.get('is_video', True):
                raise FileIsNotVideo('Файл не является видео.')
            
            await asyncio.to_thread(ydl.extract_info, url, download=True)
            file_path = ydl.prepare_filename(info)
            
            return file_path

    except Exception as e:
        if 'tiktok.com' in url:
            raise TikTokVideoDownloadError('Ошибка при скачивании с TikTok. Возможно, ссылка устарела.')
        elif 'instagram.com' in url:
            if 'empty media response' in str(e).lower():
                raise UnknownDownloadError('Неизвестная ошибка')
            elif 'url' not in locals().get('info', {}):
                raise InstagramVideoDownloadError('Поддерживаются только Reels и видео.')
            raise
        
        raise UnknownDownloadError('Неизвестная ошибка')