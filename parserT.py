# #NODES 
from TT_DIGITS import *
from errorT import InvalidSyntaxError
class NumberNode:
    def __init__(self, token):
        self.token =  token
        self.pos_start = self.token.pos_start
        self.pos_end = self.token.pos_end

    def __repr__(self):
        return f'{self.token}'


class BinNode:
    def __init__(self, left_node, op_token, right_node):
        self.left_node =  left_node
        self.right_node =  right_node
        self.op_token = op_token
        # print('bin node')

        self.pos_start = self.left_node.pos_start
        self.pos_end = self.right_node.pos_end


    def __repr__(self):
        return f'({self.left_node}, {self.op_token}, {self.right_node})'


class UnaryOpNode:
    def __init__(self, op_token, node):
        self.op_token =  op_token
        self.node =  node
        self.pos_start = self.op_token.pos_start
        self.pos_end = node.pos_end

    def __repr__(self):
        return f'({self.op_token}, {self.node})'
        

# PARSE RESULT CLASS
class ParseResult:
    def __init__(self):
        self.error = None
        self.node =  None

    def register(self, res):
        if isinstance(res, ParseResult):
            if res.error: self.error = res.error #checking for errors
            return res.node
        
        return res

    def success(self, node):
        self.node = node 
        return self

    def failure(self, error):
        self.error = error
        return self

#PARSER CLASS
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_index = -1
        self.advance()

    def advance(self):
        self.token_index += 1 
        if self.token_index < len(self.tokens):
            # print('advance d '+str(self.tokens[self.token_index]))
            self.current_token =  self.tokens[self.token_index]
        return self.current_token
          #wahala area 


    def parse(self):
        res = self.expression()
        # print('res: '+str(res))
        if not res.error and self.current_token.type != TT_EOF:
            return res.failure(InvalidSyntaxError(self.current_token.pos_start, 
            self.current_token.pos_end, 
            "Expected '+', '-', '*' or a fucking '/' ffs"))

        return res

    def factor(self):
        result = ParseResult()
        token = self.current_token
        # print('self.current token ' + str(token))
        # print(token.type)

        #checking for uniary op

        if token.type in (TT_PLUS, TT_MINUS):
            result.register(self.advance())
            factor = result.register(self.factor())
            if result.error: return result
            return result.success(UnaryOpNode(token, factor))

        elif token.type in (TT_INT, TT_FLOAT):
            result.register(self.advance()) #rn does nothing 
            # print("🙂"+str(result.success(NumberNode(token))))
            return result.success(NumberNode(token))

        elif token.type == TT_LPAREN:
            result.register(self.advance())
            expression =  result.register(self.expression())
            if result.error: return result
            if self.current_token.type == TT_RPAREN:
                result.register(self.advance())
                return result.success(expression)

            else:
                return result.failure(InvalidSyntaxError(token.pos_start, token.pos_end, "Expected ')'"))
                 
        return result.failure(InvalidSyntaxError(token.pos_start, token.pos_end, "Expected int or float"))


    def term(self):
        # print('term')
        # print('term ran')
        return self.bin_op(self.factor, (TT_DIV, TT_MUL))

    def expression(self):
        # print('expr ran')
        return self.bin_op(self.term, (TT_PLUS, TT_MINUS))

    def bin_op(self, function, operator):
        result = ParseResult()
        left =  result.register(function()) 
        # print('uu : ' +str(left))
        if result.error: return result
        # print('left ' +  str(left))

        while self.current_token.type in operator:
            op_token = self.current_token
            result.register(self.advance())
            right =  result.register(function())
            # print('uu right: ' + str(right))
            if result.error: return result
            # print('right ' + str(right))
            left = BinNode(left, op_token, right)
            # print('while loop done bitches')
            # print('👀' + str(result.success(left)))
        
        return result.success(left)
