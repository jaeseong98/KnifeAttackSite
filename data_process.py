from bs4 import BeautifulSoup
import requests
import re
import datetime
from tqdm import tqdm
import os
import pandas as pd
import glob
import openai
from crawl import crawling

def process_data():
    crawling()
    # 경로에 있는 모든 csv 파일을 리스트로 가져옵니다.
    all_csv_files = glob.glob(os.path.join(os.getcwd() + "/data/", "*.csv"))

    # 파일의 마지막 수정 시간을 기준으로 정렬합니다.
    latest_csv_file = max(all_csv_files, key=os.path.getctime)

    # 가장 최근의 csv 파일을 pandas로 읽습니다.
    df_news = pd.read_csv(latest_csv_file)



    # 발급받은 API 키 설정 - 환경변수로 설정

    # openai API 키 인증
    openai.api_key = os.environ.get('OPENAI_API_KEY')

    df_news['link+content'] = df_news['link']+' // '+df_news['content']

    # 결과를 저장할 빈 리스트
    answer_list = []
    MAX_TOKENS = 4097
    # df['content']에서 0부터 10개까지의 텍스트를 반복하여 처리
    for text in df_news['link+content'][:20]:  # 여기서 10은 0부터 9번째 텍스트까지 가져오겠다는 의미입니다.
        print(len(text))
        if len(text) >= MAX_TOKENS-500:  # 500은 query와 기타 메시지에 대한 여유 토큰 수입니다.
            continue
        else:
            # 모델 - GPT 3.5 Turbo 선택
            model = "gpt-3.5-turbo"

            # 질문 작성하기
            query = f"이 뉴스 본문에서 언급된 칼부림예고에 대한 지역과 시간, 뉴스 링크, 요약글 , 범죄자에 대한 신상을 자세하게 뽑아줘. 이때, 지역: OO역 , 시간: 00일 00시 ,뉴스 링크 : https://~~, 요약글: ,범죄자 정보: 00세 A씨 이런 형식으로 꼭 맞춰줘. 만약 여러개의 사건이 있으면 하나의 사건만 뽑아줘 그리고 각각의 사건에서 요약글에 지하철역과 같은 장소가 있다면 지역에 넣어줘.범죄자 정보가 없으면 신원 미상으로 해줘.아래는 본문이야 \n {text}" 
            # query = f"Please select the region, time, crime trailer message, and details about the offender for the stabbing report mentioned in this news article. Please use the following format: area: OO station, time: 00:00 on the 00th, crime trailer message : ~~ , offender information: 00-year-old A, etc. If there are multiple cases, select only one case, and in each case, if the crime trailer has a location such as a subway station, put it in the region.Below is the text \n {text}"
            
            # 메시지 설정하기
            messages = [
                    {"role": "system", "content": "please say simple"},
                    {"role": "user", "content": query}
            ]

            # ChatGPT API 호출하기
            response = openai.ChatCompletion.create(
                model=model,
                messages=messages
            )
            answer = response['choices'][0]['message']['content']

            answer_list.append(answer)
    print(answer_list)
    text = "@".join(answer_list)
    text = text.replace("\n"," ")

    data = []

    # 데이터 분할 및 저장
    cases = re.split('지역: ', text)[1:]
    for case in cases:
        elements = re.split('(시간: |뉴스 링크: |요약글: |범죄자 정보: )', case)
        try:
            location = elements[0].strip()
            time = elements[2].strip()
            link = elements[4].strip()
            message = elements[6].strip()
            criminal_info = elements[8].strip()
            if "@" in criminal_info:
                temp_info = criminal_info.split("@")[0].strip()  # '@' 문자 이후의 텍스트 제거
                criminal_info = temp_info

            data.append([location, time, link, message, criminal_info])
        except IndexError:  # 형식에 맞지 않는 경우
            print(f"Error in parsing: {case}")

    # 데이터프레임 생성
    df = pd.DataFrame(data, columns=['Location', 'Time', 'Link', 'Text', 'Criminal Info'])
    df = df.head(10)
    df = df.replace(",","",regex=True)

    import datetime
    now = datetime.datetime.now() 
    df.to_csv('data/final/{}_{}.csv'.format('final_data',now.strftime('%Y%m%d_%H시%M분%S초')),encoding='utf-8-sig',index=False)

    import datetime
    now = datetime.datetime.now() 
    answer_list = pd.DataFrame(answer_list, columns = ['gpt_answer'])
    answer_list.to_csv('data/gpt/{}_{}.csv'.format('gpt_answer_list',now.strftime('%Y%m%d_%H시%M분%S초')),encoding='utf-8-sig',index=False)

    return df