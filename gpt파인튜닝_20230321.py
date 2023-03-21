import json
import openai

# API Key 설정
openai.api_key = ""

# 대화 생성
def generate_agent_response(conversation):
    prompt = f'Summary: {conversation["summary"]}\n\nSpecific information:{conversation["specific_information"]}\n\n###\n\n'

    for msg in conversation["messages"]:
        prompt += f'{msg["role"]}: {msg["content"]}\n'

    prompt += 'Agent:'
    
    response = openai.Completion.create(
        engine="davinci:ft-personal-2023-03-20-04-16-11",
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=["\n"],
        temperature=0.5
    )

    return response.choices[0].text.strip()

# 대화 요약 및 중요한 정보 생성
def generate_summary_and_specific_info(conversation):
    messages = "\n".join([msg["content"] for msg in conversation["messages"]])
    
    summary_prompt = f"Please provide a summary of the following conversation in korean:\n\n{messages}"
    summary_response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=summary_prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5
    )
    
    summary = summary_response.choices[0].text.strip()

    specific_info_prompt = f"Please extract the specific information from the following conversation in korean:\n\n{messages}"
    specific_info_response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=specific_info_prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5
    )
    
    specific_information = specific_info_response.choices[0].text.strip()

    return summary, specific_information

# 대화 초기화 함수
def initialize_conversation():
    return {
        "summary": "",
        "specific_information": "",
        "messages": [
            {
                "role": "Agent",
                "content": "무엇을 도와 드릴까요 경희대학교 행정실 안결입니다"
            }
        ]
    }

# 대화 불러오기
def load_conversation(filename):
    with open(filename, "r", encoding='utf-8') as f:
        return json.load(f)

# 대화 저장하기
def save_conversation(conversation, filename):
    with open(filename, "w", encoding='utf-8') as f:
        json.dump(conversation, f, indent=2)

# 새로운 대화 시작 및 대화 불러오기
conversation_counter = 1

while True:
    print("\n새로운 대화를 시작합니다.\n")
    conversation = initialize_conversation()
    conversation_filename = f"conversation_{conversation_counter}.json"

    while True:
        # 사용자 질문 입력
        user_question = input("Customer: ")

        # 대화 종료 명령
        if user_question.lower() in ["exit", "quit", "종료"]:
            save_conversation(conversation, conversation_filename)
            conversation_counter += 1
            break

        # 대화에 사용자 질문 추가
        conversation["messages"].append({"role": "Customer", "content": user_question})

        # 요약 및 중요한 정보 업데이트
        conversation["summary"], conversation["specific_information"] = generate_summary_and_specific_info(conversation)
        
        # 에이전트 응답 생성
        agent_response = generate_agent_response(conversation)
        conversation["messages"].append({"role": "Agent", "content": agent_response})

        # 에이전트 응답 출력
        print(f"Agent: {agent_response}")
       
