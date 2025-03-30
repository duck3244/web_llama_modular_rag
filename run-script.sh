#!/bin/bash

# 필요한 디렉토리 생성
mkdir -p cache vector_db temp models visualizations

# 가상 환경 생성 (선택 사항)
if [ ! -d "venv" ]; then
  echo "가상 환경 생성 중..."
  python -m venv venv
  
  # 운영체제에 따른 활성화 명령
  if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
  else
    source venv/bin/activate
  fi
  
  # 필요한 패키지 설치
  pip install -r requirements.txt
else
  # 운영체제에 따른 활성화 명령
  if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
  else
    source venv/bin/activate
  fi
fi

# Streamlit 앱 실행
echo "Streamlit 앱 시작 중..."
streamlit run app.py
