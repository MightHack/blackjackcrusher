import tkinter as tk
from tkinter import messagebox

import keyboard as keyboard
from keyboard._keyboard_event import KEY_DOWN, KEY_UP

# Last ten cards list:
last_ten_cards = []

# Global variable to keep track of the current color
current_label_color = 'pink'

# This dictionary will hold the state of whether a key is currently pressed
key_pressed_state = {str(i): False for i in range(2, 10)}
key_pressed_state['0'] = False
key_pressed_state['a'] = False
key_pressed_state['A'] = False


class CardCounting:
    def __init__(self, num_decks=8):
        self.count = 0
        self.num_decks = num_decks
        self.card_frequency = {i: num_decks * 4 for i in range(2, 12)}
        self.card_frequency[10] = 4 * 4 * num_decks  # 10, Jack, Queen, King * 4 sets

    def update_count(self, card_value):
        if self.card_frequency[card_value] > 0:
            if 2 <= card_value <= 6:
                self.count += 1
            elif 10 <= card_value <= 11:
                self.count -= 1
            self.card_frequency[card_value] -= 1
        else:
            messagebox.showinfo("Info", f"No more {card_value}'s left in the decks")

    def reset_count(self, num_decks):
        self.count = 0
        self.card_frequency = {i: self.num_decks * 4 for i in range(2, 12)}
        self.card_frequency[10] = 4 * 4 * int(num_decks.get())  # 10, Jack, Queen, King * 4 sets

    def calculate_house_edge(self):
        remaining_cards = sum(self.card_frequency.values())
        remaining_decks = remaining_cards / 52
        true_count = self.count / remaining_decks
        true_count_label.config(text=f"True Count: {true_count:.2f}")

        # Player's advantage calculation
        # Player gains a 0.5% advantage for each positive true count
        # For negative true count, the house gains an advantage
        player_advantage = true_count * 0.5

        # Adjusting the house edge based on player's advantage
        # The base house edge is 0.61%, and it decreases with player's increasing advantage
        house_edge = 0.6 - player_advantage

        return house_edge  # Convert to percentage


def update_count_button(card_value, num_decks_entry, house_edge_label):
    counter.update_count(card_value)
    count_label.config(text=f"Count: {counter.count}")
    update_house_edge(num_decks_entry, house_edge_label)


def reset_count_button(num_decks_entry, house_edge_label):
    global last_ten_cards  # Use the global list
    count_label.config(text="Count: 0")
    true_count_label.config(text=f"True Count: 0.0")
    update_house_edge(num_decks_entry, house_edge_label)
    update_remaining_cards()  # Add this line to update the remaining cards label
    counter.reset_count(num_decks_entry)
    last_ten_cards.clear()
    update_last_ten_cards_label("")


def update_house_edge(num_decks_entry, house_edge_label):
    try:
        num_decks = int(num_decks_entry.get())
        if num_decks <= 0:
            raise ValueError
        counter.num_decks = num_decks
        house_edge = counter.calculate_house_edge()

        # Set label color based on house edge value
        label_color = 'green' if house_edge < 0 else 'red'

        house_edge_label.config(text=f"House Edge: {house_edge:.2f}%", fg=label_color)
        update_remaining_cards()
    except ValueError:
        messagebox.showwarning("Warning", "Please enter a valid number of decks")


# Function to initialize the last ten cards labels
def initialize_last_ten_cards_labels():
    for _ in range(10):
        label = tk.Label(last_ten_cards_frame, text="", width=2, height=1, bg="#ADD8E6")
        label.pack(side="left", padx=2)
        last_ten_cards_labels.append(label)


def update_last_ten_cards_label(card_value):
    global last_ten_cards  # Use the global list
    # Convert card value to a string representation
    card_str = str(card_value) if card_value != 11 else 'A'

    # Add the card to the list and keep only the last 10
    if card_str:
        last_ten_cards.append(card_str)
    if len(last_ten_cards) > 10:
        last_ten_cards.pop(0)

    # Update each label in the list of last ten cards labels
    for i in range(10):
        card = last_ten_cards[i] if i < len(last_ten_cards) else ""
        last_ten_cards_labels[i].config(text=card)


def update_remaining_cards():
    global current_label_color  # Use the global variable

    # Toggle the color
    if current_label_color == 'pink':
        current_label_color = 'blue'
    else:
        current_label_color = 'pink'

    # Update each label with the current frequency of the corresponding card
    for card_value in counter.card_frequency:
        card_label = remaining_cards_labels[card_value]
        card_label.config(text=f"{counter.card_frequency[card_value]}")

    # Update the text and color of the remaining cards label
    remaining_cards_label.config(text=f"Remaining Cards: {sum(counter.card_frequency.values())}",
                                 fg=current_label_color)


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
        root.after(0, update_count_button, card_value, num_decks_entry, house_edge_label)
        update_last_ten_cards_label(card_value)  # Update the last 10 cards label


if __name__ == '__main__':
    # Create the main window
    root = tk.Tk()
    root.title("Hi-Lo Card Counting Simulator")

    button_frame = tk.Frame(root)
    button_frame.pack()

    # Create an instance of CardCounting
    counter = CardCounting(num_decks=8)

    # Create and configure GUI elements
    count_label = tk.Label(root, text="Count: 0")
    count_label.pack(pady=10)

    true_count_label = tk.Label(root, text="True Count: 0.0")
    true_count_label.pack(pady=10)

    remaining_cards_label = tk.Label(root, text=f"Remaining Cards: ")
    remaining_cards_label.pack(pady=10)

    button_frame = tk.Frame(root)
    button_frame.pack()

    num_decks_entry = tk.Entry(root)
    num_decks_entry.insert(0, "8")
    num_decks_entry.pack()

    house_edge_label = tk.Label(root, text="House Edge: ")
    house_edge_label.pack()

    # Frame for the last ten cards
    last_ten_cards_frame = tk.Frame(root, bg="#ADD8E6")
    last_ten_cards_frame.pack(pady=10)

    # List to hold the label widgets for the last ten cards
    last_ten_cards_labels = []

    # Initialize the last ten cards labels
    initialize_last_ten_cards_labels()

    # Create a dictionary for the remaining cards labels
    remaining_cards_labels = {}

    # Create the card buttons and remaining card labels
    for card_value in range(2, 12):
        # Create a frame for each card button and its label
        card_frame = tk.Frame(button_frame)
        card_frame.pack(side="left", padx=5)

        # Create and pack the label for the remaining cards above the button
        card_remaining_label = tk.Label(card_frame, text=str(counter.card_frequency[card_value]))
        card_remaining_label.pack()

        # Store the label in the dictionary using the card value as the key
        remaining_cards_labels[card_value] = card_remaining_label

        # Create the button for the card
        card_text = 'A' if card_value == 11 else str(card_value)
        button = tk.Button(card_frame, text=card_text, width=3, height=2,
                           command=lambda cv=card_value: update_count_button(cv, num_decks_entry, house_edge_label))
        button.pack()

    # Register the global key down and key up event handlers
    keyboard.hook(lambda e: on_action(e))

    reset_button = tk.Button(root, text="Reset Count",
                             command=lambda: reset_count_button(num_decks_entry, house_edge_label))
    reset_button.pack(pady=10)

    # Start the GUI application
    root.mainloop()
