from tkinter import 
import random
from PIL import Image, ImageTk
import os

# Initialize the main window
root = Tk()
root.title('Codemy.com - Card Deck')
root.iconbitmap('c:/gui/codemy.ico')
root.geometry("900x500")
root.configure(background="green")

# Path to the card images
card_image_path = 'images/cards/'

def resize_cards(card_image):
    """Resize the card image and return it as a PhotoImage object."""
    with Image.open(card_image) as img:
        resized_image = img.resize((150, 218))
        return ImageTk.PhotoImage(resized_image)

def shuffle():
    """Shuffle the deck and display one card for dealer and one for player."""
    global deck, dealer, player, dealer_image, player_image

    suits = ["diamonds", "clubs", "hearts", "spades"]
    values = range(2, 15)  # 2 to 14 (Jack, Queen, King, Ace)

    deck = [f'{value}_of_{suit}' for suit in suits for value in values]
    dealer = []
    player = []

    def deal_one_card(for_who):
        """Deal one card to the specified player (dealer or player) and update the display."""
        if deck:
            card = random.choice(deck)
            deck.remove(card)
            if for_who == 'dealer':
                dealer.append(card)
                image = resize_cards(os.path.join(card_image_path, f'{card}.png'))
                dealer_label.config(image=image)
                global dealer_image
                dealer_image = image
            elif for_who == 'player':
                player.append(card)
                image = resize_cards(os.path.join(card_image_path, f'{card}.png'))
                player_label.config(image=image)
                global player_image
                player_image = image

            root.title(f'Codemy.com - {len(deck)} Cards Left')
        else:
            root.title('Codemy.com - No Cards In Deck')

    deal_one_card('dealer')
    deal_one_card('player')

def deal_cards():
    """Deal one card to both dealer and player."""
    try:
        shuffle()
    except Exception as e:
        print(f"An error occurred: {e}")
        root.title('Codemy.com - Error Occurred')

# Create UI Frames and Buttons
my_frame = Frame(root, bg="green")
my_frame.pack(pady=20)

dealer_frame = LabelFrame(my_frame, text="Dealer", bd=0)
dealer_frame.grid(row=0, column=0, padx=20, ipadx=20)

player_frame = LabelFrame(my_frame, text="Player", bd=0)
player_frame.grid(row=0, column=1, ipadx=20)

dealer_label = Label(dealer_frame, text='')
dealer_label.pack(pady=20)

player_label = Label(player_frame, text='')
player_label.pack(pady=20)

shuffle_button = Button(root, text="Shuffle Deck", font=("Helvetica", 14), command=shuffle)
shuffle_button.pack(pady=20)

card_button = Button(root, text="Get Cards", font=("Helvetica", 14), command=deal_cards)
card_button.pack(pady=20)

# Shuffle Deck On Start
shuffle()

root.mainloop()
