"""Original geometric v2 fixture, no character art. Requires Pillow."""
from pathlib import Path
import sys
from PIL import Image, ImageDraw
p=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name('fixture-v2.png')
if p.exists():raise SystemExit('Refusing to overwrite existing fixture')
im=Image.new('RGBA',(1536,2288));d=ImageDraw.Draw(im)
for row,n in enumerate([6,8,8,4,5,8,6,6,6,8,8]):
    for col in range(n):
        x,y=col*192,row*208
        d.rectangle((x+35+col*3,y+50,x+105+col*3,y+150),fill=(40+row*18,100+col*15,210,255))
        d.text((x+40,y+60),f'{row}:{col}',fill='white')
im.save(p);print(p)
