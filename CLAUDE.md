# 김씨육면 디자인 메이커

김씨육면(@kimsnoodle) 인스타 콘텐츠를 만드는 웹 도구. 틀(레이아웃·폰트·색 규칙)은 고정하고 사진·문구만 바꿔 넣는다.
사용자는 졍(비개발자, 반말로 쉽게 설명). 목업은 PNG 이미지 한 장으로 보여준다.

## 파일 구조
- `src.html` — 실제 코드(HTML·CSS·JS 전부). **수정은 여기서만** 한다.
- `assets/fonts.json` · `samples2.json` · `logo.json` — 폰트·예시 사진·로고(base64). 직접 고치지 않는다.
- `assets/logo_mark.png`, `logo_text.png` — 로고 원본(그릇 그림 / 金氏肉麵 글자, 투명 PNG).
- `assets/chorok.png` — 캐릭터 초록이 누끼 원본. `chorok_small.png`는 상단 제목 옆·브라우저 탭 아이콘용(build.py가 넣음).
- `build.py` — `src.html` + assets → `carousel-maker.html`(한 파일). **src.html을 고친 뒤 항상 `python3 build.py` 실행.**
- `carousel-maker.html` — 크롬에서 여는 완성 파일. 직접 고치지 않는다.
- `dist/index.html` — build.py가 같이 만드는 버셀 배포용 파일(깃에는 안 올림).

## 배포 (버셀)
- 주소: https://ksn-maker-849fbf.vercel.app (공개, 잠금 없음. 데이터는 각자 브라우저에 저장돼 공유 안 됨)
- 다시 올리기: `python3 build.py` → `cd dist && npx vercel@latest deploy --prod --yes`
- dist 폴더만 올린다. photos/·backup/은 절대 올리지 않는다.

## 화면 구성 (탭 5개)
1. 콘텐츠 플래너 — 달력/목록. 노션 연결 없이 브라우저에만 저장(localStorage `ksn-plan-cache`).
2. 시놉시스 보관함 — 콘텐츠 카드(아이디어 → 문구 완성 → 디자인 중 → 완성).
3. 사진 보관함 — 사진 여러 장 올려두고 분류(음식·매장·누끼·기타, 투명 PNG는 자동 누끼). 디자인 작업의 '보관함에서 고르기'로 장에 넣음. IndexedDB `lib:*`, 백업 JSON의 `lib`에 포함.
4. 디자인 작업 — 왼쪽 장 목록 / 가운데 캔버스 미리보기(1080×1440) / 오른쪽 편집.
5. 완성 아카이브 — 완성본, ZIP 다시 받기, 업로드 표시, 보관함 백업 받기/불러오기(JSON, 플래너 포함).
저장: 메타데이터 localStorage `ksn-design-v4`, 사진·영상 IndexedDB `ksn-carousel`.

## 템플릿 (확정)
- A 스토리 · B 질문·후기 · C 리뷰 — 캐러셀(표지/본문/마지막 장)
- D 단일 이미지 — d1 매거진 커버 / d2 프레임 에디토리얼 / d3 미니멀 캡션 (메뉴 소개·신메뉴, 영업시간·가격 넣지 않음, 글 작게, 사진이 주인공, 사진 채도는 건드리지 않음)
- E 시리즈 — e1 밝은 바탕+누끼 / e2 진한 바탕+누끼 / e3 사진+영문 한 줄. 투명 PNG(누끼)면 음식만 놓고, 일반 사진은 동그랗게 잘라 넣음.

## 디자인 규칙 (확정, 바꾸려면 졍에게 먼저 물어보기)
- 크기 3:4 (1080×1440). 9:16·A4는 아직 비활성.
- 폰트: 한글 큰 제목 Pretendard ExtraBold~Black / 감성 본문 마루 부리 / 정보·가격·라벨 Pretendard / 영문 제목·숫자 Newsreader / 브랜드 이름 KIMSNOODLE은 Libre Caslon만 / 고운바탕은 B 마지막 장 큰 제목에만. Young Serif·Noto Sans 쓰지 않음.
- 로고: 金氏肉麵 한자는 글꼴이 아니라 로고 이미지(assets/logo_*.png)로 넣는다.
- 템플릿 A 머리(표지·본문·마지막 장 왼쪽 위): 초록 네모+로고 대신 캐릭터 초록이(assets/chorok_mid.png)를 넣는다.
- 글자 위치(안전 영역): 모든 글자는 위아래 가장자리에서 60px 이상 안쪽, 큰 제목은 아래에서 170px 이상, 양옆 50px 이상.
- 색: A 딥그린 #2F5130(라임 없음), B 검정+라임 #C6F03E, D 기본 글자 검정. 색은 편집 칸 '색 바꾸기'에서 바꿈.
- 글씨 크기는 전체적으로 3px 줄인 상태(TXT_DOWN=3).

## 작업 방식
- 고치기 전에 무엇을 바꿀지 쉽게 설명하고, 고친 뒤 build.py 실행 → 크롬에서 확인할 수 있게 안내.
- 큰 변경 전에는 git 커밋으로 되돌릴 지점을 남긴다.

## 다음에 하고 싶은 것
- 로컬 사진 폴더를 지정하면 누끼(rembg 등)까지 자동으로 따서 E 시리즈/D 이미지를 만들어 폴더에 저장.
- 사진 색감 보정 프리셋(밝기·대비·채도·색온도) — 졍이 매장 사진 2~3장 + 레퍼런스 1장 줄 예정.
- 9:16 스토리, A4 매장 출력 크기 열기.
- 폰에서도 쓰고 싶어지면 저장소(Supabase 등) + 배포(Vercel).

## 폴더 안 도구
- `열기.command` — 크롬으로 carousel-maker.html 열기 (Mac).
- `tools/cutout.py` — photos/inbox 사진 → photos/cutout 누끼 PNG (rembg isnet-general-use). 처음엔 `pip3 install "rembg[cpu]" pillow` 필요. 졍이 "누끼 따줘"라고 하면 이걸 실행한다.
- `backup/` — 아티팩트 메이커에서 받은 보관함 백업 JSON 보관.
- `사용법.md` — 졍용 쉬운 안내.

## 처음 세션에서 할 일 (아직 안 했으면)
1. `git init` 후 첫 커밋 ("아티팩트에서 옮겨온 v2.3").
2. `.gitignore`에 `photos/`, `backup/`, `.DS_Store` 추가 (사진·백업은 커밋하지 않음).
3. rembg 설치 확인.
