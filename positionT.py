class Position:
    def __init__(self, index, line_nummber, col_index, file_name, file_txt):
        self.index =  index
        self.line_number = line_nummber
        self.col_index =  col_index
        self.file_name = file_name
        self.file_txt = file_txt

    def advance(self, current_char=None):
        self.index += 1
        self.col_index += 1

        if current_char == '\n':
            self.line_number += 1
            self.col_index = 0

        return self

    def copy(self):
        return Position(self.index, self.line_number, self.col_index, self.file_name, self.file_txt)

    
        