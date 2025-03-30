@echo off
SETLOCAL

:: 필요한 디렉토리 생성
mkdir cache 2>nul
mkdir vector_db 2>nul
mkdir temp 2>nul
mkdir models 2>nul
mkdir visualizations 2>nul

:: 가상 환경 생성 (선택 사항)
IF NOT EXIST venv (
  echo 가상 환경 생성 중...
  python -m venv venv
  
  :: 가상 환경 활성화
  call venv\Scripts\activate.bat
  
  :: 필요한 패키지 설치
  pip install -r requirements.txt
) ELSE (
  :: 가상 환경 활성화
  call venv\Scripts\activate.bat
)

:: Streamlit 앱 실행
echo Streamlit 앱 시작 중...
streamlit run app.py

ENDLOCAL
