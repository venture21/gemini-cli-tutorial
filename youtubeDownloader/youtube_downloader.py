from yt_dlp import YoutubeDL

def download_youtube_video(url, output_path='.'):
    ydl_opts = {
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'format': 'best', # 가장 좋은 품질로 다운로드
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    print(f"'{url}' 동영상 다운로드가 완료되었습니다.")

import sys

if __name__ == "__main__":
    if len(sys.argv) > 1:
        video_url = sys.argv[1]
        download_youtube_video(video_url)
    else:
        print("사용법: python youtube_downloader.py [유튜브 동영상 URL]")
        print("예시: python youtube_downloader.py https://www.youtube.com/watch?v=dQw4w9WgXcQ")
