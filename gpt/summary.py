import openai
from dotenv import load_dotenv
load_dotenv()

import os

def generate_summary(breed, age, gender, weight, neutered, environment, condition, vulnerability, cause, disease, tip, treatment):
    prompt = (
        f"다음 반려견의 건강 정보와 진단 정보를 바탕으로, 보호자에게 전달하는 수의사의 요약 설명을 1~2문장으로 작성해줘.\n"
        f"전문 용어는 가능한 쉬운 말로 바꾸고, 진정성 있게 설명해줘.\n"
        f"- 증상: {condition}\n"
        f"- 취약 요인: {vulnerability}\n"
        f"- 추정 원인: {cause}\n"
        f"- 질병명: {disease}\n"
        f"- 팁: {tip}\n"
        f"- 치료법: {treatment}\n"
        f"\n"
        f"예시 출력: '현재 증상은 {disease}로 의심되며, 원인으로는 {cause}가 추정됩니다. 치료와 관리를 위해 {treatment}를 권장드리며, {tip} 또한 함께 신경 써주세요.'\n"
        f"\n"   
        f"요약:"
    )

    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "너는 동물 병원 피부과 수의사 역할을 하는 AI야."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=100
    )
    return response.choices[0].message.content.strip()