#!/bin/bash
# 두 번 클릭하면 디자인 메이커가 열려요 (크롬이 있으면 크롬, 없으면 기본 브라우저)
F="$(cd "$(dirname "$0")" && pwd)/carousel-maker.html"
open -a "Google Chrome" "$F" 2>/dev/null || open "$F"
