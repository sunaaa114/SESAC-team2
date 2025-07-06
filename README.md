# SESAC-team2
- 새싹 청년취업사관학교 도봉캠퍼스 Python 데이터분석 및 AI/딥러닝 Full PKG 개발과정 1기
- 팀명 : 2렇게잘하조
## 팀원 구성
| 조선아 | 한승아 |
|:---:|:---:|
|<a href='https://github.com/sunnaaa114'> <img src='https://github.com/suusuu00/SESAC-team2/assets/124228791/43413408-df69-4377-b599-a0396aad71d1' width='300'> <br> @sunaaa114 </a> | <a href='https://github.com/xloor0219'> <img src='https://github.com/suusuu00/SESAC-team2/assets/124228791/a7bc9554-fa4a-4705-a3a6-d1c05d897cc4' width='300'> <br> @xloor0219 </a> |

## 목차
1. [약 정보 챗봇](#약-정보-챗봇-pill-information-chat-bot)
    - [프로젝트 소개](#프로젝트-소개)
    - [개발 환경](#개발-환경)
    - [역할 분담](#역할-분담)
2. [코딩 테스트 스터디](#코딩-테스트-스터디)

# 약 정보 챗봇 (pill information chat-bot)
<p align='center'>
<img src='https://github.com/suusuu00/SESAC-team2/assets/124228791/58c1a345-95d7-4b67-9051-d134801d3ee4' width='500'>
</p>

## 프로젝트 소개
- 대화를 통해 원하는 약에 대한 정보를 알려주는 LLM기반 챗봇
- 약의 효과, 성분, 주의사항 등을 알려줌

## 개발 환경
- **URL Crawling** : Selenium
    - 사용 데이터 : 약학정보원 약 정보 데이터 (제품명, 성분, 효과, 주의사항 등)
- **Frontend** : streamlit
- **Backend** : FastAPI
- **RAG** : Langchain
    - Langchain을 이용하여 vectorstore 저장
    - 검색기인 retriever와 LLAMA3 연결하여 질문과 답변 제공
    - Embedding 모델 : `intfloat/multilingual-e5-base`
    - RAG 프롬프트 : `rlm/rag-prompt`
    - LLM : `meta-llama/Meta-Llama-3-8B`
- **서버** : GCP
- **협업 툴**
    - Github : 브랜치를 이용하여 만든 코드 업로드, Merge 등
    - Notion : 프로젝트 목표 및 로드맵 정리를 통해 해야 할 일 확인
    - Slack : 참고 자료 공유

## 역할 분담
### 🍑 조선아
- **Selenium 크롤링**
    - 약 페이지 URL 크롤링 코드 작성
    - 게시물 하나하나 들어가서 현재 URL을 가져오던 것을 게시물 목록 화면에서 바로 URL 가져올 수 있게 바꿈
    - ㄱ~ㅇ으로 시작하는 약 정보 페이지 URL 크롤링
- **Streamlit 프론트엔드**
    - 받은 질문 GCP에 있는 백엔드로 post 보냄
    - 받은 답변 채팅 형태로 화면 출력
    - 백엔드 에러 시 System Error 채팅 형태로 출력
    - 답변 받을 때까지 질문 못하게 막고 로딩 화면 출력
- **FastAPI 백엔드**
    - `'/question/'` post 함수로 질문 받으면 LLAMA3 langchain invoke에 넣어 답변 return
- **Langchain RAG**
    - 전체적인 코드 작성 
    - `SeleniumURLLoader`를 이용하여 약 정보 가져오고 필요없는 정보 제거
    - parent_splitter와 child_splitter를 이용하여 `ParentDocumentRetriever`로 정보를 더 작게 나눌 수 있게 함
    - vectorstore에 저장하는 반복 과정을 함수로 만들어 반복 과정 줄임
    - 8-bit 양자화 `BitsAndBytesConfig` 사용
- **GCP 서버**
    -  OS, CPU, RAM, GPU (Nvidia T4), 하드디스크 등 GCP 서버 환경 설정
    -  GPU, 하드디스크 할당량 받기
    -  더 큰 하드디스크 교체를 위한 스냅샷 백업
    -  방화벽 특정 port를 열어 외부에서 jupyter lab 실행과 외부 프론트엔드에서 보낸 post 요청 받음

### 🍰 한승아
- **Selenium 크롤링**
    - ㅈ~ㅎ으로 시작하는 약 정보 페이지 URL 크롤링
- **Streamlit 프론트엔드**
    - 전체적인 화면 구조 코드 작성
    - 질문 받아 채팅 형태로 화면 출력
- **Langchain RAG**
    - vectorstore를 디스크에 저장할 수 있도록 함
- **GCP 서버**
    -  OS, CPU, RAM, GPU (Nvidia T4), 하드디스크 등 GCP 서버 환경 설정
    -  GPU, 하드디스크 할당량 받기
    -  더 큰 하드디스크 교체를 위한 스냅샷 백업
    -  방화벽 port를 열어 외부에서 jupyter lab 실행과 외부 프론트엔드에서 보낸 post 요청 받음



# 코딩 테스트 스터디
- 책 정보 : 이것이 취업을 위한 코딩 테스트다 with 파이썬 (나동빈)
