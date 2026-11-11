
#!/usr/bin/env python3

import random
import os
import sys

WORDS = {
    "Places": [
        "Airport", "Beach", "Castle", "Desert", "Forest",
        "Hospital", "Hotel", "Island", "Library", "Mountain",
        "Museum", "School", "Stadium", "Train Station",
        "Volcano", "Zoo"
    ],
    "Food": [
        "Apple", "Burger", "Chocolate", "Coffee", "Ice Cream",
        "Pancake", "Pizza", "Popcorn", "Sushi", "Taco"
    ],
    "Objects": [
        "Camera", "Computer", "Guitar", "Headphones",
        "Microwave", "Phone", "Piano", "Skateboard",
        "Television", "Umbrella"
    ],
    "Animals": [
        "Cat", "Dolphin", "Elephant", "Penguin",
        "Shark", "Snake", "Tiger", "Turtle"
    ],
    "Transport": [
        "Airplane", "Bicycle", "Bus", "Ferry",
        "Helicopter", "Subway", "Taxi", "Train"
    ]
}


def clear():
    # ANSI escape sequences work in iSH.
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()


def pause(message="Press ENTER to continue..."):
    input(message)


def get_number(prompt, minimum, maximum):
    while True:
        try:
            value = int(input(prompt))

            if minimum <= value <= maximum:
                return value

            print(f"Enter a number from {minimum} to {maximum}.")

        except ValueError:
            print("Please enter a valid number.")


def setup():
    clear()

    print("=" * 30)
    print("       IMPOSTER CLI")
    print("=" * 30)

    count = get_number("\nNumber of players (3-20): ", 3, 20)

    players = []

    for i in range(count):
        name = input(f"Player {i + 1} name: ").strip()

        if not name:
            name = f"Player {i + 1}"

        players.append(name)

    max_imposters = min(3, count - 1)

    imposters_count = get_number(
        f"\nNumber of imposters (1-{max_imposters}): ",
        1,
        max_imposters
    )

    return players, imposters_count


def assign_roles(players, imposters_count):
    category = random.choice(list(WORDS.keys()))
    word = random.choice(WORDS[category])

    imposters = set(random.sample(range(len(players)), imposters_count))

    roles = []

    for i in range(len(players)):
        if i in imposters:
            roles.append("IMPOSTER")
        else:
            roles.append(word)

    return roles, word, category, imposters


def reveal_roles(players, roles, category):
    for i, player in enumerate(players):
        clear()

        print("=" * 30)
        print(f"       PLAYER {i + 1}")
        print("=" * 30)

        print(f"\nGive the phone to {player}.")

        pause("\nPress ENTER when ready to reveal your role...")

        clear()

        print(f"\n{player}, your secret role is:\n")

        if roles[i] == "IMPOSTER":
            print("YOU ARE THE IMPOSTER!")
            print(f"Category: {category}")
            print("\nTry to blend in.")
        else:
            print(f"SECRET WORD: {roles[i].upper()}")
            print("\nGive clues without revealing the word.")

        pause()

        # Hide the role immediately.
        clear()

    print("Everyone has seen their role.")
    pause()


def clue_round(players):
    clear()

    print("=" * 30)
    print("          CLUE ROUND")
    print("=" * 30)

    print("\nEveryone gives one clue.")
    print("Do NOT say the secret word.")

    pause()

    order = list(players)
    random.shuffle(order)

    for player in order:
        clear()

        print(f"\n{player}'s turn to give a clue.")

        pause("Press ENTER when ready...")

    clear()


def voting_round(players):
    clear()

    print("=" * 30)
    print("           VOTING")
    print("=" * 30)

    votes = {}

    for player in players:
        clear()

        print(f"\n{player}, it's your turn to vote.")

        for i, candidate in enumerate(players, 1):
            print(f"{i}. {candidate}")

        vote = get_number(
            "\nWho is the imposter? ",
            1,
            len(players)
        )

        target = players[vote - 1]

        votes[target] = votes.get(target, 0) + 1

    highest = max(votes.values())

    eliminated = [
        player for player, count in votes.items()
        if count == highest
    ]

    clear()

    if len(eliminated) > 1:
        print("IT'S A TIE!")
        print("Nobody was eliminated.")

        return None

    print(f"The group voted out: {eliminated[0]}")

    return eliminated[0]


def play():
    players, imposters_count = setup()

    roles, word, category, imposters = assign_roles(
        players,
        imposters_count
    )

    reveal_roles(players, roles, category)

    clue_round(players)

    eliminated = voting_round(players)

    clear()

    print("=" * 30)
    print("         GAME RESULTS")
    print("=" * 30)

    if eliminated is None:
        print("\nNobody was eliminated.")
        print(f"The secret word was: {word}")

        return

    eliminated_index = players.index(eliminated)

    if eliminated_index in imposters:
        print(f"\n{eliminated} WAS AN IMPOSTER!")

        if imposters_count == 1:
            guess = input(
                "\nThe imposter gets one chance to guess the word: "
            ).strip()

            if guess.lower() == word.lower():
                print("\nThe imposter guessed correctly!")
                print("IMPOSTER WINS!")
            else:
                print(f"\nWrong! The word was {word}.")
                print("THE GROUP WINS!")

        else:
            print(f"\nThe secret word was: {word}")
            print("THE GROUP WINS!")

    else:
        print(f"\n{eliminated} WAS NOT AN IMPOSTER!")

        print("\nThe imposters win!")

        print("\nThe imposters were:")

        for i in imposters:
            print(f"- {players[i]}")

        print(f"\nThe secret word was: {word}")


def main():
    while True:
        play()

        pause("\nPress ENTER to return to the menu...")

        clear()

        again = input("Play again? (y/n): ").strip().lower()

        if again != "y":
            print("\nThanks for playing!")
            break


if __name__ == "__main__":
    main()

