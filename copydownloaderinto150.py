import os
import time
import requests
import pyperclip
from PIL import Image
from io import BytesIO
import base64
import tempfile
import pygame

SAVE_DIR = "captcha"
choice = input("O/M: ").upper()
if choice == "O":
    PREFIX = "ro"
elif choice == "M":
    PREFIX = "rm"
else:
    exit(7)
EXT = ".png"

# Base64-encoded short audio (success and error)
SUCCESS_AUDIO_BASE64 = b'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'
ERROR_AUDIO_BASE64 = b'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yqNRLSx17qCJENoiuoGy9HxYRgiP7lw/IYDi7LGcMkWPWrR+GXZoIedqW0u66wiv//PEZPIu/hlfj83oAAAAA0gBgAAAE62vwOyyMSiH529HV1s3WpYq3HIeRY7L23Yg/kxPxiljOUahqllMt1dxrT0a3GXfftxGUOoxNl7vqAOw4ix13uu4kokDltbftiDWH4d+V16WG424jWIcceXz85/wzco6bWUqoYzDuUqjWN/98lu/+MSe/RVbteGIxSNfcN/2CORFHfhuRzgJKVyOxyORup1OJtNusxuCzQARMXGI04MToxTNmCExULzC4EMahExEOjKgPMHiAw+FjFIeMOBIwwCjCISGQEFhTQHMg0/YznfB1YwGWhLMlzi4xZJpJvGGIILEGeOsYuUgCbiu1pL7SugCAw4MHEFoEuETWCwYxKD5p2mdR1dqwqANIte6ABQBtIiu2QyR2p90nKXNALWWGw0oOsO66gi7HkVPm/sUq2o7PO85UZf2Ge8rZMPdddDLIEXezuLs4xmqu4jluAqWXS6ZjMZppVDUzDrszTkQI19rcPtcch3Gvv+87+Yy//PEZOUsphlZL85kAAAAA0gBgAAAmtlEqtLDNamhqUw87VLKZT3P/yrXZTLaCmciMP++8Du5DEsi7/xt2IYon/d+MwzKo1DVWUwzKo07UpjMMxKHoaiMOw7NSqNUNWlyrX8Na3My3f/adxxKRx4vD7sQ5Mw++9uHIxx/4Dk/f+GpmMuzTRp/pmUvrKo0/1WlhmtGpdlVAJluTS80fPDts0NgiwyMfzQxvMhBUkABgsIGFQ0YOBokAXScbeFqIv7a+q7K7Wuy3CaBqOB4FxxIKQFQW2Kiq0wsPJFhYOgbHcqS4NRWmKFjra+VD1AbB8Km0zSqq3KqKmr/DXJIqbqtMdfLMzXysVtlHSqw0iorXAstbMzMyqqrX/szSSKm6qv/szXqq//DCwsLLX///wzMUq1+qq2qr//s1yHIKQbB9aioqtcMzMzfKqq6kirRRSoGSOy10ADtEIwfcjAykk1aFRqNxOiURNo/K/9GoAI8aDFLjS/9yhgoMTVMTEFNRTMu//OEZOoXBg0+L+4gAIAAA0gBwAAAMTAwVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV//NEZNwFLG8bLCTCZIAAA0gAAAAAVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV//MUZPwAAAH+AAAAAAAAA0gAAAAAVVVV'

# Initialize mixer
pygame.mixer.init()

def play_audio(base64_audio):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(base64.b64decode(base64_audio))
            tmp_path = tmp.name
        sound = pygame.mixer.Sound(tmp_path)
        sound.play()
    except Exception as e:
        print(f"⚠️ Could not play sound: {e}")

# Create folder if not exists
os.makedirs(SAVE_DIR, exist_ok=True)

def trim_image(image_name):
    img = Image.open(image_name)
    original_width, original_height = img.size
    print(f"Original dimensions: {original_width}x{original_height}")
    scale = 150 / min(original_width, original_height)
    if scale >= 1:
        scale = 1
    print(f"Scale factor: {scale}")
    new_width = int(original_width * scale)
    new_height = int(original_height * scale)
    img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    print(f"Resized dimensions: {new_width}x{new_height}")
    left = max((new_width - 150) / 2, 0)
    top = max((new_height - 150) / 2, 0)
    right = min((new_width + 150) / 2, new_width)
    bottom = min((new_height + 150) / 2, new_height)
    print(f"Cropping box: left={left}, top={top}, right={right}, bottom={bottom}")
    img_cropped = img_resized.crop((left, top, right, bottom))
    img_cropped.save(image_name)
    print(f"Image trimmed as {image_name} ✅")

# Get next index
def get_next_index():
    existing = [f for f in os.listdir(SAVE_DIR) if f.startswith(PREFIX) and f.endswith(EXT)]
    numbers = [int(f[len(PREFIX):-len(EXT)]) for f in existing if f[len(PREFIX):-len(EXT)].isdigit()]
    return max(numbers) + 1 if numbers else 0

# Check if URL is probably valid
def is_probably_url(text):
    return text.startswith("http://") or text.startswith("https://")

# Download and save as PNG
def download_and_convert(url, index):
    print(f"⬇️ Downloading image: {url}")
    try:
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()

        content_type = response.headers.get("Content-Type", "")
        if not content_type.startswith("image/"):
            print(f"⚠️ Not an image: {url} (Content-Type: {content_type})")
            play_audio(ERROR_AUDIO_BASE64)
            return

        image = Image.open(BytesIO(response.content)).convert("RGBA")
        output_path = os.path.join(SAVE_DIR, f"{PREFIX}{index}{EXT}")
        image.save(output_path, "PNG")
        trim_image(output_path)
        print(f"💾 Saved: {output_path} ✅")
        play_audio(SUCCESS_AUDIO_BASE64)

    except requests.exceptions.RequestException as e:
        print(f"🚨 Network error: {e}")
        play_audio(ERROR_AUDIO_BASE64)
    except Exception as e:
        print(f"❌ Error processing {url}: {e}")
        play_audio(ERROR_AUDIO_BASE64)

# Clipboard watcher
def monitor_clipboard():
    last_clipboard = pyperclip.paste()
    index = get_next_index()
    print("📋 Monitoring clipboard... (Ctrl+C to exit)")

    while True:
        try:
            current_clipboard = pyperclip.paste()
            if current_clipboard != last_clipboard:
                last_clipboard = current_clipboard
                if is_probably_url(current_clipboard):
                    print(f"🔗 Detected URL: {current_clipboard}")
                    download_and_convert(current_clipboard, index)
                    index += 1
            time.sleep(.5)  # Check clipboard every 500ms
        except KeyboardInterrupt:
            print("\n🛑 Stopped.")
            break
        except Exception as e:
            print(f"⚠️ Unexpected error: {e}")
            play_audio(ERROR_AUDIO_BASE64)

monitor_clipboard()
