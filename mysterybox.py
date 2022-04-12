from tkinter import *
from functools import partial # To prevent unwanted windows
import random

class Start:
    def __init__(self, parent):

        # GUI to get starting balence and stakes
        self.start_frame = Frame(padx=10, pady=10)
        self.start_frame.grid()

        # Mystery Heading
        self.mystery_box_label = Label(self.start_frame, text="Mystery Box Game",
                                       font="Arial 19 bold")
        self.mystery_box_label.grid(row=1)

        # Entry box.. (row 1)
        self.start_amount_entry = Entry(self.start_frame, font="Arial 16 bold")
        self.start_amount_entry.grid(row=2)

        # Play Button (row 2)
        self.lowstakes_button = Button(text="Low ($5)",
                                       command=lambda: self.to_game(1))
        self.lowstakes_button.grid(row=2, pady=10)

    def to_game(self, stakes):
        starting_balance = self.start_amount_entry.get()
        Game(self, stakes, starting_balance)
        root.withdraw()

class Game:
    def __init__(self, partner, stakes, starting_balance):
        print(stakes)
        print(starting_balance)

        partner.lowstakes_button.config(state=DISABLED)

        # Initalise variables
        self.balance = IntVar()

        # Set up starting balance to amount entered by user at start of game
        self.balance.set(starting_balance)

        # GUI setup
        self.game_box = Toplevel()
        self.game_frame = Frame(self.game_box)
        self.game_frame.grid()

        # GUI Heading
        self.heading_label = Label(self.game_frame, text="Heading",
                                   font="Arial 24 bold", padx=10, pady=10)
        self.heading_label.grid(row=0)

        # Balance label

        # gain button (row 2)
        self.gain_button = Button(text="Low ($5)",
                                       command=lambda: self.reveal_boxes)
        self.gain_button.grid(row=2, pady=10)

    def reveal_boxes(self):
        # retrives the balance from the initaol function...
        current_balance = self.balance.get()

        # adjust the balance (subtract game cost and add pay out)
        # For testing purposes add 2
        current_balance += 2
        self.balance.set(current_balance)

        # edit label to user can see their balance
        self.balance_label.configure(text="Balance: {}".format(current_balance))

# main routine
if __name__ == "__main__":
    root = Tk()
    root.title = "Mystery Box Game"
    something = Start(root)
    root.mainloop()







