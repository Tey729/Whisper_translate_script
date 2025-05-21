import requests
import re
import os

def parse_srt(content):
    pattern = r'(\d+)\n(\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3})\n((?:.*?\n)*?)(?:\n|$)'
    matches = re.findall(pattern, content, re.MULTILINE)
    return matches

def translate_text(text, ollama_api="localhost:11434"):
    prompt = """你是一个专业的翻译助手。请将以下英文翻译成中文。
要求：
1. 只输出翻译后的中文文本
2. 不要添加任何解释或额外的文字
3. 翻译要准确、自然、符合中文表达习惯
4. 翻译的时候可以联系一下上文
5. 以下是一些特殊翻译词组：heal，healing是回血；AUBREY,KEL,OMORI,MARI,HERO都是人名，KEL可能在文本中被错认为Cow，可以直接输出这些的大写字母；headbutt是头槌；fuck可以翻译成咩的，或者特咩，shit也是

英文文本：
"""
    data = {
        "model": "qwen2.5:7b",
        "prompt": prompt + text.strip(),
        "stream": False
    }
    
    try:
        response = requests.post(f'http://{ollama_api}/api/generate', json=data, timeout=60)
        response.raise_for_status()
        result = response.json()
        return result['response'].strip()
    except Exception as e:
        print(f"翻译出错: {str(e)}")
        return "[翻译失败] " + text

def translate_srt_file(input_file, output_file, ollama_api="localhost:11434"):
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    subtitle_blocks = parse_srt(content)
    output_content = ""

    total_blocks = len(subtitle_blocks)
    for i, block in enumerate(subtitle_blocks, 1):
        number = block[0]
        timestamp = block[1]
        text = block[2].strip().replace("\n", " ")
        
        print(f"正在翻译 {os.path.basename(input_file)} - 第 {i}/{total_blocks} 条字幕...")
        translated_text = translate_text(text, ollama_api=ollama_api)
        
        output_content += f"{number}\n{timestamp}\n{text}\n{translated_text}\n\n"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(output_content)
    
    print(f"✅ {os.path.basename(input_file)} 翻译完成，保存为 {os.path.basename(output_file)}")

def batch_translate_srt(folder_path, ollama_api="localhost:11434"):
    for filename in os.listdir(folder_path):
        if filename.endswith(".srt") and not filename.endswith("_cn.srt"):
            input_path = os.path.join(folder_path, filename)
            output_path = os.path.join(folder_path, filename.replace(".srt", "_cn.srt"))
            translate_srt_file(input_path, output_path, ollama_api=ollama_api)

if __name__ == "__main__":
    folder_path = r"D:/iTubeGo\DOWNLOAD/Omori/split"
    ollama_api = "localhost:11434"
    batch_translate_srt(folder_path, ollama_api)

