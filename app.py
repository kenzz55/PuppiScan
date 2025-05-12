from flask import Flask, render_template, request, redirect, flash
import os
import secrets
from datetime import datetime
from gpt.summary import generate_summary

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = secrets.token_hex(16)  # flash 메시지를 위해 설정

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    # 입력값 받기
    breed = request.form.get('breed')
    age = request.form.get('age')
    gender = request.form.get('gender')
    weight = request.form.get('weight')
    neutered = request.form.get('neutered')
    environment = request.form.get('environment')
    condition = request.form.get('condition')
    vulnerability = request.form.get('special')  # special 필드 이름
    image = request.files.get('image')
    filename = image.filename if image else request.form.get('saved_image')

    # 유효성 검사
    if not all([breed, age, gender, weight, neutered, environment, condition, vulnerability]):
        flash("모든 항목을 입력해 주세요.")
        return render_template('index.html', breed=breed, age=age, gender=gender, weight=weight,
                               neutered=neutered, environment=environment,
                               condition=condition, special=vulnerability)

    if not image or image.filename == '':
        flash("사진을 업로드해 주세요.")
        return render_template('index.html', breed=breed, age=age, gender=gender, weight=weight,
                               neutered=neutered, environment=environment,
                               condition=condition, special=vulnerability)

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
    image.save(filepath)

    # (모형 추론 결과)
    inferred_cause = "알레르기성 접촉성 피부염"
    disease = "농포성 여드름"
    tip = "실내 환경 청결 유지와 적절한 샴푸 사용을 권장합니다."
    treatment = "항생제 연고 도포 및 수의사 진료 필요"

    # 날짜 변수 추가
    today = datetime.now().strftime("%Y-%m-%d")  # 형식: 2025-05-12

    # GPT 기반 summary 생성
    summary = generate_summary(
        breed, age, gender, weight, neutered,
        environment, condition, vulnerability,
        inferred_cause, disease, tip, treatment
    )

    return render_template('report.html',
                           breed=breed,
                           age=age,
                           gender=gender,
                           weight=weight,
                           neutered=neutered,
                           environment=environment,
                           condition=condition,
                           vulnerability=vulnerability,
                           cause=inferred_cause,
                           disease=disease,
                           tip=tip,
                           treatment_breed=treatment,
                           treatment_age=treatment,
                           treatment_gender=treatment,
                           treatment_neutered=treatment,
                           treatment_environment=treatment,
                           treatment_condition=treatment,
                           recommended_meds="피부연고 A",
                           cost1="15,000원",
                           cost2="8,000원",
                           cost3="10,000원",
                           confidence="87%",
                           feature="붉은 반점과 농포",
                           similarity="92%",
                           summary=summary,
                           date_today=today
                           )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
