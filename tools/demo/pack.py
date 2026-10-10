# tools/demo/out 의 사진 → assets/demo.json(사진 보관함용) + assets/samples2.json(앱 기본 예시 사진, 얼굴·실제 리뷰 없는 것으로 교체)
import json, base64, io
from pathlib import Path
from PIL import Image
root = Path(__file__).resolve().parents[2]; out = root/'tools'/'demo'/'out'
def uri(p): return ('data:image/png;base64,' if p.suffix=='.png' else 'data:image/jpeg;base64,') + base64.b64encode(p.read_bytes()).decode()
LIB = [('green','food','초록국수'),('beef','food','홍직화 우삼겹 쌀국수'),('beef2','food','쌀국수 클로즈업'),('lift','food','면 한 젓가락'),
       ('spread','food','한 상 차림'),('shrimp','food','새우 사이드'),('side','food','튀김 사이드'),('bowls','store','비워진 그릇들'),
       ('store','store','매장 입구'),('chorok','cut','초록이 누끼')]
photos = [{'id':'demo-'+k,'cat':c,'name':n,'src':uri(out/(k+('.png' if k=='chorok' else '.jpg')))} for k,c,n in LIB]
shots = {f'review{i}': uri(out/f'review{i}.jpg') for i in range(1,5)}
(root/'assets'/'demo.json').write_text(json.dumps({'photos':photos,'shots':shots},ensure_ascii=False),encoding='utf-8')
# 기본 예시 사진: 같은 사진이라도 바이트가 달라야 '예시 사진'으로 오인되지 않음 → 760px / 품질 72로 다시 인코딩
def small(p, edge=760, q=72):
    im = Image.open(p).convert('RGB'); im.thumbnail((edge,edge)); b = io.BytesIO(); im.save(b,'JPEG',quality=q,optimize=True)
    return 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()
M = {'bowl':'green','store':'store','chef':'spread','dish':'bowls','cbg1':'beef','cbg2':'lift','cbg3':'beef2',
     'shot1':'review1','shot2':'review2','shot3':'review3','shot4':'review4'}
(root/'assets'/'samples2.json').write_text(json.dumps({k:small(out/(v+'.jpg')) for k,v in M.items()}),encoding='utf-8')
print('demo.json', (root/'assets'/'demo.json').stat().st_size, 'samples2.json', (root/'assets'/'samples2.json').stat().st_size)
