#Error class
class Error:
    def __init__(self, pos_start, pos_end, error_name, error_detail):
        self.error_name = error_name
        self.error_detail =  error_detail
        self.pos_start = pos_start
        self.pos_end = pos_end

    def as_string(self):
        result =  f'{self.error_name} : {self.error_detail} File: {self.pos_start.file_name}, line: {self.pos_start.line_number + 1}'
        result += 'sting with arrows'
        return result


class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Illegal Character', details)

class InvalidSyntaxError(Error):
    def __init__(self, pos_start, pos_end, details=''):
        super().__init__(pos_start, pos_end, 'Invalid Syntax', details)


class RunTimeError(Error):
    def __init__(self, pos_start, pos_end, error_name, error_detail=''):
        super().__init__(pos_start, pos_end, 'Runtime Error', error_detail)