from dotenv import load_dotenv
import os
import pandas as pd
import json
from datetime import datetime

load_dotenv(dotenv_path = 'keys.env')

from openai import OpenAI
openAI_key = os.getenv('OPENAI_KEY')

client = OpenAI(
    api_key = openAI_key
)

df = pd.read_csv('create.csv')

def create_prompt(user_input):
    prompt = (
        "당신은 사용자와의 챗봇 서비스의 일정 관리 역할을 맡고 있습니다.\n"
        "이전 대화에서 일정 생성에 관한 기능이 요구되어, 당신이 호출 되었습니다.\n"
        f"이전 대화의 내용은 {user_input}입니다.\n"
        "당신은 사용자가 제공한 일정 텍스트를 정형화하는 역할을 합니다. 해당 사실은 시스템 내부에서 이루어지는 것이니, 사용자에게 JSON에 대해 언급하지 마세요.\n"
        "만약 일정에 관한 질문이 아닐 시, 친철하게 일정을 물어봐 주세요.(이모티콘도 적극적으로 활용하세요)\n\n"
        "이 입력을 분석하여 텍스트를 구조화하고, JSON 형식으로 반환해 주세요.\n"
        f"'{user_input}'에서 시작 날짜, 시작 시간, 일정 이름이 반드시 필요합니다.\n"
        "만약 시작 시간, 시작 날짜에 대한 정보가 없다면, 사용자에게 시작 시간이 무엇인지 위트있게 물어봐 주세요.\n"
        "입력된 일정에서 종료 시간이 없다면 기본적으로 시작 시간으로부터 1시간 뒤로 간주합니다.\n"
        "날짜와 시간은 현재 시점 기준으로 '내일', '다음 주 월요일' 등 자연어로 표현될 수 있습니다.\n"
        f"현재 시각은 {datetime.now().strftime('%Y-%m-%d %H:%M')}입니다.\n\n"
        "--------데이터 예시--------\n"
        f"{df.to_string(index=False)}\n"
        "------------------------\n\n"
        "입력된 데이터를 아래와 같은 형식으로 JSON으로 반환하세요.\n"
        "JSON으로 반환할 수 있다면, 당신의 대답 그대로 데이터베이스로 보낼 생각입니다."
        "그러니 JSON 형식을 꼭 지켜주세요.\n\n"
        "추가 정보가 필요할 시, 추가정보 요청에 대한 멘트는 위트있게 요청해주세요\n"
        "모든 데이터가 충족되었을 경우, 다음 예시 JSON파일 텍스트만 반환하세요."
        "이외의 텍스트는 출력하지 않습니다.\n"
        "-----------------------출력 예시----------------------\n"
        "{\n"
        "  'date': '2022-10-10',\n"
        "  'start_time': '15:00',\n"
        "  'end_time': '17:00',\n"
        "  'name': '회의'\n"
        "}\n"
        "----------------------------------------------------\n"
    )

    return prompt

def is_json(text):
    try:
        json.loads(text)
    except ValueError as e:
        return False
    return True


def get_gpt_response(prompt):
    message = [
        {'role': 'system', 'content': "당신은 사용자가 제공한 일정 텍스트를 정형화하는 역할을 합니다"},
        {'role': 'user', 'content': prompt},
    ]
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=message,
        max_tokens=150,
        temperature=0.7,
    )

    # GPT 응답을 받음
    gpt = response.choices[0].message.content

    if not is_json(gpt):
        # GPT 응답을 assistant 메시지로 저장
        message.append({'role': 'assistant', 'content': gpt})
        message.append({'role': 'system', 'content': "JSON 조건이 충족되면 JSON형식만 출력하세요."})
        return gpt
    else:
        # JSON 형식일 때 응답 반환
        print(gpt)
        return "일정을 추가했어요!"

# 프롬프트 생성 및 GPT 호출
def run(user_input):
    global prompt
    prompt = create_prompt(user_input)
    return get_gpt_response(prompt)
