from tkinter import messagebox
import tkinter as tk

# Global variable to keep track of the current color
import keyboard
from keyboard import KEY_DOWN, KEY_UP

current_label_color = 'pink'

# This dictionary will hold the state of whether a key is currently pressed
key_pressed_state = {str(i): False for i in range(2, 10)}
key_pressed_state['0'] = False
key_pressed_state['a'] = False
key_pressed_state['A'] = False


class Game:
    def __init__(self, num_decks=8):
        self.num_decks = num_decks
        self.cards_seen = []
        self.count = 0
        self.true_count = 0.0
        self.remaining_cards = 0
        self.remaining_decks = 0.0
        self.house_edge = 0.0
        self.card_frequency = {i: num_decks * 4 for i in range(2, 12)}
        self.card_frequency[10] = 4 * 4 * num_decks  # 10, Jack, Queen, King * 4 sets

    def remove_card(self):
        if len(self.cards_seen) > 0:
            card_removed_value = self.cards_seen.pop()
            if self.card_frequency[card_removed_value] > 0:
                if 2 <= card_removed_value <= 6:
                    self.count -= 1
                elif 10 <= card_removed_value <= 11:
                    self.count += 1
                self.card_frequency[card_removed_value] += 1
                refresh_last_ten_cards_gui()  # Refresh the GUI for last ten cards
            else:
                messagebox.showinfo("Info", f"No more {card_removed_value}'s left in the decks")
        else:
            messagebox.showinfo("Info", "No cards to remove")

    def add_card(self, card_value):
        self.cards_seen.append(card_value)
        if self.card_frequency[card_value] > 0:
            if 2 <= card_value <= 6:
                self.count += 1
            elif 10 <= card_value <= 11:
                self.count -= 1
            self.card_frequency[card_value] -= 1
        else:
            messagebox.showinfo("Info", f"No more {card_value}'s left in the decks")

    def reset_count(self, num_decks):
        self.cards_seen.clear()
        self.count = 0
        self.card_frequency = {i: self.num_decks * 4 for i in range(2, 12)}
        self.card_frequency[10] = 4 * 4 * int(num_decks.get())  # 10, Jack, Queen, King * 4 sets

    def calculate_house_edge(self):
        self.remaining_cards = sum(self.card_frequency.values())
        self.remaining_decks = self.remaining_cards / 52
        self.true_count = self.count / self.remaining_decks

        # Player's advantage calculation
        # Player gains a 0.5% advantage for each positive true count
        # For negative true count, the house gains an advantage
        player_advantage = self.true_count * 0.5

        # Adjusting the house edge based on player's advantage
        # The base house edge is 0.61%, and it decreases with player's increasing advantage
        self.house_edge = 0.6 - player_advantage

        return self.house_edge  # Convert to percentage

    def reset(self, num_decks):
        self.num_decks = 8
        self.cards_seen = []
        self.count = 0
        self.true_count = 0.0
        self.remaining_cards = 0
        self.remaining_decks = 0.0
        self.house_edge = 0.0
        self.card_frequency = {i: num_decks * 4 for i in range(2, 12)}
        self.card_frequency[10] = 4 * 4 * num_decks  # 10, Jack, Queen, King * 4 sets


# Function to initialize the last ten cards labels
def initialize_last_ten_cards_labels_gui():
    for _ in range(10):
        label = tk.Label(last_ten_cards_frame, text="", width=2, height=1, bg="#ADD8E6")
        label.pack(side="left", padx=2)
        last_ten_cards_labels.append(label)


def refresh_last_ten_cards_gui():
    # Clear all labels first
    for label in last_ten_cards_labels:
        label.config(text="")

    # Get the last ten cards (or fewer if less than ten have been seen)
    last_ten_cards = game.cards_seen[-10:]

    # Start filling the labels from the right
    start_index = len(last_ten_cards_labels) - len(last_ten_cards)
    for i, card in enumerate(last_ten_cards):
        last_ten_cards_labels[start_index + i].config(text=str(card))


def update_house_edge_gui(num_decks_entry, house_edge_label):
    try:
        num_decks = int(num_decks_entry.get())
        if num_decks <= 0:
            raise ValueError
        game.num_decks = num_decks
        game.calculate_house_edge()  # Ensure house edge is recalculated
        house_edge = game.house_edge

        # Set label color based on house edge value
        label_color = 'green' if house_edge < 0 else 'red'

        house_edge_label.config(text=f"House Edge: {house_edge:.2f}%", fg=label_color)
        update_remaining_cards_gui()
    except ValueError:
        messagebox.showinfo("Error", "Number of decks must be a positive integer")


def update_remaining_cards_gui():
    global current_label_color  # Use the global variable

    # Toggle the color
    if current_label_color == 'pink':
        current_label_color = 'blue'
    else:
        current_label_color = 'pink'

    # Update each label with the current frequency of the corresponding card
    for card_value in game.card_frequency:
        card_label = remaining_cards_labels[card_value]
        card_label.config(text=f"{game.card_frequency[card_value]}")

    # Update the text and color of the remaining cards label
    remaining_cards_label.config(text=f"Remaining Cards: {sum(game.card_frequency.values())}",
                                 fg=current_label_color)


def add_card_button(card_value, num_decks_entry, house_edge_label):
    game.add_card(card_value)
    update_house_edge_gui(num_decks_entry, house_edge_label)
    count_label.config(text=f"Count: {game.count}")
    true_count_label.config(text=f"True Count: {game.true_count:.2f}%")
    update_last_ten_cards_gui()  # Update the last ten cards display
    update_remaining_cards_labels_gui()


def update_remaining_cards_labels_gui():
    # Clear all labels first
    for label in last_ten_cards_labels:
        label.config(text="")

    # Get the last ten cards (or fewer if less than ten have been seen)
    last_ten_cards = game.cards_seen[-10:]

    # Start filling the labels from the right
    start_index = len(last_ten_cards_labels) - len(last_ten_cards)
    for i, card in enumerate(last_ten_cards):
        last_ten_cards_labels[start_index + i].config(text=str(card))


def update_last_ten_cards_gui():
    # Clear all labels first
    for label in last_ten_cards_labels:
        label.config(text="")

    # Update labels with the last ten cards, if available
    for i, card in enumerate(reversed(game.cards_seen[-10:])):
        last_ten_cards_labels[i].config(text=str(card))


def reset_remaining_cards_labels_gui():
    for card_value in game.card_frequency:
        card_label = remaining_cards_labels[card_value]
        card_label.config(text=str(game.card_frequency[card_value]))


def on_action(event):
    if event.event_type == KEY_DOWN:
        on_key_down(event)

    elif event.event_type == KEY_UP:
        on_key_up(event)


def on_key_down(e):
    # This function is called when a key is pressed down
    if not key_pressed_state.get(e.name, False):  # If the key was not already pressed
        key_pressed_state[e.name] = True  # Set the key state as pressed
        on_key_event(e)  # Call the key event handler


def on_key_up(e):
    # This function is called when a key is released
    key_pressed_state[e.name] = False  # Reset the key state


def on_key_event(e):
    # Map the key to the card value
    key_to_card = {
        '2': 2, '3': 3, '4': 4, '5': 5,
        '6': 6, '7': 7, '8': 8, '9': 9, '0': 10,
        'a': 11, 'A': 11
    }

    card_value = key_to_card.get(e.name)

    if card_value:
        root.after(0, add_card_button, card_value, num_decks_entry, house_edge_label)


def reset_game_and_gui():
    game.reset(num_decks=int(num_decks_entry.get()))
    count_label.config(text=f"Count: {game.count}")
    true_count_label.config(text=f"True Count: {game.true_count:.2f}%")
    remaining_cards_label.config(text=f"Remaining Cards: {game.remaining_cards}")
    house_edge_label.config(text=f"House Edge: {game.house_edge}")
    update_last_ten_cards_gui()  # Reset the last ten cards display
    update_remaining_cards_labels_gui()
    reset_remaining_cards_labels_gui()


if __name__ == '__main__':
    # Create the main window
    root = tk.Tk()
    root.title("Hi-Lo Card Counting Simulator")

    button_frame = tk.Frame(root)
    button_frame.pack()

    # Create an instance of Game
    game = Game(num_decks=8)

    # Create and configure GUI elements
    count_label = tk.Label(root, text=f"Count: {game.count}")
    count_label.pack(pady=10)

    true_count_label = tk.Label(root, text=f"True Count: {game.true_count:.2f}%")

    true_count_label.pack(pady=10)

    remaining_cards_label = tk.Label(root, text=f"Remaining Cards: {game.remaining_cards}")
    remaining_cards_label.pack(pady=10)

    button_frame = tk.Frame(root)
    button_frame.pack()

    num_decks_entry = tk.Entry(root)
    num_decks_entry.insert(0, f"{game.num_decks}")
    num_decks_entry.pack()

    house_edge_label = tk.Label(root, text=f"House Edge: {game.house_edge}")
    house_edge_label.pack()

    # Frame for the last ten cards
    last_ten_cards_frame = tk.Frame(root, bg="#ADD8E6")
    last_ten_cards_frame.pack(pady=10)

    # List to hold the label widgets for the last ten cards
    last_ten_cards_labels = []

    # Initialize the last 10 cards labels on GUI
    initialize_last_ten_cards_labels_gui()

    # Create a dictionary for the remaining cards labels
    remaining_cards_labels = {}

    # Create the card buttons and remaining card labels
    for card_value in range(2, 12):
        # Create a frame for each card button and its label
        card_frame = tk.Frame(button_frame)
        card_frame.pack(side="left", padx=5)

        # Create and pack the label for the remaining cards above the button
        card_remaining_label = tk.Label(card_frame, text=str(game.card_frequency[card_value]))
        card_remaining_label.pack()

        # Store the label in the dictionary using the card value as the key
        remaining_cards_labels[card_value] = card_remaining_label

        # Create the button for the card
        card_text = 'A' if card_value == 11 else str(card_value)
        button = tk.Button(card_frame, text=card_text, width=3, height=2,
                           command=lambda cv=card_value: add_card_button(cv, num_decks_entry, house_edge_label))
        button.pack()

    # Register the global key down and key up event handlers
    keyboard.hook(lambda e: on_action(e))

    reset_button = tk.Button(root, text="Reset Count",
                             command=lambda: reset_game_and_gui())
    reset_button.pack(pady=10)

    # Button to remove the last card
    remove_last_card_button = tk.Button(root, text="Remove Last Card",
                                        command=lambda: [game.remove_card(), refresh_last_ten_cards_gui()])
    remove_last_card_button.pack(pady=10)

    # Start the GUI application
    root.mainloop()
