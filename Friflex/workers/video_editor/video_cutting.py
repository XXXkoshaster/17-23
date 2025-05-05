import argparse
import json
from moviepy import VideoFileClip, AudioFileClip, CompositeAudioClip
import os
# os.environ["IMAGEIO_FFMPEG_EXE"] = r"C:\Users\Redmi\ffmpeg\bin\ffmpeg.exe"
# os.environ["FFMPEG_BINARY"] = os.environ["IMAGEIO_FFMPEG_EXE"]


parser = argparse.ArgumentParser(
    description="Нарезка видео на фрагменты по временным меткам из JSON"
)
parser.add_argument("video", help="путь к входному MP4-видео")
parser.add_argument(
    "json", help="путь к JSON-файлу со списком меток (start, end)")
parser.add_argument(
    "language", help="язык")
args = parser.parse_args()

video_file = args.video
json_file = args.json
video = VideoFileClip(video_file).without_audio()
duration = video.duration

with open(json_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

cnt = 1
tmp_data = dict()
for part in data["events"]:
    print(data)
    start = part["start"]
    end = part["end"]
    # print((start, end))
    clip = video.subclipped(start, end)
    # path = f"short_video_{cnt}.mp4"
    output_path = f"Shorts/short_video_{cnt}.mp4"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    clip.write_videofile(output_path, codec="libx264",
                         preset="ultrafast",
                         threads=4,
                         fps=24)
    with open(f"comments/short_video_{cnt}_{args.language}.json", "w", encoding='utf-8') as f:
        f.write(json.dumps(part, ensure_ascii=False))
    cnt += 1
    clip.close()
video.close()
