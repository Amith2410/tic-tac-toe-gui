import yt_dlp

url = input("Enter YouTube URL: ")

# Only download best progressive format (video+audio already combined)
ydl_opts = {
    'format': 'best[ext=mp4][vcodec^=avc1][acodec^=mp4a]/best',  # combined streams only
    'outtmpl': '%(title)s.%(ext)s'  # Save as video_title.mp4
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])
