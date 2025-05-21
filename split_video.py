# import os
# import subprocess

# # -------- 配置区：你只需要改下面这些就行 --------
# input_video = r"D:/iTubeGo/DOWNLOAD/Omori/【Omori】 When I Flex I Feel My Best! 【NIJISANJI EN  Fulgur Ovid】.mp4"
# output_dir = r"D:/iTubeGo/DOWNLOAD/Omori/split"
# segment_duration = 1800  # 单位：秒，1800 = 30分钟
# # ---------------------------------------------------

# os.makedirs(output_dir, exist_ok=True)

# # 输出文件模板
# output_template = os.path.join(output_dir, "output_%03d.mp4")

# # 构建 ffmpeg 命令
# cmd = [
#     "ffmpeg",
#     "-i", input_video,
#     "-force_key_frames", f"expr:gte(t,n_forced*{segment_duration})",
#     "-c:v", "libx264",
#     "-preset", "veryfast",
#     "-crf", "18",
#     "-c:a", "aac",
#     "-b:a", "128k",
#     "-map", "0",
#     "-f", "segment",
#     "-reset_timestamps", "1",
#     "-segment_time", str(segment_duration),
#     output_template
# ]

# # 执行命令
# print("🔧 正在切割中，请稍等...")
# subprocess.run(cmd)
# print(f"✅ 切割完成！分段视频保存在：{output_dir}")


import whisper
import os


def format_timestamp(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds - int(seconds)) * 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

folder_path = r"D:/iTubeGo/DOWNLOAD/Omori/split"
model = whisper.load_model("small").to("cuda")

for filename in os.listdir(folder_path):
    if filename.endswith((".mp4", ".mp3", ".wav", ".mkv", ".flac")):
        file_path = os.path.join(folder_path, filename)
        print(f"Processing: {file_path}")
        result = model.transcribe(file_path, language="English")

        srt_path = os.path.splitext(file_path)[0] + ".srt"
        with open(srt_path, "w", encoding="utf-8") as f:
            for i, segment in enumerate(result["segments"]):
                start = format_timestamp(segment["start"])
                end = format_timestamp(segment["end"])
                text = segment["text"].strip()
                f.write(f"{i+1}\n")
                f.write(f"{start} --> {end}\n")
                f.write(f"{text}\n\n")

