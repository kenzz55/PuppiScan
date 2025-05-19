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