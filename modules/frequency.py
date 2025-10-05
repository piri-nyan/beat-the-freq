import random
from modules.text import Reader


class Analyzer:
    def __init__(self, difficulty, data_path):
        self.reader = Reader(data_path)
        self.frequencies = {}
        self.difficulty = difficulty
        self.text_analyzed = False

    def analyze(self):
        for block in self.reader.block_read(self.difficulty*10):
            for batch in self.reader.batch_read(block, self.difficulty):
                current_depth = self.frequencies
                word_index = 0
                for word in batch:
                    if word_index < self.difficulty-1:
                        current_depth.setdefault(word, {})
                        current_depth = current_depth[word]
                    else:
                        current_depth.setdefault(word, 0)
                        current_depth[word] += 1
                        current_depth = self.frequencies
                    word_index+=1
        self.text_analyzed = True

    def riddle(self):
        if not self.text_analyzed:
            self.analyze()
        line_acceptable = False
        while not line_acceptable:
            current_line = 0
            selected_line = random.randint(0, self.reader.line_count)
            for line in self.reader.line_read():
                if current_line == selected_line:
                    if len(line.split(' ')) < self.difficulty+1:
                        line = False
                        break
                    break
                else:
                    current_line+=1
            if not line:
                continue
            words = [word for word in line.split(' ') if word]
            selected_word_index = random.randint(self.difficulty-1, len(words)-1)
            depth = self.frequencies
            for i in range(selected_word_index-(self.difficulty-1), selected_word_index):
                depth = depth[words[i]]
            if words[selected_word_index-1].isalpha() and len(depth.keys())>=4:
                line_acceptable = True

        return words, selected_word_index, depth