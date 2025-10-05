import tkinter
from tkinter.messagebox import showinfo
import sv_ttk
import random
import sys
import platform
if platform.system() == "Windows":
    import pywinstyles

class Window(tkinter.Frame):
    def __init__(self, root):
        self.root = root
        self.game_host = None
        self.max_score = 5
        self.player_score_points = {}
        self.freq_score_points = {}
        self.buttons = {}

        # SCORE BOARDS
        ## PLAYER SCORE
        player_score_frame = tkinter.Frame(master=root, height=64, width=128)
        player_score_frame.pack(fill=tkinter.Y, side=tkinter.LEFT)
        player_score_frame.pack_propagate(False) 

        player_name_label = tkinter.Label(player_score_frame, height=4, text="You")
        player_name_label.pack(fill=tkinter.X, side=tkinter.TOP)

        player_score_board = tkinter.Frame(player_score_frame)
        player_score_board.pack(fill=tkinter.BOTH, side=tkinter.TOP, expand=True)
        for i in range(0, self.max_score):
            player_score_board.columnconfigure(i, weight=1)
            player_score_board.rowconfigure(i, weight=1, minsize=80)
            canvas = tkinter.Canvas(player_score_board, height=64)
            canvas.grid(row=(self.max_score-1)-i, column=0, pady=5)
            oval = canvas.create_oval(128/2-30, 64/2-29, 128/2+30, 64/2+31)
            canvas.itemconfig(oval, fill='white')
            self.player_score_points[i] = [canvas, oval]


        ## FREQ SCORE
        freq_score_frame = tkinter.Frame(master=root, height=64, width=128)
        freq_score_frame.pack(fill=tkinter.Y, side=tkinter.RIGHT)
        freq_score_frame.pack_propagate(False) 

        freq_name_label = tkinter.Label(freq_score_frame, height=4, text="Freq", fg='blue')
        freq_name_label.pack(fill=tkinter.X, side=tkinter.TOP)

        freq_score_board = tkinter.Frame(freq_score_frame)
        freq_score_board.pack(fill=tkinter.BOTH, side=tkinter.TOP, expand=True)
        for i in range(0, self.max_score):
            freq_score_board.columnconfigure(i, weight=1)
            freq_score_board.rowconfigure(i, weight=1, minsize=80)
            canvas = tkinter.Canvas(freq_score_board, height=64)
            canvas.grid(row=(self.max_score-1)-i, column=0, pady=5)
            oval = canvas.create_oval(128/2-30, 64/2-29, 128/2+30, 64/2+31)
            canvas.itemconfig(oval, fill='white')
            self.freq_score_points[i] = [canvas, oval]


        # QUESTION
        question_frame = tkinter.Frame(master=root, height=128, width=512)
        question_frame.pack(fill=tkinter.BOTH, side=tkinter.TOP, expand=True)

        question_label = tkinter.Label(question_frame, height=4, text='What comes after...')
        question_label.pack(fill=tkinter.BOTH, side=tkinter.TOP, expand=True)


        # CLUE
        clue_frame = tkinter.Frame(master=root, height=160, width=512, bg='green')
        clue_frame.pack(fill=tkinter.BOTH, side=tkinter.TOP, expand=True)

        self.clue_label = tkinter.Label(clue_frame, height=8, text='BLANK')
        self.clue_label.pack(fill=tkinter.BOTH, side=tkinter.TOP, expand=True)

        # ANSWERS
        answers_frame = tkinter.Frame(master=root, height=288, width=512)
        answers_frame.pack(fill=tkinter.BOTH, side=tkinter.TOP, expand=True)

        for i in range(0,2):
            answers_frame.columnconfigure(i, weight=1, minsize=256)
            answers_frame.rowconfigure(i, weight=1, minsize=32)
            for j in range(0,2):
                button = tkinter.Button(answers_frame, width=32, height=6, text=f"Answer {i} {j}")
                button.grid(column=i, row=j, pady=5)
                self.buttons[i, j] = button

        # NEXT
        next_question_frame = tkinter.Frame(master=root, height=64, width=512)
        next_question_frame.pack(fill=tkinter.BOTH, side=tkinter.TOP, expand=True)

        for i in range(0, 2):
            next_question_frame.columnconfigure(i, weight=1, minsize=256)
        next_question_frame.rowconfigure(0, weight=1, minsize=32)

        self.next_question_timer = tkinter.Label(next_question_frame, width=16, height=2, text='')
        # self.next_question_timer.pack(side=tkinter.LEFT, pady=5)
        self.next_question_timer.grid(column=0, row=0, pady=5)

        self.next_question_button = tkinter.Button(next_question_frame, width=16, height=2, text="Next question")
        # self.next_question_button.pack(side=tkinter.TOP, pady=5)
        self.next_question_button.grid(column=1, row=0, pady=5)

        root.update()
        root.minsize(root.winfo_width(), root.winfo_height())

        self.set_theme()
    
    def set_theme(self):
        sv_ttk.set_theme("dark")
        if platform.system() == "Windows":
            self.apply_theme_to_titlebar(self.root)

    def apply_theme_to_titlebar(self, root):
        version = sys.getwindowsversion()

        if version.major == 10 and version.build >= 22000:
            pywinstyles.change_header_color(root, "#1c1c1c" if sv_ttk.get_theme() == "dark" else "#fafafa")
        elif version.major == 10:
            pywinstyles.apply_style(root, "dark" if sv_ttk.get_theme() == "dark" else "normal")

            root.wm_attributes("-alpha", 0.99)
            root.wm_attributes("-alpha", 1)

    def set_game_host(self, host):
        self.game_host = host
        self.next_question_button['command'] = host.next_question

    def set_question(self, line, clue, answer, variants):
        self.clue_label['text'] = clue
        variants_slice = list(variants.keys())[0:min(5, len(variants))]
        options = [answer] + [option for option in variants_slice if option!=answer][0:3]
        for i in range(0, 2):
            for j in range(0, 2):
                option = random.choice(options)
                self.buttons[i, j]['text'] = option
                self.buttons[i, j]['bg'] = 'black'
                self.buttons[i, j]['command'] = lambda argument=[i, j]: self.game_host.verify_answer(argument)
                options.remove(option)
        self.unlock_buttons()

    def color_button(self, button_coords, color):
        self.buttons[*button_coords]['bg'] = color

    def lock_buttons(self):
        for i in range(0,2):
            for j in range(0,2):
                self.buttons[i, j]["state"] = "disabled"

    def unlock_buttons(self):
        for i in range(0,2):
            for j in range(0,2):
                self.buttons[i, j]["state"] = "normal"

    def update_score(self, player_score, freq_score):
        competitors = {'player': player_score, 'freq': freq_score}
        for i in range(0, self.max_score):
            for competitor in competitors:
                point=getattr(self, f"{competitor}_score_points")[i]
                if competitors[competitor]>=i+1:
                    point[0].itemconfig(point[1], fill='green')
                else:
                    point[0].itemconfig(point[1], fill='white')

    def show_popup(self, title, message):
        showinfo(title, message)