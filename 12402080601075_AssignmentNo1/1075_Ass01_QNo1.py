# Campus Merit Analyzer using Compound Data Structures

n, k, m = map(int, input().split())

# Dictionary to store student records
students = {}

# Dictionary to group students by semester
semester_students = {}

# Dictionary to store subject-wise highest marks
subject_topper = {f"S{i+1}": [] for i in range(m)}

# Read student records
for _ in range(n):
    data = input().split()

    enrollment = data[0]
    name = data[1]
    semester = int(data[2])
    cpi = float(data[3])

    # Store marks as a list
    marks = list(map(int, data[4:4 + m]))

    # Store student information using dictionary + tuple
    students[enrollment] = (name, semester, cpi, marks)

    # Group students semester-wise
    if semester not in semester_students:
        semester_students[semester] = []

    semester_students[semester].append(enrollment)


# ---------------------------------------------------
# Semester-wise Top K Students
# ---------------------------------------------------

for semester in sorted(semester_students):

    enrollments = semester_students[semester]

    # Sort using:
    # 1. Higher CPI
    # 2. Higher average marks
    # 3. Lexicographically smaller enrollment number

    enrollments.sort(
        key=lambda e: (
            -students[e][2],                    # Higher CPI
            -sum(students[e][3]) / m,            # Higher average marks
            e                                    # Smaller enrollment
        )
    )

    top_k = enrollments[:k]

    print(f"Semester {semester}:", *top_k)


# ---------------------------------------------------
# Subject-wise Toppers
# ---------------------------------------------------

for subject_index in range(m):

    subject_code = f"S{subject_index + 1}"

    # Find maximum mark in this subject
    max_mark = max(
        students[e][3][subject_index]
        for e in students
    )

    # Find all students having maximum marks
    toppers = []

    for e in students:
        if students[e][3][subject_index] == max_mark:
            toppers.append(e)

    # Lexicographically sort enrollment numbers
    toppers.sort()

    print(f"{subject_code}:", *toppers)