import random

def create_deck():
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
    deck = [f'{rank} of {suit}' for suit in suits for rank in ranks]
    return deck

def shuffle_deck(deck):
    random.shuffle(deck)

def print_deck(deck):
    for card in deck:
        print(card)

def main():
    deck = create_deck()
    print("Original Deck:")
    print_deck(deck)
    
    shuffle_deck(deck)
    print("\nShuffled Deck:")
    print_deck(deck)

if __name__ == "__main__":
    main()
