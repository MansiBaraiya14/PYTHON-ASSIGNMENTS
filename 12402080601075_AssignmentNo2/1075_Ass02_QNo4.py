import mysql.connector


# ---------------- WHITELISTS ----------------

ALLOWED_COLUMNS = {
    "student.id": "s.id",
    "student.name": "s.name",
    "student.spi": "s.spi",

    "course.id": "c.id",
    "course.name": "c.name",

    "registration.student_id": "cr.student_id",
    "registration.course_id": "cr.course_id"
}

ALLOWED_OPERATORS = {
    "=": "=",
    ">": ">",
    "<": "<",
    ">=": ">=",
    "<=": "<=",
    "LIKE": "LIKE"
}

ALLOWED_ORDER_COLUMNS = {
    "student.id": "s.id",
    "student.name": "s.name",
    "student.spi": "s.spi",
    "course.id": "c.id",
    "course.name": "c.name"
}


def build_query(columns, filters, order_column, sort_direction, limit):

    # -------- Validate columns --------

    selected_columns = []

    for column in columns:

        if column not in ALLOWED_COLUMNS:
            raise ValueError("Invalid column: " + column)

        selected_columns.append(ALLOWED_COLUMNS[column])

    # -------- Validate order column --------

    if order_column not in ALLOWED_ORDER_COLUMNS:
        raise ValueError("Invalid order column")

    # -------- Validate sort direction --------

    sort_direction = sort_direction.upper()

    if sort_direction not in ["ASC", "DESC"]:
        raise ValueError("Invalid sort direction")

    # -------- Validate LIMIT --------

    if not (1 <= limit <= 1000):
        raise ValueError("Limit must be between 1 and 1000")

    # -------- Build WHERE --------

    where_parts = []
    parameters = []

    for column, operator, value in filters:

        if column not in ALLOWED_COLUMNS:
            raise ValueError("Invalid filter column")

        if operator.upper() not in ALLOWED_OPERATORS:
            raise ValueError("Invalid operator")

        sql_column = ALLOWED_COLUMNS[column]
        sql_operator = ALLOWED_OPERATORS[operator.upper()]

        where_parts.append(
            sql_column + " " + sql_operator + " %s"
        )

        parameters.append(value)

    # -------- Build SQL --------

    sql = """
SELECT {columns}
FROM Student s
JOIN CourseRegistration cr
    ON s.id = cr.student_id
JOIN Course c
    ON cr.course_id = c.id
""".format(columns=", ".join(selected_columns))

    if where_parts:
        sql += "WHERE " + " AND ".join(where_parts) + "\n"

    sql += "ORDER BY " + ALLOWED_ORDER_COLUMNS[order_column]
    sql += " " + sort_direction + "\n"

    # LIMIT is converted to integer after validation
    sql += "LIMIT " + str(limit)

    return sql, parameters


# ---------------- MAIN PROGRAM ----------------

try:

    # Connect to MySQL
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="mysqlmansib@14",
        database="college"
    )

    cursor = conn.cursor()

    # Selected columns
    print("Available columns:")
    print("student.id")
    print("student.name")
    print("student.spi")
    print("course.id")
    print("course.name")

    columns_input = input(
        "Enter columns separated by comma: "
    )

    columns = [
        x.strip()
        for x in columns_input.split(",")
    ]

    # Filter
    filter_column = input(
        "Enter filter column (or press Enter to skip): "
    )

    filters = []

    if filter_column:

        operator = input(
            "Enter operator (=, >, <, >=, <=, LIKE): "
        )

        value = input("Enter value: ")

        filters.append(
            (filter_column, operator, value)
        )

    # Order
    order_column = input(
        "Enter order column: "
    )

    sort_direction = input(
        "Enter sort direction (ASC/DESC): "
    )

    # Limit
    limit = int(input("Enter limit: "))

    # Build query
    sql, parameters = build_query(
        columns,
        filters,
        order_column,
        sort_direction,
        limit
    )

    print("\nSQL_OK")
    print("\nGenerated SQL:")
    print(sql)

    print("\nParameters:")
    print(parameters)

    # Execute safely
    cursor.execute(sql, parameters)

    results = cursor.fetchall()

    print("\nQuery Result:")

    for row in results:
        print(*row)


except mysql.connector.Error as e:
    print("Database Error:", e)

except ValueError as e:
    print("Validation Error:", e)

except Exception as e:
    print("Error:", e)

finally:

    try:
        cursor.close()
        conn.close()
    except:
        pass