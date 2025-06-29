import random
from core.player import Player
from core.card import Card


class GameEngine:
    def __init__(self):
        self.player = None
        self.cards = self.load_sample_cards()
        self.age = 1
        self.consequence_next = False

    def reset_player(self):
        print(
            "\nNow open your eyes as your soul is brought to life. I am the one who has created everything and I am giving you "
            "a chance to experience my creation. You shall inhabit mortal bodies and continue in the cycle of birth and rebirth, "
            "but of course it is not that simple. You must keep track of your virtues which will determine your lifespan: Vitality, Morale, "
            "Relations, and Funds. Always keep them in balance — too little or too low and you die. Life will give you options and each step "
            "your choice would be 1 for left option or 0 for the right one. Make your decisions wisely and I will meet you after 500 years."
        )
        name = input("\nWhat shall be your name, mortal? ").strip()
        gender = input("What gender do you identify as? ").strip()
        self.player = Player(name, gender)
        self.age = 1

    def load_sample_cards(self):
        return [
            # Childhood (1–12)
            Card(
                id=1,
                description="You find a stray dog on the street.",
                left_option=("Adopt it", {"morale": +5, "social": +2}),
                right_option=("Ignore it", {"morale": -1}),
                age_range=(1, 12),
                has_consequence=False
            ),
            Card(
                id=4,
                description="You struggle to make friends in school.",
                left_option=("Try harder", {"social": +5}),
                right_option=("Stay quiet", {"morale": -3}),
                age_range=(6, 12),
                has_consequence=False
            ),

            # Youth (13–25)
            Card(
                id=2,
                description="You are offered a dangerous job for lots of money.",
                left_option=("Accept it", {"wealth": +10, "vitality": -10}),
                right_option=("Decline", {"wealth": -2}),
                age_range=(18, 25),
                has_consequence=True
            ),
            Card(
                id=5,
                description="You develop a new hobby and make new friends.",
                left_option=("Join a club", {"morale": +4, "social": +3}),
                right_option=("Ignore it", {"morale": -2}),
                age_range=(13, 25),
                has_consequence=False
            ),

            # Adulthood (26–60)
            Card(
                id=6,
                description="You consider investing in a new business.",
                left_option=("Invest boldly", {"wealth": +15, "morale": +3, "vitality": -5}),
                right_option=("Play it safe", {"wealth": +2}),
                age_range=(30, 60),
                has_consequence=False
            ),
            Card(
                id=7,
                description="Your relationship is going through a rough patch.",
                left_option=("Work on it", {"social": +5, "morale": -2}),
                right_option=("End it", {"morale": +2, "social": -5}),
                age_range=(26, 60),
                has_consequence=False
            ),

            # Old Age (61–99)
            Card(
                id=8,
                description="You reflect on your life choices.",
                left_option=("Cherish the memories", {"morale": +10}),
                right_option=("Dwell on regrets", {"morale": -10}),
                age_range=(61, 99),
                has_consequence=False
            ),
            Card(
                id=9,
                description="You are asked to mentor a young soul.",
                left_option=("Accept", {"social": +5, "morale": +5}),
                right_option=("Decline", {"social": -3}),
                age_range=(65, 99),
                has_consequence=False
            ),

            # Consequence card (used by ID)
            Card(
                id=99,
                description="The job was more dangerous than expected. You're seriously injured.",
                left_option=("Take time off", {"vitality": -20, "wealth": -5}),
                right_option=("Push through", {"morale": -15, "vitality": -10}),
                age_range=(1, 99),
                has_consequence=False
            ),
        ]

    def get_next_card(self):
        if self.consequence_next:
            for card in self.cards:
                if card.id == 99:
                    return card

        available = [
            card for card in self.cards
            if card.age_range is None or (self.age >= card.age_range[0] and self.age <= card.age_range[1])
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

                effect = card.get_effect(choice)
                for stat, value in effect.items():
                    if hasattr(self.player, stat):
                        setattr(self.player, stat, getattr(self.player, stat) + value)

                # Check for consequence card
                if card.has_consequence:
                    print("\n⚠️ Consequence of your choice follows...\n")
                    consequence_card = next((c for c in self.cards if c.id == 99), None)
                    if consequence_card:
                        print(f"{consequence_card.description}")
                        print(f"  1 → {consequence_card.left_option[0]}")
                        print(f"  0 → {consequence_card.right_option[0]}")

                        while True:
                            try:
                                followup_choice = int(input("Choose 1 for left and 0 for right: "))
                                if followup_choice not in (0, 1):
                                    raise ValueError
                                break
                            except ValueError:
                                print("Please enter a valid choice: 1 or 0")

                        followup_effect = consequence_card.get_effect(followup_choice)
                        for stat, value in followup_effect.items():
                            if hasattr(self.player, stat):
                                setattr(self.player, stat, getattr(self.player, stat) + value)

                self.consequence_next = False
                self.age += 1

                if (
                    self.player.vitality <= 0 or self.player.vitality > 100 or
                    self.player.wealth <= 0 or self.player.wealth > 100 or
                    self.player.morale <= 0 or self.player.morale > 100 or
                    self.player.social <= 0 or self.player.social > 100
                ):
                    print("\n💀 You have passed away this year...")
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

        print("\n🧾 Final Reflections:")
        if v > 80 and m > 80:
            print("✨ You lived a fulfilling life, vibrant and joyful. Your legacy is one of warmth.")
        elif w > 80 and m < 30:
            print("💼 You died rich, but deeply unsatisfied. Money could not buy peace.")
        elif r < 20:
            print("😔 You passed away with few connections. Loneliness followed you.")
        elif 40 <= v <= 60 and 40 <= w <= 60 and 40 <= m <= 60 and 40 <= r <= 60:
            print("🌀 You lived a balanced, ordinary life. Perhaps your next one will be more eventful.")
        elif m > 85 and r > 85:
            print("🎉 Your kindness and love inspired many. You are remembered dearly.")
        else:
            print("🔚 Your soul returns to the cycle, carrying the echoes of this life.")






