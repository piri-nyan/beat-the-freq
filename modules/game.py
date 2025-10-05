import sys, os, time
import threading
from modules.frequency import Analyzer

class TimerWrapper():
    def __init__(self, timer, display):
        self.started_at = None
        self.timer = timer
        self.display = display

    def start(self):
        self.started_at = time.time()
        self.timer.start()
        self.update_display()

    def elapsed(self):
        return time.time() - self.started_at
    
    def remaining(self):
        return self.timer.interval - self.elapsed()
    
    def update_display(self):
        if self.timer.is_alive():
            self.display['text'] = round(self.remaining())
            clock = threading.Timer(0.1, self.update_display)
            clock.start()
        else:
            self.display['text'] = ''
            

class Host:
    def __init__(self, window):
        self.window = window
        self.awaiting = None
        self.difficulty = 2
        self.analyzer = None
        self.correct_answer = None
        self.full_line = None
        self.player_choice = None
        self.freq_choice = None
        self.player_score = 0
        self.freq_score = 0
        self.select_data('test4.txt')
        self.next_question()

    def resource_path(self, relative_path):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("./test_data"), relative_path)

    def select_data(self, data_name):
        self.analyzer = Analyzer(self.difficulty, self.resource_path(data_name))

    def next_question(self):
        if self.awaiting:
            self.awaiting.cancel()
        
        words, selected_word_index, depth = self.analyzer.riddle()

        answers = dict(sorted(depth.items(), key=lambda item: item[1], reverse=True))

        self.full_line = ' '.join(words)
        self.correct_answer = words[selected_word_index]
        self.window.set_question(words, words[selected_word_index-1], self.correct_answer, dict(sorted(depth.items(), key=lambda item: item[1], reverse=True)))
        for button in self.window.buttons:
            if self.window.buttons[button]['text'] == list(answers.keys())[0]:
                self.window.buttons[button]['bg'] = 'blue'
                self.freq_choice = button

    def delay_action(self, delay, action, args=[]):
        timer = threading.Timer(delay, self.wake_up, args=[action, args])
        timer_wrapper = TimerWrapper(timer, self.window.next_question_timer)
        self.awaiting = timer
        timer_wrapper.start()

    def wake_up(self, action, args=[]):
        self.awaiting = None
        action(*args)

    def verify_answer(self, button_coords):
        if self.window.buttons[*button_coords]['text'] == self.correct_answer:
            self.player_score+=1
        else:
            self.window.color_button(button_coords, 'red')
        
        for button in self.window.buttons:
            button_obj = self.window.buttons[button]
            if button_obj['text'] == self.correct_answer:
                self.window.color_button(button, 'green')
                
                if self.freq_choice == button:
                    self.freq_score+=1
                    
        self.window.clue_label['text'] = self.full_line
        self.window.lock_buttons()
        self.window.update_score(self.player_score, self.freq_score)
        if max(self.player_score, self.freq_score) >= self.window.max_score:
            self.nominate_winner()
        else:
            self.delay_action(3, self.next_question)

    def nominate_winner(self):
        scores = {'You': self.player_score, 'Freq': self.freq_score}
        winner = max(scores, key=scores.get)
        self.window.show_popup("Winner", winner)
        self.reset_game()

    def reset_game(self):
        self.player_score = 0
        self.freq_score = 0
        self.window.update_score(self.player_score, self.freq_score)
        self.next_question()