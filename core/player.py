class Player:
    def __init__(self, name="Nameless", gender="Unknown"):
        self.name = name
        self.age = 0
        self.gender = gender
        self.vitality = 100
        self.morale = 50
        self.wealth = 50
        self.social = 50

    def new_life(self, name, gender):
        self.name = name
        self.gender = gender
        self.age = 0
        self.vitality = 100
        self.wealth = 50
        self.morale = 50
        self.social = 50
