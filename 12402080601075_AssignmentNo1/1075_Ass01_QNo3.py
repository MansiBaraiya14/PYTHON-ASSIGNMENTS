import re
import sys

sys.setrecursionlimit(1000000)


# -----------------------------
# Tokenizer
# -----------------------------
def tokenize(expr):
    tokens = re.findall(r'[A-Za-z_][A-Za-z0-9_]*|\d+|[()+*-]', expr)

    # Make sure everything in the expression was valid
    cleaned = re.sub(r'\s+', '', expr)
    rebuilt = ''.join(tokens)

    if cleaned != rebuilt:
        raise ValueError()

    return tokens


# -----------------------------
# Parser
# -----------------------------
class Parser:
    def __init__(self, tokens, variables, state, memo):
        self.tokens = tokens
        self.pos = 0
        self.variables = variables
        self.state = state
        self.memo = memo

    def parse(self):
        if not self.tokens:
            raise ValueError()

        value = self.expression()

        if self.pos != len(self.tokens):
            raise ValueError()

        return value

    # expression = term ((+|-) term)*
    def expression(self):
        value = self.term()

        while self.pos < len(self.tokens):
            op = self.tokens[self.pos]

            if op not in ('+', '-'):
                break

            self.pos += 1
            right = self.term()

            if op == '+':
                value += right
            else:
                value -= right

        return value

    # term = factor (* factor)*
    def term(self):
        value = self.factor()

        while self.pos < len(self.tokens):
            op = self.tokens[self.pos]

            if op != '*':
                break

            self.pos += 1
            right = self.factor()
            value *= right

        return value

    # factor = number | variable | (expression)
    def factor(self):
        if self.pos >= len(self.tokens):
            raise ValueError()

        token = self.tokens[self.pos]

        # Number
        if token.isdigit():
            self.pos += 1
            return int(token)

        # Parentheses
        if token == '(':
            self.pos += 1

            value = self.expression()

            if self.pos >= len(self.tokens) or self.tokens[self.pos] != ')':
                raise ValueError()

            self.pos += 1
            return value

        # Variable
        if re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*', token):
            self.pos += 1

            if token not in self.variables:
                raise ValueError()

            return evaluate_variable(
                token,
                self.variables,
                self.state,
                self.memo
            )

        raise ValueError()


# -----------------------------
# Evaluate variable
# -----------------------------
def evaluate_variable(name, variables, state, memo):

    # Already completely evaluated
    if state.get(name) == 2:
        return memo[name]

    # Currently being evaluated -> cycle
    if state.get(name) == 1:
        raise RuntimeError("CYCLE")

    state[name] = 1

    tokens = tokenize(variables[name])

    parser = Parser(tokens, variables, state, memo)

    value = parser.parse()

    memo[name] = value
    state[name] = 2

    return value


# -----------------------------
# Main program
# -----------------------------
try:
    v = int(input().strip())

    variables = {}

    for _ in range(v):
        line = input()

        if '=' not in line:
            print("INVALID")
            sys.exit()

        name, expr = line.split('=', 1)

        name = name.strip()
        expr = expr.strip()

        if not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*', name):
            print("INVALID")
            sys.exit()

        if name in variables:
            print("INVALID")
            sys.exit()

        variables[name] = expr

    final_expression = input().strip()

    state = {}
    memo = {}

    tokens = tokenize(final_expression)

    parser = Parser(tokens, variables, state, memo)

    answer = parser.parse()

    print(answer)

except RuntimeError as e:
    if str(e) == "CYCLE":
        print("CYCLE")
    else:
        print("INVALID")

except Exception:
    print("INVALID")