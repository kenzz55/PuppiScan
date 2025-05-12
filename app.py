from flask import Flask, render_template, request, redirect, flash
import os
import secrets
from datetime import datetime

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
    condition = request.form.get('condition')

    plastic_dish = request.form.get('plastic_dish')
    season = request.form.get('season')
    bath_cycle = request.form.get('bath_cycle')
    walk_habit = request.form.get('walk_habit')
    sun_exposure = request.form.get('sun_exposure')
    housing = request.form.get('housing')
    toy_wash_cycle = request.form.get('toy_wash_cycle')
    image = request.files.get('image')

    # 검증 목록에 새 필드 전부 추가!
    if not all([
        breed, age, gender, weight, neutered, condition,
        plastic_dish, season, bath_cycle, walk_habit,
        sun_exposure, housing, toy_wash_cycle
    ]):
        flash("모든 항목을 입력해 주세요.")
        return render_template('index.html',
                               breed=breed, age=age, gender=gender, weight=weight,
                               neutered=neutered, condition=condition,
                               plastic_dish=plastic_dish, season=season,
                               bath_cycle=bath_cycle, walk_habit=walk_habit,
                               sun_exposure=sun_exposure, housing=housing,
                               toy_wash_cycle=toy_wash_cycle
                               )
    # 이미지 유효성 검사
    if not image or image.filename == '':
        flash("사진을 업로드해 주세요.")
        return render_template('index.html',
                               breed=breed, age=age, gender=gender, weight=weight,
                               neutered=neutered, condition=condition,
                               plastic_dish=plastic_dish, season=season,
                               bath_cycle=bath_cycle, walk_habit=walk_habit,
                               sun_exposure=sun_exposure, housing=housing,
                               toy_wash_cycle=toy_wash_cycle)
    # 파일 저장 및 url 생성
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
    image.save(filepath)

    # (모형 추론 결과)
    inferred_cause = "알레르기성 접촉성 피부염"
    disease = "농포성 여드름"
    tip = "실내 환경 청결 유지와 적절한 샴푸 사용을 권장합니다."
    treatment = "항생제 연고 도포 및 수의사 진료 필요"

    # 날짜 변수 추가
    today = datetime.now().strftime("%Y-%m-%d")  # 형식: 2025-05-12

    return render_template('report.html',
                           breed=breed,
                           age=age,
                           gender=gender,
                           weight=weight,
                           neutered=neutered,
                           plastic_dish=plastic_dish,
                           season=season,
                           bath_cycle=bath_cycle,
                           walk_habit=walk_habit,
                           sun_exposure=sun_exposure,
                           housing=housing,
                           toy_wash_cycle=toy_wash_cycle,
                           condition=condition,
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
                           summary="농포성 여드름 가능성이 높으며 빠른 치료가 권장됩니다.",
                           date_today=today  # ✅ 여기에 추가
                           )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
