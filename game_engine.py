import random
import json
import os
from core.player import Player
from core.card import Card


class GameEngine:
    def __init__(self):
        self.player = None
        self.cards = self.load_sample_cards()
        self.age = 1
        self.consequence_next = False
        self.current_consequence_id = None  # Track which consequence to show next

    def reset_player(self):
        print(
            "\nNow open your eyes as your soul is brought to life. I am the one who has created everything and I am giving you "
            "a chance to experience my creation. You shall inhabit mortal bodies and continue in the cycle of birth and rebirth, "
            "but of course it is not that simple. You must keep track of your virtues which will determine your lifespan: Vitality, Morale, "
            "Socials, and Funds. Always keep them in balance  too little or too low and you die. Life will give you options and each step "
            "your choice would be 1 for left option or 0 for the right one. Make your decisions wisely and I will meet you after 500 years."
        )
        name = input("\nWhat shall be your name, mortal? ").strip()
        gender = input("What gender do you identify as? ").strip()
        self.player = Player(name, gender)
        self.age = 1
        self.consequence_next = False
        self.current_consequence_id = None

    def load_sample_cards(self):
        cards_path = os.path.join("cards", "cards.json")
        with open(cards_path, "r") as f:
            data = json.load(f)

        cards = []
        for item in data:
            age_range = tuple(item["age_range"]) if item["age_range"] is not None else None
            card = Card(
                id=item["id"],
                description=item["description"],
                left_option=tuple(item["left_option"]),
                right_option=tuple(item["right_option"]),
                age_range=age_range,
                has_consequence=item["has_consequence"],
                consequence_ids=item.get("consequence_ids")  # <-- changed here
            )
            cards.append(card)
        return cards

    def get_next_card(self):
        if self.consequence_next and self.current_consequence_id is not None:
            # Return the consequence card by its ID
            consequence_card = next((c for c in self.cards if c.id == self.current_consequence_id), None)
            if consequence_card:
                return consequence_card

        # Normal cards: exclude consequence cards (assumed to have IDs >= 100)
        available = [
            card for card in self.cards
            if (card.age_range is None or (self.age >= card.age_range[0] and self.age <= card.age_range[1]))
            and (card.id < 100)  # Exclude consequence cards from normal draws
        ]
        return random.choice(available)

    def play(self):
        print("Welcome to Soulbound - The Cycle Begins.")
        self.reset_player()

        while True:
            while True:
                print(
                    f"\nYear: {self.age} | Name: {self.player.name} | Gender: {self.player.gender} | "
                    f"Vitality: {self.player.vitality} | Wealth: {self.player.wealth} | "
                    f"Morale: {self.player.morale} | Social: {self.player.social}"
                )

                card = self.get_next_card()

                if self.consequence_next:
                    # Consequence card: show description only, no choice needed
                    print(f"\n{card.description}")
                    # Apply effects from either left or right option — 
                    # your consequence cards have no choices, but if they do effects in both options,
                    # you can pick left_option effects by default or you can adjust this logic if needed.
                    # Assuming no choice on consequence cards, apply combined effects (or left_option by default):

                    # Here, applying effects from left_option as consequences have empty option texts anyway:
                    for stat, value in card.left_option[1].items():
                        if hasattr(self.player, stat):
                            setattr(self.player, stat, getattr(self.player, stat) + value)

                    # Reset flags
                    self.consequence_next = False
                    self.current_consequence_id = None
                    self.age += 1

                    # Check for death
                    if (
                        self.player.vitality <= 0 or self.player.vitality > 100 or
                        self.player.wealth <= 0 or self.player.wealth > 100 or
                        self.player.morale <= 0 or self.player.morale > 100 or
                        self.player.social <= 0 or self.player.social > 100
                    ):
                        print("\n You have passed away this year...")
                        print(f"You lived {self.age} years in this life.")
                        self.show_ending()
                        break

                    continue  # Skip to next iteration to avoid drawing new card

                # Normal card handling
                print(f"\n{card.description}")
                print(f"  1 → {card.left_option[0]}")
                print(f"  0 → {card.right_option[0]}")

                while True:
                    try:
                        choice = int(input("Choose 1 for left and 0 for right: "))
                        if choice not in (0, 1):
                            raise ValueError
                        break
                    except ValueError:
                        print("Please enter a valid choice: 1 or 0")

                # Apply choice effects
                chosen_effect = card.left_option[1] if choice == 1 else card.right_option[1]
                for stat, value in chosen_effect.items():
                    if hasattr(self.player, stat):
                        setattr(self.player, stat, getattr(self.player, stat) + value)

                # If card has multiple consequences, set the appropriate consequence id
                if card.has_consequence and card.consequence_ids:
                    print("\nConsequence of your choice follows...\n")
                    self.consequence_next = True
                    # Pick consequence id matching the choice
                    self.current_consequence_id = card.consequence_ids[0] if choice == 1 else card.consequence_ids[1]
                else:
                    self.consequence_next = False
                    self.current_consequence_id = None
                    self.age += 1

                # Check for death after normal card
                if (
                    self.player.vitality <= 0 or self.player.vitality > 100 or
                    self.player.wealth <= 0 or self.player.wealth > 100 or
                    self.player.morale <= 0 or self.player.morale > 100 or
                    self.player.social <= 0 or self.player.social > 100
                ):
                    print("\n You have passed away this year...")
                    print(f"You lived {self.age} years in this life.")
                    self.show_ending()
                    break

            again = input("Do you want to start a new life? (y/n): ").lower()
            if again in ('y', 'yes'):
                self.reset_player()
            elif again in ('n', 'no'):
                print("Thanks for playing!")
                return
            else:
                print("Invalid input, exiting game.")
                return

    def show_ending(self):
        v = self.player.vitality
        w = self.player.wealth
        m = self.player.morale
        r = self.player.social

        print("\n Final Reflections:")
        if v > 80 and m > 80:
            print(" You lived a fulfilling life, vibrant and joyful. Your legacy is one of warmth.")
        elif w > 80 and m < 30:
            print(" You died rich, but deeply unsatisfied. Money could not buy peace.")
        elif r < 20:
            print(" You passed away with few connections. Loneliness followed you.")
        elif 40 <= v <= 60 and 40 <= w <= 60 and 40 <= m <= 60 and 40 <= r <= 60:
            print(" You lived a balanced, ordinary life. Perhaps your next one will be more eventful.")
        elif m > 85 and r > 85:
            print(" Your kindness and love inspired many. You are remembered dearly.")
        else:
            print(" Your soul returns to the cycle, carrying the echoes of this life.")

    def show_final(self):
        print("You have completed 500 years of existence")
        print("what do you think life is ? lived years or years lived?")
        print("Does not matter now...")
        print("I know you have had your fair share of good and bad moments")
        print("Sometimes you must have felt that time is static while sometimes time moves so fast you barely blink and you have aged")
        print("But now that cycle is over you are back to me")
        print("Thank you for playing")
