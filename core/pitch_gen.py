import subprocess
import tempfile
import os
import sys
import io

LLAMA_BIN = "C:/Users/debim/llama.cpp/build/bin/Release/llama-cli.exe"
MODEL_PATH = "C:/Users/debim/llama.cpp/models/mistral/model_instruct.gguf"
N_PREDICT = 512

def build_prompt(bio: str, tone: str) -> str:
    return f"""[INST] 
You are a razor-sharp business consultant from a rogue empire that builds real systems for founders — no fluff, no VC talk, only precision.

Generate a concise pitch from a consultant (you) who helps founders like the one below improve their products, marketing, and monetization. Keep the tone bold, intelligent, and deeply observant.

Start with a short hook (1 line), followed by a 3–5 sentence direct pitch that shows you understand their startup. Include *no* greetings or signoffs. Focus on **why you're the guy** who can get them results. Do not include any labels like "Hook:" or "Pitch:". 

Bio: {bio}
Tone: {tone}
Service: Custom offline AI tools that give founders an unfair advantage.
[/INST]"""

def run_llama(prompt):
    with tempfile.NamedTemporaryFile("w+", delete=False, encoding="utf-8") as f:
        f.write(prompt)
        f_path = f.name

    try:
        result = subprocess.run(
            [
                LLAMA_BIN,
                "--model", MODEL_PATH,
                "--n-predict", str(N_PREDICT),
                "--file", f_path,
                "--temp", "0.7",
                "--top-k", "50",
                "--top-p", "0.9",
                "-no-cnv"
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",   
            errors="replace"    
        )
        output = (result.stdout or "").strip()
        return clean_output(output)
    finally:
        os.remove(f_path)

def clean_output(output):
    lines = output.splitlines()
    useful_lines = [line for line in lines if not line.startswith("system") and line.strip()]
    cleaned = "\n".join(useful_lines)
    
    service_index = cleaned.rfind("Service:")
    if service_index != -1:
        # Move past the end of that line
        end_of_service_line = cleaned.find("\n", service_index)
        if end_of_service_line != -1:
            cleaned = cleaned[end_of_service_line:].strip()
    
    cleaned = cleaned.replace("[end of text]", "").strip()
    return cleaned

def generate_pitches(prospects, style="empire"):
    for p in prospects:
        prompt = build_prompt(p["bio"], style)
        pitch = run_llama(prompt)
        p["pitch"] = pitch
    return prospects



