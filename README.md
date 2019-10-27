## Naver Image Crawler 프로젝트 개요
이 프로젝트는 머신러닝, 딥러닝 연구자 또는 학습자들이 네이버(Naver)에서 대량의 이미지를 수집할 수 있도록 돕기 위해 만들어졌습니다.
네이버 서버에 무리가 가지 않도록 적당한 간격을 두고 실행해주시기를 당부드리며 많은 연구자와 학습자들을 대신해 네이버에 감사드립니다.

## 프로젝트 설명
수집을 원하는 기간(년, 월)을 지정하여 실행하면 해당 월에 등록된 이미지들을 일일 단위로 검색하여 수집함으로써 대량의 이미지 데이터 수집이 가능합니다.

## 프로젝트 세팅
1. 크롬을 설치합니다.
2. 자신의 운영체제에 맞는 크롬 드라이버를 설치해 ./driver/ 경로에 넣습니다.
3. 아래 명령어로 필요한 패키지들을 설치합니다.
```
pip3 install -r requirements.txt
```

## 프로젝트 실행
1. crawler.py에 있는 NaverImageCrawler 클래스 인스턴트를 생성합니다.
2. set_keywords() 메서드의 매개변수로 크롤링할 키워드들을 전달합니다.
3. execute() 메서드로 년, 월, 일별 목표 개수를 설정해 크롤링을 실행합니다.
4. crawler.py 스크립트를 실행하면 아래 샘플 코드를 바로 실행해볼 수 있습니다.
```
crawler = NaverImageCrawler()
crawler.set_keywords('강아지', '고양이')
crawler.execute(year=2019, month=9, number_by_date=100)
```
위 코드를 실행하면 2019년 9월 1일부터 9월 30일까지 '강아지', '고양이' 이미지를 일자별로 100개씩 수집합니다.
즉, 강아지 이미지 최대 3,000개와 고양이 이미지 최대 3,000개로 총 6,000개까지 수집될 수 있습니다.
수집된 이미지는 ./images/ 디렉토리에 지정된 키워드별로 나뉘어 저장됩니다.