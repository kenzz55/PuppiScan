from flask import Flask, render_template, request, redirect, flash, session, jsonify
import os, secrets, threading, uuid
from datetime import datetime
from gpt.summary import generate_summary  # 기존 GPT summary
# 나중에 from ai.image_analysis import analyze_image 이런 식으로 붙이면 됨
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'yolov5'))
from yolov5.run_detect import detect_disease

from expert.tip import *
from expert.causemapping import *
from expert.treatment import *

from dataclasses import dataclass
@dataclass()
class PetFact:
    breed: str
    age_years: int
    gender: str
    neutered: str
    weight: int
    lesion_type: str
    underlying_conditions: str
    uses_plastic_bowl: str
    season: str
    bath_freq_per_month: int
    walk_habit: int
    sun_exposure: int
    living_area: str
    wash_cycle: int

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
UPLOAD_FOLDER = 'uploads'
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

    # 한글로 보여줄 항목 이름 매핑
    field_names = {
        'breed': '견종',
        'age': '나이',
        'gender': '성별',
        'weight': '체중',
        'neutered': '중성화 여부',
        'condition': '기저질환',
        'plastic_dish': '플라스틱 식기 사용 여부',
        'season': '계절',
        'bath_cycle': '목욕 주기',
        'walk_habit': '산책 습관',
        'sun_exposure': '햇빛 노출 정도',
        'housing': '주거 환경',
        'toy_wash_cycle': '애완용품 세탁 주기'
    }

    # 누락된 항목 필터링
    missing = [field for field in required_fields if not form_data.get(field)]

    # 누락 항목 메시지 구성
    if missing or not image or image.filename == '':
        missing_fields = [field_names.get(f, f) for f in missing]

        # 이미지 업로드 여부 확인
        if not image or image.filename == '':
            missing_fields.append('이미지 업로드')

        flash(f"{', '.join(missing_fields)} 항목을 입력해주세요")
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
    
    disease_map = {
    "dermatitis": "A4",
    "flea_allergy": "A1",
    "ringworm": "A5",
    "scabies": "A2"
    }
    disease_name = disease
    disease = disease_map.get(disease, disease)    
    
    disease_map2 = {
    "dermatitis": "피부염",
    "flea_allergy": "벼룩 알레르기 피부염",
    "ringworm": "피부사상균증",
    "scabies": "옴진드기 감염"
    }
    disease_name = disease_map2.get(disease_name, disease_name)
        
    external_fact = {
        'breed': breed,
        'gender': gender,
        'neutered': neutered,
        'uses_plastic_bowl': plastic_dish,
        'season': season,
        'bath_freq_per_month': bath_cycle,
        'walk_habit': walk_habit,
        'sun_exposure': sun_exposure,
        'living_area': housing,
        'wash_cycle': toy_wash_cycle,
        'lesion_type': disease,
        'underlying_conditions': condition,
        'age_years': age,
        'weight': weight
    }

    sample_fact = PetFact(
        breed=breed,
        age_years=age,
        gender=gender,
        neutered=neutered,
        weight=weight,
        lesion_type=disease,
        underlying_conditions=condition,
        uses_plastic_bowl=plastic_dish,
        season=season,
        bath_freq_per_month=bath_cycle,
        walk_habit=walk_habit,
        sun_exposure=sun_exposure,
        living_area=housing,
        wash_cycle=toy_wash_cycle
    )
    
    print(external_fact)

    user_env = fact_to_keywords(sample_fact)
    secondary_disease = get_secondary_disease(disease, condition)  # 2차질병
    inferred_cause, all_scores = infer_cause_for_disease(disease, user_env)  # 추론된 원인
    tip = get_treatment_tip(disease, inferred_cause)
    treatment = get_recommendation(external_fact) # assert_fact를 사용하여 정적 fact로 전달
    
    print(treatment)
    
    summary = generate_summary(condition, inferred_cause, disease, tip, treatment)


    today = datetime.now().strftime("%Y-%m-%d")
    yolo_image_url = '/static/result/result.jpg'
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
            "disease": disease_name,
            "secondary_disease" : secondary_disease,
            "tip": tip,
            "treatment": treatment,
            "confidence": f"{score:.2f}",
            #"feature": "붉은 반점과 농포",
            #"similarity": "92%",
            "summary": summary,
            "date_today": today,
            "yolo_image": yolo_image_url
        }
    }

if __name__ == '__main__':
    app.run(debug=True)
