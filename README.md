# done-it-again-analysis

https://again.misogynyx.com 에서 사용할 데이터를 만들어내는 코드.

## 데이터 흐름

1. https://github.com/misogynyx/news 에서 전체 뉴스 데이터를 수집하여 S3에 업로드
2. 이 저장소에서는 S3에서 최근 6개월 데이터만 받아서 분석하고 그 결과를 다시 S3에 업로드
3. https://github.com/misogynyx/done-it-again 에서는 이 저장소의 분석 결과를 S3에앗
   받아서 정적 웹사이트를 생성

