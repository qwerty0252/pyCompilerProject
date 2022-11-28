from TT_DIGITS import *
from positionT import Position
from errorT import IllegalCharError
from parserT import Parser
from interpreterT import Interpreter


#Token class
class Token:
    def __init__(self, type_, value = None, pos_start=None, pos_end=None):
        self.type = type_
        self.value = value

        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance()

        if pos_end:
            self.pos_end = pos_end

    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'


#lexer
class Lexer:
    def __init__(self, file_name, line,):
        self.line = line
        self.file_name = file_name
        self.pos = Position(-1, 0, -1, self.file_name, self.line)
        self.current_char =  None
        self.advance()

    def advance(self,):
        self.pos.advance(self.current_char)
        if self.pos.index < len(self.line):
            self.current_char = self.line[self.pos.index]
        else:
            self.current_char = None

# timestap
    def make_number(self,):
        num_str = ''
        dot_count =  0    ##error might appear here
        pos_start = self.pos.copy()
        while self.pos.index < len(self.line) and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_count == 1: break
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.current_char
            self.advance()

        if dot_count == 0:
            return Token(TT_INT, int(num_str), pos_start, self.pos)
        else:
            return Token(TT_FLOAT, float(num_str), pos_start, self.pos)



    def create_token(self):
        token = []
        while self.current_char != None:
            if self.current_char in ' \t':
                self.advance()
            elif self.current_char in DIGITS:
                token.append(self.make_number())
            elif self.current_char == '(':
                token.append(Token(TT_LPAREN, pos_start= self.pos))
                self.advance()
            elif self.current_char == ')':
                token.append(Token(TT_RPAREN, pos_start= self.pos))
                self.advance()
            elif self.current_char == '+':
                token.append(Token(TT_PLUS, pos_start= self.pos))
                self.advance()
            elif self.current_char == '-':
                token.append(Token(TT_MINUS, pos_start= self.pos))
                self.advance()
            elif self.current_char == '/':
                token.append(Token(TT_DIV, pos_start= self.pos))
                self.advance()
            elif self.current_char == '*':
                token.append(Token(TT_MUL, pos_start= self.pos))
                self.advance()
            else:
                pos_start =  self.pos.copy()
                error_char =  self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, f' "{error_char}" ')
                
        token.append(Token(TT_EOF, pos_start=self.pos))
        return token, None


def run(file_name, text):
    lexer = Lexer(file_name,text)
    result, error = lexer.create_token()
    # print('lexer result: ' + str(result))
    if error:
        return None, error.as_string()

    #Generate AST
    parser = Parser(result)
    ast = parser.parse()

    if ast.error: return None, ast.error

    interpreter = Interpreter()
    result = interpreter.visit(ast.node)
    return result.value, result.error