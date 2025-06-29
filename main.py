# main.py
from game_engine import GameEngine

def main():
    game = GameEngine()
    try:
        game.play()
    except KeyboardInterrupt:
        print("\n Game exited safely. See you in the next life!")

if __name__ == "__main__":
    main()
