import json
import argparse
import librosa.effects
from moviepy import VideoFileClip, TextClip, ImageClip, CompositeVideoClip, AudioFileClip, CompositeAudioClip
import soundfile as sf
import numpy as np
import librosa

parser = argparse.ArgumentParser(
    description="Нарезка видео на фрагменты по временным меткам из JSON"
)
parser.add_argument("voice", help="путь к озвучке")
parser.add_argument(
    "music", help="путь к музыке")
parser.add_argument(
    "json", help="путь к json-у с комментариями")
parser.add_argument(
    "path_to_clip", help="путь к обрезанному клипу")
parser.add_argument(
    "number", help="какой по счету файл")
parser.add_argument(
    "language", help="язык озвучки")
args = parser.parse_args()

def load_mono(path):
    data, rate = sf.read(path)
    # Приведение к моно
    if len(data.shape) > 1:
        data = data.mean(axis=1)
    return data.astype(np.float32), rate

SR = 44100  # Частота дискретизации
voice_volume = 2.0
music_volume = 0.2

voice, _ = librosa.load(args.voice, sr=SR)
music, _ = librosa.load(args.music, sr=SR)

video = VideoFileClip(args.path_to_clip).without_audio()
video_duration = video.duration  # в секундах

voice_duration = librosa.get_duration(y=voice, sr=SR)
stretch_rate = voice_duration / video_duration
voice = librosa.effects.time_stretch(voice, rate=stretch_rate)

target_len = len(voice)
if len(music) < target_len:
    padding = np.zeros(target_len - len(music))
    music = np.concatenate([music, padding])
else:
    music = music[:target_len]

# Смешивание с учетом громкости
mixed = voice * voice_volume + music * music_volume
mixed /= np.max(np.abs(mixed)) + 1e-9 


sf.write(f"music/mixed_output_{args.number}_{args.language}.wav", mixed, 44100)

combined_audio = AudioFileClip(
    f"music/mixed_output_{args.number}_{args.language}.wav").subclipped(0, video.duration)

with open(args.json, 'r', encoding='utf-8') as f:
    comment = json.load(f)

max_message_length = 35
color = 'white'
if args.language == "hi": 
    font_path = r"C:\Fonts\NotoSansDevanagari-Regular.ttf"
elif args.language == "zh":
    font_path = r"C:\Fonts\NotoSansSC-VariableFont_wght.ttf"
else:
    font_path = r"C:/Windows/Fonts/Arial.ttf"

text_clips = []

text = comment['comment']
start_time = comment['start'] - comment['start']
end_time = comment['end'] - comment['start']
duration = end_time - start_time

words = text.split()
chunks = []
current_line = ""

for word in words:
    if len(current_line) + len(word) + 1 <= max_message_length:
        current_line += " " + word if current_line else word
    else:
        chunks.append(current_line)
        current_line = word
if current_line:
    chunks.append(current_line)

# Показываем каждую часть на экране по очереди
chunk_duration = duration / len(chunks)
for i, chunk in enumerate(chunks):
    txt_clip = TextClip(text=chunk,
                        font_size=36,
                        font=font_path,
                        color=color,
                        stroke_color="black",
                        stroke_width=4,
                        method="label",
                        size=(680, None))

    # Получаем изображение текста (одноразовый рендер)
    img = txt_clip.get_frame(0)
    img_clip = ImageClip(img).with_start(start_time + i * chunk_duration)\
                                .with_duration(chunk_duration)\
                                .with_position((20, 430))
    text_clips.append(img_clip)

final = CompositeVideoClip([video, *text_clips])
audio = CompositeAudioClip([combined_audio])
final = final.with_audio(audio)

final.write_videofile(f"Shorts/video_with_comments_{args.number}_{args.language}.mp4",
                    codec="libx264",
                    preset="ultrafast",
                    threads=4,
                    fps=24)
