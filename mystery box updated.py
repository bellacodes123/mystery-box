from tkinter import *
# To prevent unwanted windows
from functools import partial
import random


class Start:
    def __init__(self, parent):

        # GUI to get starting balence and stakes
        self.start_frame = Frame(padx=10, pady=10)
        self.start_frame.grid()

        self.starting_funds = IntVar()
        self.starting_funds.set(0)

        # Button Frame
        self.button_frame = Frame(padx=10, pady=10)
        self.button_frame.grid(row=3)

        # Mystery Heading
        self.mystery_box_label = Label(self.start_frame, text="Mystery Box Game",
                                       font="Arial 19 bold")
        self.mystery_box_label.grid(row=1)

        # Entry box.. (row 1)
        self.entry_error_frame = Frame(self.start_frame, width=200)
        self.entry_error_frame.grid(row=3)

        self.start_amount_entry = Entry(self.start_frame, font="Arial 16 bold")
        self.start_amount_entry.grid(row=2)

        self.add_funds_button = Button(self.start_frame, text="Add Funds",
                                       font="Arial 19 bold", width=10,
                                       command=self.check_funds)
        self.add_funds_button.grid(row=2, column=1)

        self.amount_error_label = Label(self.entry_error_frame, text=" ", font="Arial 12 bold")
        self.amount_error_label.grid(row=2)

        # Play Button (row 2)
        self.low_stakes_button = Button(self.button_frame, text="Low ($5)", highlightbackground="purple",
                                        command=lambda: self.to_game(1))
        self.low_stakes_button.grid(row=0, column=0, pady=10)

        self.mid_stakes_button = Button(self.button_frame, text="Mid ($10)", highlightbackground="light pink",
                                        command=lambda: self.to_game(2))
        self.mid_stakes_button.grid(row=0, column=1, pady=10)

        self.high_stakes_button = Button(self.button_frame, text="High ($15)", highlightbackground="light blue",
                                         command=lambda: self.to_game(3))
        self.high_stakes_button.grid(row=0, column=2, pady=10)

        # How to play button
        self.how_to_play_button = Button(self.button_frame, text="How to Play", highlightbackground="Magenta",
                                         command=lambda: self.instructions())
        self.how_to_play_button.grid(row=2, column=1, pady=10)

        self.low_stakes_button.config(state=DISABLED)
        self.mid_stakes_button.config(state=DISABLED)
        self.high_stakes_button.config(state=DISABLED)


    def instructions(self):
        how_to_play = Instructions(self)
        how_to_play.play_text.configure(text="Please enter a number in the box"
                                          " then push one of the buttons to "
                                          " convert the number to either C or "
                                          "degrees F. "
                                          " The calculation History area shows up "
                                          "the seven most recent calculations."
                                          " You can also export your calculation history "
                                          "to a text file if desired.")

    def check_funds(self):
        starting_balance = self.start_amount_entry.get()

        # Set error background colors, assume no errors at start
        error_back = "#ffafaf"
        has_errors = "no"

        # change background to white (for testing)
        self.start_amount_entry.config(bg="white")
        self.amount_error_label.config(text=" ")

        # Disable all stakes buttons in case user changes mind
        self.low_stakes_button.config(state=DISABLED)
        self.mid_stakes_button.config(state=DISABLED)
        self.high_stakes_button.config(state=DISABLED)

        try:
            starting_balance = int(starting_balance)

            if starting_balance < 5:
                has_errors = "yes"
                error_feedback = "Sorry, the least you can play is $5"

            elif starting_balance > 50:
                has_errors = "yes"
                error_feedback = "Too High! The most you can risk is $50"

            elif starting_balance >= 15:
                # enable all buttons
                self.low_stakes_button.config(state=NORMAL)
                self.mid_stakes_button.config(state=NORMAL)
                self.high_stakes_button.config(state=NORMAL)

            elif starting_balance >= 10:
                self.low_stakes_button.config(state=NORMAL)
                self.mid_stakes_button.config(state=NORMAL)

            else:
                self.low_stakes_button.config(state=NORMAL)

        except ValueError:
            has_errors = "yes"
            error_feedback = "Please enter a dollar amount (not text/decimals)"

        if has_errors == "yes":
            self.start_amount_entry.config(bg=error_back)
            self.amount_error_label.config(text=error_feedback)

        else:
            self.starting_funds.set(starting_balance)

    def to_game(self, stakes):
        starting_balance = self.start_amount_entry.get()
        Game(self, stakes, starting_balance)
        root.withdraw()


class Game:
    def __init__(self, partner, stakes, starting_balance):
        print(stakes)
        print(starting_balance)

        partner.low_stakes_button.config(state=DISABLED)

        # Initalise variables
        self.balance = IntVar()

        # Set up starting balance to amount entered by user at start of game
        self.balance.set(starting_balance)

        self.multiplier = IntVar()
        self.multiplier.set(stakes)

        # GUI setup
        self.game_box = Toplevel()
        self.game_frame = Frame(self.game_box)
        self.game_frame.grid()

        # GUI Heading
        self.heading_label = Label(self.game_frame, text="Play...",
                                   font="Arial 24 bold", padx=10, pady=10)
        self.heading_label.grid(row=0)

        # Balance label
        self.balance_frame = Frame(self.game_frame)
        self.balance_frame.grid(row=1)

        self.help_stats_frame = Frame(self.game_frame)
        self.help_stats_frame.grid(row=5)

        self.balance_label = Label(self.game_frame, text="Balance...")
        self.balance_label.grid(row=2)

        self.play_button = Button(self.game_frame, text="Open Boxes", padx=10, pady=10, command=self.reveal_boxes,
                                  highlightbackground="blue")
        self.play_button.focus()
        self.play_button.bind('<Return>', lambda e: self.reveal_boxes())
        self.play_button.grid(row=3)

        self.help_button = Button(self.help_stats_frame, text="Help/Rules", padx=10, pady=10,
                                  highlightbackground="pink")
        self.help_button.grid(row=0, column=0, pady=10)

        self.game_stats_button = Button(self.help_stats_frame, text="Game Stats", padx=10, pady=10,
                                        highlightbackground="pink")
        self.game_stats_button.grid(row=0, column=2, pady=0)

        self.quit_button = Button(self.game_frame, text="Quit", padx=10, pady=10, command=self.to_quit,
                                  highlightbackground="red")
        self.quit_button.grid(row=6, padx=10)

        # gain button (row 2)
        self.gain_button = Button(text="Low ($5)",
                                       command=lambda: self.reveal_boxes())
        self.gain_button.grid(row=2, pady=10)


        box_width = 5
        self.box_frame = Frame(self.game_frame)
        self.box_frame.grid(row=2, pady=10)
        box_text ="arial 12 bold"

        self.prize1_label = Label(self.box_frame, text="?\n", font="arial 12 bold",
                                  bg= "light pink", width=box_width, padx=10, pady=10)
        self.prize1_label.grid(row=0, column=0)

        self.prize2_label = Label(self.box_frame, text="?\n", font=box_text,
                                  bg= "light pink", width=box_width, padx=10, pady=10)
        self.prize2_label.grid(row=0, column=1, padx=10)

        self.prize3_label = Label(self.box_frame, text="?\n", font=box_text,
                                  bg= "light pink", width=box_width, padx=10, pady=10)
        self.prize3_label.grid(row=0, column=2)


    def reveal_boxes(self):
        # retrives the balance from the inital function...
        current_balance = self.balance.get()
        stakes_multiplier = self.multiplier.get()

        round_winnings = 0
        prizes = []
        backgrounds = []
        for item in range(0, 3):
            prize_num = random.randint(1, 100)

            if 0 < prize_num <=5:
                prize = "gold\n(${})".format(5* stakes_multiplier)
                back_color = "#CEA935"
                round_winnings += 5 * stakes_multiplier
            elif 5 < prize_num <= 25:
                prize = "silver\n(${})".format(2* stakes_multiplier)
                back_color = "#B7B7B5"
                round_winnings += 2 * stakes_multiplier
            elif 25 < prize_num <= 65:
                prize = "copper\n(${})".format(1* stakes_multiplier)
                back_color = "#BC7F61"
                round_winnings += stakes_multiplier
            else:
                prize = "lead\n($0)"
                back_color = "#595E71"

            prizes.append(prize)
            backgrounds.append(back_color)
        # Display prizes
        self.prize1_label.config(text=prizes[0], bg=backgrounds[0])
        self.prize2_label.config(text=prizes[1], bg=backgrounds[1])
        self.prize3_label.config(text=prizes[2], bg=backgrounds[2])

        # deduct cost of game.
        current_balance -= 5 * stakes_multiplier

        # add winnings
        current_balance += round_winnings

        self.balance.set(current_balance)

        balance_statement = "Game Cost: ${}\n Payback: ${} \n"\
                            "Current Balance: ${}".format(5* stakes_multiplier,
                                                          round_winnings, current_balance)

        self.balance_label.configure(text=balance_statement)
        self.balance_label.grid(row=4)

        if current_balance < 5 * stakes_multiplier:
            self.play_button.config(state=DISABLED)
            self.game_box.focus()
            self.play_button.config(text="Game Over")

            balance_statement = "Current Balance: ${}\n" \
                                "Your Balance is too low. You can only quit, or view stats." \
                                " Sorry about that.".format(current_balance)
            self.balance_label.config(fg="#660000", font="Arial 10 bold",
                                      text=balance_statement)



    def to_quit(self):
        root.destroy()


class Instructions:
    def __init__(self, partner):

        background = "pink"

        # disbable help button
        partner.how_to_play_button.config(state=DISABLED)

        # sets up child window help box
        self.how_to_play_box = Toplevel()
        # If users press cross at to, closes help and 'releases' help button
        self.how_to_play_box.protocol('WM_DELETE_WINDOW', partial(self.close_how_to_play, partner))

        # set up GUI Frame
        self.how_to_play_frame = Frame(self.how_to_play_box, bg=background)
        self.how_to_play_frame.grid()

        # set up Help heading (row 0)
        self.how_heading = Label(self.how_to_play_frame, text="Instructions",
                                 font="arial 14 bold", bg=background)
        self.how_heading.grid(row=0)

    def close_how_to_play(self, partner):
        partner.how_to_play_button.config(state=NORMAL)
        self.how_to_play_box.destroy()

# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Mystery Box")
    something = Start(root)
    root.mainloop()







