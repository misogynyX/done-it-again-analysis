# done-it-again-analysis

https://again.misogynyx.com 에서 사용할 데이터를 만들어내는 코드.

## 데이터 흐름

1. https://github.com/misogynyx/news-crawler 에서 전체 뉴스 데이터를 수집하여
   S3에 업로드
2. https://github.com/misogynyx/done-it-again-analysis 에서는
   `news-crawler`에서 수집한 데잍처 중 최근 6개월 데이터만 받아서 분석하고
   그 결과를 다시 S3에 업로드
3. https://github.com/misogynyx/done-it-again 에서는 `done-it-again-analysis`의
   분석 결과를 S3에서 받아서 정적 웹사이트를 생성

## 개발하기

Python 3.8과 [poetry](https://python-poetry.org)를 설치해주세요. [pyenv](https://github.com/pyenv/pyenv)를 쓴다면 아래와 같이 초기화하시면 됩니다.

```
# 프로젝트 디렉토리로 이동하기
cd done-it-again-analysis
# 'done-it-again-analysis'라는 이름으로 가상환경 만들기
pyenv virtualenv 3.8.2 done-it-again-analysis
# 이 디렉토리에서는 자동으로 'done-it-again-analysis' 가상환경을 사용하도록 설정하기
pyenv local done-it-again-analysis
# poetry 설치하기
pip install poetry
# 프로젝트 라이브러리 설치하기
poetry install
```

단위 테스트는 이렇게 실행하세요.

```
# 테스트 1회 실행하기
pytest
# 코드가 수정되면 자동으로 테스트가 실행되도록 하기
ptw
```

