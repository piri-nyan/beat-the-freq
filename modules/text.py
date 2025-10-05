class Reader:
    def __init__(self, file_path):
        self.line_count = 0
        self.file_path = file_path

    def line_read(self):
        with open(self.file_path, encoding='utf8', mode='r') as file_handler:
            for line in file_handler:
                lines = line.split('.')
                for line in lines:
                    new_line = [char for char in line.lower().replace(u'\xa0', u' ') if char.isalpha() or char.isspace()]
                    line = (''.join(new_line)).strip()
                    if line and not line.isdigit():
                        yield line

    def block_read(self, block_size = 50):
        self.line_count = 0
        block = ''
        for line in self.line_read():
            self.line_count+=1
            block+=line+'\n'
            if block and len(block) >= block_size:
                yield block
                block = ''
        if block:
            yield block

    def batch_read(self, block, n=2):
        lines = block.split('\n')
        for line in lines:
            words = [word for word in line.split(' ') if word]
            l = len(words)
            for ndx in range(0, l, 1):
                if ndx + n <= l:
                    yield words[ndx:ndx+n]