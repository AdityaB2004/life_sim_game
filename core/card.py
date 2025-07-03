class Card:
    def __init__(self, id, description, left_option, right_option, age_range=None, has_consequence=False, consequence_ids=None):
        self.id = id
        self.description = description
        self.left_option = left_option      # Expected format: (option_text, effects_dict)
        self.right_option = right_option    # Expected format: (option_text, effects_dict)
        self.age_range = age_range          # Tuple (min_age, max_age) or None
        self.has_consequence = has_consequence
        self.consequence_ids = consequence_ids  # List of consequence IDs or None

    def get_effect(self, choice):
        if choice == 1:
            return self.left_option[1]
        else:
            return self.right_option[1]
