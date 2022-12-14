from sqlalchemy import Boolean, Column, String


class ObjectiveFields:
    first_blood = Column(Boolean)
    place_first_blood = Column(String)
    first_herald = Column(String)
    first_herald_teamfight = Column(Boolean)
    first_herald_stealed = Column(Boolean)
    first_herald_route = Column(String)
    second_herald = Column(String)
    second_herald_teamfight = Column(Boolean)
    second_herald_stealed = Column(Boolean)
    second_herald_route = Column(String)
    first_tower = Column(String)
    first_tower_route = Column(String)
    first_tower_herald = Column(Boolean)
    first_drake = Column(String)
    first_drake_teamfight = Column(Boolean)
    first_drake_stealed = Column(Boolean)
    first_drake_type = Column(String)
    second_drake = Column(String)
    second_drake_teamfight = Column(Boolean)
    second_drake_stealed = Column(Boolean)
    second_drake_type = Column(String)
    third_drake = Column(String)
    third_drake_teamfight = Column(Boolean)
    third_drake_stealed = Column(Boolean)
    third_drake_type = Column(String)
    turrets_destroyed = Column(Boolean)
