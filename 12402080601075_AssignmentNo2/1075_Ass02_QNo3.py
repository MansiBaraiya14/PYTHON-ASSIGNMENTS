import mysql.connector
import csv


try:
    # ---------------- DATABASE CONNECTION ----------------

    host = input("Enter host: ")
    user = input("Enter username: ")
    password = input("Enter password: ")
    database = input("Enter database name: ")

    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

    cursor = conn.cursor()

    # ---------------- CREATE TABLES ----------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Student (
            student_id INT PRIMARY KEY,
            name VARCHAR(100),
            spi FLOAT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS CourseRegistration (
            student_id INT,
            course_id VARCHAR(20),
            FOREIGN KEY (student_id)
            REFERENCES Student(student_id)
        )
    """)

    # ---------------- INSERT STUDENTS ----------------

    student_file = input("Enter student CSV file: ")

    with open(student_file, "r", newline="", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        for row in reader:

            cursor.execute("""
                INSERT IGNORE INTO Student
                (student_id, name, spi)
                VALUES (%s, %s, %s)
            """, (
                row["student_id"],
                row["name"],
                row["spi"]
            ))

    # ---------------- INSERT REGISTRATIONS ----------------

    registration_file = input("Enter registration CSV file: ")

    with open(registration_file, "r", newline="", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        for row in reader:

            cursor.execute("""
                INSERT INTO CourseRegistration
                (student_id, course_id)
                VALUES (%s, %s)
            """, (
                row["student_id"],
                row["course_id"]
            ))

    conn.commit()

    # ---------------- SEARCH ----------------

    course_id = input("Enter course id: ")
    spi_threshold = float(input("Enter SPI threshold: "))

    query = """
        SELECT s.student_id, s.name, s.spi, r.course_id
        FROM Student s
        JOIN CourseRegistration r
        ON s.student_id = r.student_id
        WHERE r.course_id = %s
        AND s.spi > %s
        ORDER BY s.spi DESC, s.student_id ASC
    """

    cursor.execute(query, (course_id, spi_threshold))

    results = cursor.fetchall()

    # ---------------- OUTPUT ----------------

    for student_id, name, spi, course in results:
        print(student_id, name, spi, course)


except mysql.connector.Error as e:
    print("Database Error:", e)

except FileNotFoundError:
    print("CSV file not found.")

except Exception as e:
    print("Error:", e)

finally:
    try:
        cursor.close()
        conn.close()
    except:
        pass