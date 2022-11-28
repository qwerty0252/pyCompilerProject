from errorT import RunTimeError
class Number:
    def __init__(self, value):
        self.value = value
        self.set_position()

    def set_position(self, pos_start=None, pos_end=None): #not even sure if that how to spell position
        self.pos_start =  pos_start
        self.pos_end = pos_end
        return self

    def added_to(self, other_no): #asin other number, it justs adds numbers
        if isinstance(other_no, Number):
            return Number(self.value + other_no.value), None

    def subbed_by(self, other_no):
        if isinstance(other_no, Number):
            return Number(self.value - other_no.value), None

    def divided_by(self, other_no):
        if isinstance(other_no, Number):
            if other_no.value == 0:
                return None, RunTimeError(other_no.pos_start, other_no.pos_end, 'Divison by zero')
            return Number(self.value / other_no.value), None

    def multiply_by(self, other_no):
        if isinstance(other_no, Number):
            return Number(self.value * other_no.value), None

    def __repr__(self):
        return  str(self.value) 