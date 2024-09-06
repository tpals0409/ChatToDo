from dotenv import load_dotenv
import os

message = []
load_dotenv(dotenv_path = 'keys.env')

from openai import OpenAI
openAI_key = os.getenv('OPENAI_KEY')

client = OpenAI(
    api_key = openAI_key
)

categories = ['생성', '조회', '수정', '삭제']
category = "NONE"

prompt = (
    "당신은 사용자와의 챗봇 서비스의 일정 관리 역할을 맡고 있습니다.\n"
    "당신은 사용자가 제공한 일정 텍스트에서 해당 기능으로의 접근을 위해 카테고리를 분류하는 역할입니다.\n"
    "만약 일정에 관한 질문이 아닐 시, 친철하게 일정을 물어봐 주세요.(이모티콘도 적극적으로 활용하세요)\n\n"
    f"당신이 분류할 카테고리 목록은 {categories}입니다.\n"
    f"카테고리가 분류되었다면, 다른 텍스트 없이 카테고리명만 출력하세요.\n"
    "-----------------------출력 예시----------------------\n"
    "생성"
)
init_message = [
        {'role': 'system', 'content': "당신은 사용자가 제공한 일정의 카테고리를 구분하는 역할을 합니다"},
        {'role': 'user', 'content': prompt},
    ]
def get_gpt_response(user_input):
    global message
    message.append({'role': 'user', 'content': user_input})
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=init_message + message,
        max_tokens=50,
        temperature=0.7,
    )
    gpt = response.choices[0].message.content
    if gpt not in categories:
        message.append({'role': 'user', 'content': user_input})
        message.append({'role': 'assistant', 'content': gpt})
        message.append({'role': 'system', 'content': "사용자 응답에서 카테고리를 분류하세요. 카테고리가 분류되었다면, 다른 텍스트 없이 카테고리명만 출력하세요."})
        return gpt, "NONE"
    else:
        return message, gpt
def run(user_input):
    category, gpt_response = get_gpt_response(user_input)
    return category, gpt_response