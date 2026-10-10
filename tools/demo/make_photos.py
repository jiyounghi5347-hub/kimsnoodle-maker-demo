# 데모용 사진 만들기: 얼굴·개인정보 없는 사진만 골라 1080px / JPEG 80으로 줄이고,
# 가짜 리뷰 캡처(지어낸 문구)를 그려서 demo_src/ 에 저장한다.
# 실행: python3 tools/demo/make_photos.py <원본 이미지 폴더>
import sys, io, json, base64
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont

src = Path(sys.argv[1]); root = Path(__file__).resolve().parents[2]
out = root/'tools'/'demo'/'out'; out.mkdir(parents=True, exist_ok=True)

def fit(im, edge=1080):
    im = im.copy(); im.thumbnail((edge, edge), Image.LANCZOS); return im
def jpg(im, name, q=80):
    fit(im).convert('RGB').save(out/name, 'JPEG', quality=q, optimize=True, progressive=True)

O = lambda n: Image.open(src/n)
jpg(O('sample_4d0c6c93.jpg'), 'green.jpg')        # 초록국수
jpg(O('sample_193e2c02.jpg'), 'beef.jpg')         # 홍직화 우삼겹 쌀국수
jpg(O('sample_ca9b76d2.jpg'), 'beef2.jpg')
jpg(O('sample_6497aa74.jpg'), 'lift.jpg')         # 면 들어올린 컷
spread = O('media_695f17cd.jpg'); jpg(spread, 'spread.jpg')  # 한 상
w, h = spread.size
jpg(spread.crop((int(w*.30), 0, w, int(h*.40))), 'shrimp.jpg')          # 새우 사이드
jpg(spread.crop((0, int(h*.26), int(w*.62), int(h*.66))), 'side.jpg')   # 튀김·소스
jpg(O('sample_8de4b610.jpg'), 'bowls.jpg')        # 비워진 그릇들
# 매장 외관: 가운데 걸린 현수막(사람 그림)을 흐리게
st = O('s2_store.jpg').convert('RGB'); sw, sh = st.size
box = (int(sw*.38), int(sh*.40), int(sw*.73), sh)
st.paste(st.crop(box).filter(ImageFilter.GaussianBlur(28)), box[:2]); jpg(st, 'store.jpg')
# 초록이 누끼 (투명 PNG 유지)
ch = Image.open(root/'assets'/'chorok.png'); ch.thumbnail((800, 800), Image.LANCZOS)
ch.save(out/'chorok.png', optimize=True)

# 가짜 리뷰 캡처 4장 — 문구는 전부 지어낸 것, 닉네임은 가림 처리 모양
F = '/System/Library/Fonts/AppleSDGothicNeo.ttc'
def font(sz, bold=False): return ImageFont.truetype(F, sz, index=6 if bold else 0)
def wrap(d, text, f, maxw):
    lines = []
    for para in text.split('\n'):
        cur = ''
        for ch_ in para:
            if d.textlength(cur+ch_, font=f) > maxw: lines.append(cur); cur = ch_
            else: cur += ch_
        lines.append(cur)
    return lines
REV = [
  ('맛*** 님', '★★★★★', '국물이 진짜 초록색이라 놀랐는데\n한 입 먹고 더 놀랐어요. 시금치 향이\n은은하고 하나도 안 느끼해요.\n다음엔 친구 데리고 올게요!', '초록국수 · 새우튀김'),
  ('국***러버 님', '★★★★★', '하루 40그릇이라 해서 일찍 갔어요.\n고기가 정말 넉넉하고 면이 부드러워요.\n왜 줄 서는지 알겠네요 :)', '홍직화 우삼겹 쌀국수'),
  ('민락*** 님', '★★★★★', '배달로 시켰는데 국물이 안 식고 왔어요.\n포장이 꼼꼼해서 감동.\n아이들도 국물까지 다 먹었어요.', '초록국수 2 · 사이드'),
  ('동네***객 님', '★★★★★', '작은 가게인데 한 그릇에 정성이 보여요.\n사장님이 국물 리필도 먼저 물어봐주시고\n단골 될 것 같아요.', '홍직화 우삼겹 쌀국수'),
]
for i, (who, star, body, menu) in enumerate(REV, 1):
    W_, H_ = 600, 820; im = Image.new('RGB', (W_, H_), '#FFFFFF'); d = ImageDraw.Draw(im)
    d.rectangle((0, 0, W_, 64), fill='#F6F6F6'); d.text((24, 18), '리뷰', font=font(26, True), fill='#111')
    d.ellipse((24, 92, 76, 144), fill='#DDE7D6'); d.text((92, 96), who, font=font(24, True), fill='#222')
    d.text((92, 128), star + '  2026.' + ['09.12','09.21','09.28','10.03'][i-1], font=font(20), fill='#F2A100')
    y = 176
    # 음식 사진 자리 (데모 사진 썸네일)
    th = Image.open(out/['green.jpg','beef.jpg','spread.jpg','beef2.jpg'][i-1]).convert('RGB')
    th = th.resize((552, int(552*th.height/th.width))).crop((0, 0, 552, 300)); im.paste(th, (24, y)); y += 320
    f = font(24)
    for ln in wrap(d, body, f, 552): d.text((24, y), ln, font=f, fill='#222'); y += 36
    y += 10; d.text((24, y), '주문메뉴  ' + menu, font=font(19), fill='#888')
    d.text((24, H_-40), '※ 데모용으로 지어낸 리뷰예요', font=font(17), fill='#AAA')
    im.save(out/f'review{i}.jpg', 'JPEG', quality=82)
print('done', sorted(p.name for p in out.iterdir()))
