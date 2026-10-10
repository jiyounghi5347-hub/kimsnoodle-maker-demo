# src.html + assets → carousel-maker.html (한 파일로 묶기)
# 실행: python3 build.py
from pathlib import Path
d = Path(__file__).parent
s = (d/'src.html').read_text(encoding='utf-8')
for key, f in [('FONTS','fonts.json'),('SAMPLES','samples2.json'),('LOGO','logo.json'),('DEMO','demo.json')]:
    s = s.replace('/*%s*/{}' % key, (d/'assets'/f).read_text(encoding='utf-8'))
import base64
s = s.replace('%%CHOROK_MID%%', 'data:image/png;base64,' + base64.b64encode((d/'assets'/'chorok_mid.png').read_bytes()).decode())
s = s.replace('%%CHOROK%%', 'data:image/png;base64,' + base64.b64encode((d/'assets'/'chorok_small.png').read_bytes()).decode())
(d/'carousel-maker.html').write_text(s, encoding='utf-8')
print('carousel-maker.html 만들었어요')

# 버셀 배포용: dist/ 폴더에는 완성 파일 하나만 (사진·백업은 절대 안 올라감)
(d/'dist').mkdir(exist_ok=True)
(d/'dist'/'index.html').write_text(s, encoding='utf-8')
