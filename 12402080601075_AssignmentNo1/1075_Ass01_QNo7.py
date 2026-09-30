class InvalidFormatError(Exception):
    pass


class UnknownVariableError(Exception):
    pass


class DivisionByZeroError(Exception):
    pass


class UnsupportedOperatorError(Exception):
    pass


variables = {}


def get_value(value):
    # Check if it is a number
    try:
        return float(value)
    except ValueError:
        pass

    # Check if it is a variable
    if value in variables:
        return variables[value]

    raise UnknownVariableError(
        "Unknown variable: " + value
    )


def calculate(left, operator, right):

    a = get_value(left)
    b = get_value(right)

    if operator == "+":
        return a + b

    elif operator == "-":
        return a - b

    elif operator == "*":
        return a * b

    elif operator == "/":
        if b == 0:
            raise DivisionByZeroError(
                "Cannot divide by zero"
            )
        return a / b

    elif operator == "%":
        if b == 0:
            raise DivisionByZeroError(
                "Cannot take modulo by zero"
            )
        return a % b

    else:
        raise UnsupportedOperatorError(
            "Unsupported operator: " + operator
        )


while True:

    line = input().strip()

    if line.lower() == "quit":
        break

    try:

        # Assignment: x = 10
        if "=" in line:

            parts = line.split("=")

            if len(parts) != 2:
                raise InvalidFormatError(
                    "Invalid assignment format"
                )

            variable = parts[0].strip()
            value = parts[1].strip()

            if not variable.isidentifier():
                raise InvalidFormatError(
                    "Invalid variable name"
                )

            if not value:
                raise InvalidFormatError(
                    "Missing value"
                )

            variables[variable] = get_value(value)

        else:

            # Formula: operand operator operand
            parts = line.split()

            if len(parts) != 3:
                raise InvalidFormatError(
                    "Formula must be: operand operator operand"
                )

            left, operator, right = parts

            result = calculate(left, operator, right)

            # Print integer without .0
            if result.is_integer():
                print(int(result))
            else:
                print(result)

    except InvalidFormatError as e:
        print("InvalidFormatError")

    except UnknownVariableError as e:
        print("UnknownVariableError")

    except DivisionByZeroError as e:
        print("DivisionByZeroError")

    except UnsupportedOperatorError as e:
        print("UnsupportedOperatorError")

    except Exception:
        print("InvalidFormatError")