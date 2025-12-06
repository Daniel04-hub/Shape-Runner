from PIL import Image, ImageDraw
import wave
import math
import struct
import os

def create_image(filename, color, shape='rect'):
    img = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    if shape == 'rect':
        draw.rectangle([0, 0, 64, 64], fill=color)
    elif shape == 'circle':
        draw.ellipse([0, 0, 64, 64], fill=color)
    elif shape == 'triangle':
        draw.polygon([(32, 0), (0, 64), (64, 64)], fill=color)
    img.save(filename)
    print(f"Created {filename}")

def create_sound(filename, frequency=440, duration=0.1):
    # simple sine wave
    sample_rate = 44100
    n_samples = int(sample_rate * duration)
    
    with wave.open(filename, 'w') as obj:
        obj.setnchannels(1) # mono
        obj.setsampwidth(2) # 2 bytes
        obj.setframerate(sample_rate)
        
        for i in range(n_samples):
            value = int(32767.0 * math.sin(2.0 * math.pi * frequency * i / sample_rate))
            data = struct.pack('<h', value)
            obj.writeframesraw(data)
    print(f"Created {filename}")

if __name__ == "__main__":
    if not os.path.exists('assets'):
        os.makedirs('assets')

    # Player: Blue square
    create_image('assets/player.png', (50, 50, 255, 255), 'rect')
    
    # Coin: Yellow circle
    create_image('assets/coin.png', (255, 215, 0, 255), 'circle')
    
    # Wall: Gray square
    create_image('assets/wall.png', (128, 128, 128, 255), 'rect')
    
    # Enemy: Red Triangle
    create_image('assets/enemy.png', (255, 50, 50, 255), 'triangle')
    
    # Sounds
    create_sound('assets/coin.wav', 880, 0.1) # High beep
    create_sound('assets/hit.wav', 220, 0.3)  # Low bumped sound
    create_sound('assets/gameover.wav', 300, 1.0) # Longer, clearer sound
