"""음식 사진 누끼 따기
photos/inbox 에 사진을 넣고 실행하면 photos/cutout 에 배경 없는 PNG가 생겨요.
처음 한 번: pip3 install "rembg[cpu]" pillow
실행: python3 tools/cutout.py
"""
from pathlib import Path
from rembg import remove, new_session
from PIL import Image, ImageOps

root = Path(__file__).resolve().parent.parent
src, dst = root/'photos'/'inbox', root/'photos'/'cutout'
dst.mkdir(parents=True, exist_ok=True)
session = new_session('isnet-general-use')
files = [p for p in sorted(src.iterdir()) if p.suffix.lower() in ('.jpg', '.jpeg', '.png', '.heic', '.webp')]
if not files:
    print('photos/inbox 폴더에 사진이 없어요.')
for p in files:
    out = dst/(p.stem + '.png')
    if out.exists():
        print('건너뜀(이미 있음):', out.name); continue
    im = ImageOps.exif_transpose(Image.open(p)).convert('RGB')
    im.thumbnail((2000, 2000))
    cut = remove(im, session=session)
    bbox = cut.getbbox()
    if bbox: cut = cut.crop(bbox)
    cut.save(out)
    print('누끼 완료:', out.name)
