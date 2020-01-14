from PIL import Image, ImageDraw, ImageFont
import json

dta = {}

def main(pth):
    with open(pth, 'r') as f:
        dta = json.load(f)
    img = Image.new('RGB', (1920, 1080), color = (255, 255, 255))
    fnt = ImageFont.truetype('fonts/ubuntu.ttf', 45)
    d = ImageDraw.Draw(img)
    d.text((50,50), dta["source"], fill=(0,0,0), font = fnt)
    img.save('img.png')

main("data.json")