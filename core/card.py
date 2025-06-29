class Card:
    def __init__(self, id, description, left_option, right_option, age_range=None, has_consequence=False):
        self.id = id
        self.description = description
        self.left_option = left_option  # Tuple: (text, effect_dict)
        self.right_option = right_option  # Tuple: (text, effect_dict)
        self.age_range = age_range
        self.has_consequence = has_consequence

    def get_effect(self, choice):
        if choice == 1:
            return self.left_option[1]
        else:
            return self.right_option[1]
