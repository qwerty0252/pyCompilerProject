from TT_DIGITS import *
from numberClassT import Number
class Interpreter:
    def visit(self, node):
        method_name =  f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node)

    def no_visit_method(self, node):
        raise Exception(f'No visit_{type(node).__name__} method defined')

    def visit_NumberNode(self, node):
        return RunTimeResult().success(Number(node.token.value).set_position(node.pos_start, node.pos_end))# time stamp

    def visit_BinNode(self, node):
        # print('found number binary op node')
        resultRT = RunTimeResult() #runtime result
        left = resultRT.register(self.visit(node.left_node))
        if resultRT.error: return resultRT
        right =  resultRT.register(self.visit(node.right_node))

        if node.op_token.type == TT_PLUS:
            result, error = left.added_to(right)
        elif node.op_token.type == TT_MINUS:
            result, error = left.subbed_by(right)
        elif node.op_token.type == TT_MUL:
            result, error = left.multiply_by(right)
        elif node.op_token.type == TT_DIV:
            result, error = left.divided_by(right)

        if error:
            return resultRT.failure(error)
        else:
            return resultRT.success(result.set_position(node.pos_start, node.pos_end))

    
    def visit_UnaryOpNode(self, node):
        resultRT =  RunTimeResult()
        number = resultRT.register(self.visit(node.node))
        if resultRT.error: return resultRT

        error = None

        if node.op_token.type == TT_MINUS:
            number, error = number.multiply_by(Number(-1))

        if error:
            return resultRT.failure(error)
        else:
            return resultRT.success(number.set_position(node.pos_start, node.pos_end))


class RunTimeResult:
    def __init__(self):
        self.value = None
        self.error = None

    def register(self, result):
        if result.error: self.error = result.error
        return  result.value

    def success(self, value):
        self.value = value
        return self

    def failure(self, error):
        self.error =  error
        return self

