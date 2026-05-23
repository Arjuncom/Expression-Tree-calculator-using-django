class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def is_operator(c):
    return c in '+-*/'

def precedence(op):
    if op in ('+', '-'): return 1
    if op in ('*', '/'): return 2
    return 0

def infix_to_postfix(expression):
    stack = []
    output = []
    number = ''
    for char in expression:
        if char.isdigit() or char == '.':
            number += char
        else:
            if number:
                output.append(number)
                number = ''
            if char == '(':
                stack.append(char)
            elif char == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                if not stack: raise ValueError("Mismatched parentheses")
                stack.pop()
            elif is_operator(char):
                while stack and precedence(stack[-1]) >= precedence(char):
                    output.append(stack.pop())
                stack.append(char)
            elif char != ' ':
                raise ValueError(f"Invalid character: {char}")
    if number:
        output.append(number)
    while stack:
        if stack[-1] == '(':
            raise ValueError("Mismatched parentheses")
        output.append(stack.pop())
    return output

def build_tree(postfix):
    stack = []
    for token in postfix:
        node = TreeNode(token)
        if is_operator(token):
            node.right = stack.pop()
            node.left = stack.pop()
        stack.append(node)
    return stack[-1]

def evaluate_tree(node):
    if node is None:
        return 0
    if not is_operator(node.value):
        return float(node.value)
    left = evaluate_tree(node.left)
    right = evaluate_tree(node.right)
    if node.value == '+': return left + right
    if node.value == '-': return left - right
    if node.value == '*': return left * right
    if node.value == '/':
        if right == 0:
            raise ZeroDivisionError("Division by zero")
        return left / right
