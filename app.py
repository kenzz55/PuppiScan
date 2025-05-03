from flask import Flask, render_template, request, jsonify
import os
import secrets

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
secret_key = secrets.token_hex(16)

@app.route('/')
def index():
    return render_template('index.html')  # (참고) HTML 템플릿이 있을 경우

@app.route('/upload', methods=['POST'])
def upload_image():
    # 1. 텍스트 폼 입력 받기
    breed = request.form.get('breed')
    age = request.form.get('age')
    gender = request.form.get('gender')
    weight = request.form.get('weight')
    neutered = request.form.get('neutered')
    environment = request.form.get('environment')
    condition = request.form.get('condition')
    vulnerability = request.form.get('vulnerability')

    # 2. 이미지 저장
    image = request.files.get('image')
    if image:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
        image.save(filepath)
    else:
        return jsonify({'error': '이미지가 누락되었습니다'}), 400

    # 3. AI 추론 결과 (임시 mock 데이터)
    # result = diagnose_image(filepath)
    inferred_cause = "알레르기성 접촉성 피부염"
    disease = "농포성 여드름"
    tip = "실내 환경 청결 유지와 적절한 샴푸 사용을 권장합니다."
    treatment = "항생제 연고 도포 및 수의사 진료 필요"

    # 4. 출력 데이터 구성
    result = {
        "입력 정보": {
            "견종": breed,
            "나이": age,
            "성별": gender,
            "체중": weight,
            "중성화 여부": neutered,
            "생활 환경": environment,
            "기저 질환": condition,
            "특이 질병 취약 여부": vulnerability
        },
        "추론된 원인 정보": inferred_cause,
        "질병명 (2차 질병)": disease,
        "예방/관리 팁": tip,
        "치료 추천사항": treatment
    }

    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)