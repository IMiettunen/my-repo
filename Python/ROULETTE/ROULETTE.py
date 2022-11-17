"""
COMP.CS.100 Ohjelmointi 1
Ilari Miettunen
Ilari.miettunen@tuni.fi
opiskelijanumero: 050371213
RULETTI.
"""
from tkinter import *
import random
import time
from tkinter import simpledialog
import math
import winsound


class Roulette:
    def __init__(self):

        self.__mw = Tk()
        self.__mw.geometry("400x200+500+200")
        self.__mw.title("ROULETTE")
        self.__mw.option_add("*Font", "Helvetica 10")

        self.__images = []
        for i in range(0, 41):
            new_image = PhotoImage(file=f"{i}.PNG")
            self.__images.append(new_image)

        background_label = Label(self.__mw, image=self.__images[40])
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        add_money_button = Button(self.__mw, text="Add money €", font='Bold', bg='yellow', relief=GROOVE, command=self.add_money)
        add_money_button.grid(row=2, column=0, columnspan=4, sticky=W+E)
        self.__wallet = Label(self.__mw, text=0.0, bg='grey')
        self.__wallet.grid(row=3, column=1, columnspan=2, sticky=W+E)

        bet_label = Label(self.__mw, text="Place a bet", font='Bold', bg='yellow', relief=GROOVE)
        bet_label.grid(row=2, column=10, columnspan=4, sticky=W+E)
        self.__your_bet = Label(self.__mw, text=0.0, bg='grey')
        self.__your_bet.grid(row=3, column=10, columnspan=2, sticky=W+E)
        self.__bet_less = Button(self.__mw, text="-", bg='green', relief=GROOVE, command=lambda: self.place_bet(0))
        self.__bet_less.grid(row=3, column=12, sticky=W+E)
        self.__bet_more = Button(self.__mw, text="+", bg='green', relief=GROOVE, command=lambda: self.place_bet(1))
        self.__bet_more.grid(row=3, column=13, sticky=W+E)

        self.__pick_color = Label(self.__mw, text="Pick a color",bg='green', borderwidth=3, relief=RAISED)
        self.__pick_color.grid(row=5, column=0, columnspan=4, sticky=W+E)

        self.__roulette_wheel = Label(self.__mw, image=self.__images[39], relief=GROOVE, borderwidth=0)
        self.__roulette_wheel.grid(row=7, column=7, columnspan=2)

        self.__black_button = Button(self.__mw, image=self.__images[38],bg='grey', borderwidth=2, relief=RAISED, command=lambda: self.color(2))
        self.__black_button.grid(row=7, column=0, columnspan=2, sticky=W + E)
        self.__red_button = Button(self.__mw, image=self.__images[37],bg='grey', borderwidth=2, relief=RAISED, command=lambda: self.color(1))
        self.__red_button.grid(row=7, column=2, columnspan=2, sticky=W + E)

        self.__pick_number = Label(self.__mw, text="Pick number(s) between 0-36", bg='green', borderwidth=3, relief=RAISED)
        self.__pick_number.grid(row=5, column=10, columnspan=4, sticky=W+E)
        self.__number_pick = Entry(width=16, bg='grey')
        self.__number_pick.grid(row=6, column=10, columnspan=4)

        self.__spin_button = Button(self.__mw, text="Spin the wheel", bg='black', fg='white', borderwidth=3, relief=RAISED, command=lambda :self.spin(self.__your_bet['text']))
        self.__spin_button.grid(row=7, column=10, columnspan=4, rowspan=2, sticky=W+E+N+S)

        self.__quit_button = Button(self.__mw, text="Quit", command=self.quit, bg='black', fg='white')
        self.__quit_button.grid(row=9, column=13, columnspan=2, sticky=W+E)

        self.__help_button = Button(self.__mw, text="?", bg='black', fg='white', command=self.help)
        self.__help_button.grid(row=9, column=12, sticky=W+E)

        self.__result_window = Label(self.__mw, text="", bg='green', fg='black')
        self.__result_window.grid(row=9, column=0, columnspan=8, sticky=W)

        self.__mw.mainloop()

    def spin(self, bet):

        self.__result_window['text'] = ""
        numbers = self.__number_pick.get()
        chosen_numbers = list(numbers.split(","))

        for entry in chosen_numbers:
            try:
                val = int(entry)
            except ValueError:
                self.__result_window['text'] = "Must be integer(s)!"
                self.reset_fields()
                return
        for entry in chosen_numbers:
            if int(entry) < 0:
                self.__result_window['text'] = "Only positive numbers!"
                self.reset_fields()
                return
            if int(entry) > 36:
                self.__result_window['text'] = "Numbers from 0 to 36!"
                self.reset_fields()
                return

        self.__quit_button.config(state=DISABLED)
        self.__black_button.config(state=DISABLED)
        self.__red_button.config(state=DISABLED)
        self.__spin_button.config(relief=SUNKEN)
        self.__help_button.config(state=DISABLED)

        arvottu = random.randint(0, 36)
        result = False
        if self.wallet(bet):
            self.spin_animation(arvottu)

            for i in chosen_numbers:
                if int(i) == arvottu:
                    result = True
            if result:
                prize = winnings(chosen_numbers, bet)
                self.__result_window['text'] = f"You Won {prize}€!"
            else:

                self.__result_window['text'] = "You Lost"
        self.__spin_button.config(relief=RAISED)
        self.__quit_button.config(state=NORMAL)
        self.__black_button.config(state=NORMAL)
        self.__red_button.config(state=NORMAL)
        self.__help_button.config(state=NORMAL)

    def color(self, color):
        self.__help_button.config(state=DISABLED)
        self.__spin_button.config(state=DISABLED)
        self.__quit_button.config(state=DISABLED)
        if color == 1:
            self.__red_button.config(relief=SUNKEN)
        if color == 2:
            self.__black_button.config(relief=SUNKEN)
        self.__result_window['text'] = ""
        self.__number_pick.delete(0, 'end')
        bet = self.__your_bet['text']

        arvottu = random.randint(0, 36)
        value = int(color)
        if self.wallet(bet):
            self.spin_animation(arvottu)
            if arvottu == 0:
                self.__result_window['text'] = "You Lose"
            elif arvottu % 2 == value % 2:
                self.__result_window['text'] = f"You Win {2*bet}€"
                self.__wallet['text'] += 2*bet
            else:
                self.__result_window['text'] = "You Lose"
        if color == 1:
            self.__red_button.config(relief=RAISED)
        if color == 2:
            self.__black_button.config(relief=RAISED)
        self.__quit_button.config(state=NORMAL)
        self.__spin_button.config(state=NORMAL)
        self.__help_button.config(state=NORMAL)

    def add_money(self):
        money = simpledialog.askfloat("Add money to your wallet",
                                      "Type in amount")
        self.__wallet['text'] += money

    def wallet(self, bet):
        self.__result_window['text'] = ""
        money = self.__wallet['text']
        if bet == 0:
            self.__result_window['text'] = "Poor person spin"
            return True
        if money - bet < 0:
            self.__result_window['text'] = "Add money or bet less"
            return False
        else:
            self.__wallet['text'] = money - bet
            return True

    def place_bet(self, value):
        your_bet = self.__your_bet['text']
        if value == 0:
            your_bet -= 0.5
        if value == 1:
            your_bet += 0.5
        if your_bet < 0:
            self.__your_bet['text'] = 0.0
        else:
            self.__your_bet['text'] = your_bet

    def spin_animation(self, arvottu):
        winsound.PlaySound('Ruletti.wav', winsound.SND_ASYNC |
                           winsound.SND_ALIAS)
        for i in range(0, 20):
            hit = random.randint(0, 36)
            self.__roulette_wheel["image"] = self.__images[hit]
            self.__mw.update_idletasks()
            time.sleep(0.09)
        for i in range(0, 10):
            hit = random.randint(0, 36)
            self.__roulette_wheel["image"] = self.__images[hit]
            self.__mw.update_idletasks()
            time.sleep(0.18)
        for i in range(0, 8):
            hit = random.randint(0, 36)
            self.__roulette_wheel["image"] = self.__images[hit]
            self.__mw.update_idletasks()
            time.sleep(0.23)
        for i in range(0, 6):
            hit = random.randint(0, 36)
            self.__roulette_wheel["image"] = self.__images[hit]
            self.__mw.update_idletasks()
            time.sleep(0.3)
        for i in range(0, 3):
            hit = random.randint(0, 36)
            self.__roulette_wheel["image"] = self.__images[hit]
            self.__mw.update_idletasks()
            time.sleep(0.42)
        self.__roulette_wheel["image"] = self.__images[arvottu]

    def reset_fields(self):
        """
        In error situations this method will zeroize the elements
        self.__number_pick.
        """
        self.__number_pick.delete(0, END)
        pass

    def help(self):
        help_box = Toplevel(self.__mw)
        help_box.title("INSTRUCTIONS")
        help_box.configure(bg='green')
        help_box.geometry("500x400+600+100")
        txt_file = open(file="Instructions.txt", mode="r")
        instructions = txt_file.read()
        how_to_play = Label(help_box, text=instructions)
        how_to_play.pack()

        txt_file.close()

    def quit(self):
        self.__mw.destroy()


def winnings(luckynumbers, bet):
    factor = 35//len(luckynumbers)
    bet_per_pick = bet/len(luckynumbers)
    real_prize = float(factor * bet_per_pick)
    roundup_real_prize = math.ceil(real_prize)
    rounddown_real_prize = math.floor(real_prize)

    if roundup_real_prize - real_prize >= 0.75:
        paid_prize = rounddown_real_prize
    elif roundup_real_prize - real_prize >= 0.5:
        paid_prize = roundup_real_prize - 0.5
    else:
        paid_prize = roundup_real_prize
    return float(paid_prize)


def main():
    Roulette()


if __name__ == "__main__":
    main()
