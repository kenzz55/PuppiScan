from flask import Flask, render_template, request
import os
import secrets

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
secret_key = secrets.token_hex(16)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/report', methods=['POST'])
def make_report():
    # 1. 텍스트 입력 받기
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
        return "이미지가 누락되었습니다", 400

    # 3. AI 추론 결과 (mock)
    # disease_name = diagnosis_puppy_skin(image)
    # data = make_puppy_report(breed,age,gender,weight,neutered,enviroment,condition,vulnerability,disease_name)
    inferred_cause = "알레르기성 접촉성 피부염"
    disease = "농포성 여드름"
    tip = "실내 환경 청결 유지와 적절한 샴푸 사용을 권장합니다."
    treatment_breed = "특정 견종의 유전적 요인 고려"
    treatment_age = "어린 나이일수록 저자극 치료 권장"
    treatment_gender = "성별 호르몬 영향 고려"
    treatment_neutered = "호르몬 변화에 따른 치료 조정"
    treatment_environment = "청결한 환경 유지"
    treatment_condition = "기저 질환과 병행 치료 필요"
    recommended_meds = "베타메타손 크림, 살리실산 샴푸"
    cost1 = "30,000원"
    cost2 = "20,000원"
    cost3 = "10,000원"
    confidence = "92%"
    feature = "농포성 병변, 발적"
    similarity = "유사 증례 87% 유사"
    summary = "중소형견에서 자주 나타나는 접촉성 피부염의 전형적인 사례로 판단됨."

    return render_template("report.html",
        breed=breed, age=age, gender=gender, weight=weight, neutered=neutered,
        environment=environment, condition=condition, vulnerability=vulnerability,
        cause=inferred_cause, disease=disease, tip=tip,
        treatment_breed=treatment_breed, treatment_age=treatment_age,
        treatment_gender=treatment_gender, treatment_neutered=treatment_neutered,
        treatment_environment=treatment_environment, treatment_condition=treatment_condition,
        recommended_meds=recommended_meds,
        cost1=cost1, cost2=cost2, cost3=cost3,
        confidence=confidence, feature=feature, similarity=similarity, summary=summary
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)