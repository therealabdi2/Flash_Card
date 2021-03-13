from tkinter import *
import pandas
import random

current_card = {}

BACKGROUND_COLOR = "#B1DDC6"

try:
    data = pandas.read_csv("data/words_to_learn.csv")
    to_learn = data.to_dict(orient="records")
except FileNotFoundError:
    data = pandas.read_csv("data/french_words.csv")
    to_learn = data.to_dict(orient="records")


# ---------------------------- Next Card Generator------------------------------- #
def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    random_word_french = current_card["French"]
    canvas.itemconfig(canvas_image, image=card_front_img)
    canvas.itemconfig(title_text, text="French", fill="black")
    canvas.itemconfig(word_text, text=random_word_french, fill="black")

    flip_timer = window.after(3000, flip_card)


def flip_card():
    global current_card
    random_word_english = current_card["English"]

    canvas.itemconfig(canvas_image, image=card_back_img)
    canvas.itemconfig(title_text, text="English", fill="white")
    canvas.itemconfig(word_text, text=random_word_english, fill="white")


def is_known():
    to_learn.remove(current_card)
    to_learn_dfa = pandas.DataFrame(to_learn)
    to_learn_dfa.to_csv("data/words_to_learn.csv", index=False)
    next_card()


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, flip_card)

canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
card_front_img = PhotoImage(file="./images/card_front.png")
canvas_image = canvas.create_image(400, 263, image=card_front_img)
canvas.grid(row=0, column=0, columnspan=2)

card_back_img = PhotoImage(file="./images/card_back.png")

title_text = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))

word_text = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))

wrong_img = PhotoImage(file="./images/wrong.png")
wrong_button = Button(highlightthickness=0, image=wrong_img, command=next_card)
wrong_button.grid(column=0, row=1)

right_img = PhotoImage(file="./images/right.png")
right_button = Button(highlightthickness=0, image=right_img, command=is_known)
right_button.grid(column=1, row=1)

next_card()
window.mainloop()
