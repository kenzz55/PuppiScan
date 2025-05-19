from flask import Flask, render_template, request, redirect, flash, session, jsonify
import os, secrets, threading, uuid
from datetime import datetime
from gpt.summary import generate_summary  # 기존 GPT summary
# 나중에 from ai.image_analysis import analyze_image 이런 식으로 붙이면 됨
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'yolov5'))
from yolov5.run_detect import detect_disease

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 요청 처리 결과 캐시
result_store = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_upload', methods=['POST'])
def start_upload():
    session_id = str(uuid.uuid4())
    session['sid'] = session_id

    form_data = request.form.to_dict()
    image = request.files.get('image')

    # 필수 필드 체크
    required_fields = [
        'breed', 'age', 'gender', 'weight', 'neutered', 'condition',
        'plastic_dish', 'season', 'bath_cycle', 'walk_habit',
        'sun_exposure', 'housing', 'toy_wash_cycle'
    ]

    missing = [field for field in required_fields if not form_data.get(field)]
    if missing or not image or image.filename == '':
        flash("모든 항목을 입력하고 이미지를 업로드해 주세요.")
        return render_template('index.html', **form_data)

    image_path = None
    if image and image.filename != '':
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
        image.save(image_path)

    result_store[session_id] = {"status": "processing"}

    thread = threading.Thread(target=process_request, args=(session_id, form_data, image_path))
    thread.start()

    return render_template('loading.html')

@app.route('/process')
def check_status():
    sid = session.get('sid')
    if not sid or sid not in result_store:
        return jsonify({'status': 'error'})

    status = result_store[sid]['status']
    return jsonify({'status': status})

@app.route('/final_result')
def final_result():
    sid = session.get('sid')
    if not sid or sid not in result_store or result_store[sid]['status'] != 'done':
        return "처리 중이거나 잘못된 접근입니다.", 400

    data = result_store[sid]['data']
    return render_template('report.html', **data)

def process_request(sid, form, image_path):
    breed = form.get('breed')
    age = form.get('age')
    gender = form.get('gender')
    weight = form.get('weight')
    neutered = form.get('neutered')
    condition = form.get('condition')
    plastic_dish = form.get('plastic_dish')
    season = form.get('season')
    bath_cycle = form.get('bath_cycle')
    walk_habit = form.get('walk_habit')
    sun_exposure = form.get('sun_exposure')
    housing = form.get('housing')
    toy_wash_cycle = form.get('toy_wash_cycle')
    # result = run_image_analysis(image_path)  이후 확장
    disease, score = detect_disease(image_path)
    print(score)
    print(disease)
    # result = {
    #   "inferred_cause": "진드기 감염",
    #   "disease": "세균성 피부염",
    #   "tip": "진드기 예방제를 사용하고 자주 목욕시켜 주세요",
    #   "treatment": "항생제 처방 필요"
    # }
    # 이미지 처리 로직 (향후 여기에 YOLO 등 붙이면 됨)

    # 이후에 연결해야됨
    inferred_cause = "알레르기성 접촉성 피부염"
    disease = "농포성 여드름"
    tip = "실내 환경 청결 유지와 적절한 샴푸 사용을 권장합니다."
    treatment = "항생제 연고 도포 및 수의사 진료 필요"
    summary = generate_summary(condition, inferred_cause, disease, tip, treatment)

    today = datetime.now().strftime("%Y-%m-%d")

    result_store[sid] = {
        "status": "done",
        "data": {
            "breed": breed,
            "age": age,
            "gender": gender,
            "weight": weight,
            "neutered": neutered,
            "plastic_dish": plastic_dish,
            "season": season,
            "bath_cycle": bath_cycle,
            "walk_habit": walk_habit,
            "sun_exposure": sun_exposure,
            "housing": housing,
            "toy_wash_cycle": toy_wash_cycle,
            "condition": condition,
            "cause": inferred_cause,
            "disease": disease,
            "tip": tip,
            "treatment_breed": treatment,
            "treatment_age": treatment,
            "treatment_gender": treatment,
            "treatment_neutered": treatment,
            "treatment_environment": treatment,
            "treatment_condition": treatment,
            "recommended_meds": "피부연고 A",
            "cost1": "15,000원",
            "cost2": "8,000원",
            "cost3": "10,000원",
            "confidence": "87%",
            "feature": "붉은 반점과 농포",
            "similarity": "92%",
            "summary": summary,
            "date_today": today
        }
    }

if __name__ == '__main__':
    app.run(debug=True)
