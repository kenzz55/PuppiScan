from durable.lang import *
recommendation = {
    'treatment': ''
}

# 사실 기반 룰셋 구현
with ruleset('pet_recommendation'):
    # 상태 초기화 (assert_fact용)
    @when_all(+m.lesion_type)
    def set_code(c):
        c.s.code = c.m.lesion_type


    @when_all(+m.age_years)
    def set_age_group(c):
        years = c.m.age_years
        if years <= 1:
            c.s.age_group = 'puppy'
        elif years <= 7:
            c.s.age_group = 'adult'
        elif years <= 12:
            c.s.age_group = 'senior'
        else:
            c.s.age_group = 'geriatric'


    @when_all(+m.weight)
    def set_weight_group(c):
        mapping = {1: 'very_small', 2: 'small', 3: 'medium', 4: 'large', 5: 'very_large', 6: 'giant'}
        c.s.weight_group = mapping[c.m.weight]


    # A1 원인
    @when_all((m.lesion_type == 'A1') & (m.underlying_conditions == '알레르기성 피부염'))
    def cause_A1_allergy(c):
        c.s.cause = '알레르기성 피부염'


    @when_all((m.lesion_type == 'A1') & (m.underlying_conditions == '외부 기생충 알레르기'))
    def cause_A1_parasite(c):
        c.s.cause = '외부 기생충 알레르기'


    @when_all((m.lesion_type == 'A1') & (m.underlying_conditions == '세균/진균 감염'))
    def cause_A1_infection(c):
        c.s.cause = '세균/진균 감염'


    @when_all((m.lesion_type == 'A1') & (m.underlying_conditions == '접촉성 피부염'))
    def cause_A1_contact(c):
        c.s.cause = '접촉성 피부염'


    @when_all((m.lesion_type == 'A1') & (m.underlying_conditions == '내분비/면역 이상'))
    def cause_A1_endocrine(c):
        c.s.cause = '내분비/면역 이상'


    # A2 원인
    @when_all((m.lesion_type == 'A2') & (
            m.underlying_conditions == '알레르기성 피부염') |
              (m.underlying_conditions == '면역 매개성 질환'))
    def cause_A2_allergy(c):
        c.s.cause = '알레르기 원인'


    @when_all((m.lesion_type == 'A2') & (m.underlying_conditions == '영양 불균형'))
    def cause_A2_nutrition(c):
        c.s.cause = '영양 결핍'


    @when_all((m.lesion_type == 'A2') & (m.uses_plastic_bowl == '사용'))
    def cause_A2_environment(c):
        c.s.cause = '환경적 요인'


    @when_all((m.lesion_type == 'A2') & (m.underlying_conditions == '내분비 이상'))
    def cause_A2_systemic(c):
        c.s.cause = '내과적·전신성 질환'


    @when_all((m.lesion_type == 'A2') & (m.underlying_conditions == '세균/진균 감염'))
    def cause_A2_infection(c):
        c.s.cause = '감염성 원인'


    # A4 원인
    @when_all((m.lesion_type == 'A4') & (m.underlying_conditions == '알레르기성 피부염'))
    def cause_A4_allergy(c):
        c.s.cause = '알레르기성 피부질환'


    @when_all((m.lesion_type == 'A4') & (m.underlying_conditions == '내분비 이상'))
    def cause_A4_hormonal(c):
        c.s.cause = '호르몬 이상'


    @when_all((m.lesion_type == 'A4') & (m.underlying_conditions == '외부 기생충 알레르기'))
    def cause_A4_parasite(c):
        c.s.cause = '기생충 감염'


    @when_all((m.lesion_type == 'A4') & (m.living_area == 'outdoor'))
    def cause_A4_trauma(c):
        c.s.cause = '피부 외상 및 자극'


    @when_all((m.lesion_type == 'A4') & (m.season == 'summer'))
    def cause_A4_moisture(c):
        c.s.cause = '습한 환경'


    # A5 원인
    @when_all((m.lesion_type == 'A5') & (m.underlying_conditions == '세균/진균 감염'))
    def cause_A5_bacterial(c):
        c.s.cause = '세균 감염'


    @when_all((m.lesion_type == 'A5') & (
            m.underlying_conditions == '자가면역성 피부염') |
              (m.underlying_conditions == '면역 매개성 질환'))
    def cause_A5_autoimmune(c):
        c.s.cause = '자가면역성 피부염'


    @when_all((m.lesion_type == 'A5') & (m.living_area == 'outdoor'))
    def cause_A5_trauma(c):
        c.s.cause = '외상'


    @when_all((m.lesion_type == 'A5') & (m.bath_freq_per_month == 0))
    def cause_A5_chemical(c):
        c.s.cause = '화학적 자극'


    @when_all((m.lesion_type == 'A5') & (m.sun_exposure >= 3))
    def cause_A5_vascular(c):
        c.s.cause = '혈관장애'


    @when_all(
        ((m.lesion_type == 'A1') | (m.lesion_type == 'A2')) &
        ((m.breed == '말티즈') | (m.breed == '포메라니안') | (m.breed == '푸들')))
    def cause_breed_allergy(c):
        c.s.cause = '알레르기성 피부염'


    # 2. 호르몬 이상 (미중성화 암컷)
    @when_all(
        (m.lesion_type == 'A4') &
        (m.gender == 'female') &
        (m.neutered == '아니오'))
    def cause_A4_hormonal_female(c):
        c.s.cause = '호르몬 이상'


    # 3. 산책습관 + 실외 생활 → 외상(A5)
    @when_all(
        (m.lesion_type == 'A5') &
        (m.walk_habit >= 3) &
        (m.living_area == 'outdoor'))
    def cause_A5_trauma_walk(c):
        c.s.cause = '운동성 외상'


    # 4. 산책습관 + 실외 생활 → 기생충 알레르기 (A1, A4)
    @when_all(
        ((m.lesion_type == 'A1') | (m.lesion_type == 'A4')) &
        (m.walk_habit >= 3) &
        (m.living_area == 'outdoor'))
    def cause_parasite_walk(c):
        c.s.cause = '외부 기생충 알레르기'


    # 5. 세탁 주기 부족 → 감염성 원인 (A2, A5)
    @when_all(
        ((m.lesion_type == 'A2') | (m.lesion_type == 'A5')) &
        (m.wash_cycle >= 3))
    def cause_infection_wash_cycle(c):
        c.s.cause = '감염성 요인 (세탁 부족)'


    # 6. 대형 노령견 혈관장애 (A5)
    @when_all(
        (m.lesion_type == 'A5') &
        (m.weight == 6) &
        (m.age_years > 12))
    def cause_A5_vascular_giant_old(c):
        c.s.cause = '혈관장애'


    # 최종 처방
    @when_all((s.code == 'A1') & (s.cause == '알레르기성 피부염') & (s.age_group == 'puppy') & (s.weight_group == 'very_small'))
    def rec1(c):
        print('A1-Puppy-VS-Allergy 처방:')
        print('1) 하이포알러제닉 샴푸 목욕 2회/주 (샴푸 20,000원)')
        print('2) 스테로이드 연고 7일 (15,000원)')
        print('3) 항히스타민제 0.5mg/kg 14일 (25,000원)')
        print('총 예상 비용: 약 60,000원')
        text = (
            'A1-Puppy-VS-Allergy 처방:\n'
            '1) 하이포알러제닉 샴푸 목욕 2회/주 (샴푸 20,000원)\n'
            '2) 스테로이드 연고 7일 (15,000원)\n'
            '3) 항히스타민제 0.5mg/kg 14일 (25,000원)\n'
            '총 예상 비용: 약 60,000원\n'
        )
        recommendation['treatment'] = text
        c.s.code = 'break'
        c.retract_fact('pet_recommendation', c.m)


    @when_all((s.code == 'A1') & (s.cause == '알레르기성 피부염') & (s.age_group == 'adult') & (s.weight_group == 'small'))
    def rec2(c):
        print('A1-Adult-S-Allergy 처방:')
        print('1) 저자극 샴푸 목욕 1회/주 (15,000원)')
        print('2) 코르티코스테로이드 크림 10일 (20,000원)')
        print('총 예상 비용: 약 35,000원')
        text = (
            'A1-Adult-S-Allergy 처방:\n'
            '1) 저자극 샴푸 목욕 1회/주 (15,000원)\n'
            '2) 코르티코스테로이드 크림 10일 (20,000원)\n'
            '3) 항히스타민제 0.5mg/kg 14일 (25,000원)\n'
            '총 예상 비용: 약 35,000원\n'
        )
        recommendation['treatment'] = text
        c.s.code = 'break'
        c.retract_fact('pet_recommendation', c.m)


    @when_all((s.code == 'A1') & (s.cause == '알레르기성 피부염') & (s.age_group == 'senior') & (s.weight_group == 'medium'))
    def rec3(c):
        print('A1-Senior-M-Allergy 처방:')
        print('1) 진정 샴푸 목욕 1회/주 (25,000원)')
        print('2) 장기간 연고 14일 (30,000원)')
        print('총 예상 비용: 약 55,000원')
        text = (
            'A1-Senior-M-Allergy 처방:\n'
            '1) 진정 샴푸 목욕 1회/주 (25,000원)\n'
            '2) 장기간 연고 14일 (30,000원)\n'
            '총 예상 비용: 약 55,000원\n'
        )
        recommendation['treatment'] = text

        c.s.code = 'break'
        c.retract_fact('pet_recommendation', c.m)


    @when_all((s.code == 'A1') & (s.cause == '알레르기성 피부염') & (s.age_group == 'geriatric') & (s.weight_group == 'large'))
    def rec4(c):
        print('A1-Geriatric-L-Allergy 처방:')
        print('1) 저자극 목욕 2주 1회 (30,000원)')
        print('2) 스테로이드 연고 10일 (25,000원)')
        print('총 예상 비용: 약 55,000원')
        text = (
            'A1-Geriatric-L-Allergy 처방:\n'
            '1) 저자극 목욕 2주 1회 (30,000원)\n'
            '2) 스테로이드 연고 10일 (25,000원)\n'
            '총 예상 비용: 약 55,000원\n'
        )
        recommendation['treatment'] = text
        c.s.code = 'break'
        c.retract_fact('pet_recommendation', c.m)


    @when_all((s.code == 'A1') & (s.cause == '외부 기생충 알레르기') & (s.age_group == 'adult') & (s.weight_group == 'medium'))
    def rec5(c):
        print('A1-Adult-M-Parasite 처방:')
        print('1) 국소 살충제 2회 적용 (30,000원)')
        print('2) 내복 구충제 3일 (20,000원)')
        print('총 예상 비용: 약 50,000원')
        text = (
            'A1-Adult-M-Parasite 처방:\n'
            '1) 국소 살충제 2회 적용 (30,000원)\n'
            '2) 내복 구충제 3일 (20,000원)\n'
            '총 예상 비용: 약 50,000원\n'
        )
        recommendation['treatment'] = text
        c.s.code = 'break'
        c.retract_fact('pet_recommendation', c.m)


    @when_all((s.code == 'A1'))
    def rec5(c):
        print('국소 스테로이드 연고 도포')
        print('총 예상 비용: 약 50,000원')
        text = (
            '국소 스테로이드 연고 도포\n'
            '총 예상 비용: 약 50,000원\n'
        )
        recommendation['treatment'] = text
        c.s.code = 'break'
        c.retract_fact('pet_recommendation', c.m)


    # A2 (7)
    @when_all((s.code == 'A2') & (s.cause == '감염성 원인') & (s.age_group == 'puppy') & (s.weight_group == 'small'))
    def rec6(c):
        print('A2-Puppy-S-Infection 처방:')
        print('1) 항진균 샴푸 목욕 2회/주 (15,000원)')
        print('2) 경구 항진균제 4주 (30,000원)')
        print('3) 국소 크림 2주 (20,000원)')
        print('총 예상 비용: 약 65,000원')
        text = (
            'A2-Puppy-S-Infection 처방:\n'
            '1) 항진균 샴푸 목욕 2회/주 (15,000원)\n'
            '2) 경구 항진균제 4주 (30,000원)\n'
            '3) 국소 크림 2주 (20,000원)\n'
            '총 예상 비용: 약 65,000원\n'
        )
        recommendation['treatment'] = text
        c.s.code = 'break'
        c.retract_fact('pet_recommendation', c.m)


    @when_all((s.code == 'A2') & (s.cause == '알레르기 원인') & (s.age_group == 'puppy') & (s.weight_group == 'small'))
    def rec7(c):
        print('A2-Puppy-S-Allergy 처방:')
        print('1) 저자극 샴푸 목욕 1회/주 (10,000원)')
        print('2) 항히스타민제 14일 (15,000원)')
        print('총 예상 비용: 약 25,000원')
        text = (
            'A2-Puppy-S-Allergy 처방:\n'
            '1) 저자극 샴푸 목욕 1회/주 (10,000원)\n'
            '2) 항히스타민제 14일 (15,000원)\n'
            '총 예상 비용: 약 25,000원\n'
        )
        recommendation['treatment'] = text
        c.s.code = 'break'
        c.retract_fact('pet_recommendation', c.m)


    @when_all((s.code == 'A2') & (s.cause == '내과적·전신성 질환') & (s.age_group == 'adult') & (s.weight_group == 'medium'))
    def rec8(c):
        print('A2-Adult-M-Systemic 처방:')
        print('1) 내분비 검사 (50,000원)')
        print('2) 보조 호르몬제 30일 (40,000원)')
        print('총 예상 비용: 약 90,000원')
        text = (
            'A2-Adult-M-Systemic 처방:\n'
            '1) 내분비 검사 (50,000원)\n'
            '2) 보조 호르몬제 30일 (40,000원)\n'
            '총 예상 비용: 약 90,000원\n'
        )
        recommendation['treatment'] = text
        c.s.code = 'break'
        c.retract_fact('pet_recommendation', c.m)


    @when_all((s.code == 'A2') & (s.cause == '영양 결핍') & (s.age_group == 'adult') & (s.weight_group == 'medium'))
    def rec9(c):
        print('A2-Adult-M-Nutrition 처방:')
        print('1) 영양 보충제 30일 (30,000원)')
        print('2) 오메가-3 식이요법 30일 (25,000원)')
        print('총 예상 비용: 약 55,000원')
        text = (
            'A2-Adult-M-Nutrition 처방:\n'
            '1) 영양 보충제 30일 (30,000원)\n'
            '2) 오메가-3 식이요법 30일 (25,000원)\n'
            '총 예상 비용: 약 55,000원\n'
        )
        recommendation['treatment'] = text
        c.s.code = 'break'
        c.retract_fact('pet_recommendation', c.m)


    @when_all((s.code == 'A2') & (s.cause == '환경적 요인') & (s.age_group == 'adult') & (s.weight_group == 'medium'))
    def rec10(c):
        print('A2-Adult-M-Environment 처방:')
        print('1) 환경정화 서비스 (20,000원)')
        print('2) 스테인리스 식기 교체 (15,000원)')
        print('총 예상 비용: 약 35,000원')
        text = (
            'A2-Adult-M-Environment 처방:\n'
            '1) 환경정화 서비스 (20,000원)\n'
            '2) 스테인리스 식기 교체 (15,000원)\n'
            '총 예상 비용: 약 35,000원\n'
        )
        recommendation['treatment'] = text
        c.s.code = 'break'
        c.retract_fact('pet_recommendation', c.m)


    @when_all((s.code == 'A2') & (s.cause == '감염성 원인') & (s.age_group == 'senior') & (s.weight_group == 'large'))
    def rec11(c):
        print('A2-Senior-L-Infection 처방:')
        print('1) 항진균제 주사 (50,000원)')
        print('2) 방문 진료비 (30,000원)')
        print('총 예상 비용: 약 80,000원')
        text = (
            'A2-Senior-L-Infection 처방:\n'
            '1) 항진균제 주사 (50,000원)\n'
            '2) 방문 진료비 (30,000원)\n'
            '총 예상 비용: 약 80,000원\n'
        )
        recommendation['treatment'] = text
        c.s.code = 'break'
        c.retract_fact('pet_recommendation', c.m)


    @when_all((s.code == 'A2') & (s.cause == '알레르기 원인') & (s.age_group == 'senior') & (s.weight_group == 'large'))
    def rec12(c):
        print('A2-Senior-L-Allergy 처방:')
        print('1) 경구 항히스타민제 30일 (20,000원)')
        print('2) 스테로이드 연고 14일 (25,000원)')
        print('총 예상 비용: 약 45,000원')
        text = (
            'A2-Senior-L-Allergy 처방:\n'
            '1) 경구 항히스타민제 30일 (20,000원)\n'
            '2) 스테로이드 연고 14일 (25,000원)\n'
            '총 예상 비용: 약 45,000원\n'
        )
        recommendation['treatment'] = text
        c.s.code = 'break'
        c.retract_fact('pet_recommendation', c.m)


    @when_all((s.code == 'A2'))
    def rec5(c):
        print('케토코나졸 함유 샴푸 목욕')
        print('총 예상 비용: 약 60,000원')
        text = (
            '케토코나졸 함유 샴푸 목욕\n'
            '총 예상 비용: 약 60,000원\n'
        )
        recommendation['treatment'] = text
        c.s.code = 'break'
        c.retract_fact('pet_recommendation', c.m)


    # A4 (6)
    @when_all((s.code == 'A4') & (s.cause == '알레르기성 피부질환') & (s.age_group == 'puppy') & (s.weight_group == 'small'))
    def rec13(c):
        print('A4-Puppy-S-Allergy 처방:')
        print('1) 샴푸 목욕 1회/주 (10,000원)')
        print('2) 국소 연고 10일 (15,000원)')
        print('총 예상 비용: 약 25,000원')
        text = (
            'A4-Puppy-S-Allergy 처방:\n'
            '1) 샴푸 목욕 1회/주 (10,000원)\n'
            '2) 국소 연고 10일 (15,000원)\n'
            '총 예상 비용: 약 25,000원\n'
        )
        recommendation['treatment'] = text
        c.s.code = 'break'
        c.retract_fact('pet_recommendation', c.m)


    @when_all((s.code == 'A4') & (s.cause == '호르몬 이상') & (s.age_group == 'adult') & (s.weight_group == 'medium'))
    def rec14(c):
        print('A4-Adult-M-Hormonal 처방:')
        print('1) 호르몬 검사 (50,000원)')
        print('2) 레보티록신 30일 (60,000원)')
        print('총 예상 비용: 약 110,000원')
        text = (
            'A4-Adult-M-Hormonal 처방:\n'
            '1) 호르몬 검사 (50,000원)\n'
            '2) 레보티록신 30일 (60,000원)\n'
            '총 예상 비용: 약 110,000원\n'
        )
        recommendation['treatment'] = text
        c.s.code = 'break'
        c.retract_fact('pet_recommendation', c.m)


    @when_all((s.code == 'A4') & (s.cause == '기생충 감염') & (s.age_group == 'adult') & (s.weight_group == 'medium'))
    def rec15(c):
        print('A4-Adult-M-Parasite 처방:')
        print('1) 옴진드기 제제 2회 (30,000원)')
        print('2) 구충제 3일 (20,000원)')
        print('총 예상 비용: 약 50,000원')
        text = (
            'A4-Adult-M-Parasite 처방:\n'
            '1) 옴진드기 제제 2회 (30,000원)\n'
            '2) 구충제 3일 (20,000원)\n'
            '총 예상 비용: 약 50,000원\n'
        )
        recommendation['treatment'] = text
        c.s.code = 'break'
        c.retract_fact('pet_recommendation', c.m)


    @when_all((s.code == 'A4') & (s.cause == '피부 외상') & (s.age_group == 'adult') & (s.weight_group == 'medium'))
    def rec16(c):
        print('A4-Adult-M-Trauma 처방:')
        print('1) 상처 소독제 (10,000원)')
        print('2) 드레싱 (5,000원)')
        print('총 예상 비용: 약 15,000원')
        text = (
            'A4-Adult-M-Trauma 처방:\n'
            '1) 상처 소독제 (10,000원)\n'
            '2) 드레싱 (5,000원)\n'
            '총 예상 비용: 약 15,000원\n'
        )
        recommendation['treatment'] = text
        c.s.code = 'break'
        c.retract_fact('pet_recommendation', c.m)


    @when_all((s.code == 'A4') & (s.cause == '습한 환경') & (s.age_group == 'adult') & (s.weight_group == 'medium'))
    def rec17(c):
        print('A4-Adult-M-Moisture 처방:')
        print('1) 건조 스프레이 (20,000원)')
        print('2) 환경 개선 서비스 (30,000원)')
        print('총 예상 비용: 약 50,000원')
        text = (
            'A4-Adult-M-Moisture 처방:\n'
            '1) 건조 스프레이 (20,000원)\n'
            '2) 환경 개선 서비스 (30,000원)\n'
            '총 예상 비용: 약 50,000원\n'
        )
        recommendation['treatment'] = text
        c.s.code = 'break'
        c.retract_fact('pet_recommendation', c.m)


    @when_all((s.code == 'A4') & (s.cause == '호르몬 이상') & (s.age_group == 'senior') & (s.weight_group == 'large'))
    def rec18(c):
        print('A4-Senior-L-Hormonal 처방:')
        print('1) 호르몬 패치 (70,000원)')
        print('2) 재검진 (40,000원)')
        print('총 예상 비용: 약 110,000원')
        text = (
            'A4-Senior-L-Hormonal 처방:\n'
            '1) 호르몬 패치 (70,000원)\n'
            '2) 재검진 (40,000원)\n'
            '총 예상 비용: 약 110,000원\n'
        )
        recommendation['treatment'] = text
        c.s.code = 'break'
        c.retract_fact('pet_recommendation', c.m)


    @when_all((s.code == 'A4'))
    def rec5(c):
        print('경구용 항생제 처방 (시프로플록사신)')
        print('총 예상 비용: 약 70,000원')
        text = (
            '경구용 항생제 처방 (시프로플록사신)\n'
            '총 예상 비용: 약 70,000원\n'
        )
        recommendation['treatment'] = text
        c.s.code = 'break'
        c.retract_fact('pet_recommendation', c.m)


    # A5 (10)
    @when_all((s.code == 'A5') & (s.cause == '세균 감염') & (s.age_group == 'puppy') & (s.weight_group == 'small'))
    def rec19(c):
        print('A5-Puppy-S-Bacterial 처방:')
        print('1) 경구 항생제 14일 (30,000원)')
        print('2) 상처 소독 7일 (15,000원)')
        print('총 예상 비용: 약 45,000원')
        text = (
            'A5-Puppy-S-Bacterial 처방:'
            '1) 경구 항생제 14일 (30,000원)'
            '2) 상처 소독 7일 (15,000원)'
            '총 예상 비용: 약 45,000원'
        )
        recommendation['treatment'] = text
        c.s.code = 'break'
        c.retract_fact('pet_recommendation', c.m)


    @when_all((s.code == 'A5') & (s.cause == '자가면역성 피부염') & (s.age_group == 'puppy') & (s.weight_group == 'small'))
    def rec20(c):
        print('A5-Puppy-S-Autoimmune 처방:')
        print('1) 아자티오프린 6주 (40,000원)')
        print('2) 혈액 검사 2회 (30,000원)')
        print('총 예상 비용: 약 70,000원')
        text = (
            'A5-Puppy-S-Autoimmune 처방:'
            '1) 아자티오프린 6주 (40,000원)'
            '2) 혈액 검사 2회 (30,000원)'
            '총 예상 비용: 약 70,000원'
        )
        recommendation['treatment'] = text
        c.s.code = 'break'
        c.retract_fact('pet_recommendation', c.m)


    @when_all((s.code == 'A5') & (s.cause == '외상') & (s.age_group == 'adult') & (s.weight_group == 'medium'))
    def rec21(c):
        print('A5-Adult-M-Trauma 처방:')
        print('1) 연고 10일 (10,000원)')
        print('2) 드레싱 교체 1회 (20,000원)')
        print('총 예상 비용: 약 30,000원')
        text = (
            'A5-Adult-M-Trauma 처방:'
            '1) 연고 10일 (10,000원)'
            '2) 드레싱 교체 1회 (20,000원)'
            '총 예상 비용: 약 30,000원'
        )
        recommendation['treatment'] = text
        c.s.code = 'break'
        c.retract_fact('pet_recommendation', c.m)


    @when_all((s.code == 'A5') & (s.cause == '화학적 자극') & (s.age_group == 'adult') & (s.weight_group == 'medium'))
    def rec22(c):
        print('A5-Adult-M-Chemical 처방:')
        print('1) 중화 세척제 (5,000원)')
        print('2) 연고 14일 (15,000원)')
        print('총 예상 비용: 약 20,000원')
        text = (
            'A5-Adult-M-Chemical 처방:'
            '1) 중화 세척제 (5,000원)'
            '2) 연고 14일 (15,000원)'
            '총 예상 비용: 약 20,000원'
        )
        recommendation['treatment'] = text
        c.s.code = 'break'
        c.retract_fact('pet_recommendation', c.m)


    @when_all((s.code == 'A5') & (s.cause == '혈관장애') & (s.age_group == 'adult') & (s.weight_group == 'medium'))
    def rec23(c):
        print('A5-Adult-M-Vascular 처방:')
        print('1) 혈관 강화제 30일 (25,000원)')
        print('2) 마사지치료 4회 (30,000원)')
        print('총 예상 비용: 약 55,000원')
        text = (
            'A5-Adult-M-Vascular 처방:'
            '1) 혈관 강화제 30일 (25,000원)'
            '2) 마사지치료 4회 (30,000원)'
            '총 예상 비용: 약 55,000원'
        )
        recommendation['treatment'] = text
        c.s.code = 'break'
        c.retract_fact('pet_recommendation', c.m)


    @when_all((s.code == 'A5') & (s.cause == '세균 감염') & (s.age_group == 'senior') & (s.weight_group == 'large'))
    def rec24(c):
        print('A5-Senior-L-Bacterial 처방:')
        print('1) IV 항생제 7일 (80,000원)')
        print('2) 소독제 7일 (20,000원)')
        print('총 예상 비용: 약 100,000원')
        text = (
            'A5-Senior-L-Bacterial 처방:'
            '1) IV 항생제 7일 (80,000원)'
            '2) 소독제 7일 (20,000원)'
            '총 예상 비용: 약 100,000원'
        )
        recommendation['treatment'] = text
        c.s.code = 'break'
        c.retract_fact('pet_recommendation', c.m)


    @when_all((s.code == 'A5') & (s.cause == '자가면역성 피부염') & (s.age_group == 'senior') & (s.weight_group == 'large'))
    def rec25(c):
        print('A5-Senior-L-Autoimmune 처방:')
        print('1) 아자티오프린 8주 (60,000원)')
        print('2) 혈액 검사 3회 (50,000원)')
        print('총 예상 비용: 약 110,000원')
        c.s.code = 'break'
        c.retract_fact('pet_recommendation', c.m)


    @when_all((s.code == 'A5') & (s.cause == '외상') & (s.age_group == 'senior') & (s.weight_group == 'large'))
    def rec26(c):
        print('A5-Senior-L-Trauma 처방:')
        print('1) 드레싱 2회 (30,000원)')
        print('2) 재평가 (20,000원)')
        print('총 예상 비용: 약 50,000원')
        text = (
            'A5-Senior-L-Trauma 처방:'
            '1) 드레싱 2회 (30,000원)'
            '2) 재평가 (20,000원)'
            '총 예상 비용: 약 50,000원'
        )
        recommendation['treatment'] = text
        c.s.code = 'break'
        c.retract_fact('pet_recommendation', c.m)


    @when_all((s.code == 'A5') & (s.cause == '화학적 자극') & (s.age_group == 'senior') & (s.weight_group == 'large'))
    def rec27(c):
        print('A5-Senior-L-Chemical 처방:')
        print('1) 중화제 (10,000원)')
        print('2) 연고 14일 (20,000원)')
        print('총 예상 비용: 약 30,000원')
        text = (
            'A5-Senior-L-Chemical 처방:'
            '1) 중화제 (10,000원)'
            '2) 연고 14일 (20,000원)'
            '총 예상 비용: 약 30,000원'
        )
        recommendation['treatment'] = text
        c.s.code = 'break'
        c.retract_fact('pet_recommendation', c.m)


    @when_all((s.code == 'A5') & (s.cause == '혈관장애') & (s.age_group == 'senior') & (s.weight_group == 'large'))
    def rec28(c):
        print('A5-Senior-L-Vascular 처방:')
        print('1) 혈관 수술 (100,000원)')
        print('2) 재활 프로그램 4회 (50,000원)')
        print('총 예상 비용: 약 150,000원')
        text = (
            'A5-Senior-L-Vascular 처방:'
            '1) 혈관 수술 (100,000원)'
            '2) 재활 프로그램 4회 (50,000원)'
            '총 예상 비용: 약 150,000원'
        )
        recommendation['treatment'] = text
        c.s.code = 'break'
        c.retract_fact('pet_recommendation', c.m)


    @when_all((s.code == 'A5'))
    def rec5(c):
        print('상처 드레싱 및 소독 관리')
        print('총 예상 비용: 약 80,000원')
        text = (
            '상처 드레싱 및 소독 관리'
            '총 예상 비용: 약 80,000원'
        )
        recommendation['treatment'] = text
        c.s.code = 'break'
        c.retract_fact('pet_recommendation', c.m)


def get_recommendation(fact: dict) -> str:
    # 호출 전 초기화
    recommendation['treatment'] = ''
    # 사실 던지기
    assert_fact('pet_recommendation', fact)
    # 처리된 treatment 반환
    return recommendation['treatment']



