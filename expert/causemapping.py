from typing import List, Dict, Tuple, Any
from petfact import PetFact

# 환경 기반 원인 매핑
DISEASE_CAUSE_ENV_MAPPING: Dict[str, Dict[str, Dict[str, List[Any]]]] = {
    'A1': {
        'bacterial_infection': {
            'uses_plastic_bowl':    ['사용'],
            'season':               ['summer'],
            'bath_freq_per_month':  [0],
            'walk_habit':           [4],
            'sun_exposure':         [1],
            'living_area':          ['outdoor'],
            'wash_cycle':           [4],
        },
        'fungal_infection': {
            'uses_plastic_bowl':    ['사용X', '사용'],
            'season':               ['summer', 'fall'],
            'bath_freq_per_month':  [0],
            'walk_habit':           [3],
            'sun_exposure':         [1],
            'living_area':          ['outdoor'],
            'wash_cycle':           [4],
        },
        'allergic_dermatitis': {
            'uses_plastic_bowl':    ['사용X'],
            'season':               ['spring', 'fall'],
            'bath_freq_per_month':  [0],
            'walk_habit':           [2],
            'sun_exposure':         [1],
            'living_area':          ['indoor'],
            'wash_cycle':           [4],
        },
        'external_parasite': {
            'uses_plastic_bowl':    ['사용X'],
            'season':               ['spring', 'summer'],
            'bath_freq_per_month':  [1],
            'walk_habit':           [4],
            'sun_exposure':         [2],
            'living_area':          ['outdoor'],
            'wash_cycle':           [4],
        },
        'contact_dermatitis': {
            'uses_plastic_bowl':    ['사용X'],
            'season':               ['spring'],
            'bath_freq_per_month':  [0],
            'walk_habit':           [3],
            'sun_exposure':         [2],
            'living_area':          ['indoor'],
            'wash_cycle':           [4],
        },
        'endocrine_immune_disorder': {
            'uses_plastic_bowl':    ['사용'],
            'season':               ['fall'],
            'bath_freq_per_month':  [2],
            'walk_habit':           [1],
            'sun_exposure':         [2],
            'living_area':          ['indoor'],
            'wash_cycle':           [4],
        },
    },
    'A2': {
        'infectious_cause': {
            'uses_plastic_bowl':    ['사용X', '사용'],
            'season':               ['summer'],
            'bath_freq_per_month':  [0],
            'walk_habit':           [4],
            'sun_exposure':         [1],
            'living_area':          ['outdoor'],
            'wash_cycle':           [4],
        },
        'allergic_cause': {
            'uses_plastic_bowl':    ['사용X'],
            'season':               ['spring', 'fall'],
            'bath_freq_per_month':  [0],
            'walk_habit':           [2],
            'sun_exposure':         [1],
            'living_area':          ['indoor'],
            'wash_cycle':           [4],
        },
        'systemic_disease': {
            'uses_plastic_bowl':    ['사용X'],
            'season':               ['winter'],
            'bath_freq_per_month':  [2],
            'walk_habit':           [1],
            'sun_exposure':         [2],
            'living_area':          ['indoor'],
            'wash_cycle':           [2],
        },
        'nutritional_deficiency': {
            'uses_plastic_bowl':    ['사용X'],
            'season':               ['spring', 'winter'],
            'bath_freq_per_month':  [3],
            'walk_habit':           [1],
            'sun_exposure':         [3],
            'living_area':          ['indoor'],
            'wash_cycle':           [3],
        },
        'environmental_factor': {
            'uses_plastic_bowl':    ['사용X', '사용'],
            'season':               ['summer', 'fall'],
            'bath_freq_per_month':  [0],
            'walk_habit':           [4],
            'sun_exposure':         [1],
            'living_area':          ['outdoor'],
            'wash_cycle':           [4],
        },
    },
    'A4': {
        'allergic_skin_disease': {
            'uses_plastic_bowl':    ['사용X'],
            'season':               ['spring', 'fall'],
            'bath_freq_per_month':  [0],
            'walk_habit':           [2],
            'sun_exposure':         [1],
            'living_area':          ['indoor'],
            'wash_cycle':           [4],
        },
        'hormonal_imbalance': {
            'uses_plastic_bowl':    ['사용'],
            'season':               ['winter'],
            'bath_freq_per_month':  [2],
            'walk_habit':           [1],
            'sun_exposure':         [2],
            'living_area':          ['indoor'],
            'wash_cycle':           [1],
        },
        'parasitic_infection': {
            'uses_plastic_bowl':    ['사용X'],
            'season':               ['spring', 'summer'],
            'bath_freq_per_month':  [1],
            'walk_habit':           [4],
            'sun_exposure':         [2],
            'living_area':          ['outdoor'],
            'wash_cycle':           [4],
        },
        'skin_trauma_and_irritation': {
            'uses_plastic_bowl':    ['사용X'],
            'season':               ['summer'],
            'bath_freq_per_month':  [0],
            'walk_habit':           [3],
            'sun_exposure':         [2],
            'living_area':          ['outdoor'],
            'wash_cycle':           [4],
        },
        'skin_folds_moist_environment': {
            'uses_plastic_bowl':    ['사용X'],
            'season':               ['summer'],
            'bath_freq_per_month':  [0],
            'walk_habit':           [4],
            'sun_exposure':         [1],
            'living_area':          ['outdoor'],
            'wash_cycle':           [4],
        },
    },
    'A5': {
        'bacterial_infection': {
            'uses_plastic_bowl':    ['사용'],
            'season':               ['summer'],
            'bath_freq_per_month':  [0],
            'walk_habit':           [4],
            'sun_exposure':         [1],
            'living_area':          ['outdoor'],
            'wash_cycle':           [4],
        },
        'autoimmune_dermatitis': {
            'uses_plastic_bowl':    ['사용X'],
            'season':               ['spring', 'fall'],
            'bath_freq_per_month':  [0],
            'walk_habit':           [2],
            'sun_exposure':         [1],
            'living_area':          ['indoor'],
            'wash_cycle':           [4],
        },
        'traumatic_injury': {
            'uses_plastic_bowl':    ['사용X'],
            'season':               ['summer'],
            'bath_freq_per_month':  [0],
            'walk_habit':           [3],
            'sun_exposure':         [2],
            'living_area':          ['outdoor'],
            'wash_cycle':           [2],
        },
        'chemical_irritant_exposure': {
            'uses_plastic_bowl':    ['사용X'],
            'season':               ['spring'],
            'bath_freq_per_month':  [0],
            'walk_habit':           [3],
            'sun_exposure':         [2],
            'living_area':          ['indoor'],
            'wash_cycle':           [4],
        },
        'vascular_compromise': {
            'uses_plastic_bowl':    ['사용X'],
            'season':               ['winter'],
            'bath_freq_per_month':  [1],
            'walk_habit':           [1],
            'sun_exposure':         [2],
            'living_area':          ['indoor'],
            'wash_cycle':           [3],
        },
    },
}


def fact_to_keywords(fact: PetFact) -> List[str]:
    """
    PetFact 인스턴스로부터 환경 키워드 리스트 생성.
    키워드 형식: '<속성>_<값>'.
    """
    keywords = [
        f"uses_plastic_bowl_{fact.uses_plastic_bowl}",
        f"season_{fact.season}",
        f"bath_freq_per_month_{fact.bath_freq_per_month}",
        f"walk_habit_{fact.walk_habit}",
        f"sun_exposure_{fact.sun_exposure}",
        f"living_area_{fact.living_area}",
        f"wash_cycle_{fact.wash_cycle}"
    ]
    return keywords

def infer_cause_for_disease(
    disease: str,
    environment: List[str]
) -> Tuple[str, Dict[str, int]]:
    """
    disease에 대해 environment 키워드 리스트와
    DISEASE_CAUSE_ENV_MAPPING 매핑을 사용해,
    각 원인의 trigger 키워드 교집합 크기를 점수로 계산하여
    최적의 cause_id와 모든 점수 반환.
    """
    cause_map = DISEASE_CAUSE_ENV_MAPPING.get(disease, {})
    scores: Dict[str, int] = {}
    env_set = set(environment)

    for cause_id, props in cause_map.items():
        # props 딕셔너리를 키워드 리스트로 변환
        triggers = []
        for prop, values in props.items():
            for v in values:
                triggers.append(f"{prop}_{v}")
        # 교집합 크기 계산
        scores[cause_id] = len(env_set & set(triggers))

    # 최고 점수 원인 선택 (없으면 None)
    best_cause = max(scores, key=scores.get) if scores else None
    return best_cause, scores

#2차질병 맵핑----------------------------------------------------------------------------
SECONDARY_DISEASE_MAPPING = {
    ("A1", "알레르기성 피부염"): "만성 습진성 피부염",
    ("A2", "영양불균형"):       "피부 곰팡이병",
    ("A4", "피지 과다 분비"):       "피부 포도상구균증",
    ("A5", "내분비 이상"):       "만성 궤양성 피부염"
}

# 조회 함수는 그대로 사용
def get_secondary_disease(
    lesion_type: str,
    underlying_conditions: str
) -> str:
    return SECONDARY_DISEASE_MAPPING.get(
        (lesion_type, underlying_conditions),
        "해당 없음"
    )
#---------------------------------------------------------------------------------------




