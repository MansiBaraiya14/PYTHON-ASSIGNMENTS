import pandas as pd
import matplotlib.pyplot as plt
import os

# Input
file_path = input("Enter CSV file path: ")
output_folder = input("Enter output folder path: ")

# Create output folder if it does not exist
os.makedirs(output_folder, exist_ok=True)

# Read CSV
df = pd.read_csv(file_path)

# Identify subject columns
subject_columns = [
    col for col in df.columns
    if col not in ["enrollment", "name"]
]

# Convert subject marks to numeric
for subject in subject_columns:
    df[subject] = pd.to_numeric(df[subject], errors="coerce")

# Fill missing marks with subject-wise average
for subject in subject_columns:
    average = df[subject].mean()
    df[subject] = df[subject].fillna(average)

# Calculate total and average
df["Total"] = df[subject_columns].sum(axis=1)
df["Average"] = df[subject_columns].mean(axis=1)

# Assign grades
def get_grade(avg):
    if avg >= 90:
        return "A+"
    elif avg >= 80:
        return "A"
    elif avg >= 70:
        return "B"
    elif avg >= 60:
        return "C"
    elif avg >= 50:
        return "D"
    else:
        return "F"

df["Grade"] = df["Average"].apply(get_grade)

# --------------------------------
# 1. Save cleaned CSV
# --------------------------------

cleaned_file = os.path.join(
    output_folder, "cleaned_marks.csv"
)

df.to_csv(cleaned_file, index=False)


# --------------------------------
# 2. Subject-wise summary
# --------------------------------

summary = pd.DataFrame({
    "Subject": subject_columns,
    "Average": [df[s].mean() for s in subject_columns],
    "Minimum": [df[s].min() for s in subject_columns],
    "Maximum": [df[s].max() for s in subject_columns]
})

summary_file = os.path.join(
    output_folder, "summary.csv"
)

summary.to_csv(summary_file, index=False)


# --------------------------------
# 3. Grade Distribution Chart
# --------------------------------

grade_counts = df["Grade"].value_counts()

plt.figure(figsize=(8, 5))
grade_counts.sort_index().plot(kind="bar")
plt.title("Grade Distribution")
plt.xlabel("Grade")
plt.ylabel("Number of Students")
plt.tight_layout()

plt.savefig(
    os.path.join(output_folder, "grade_distribution.png")
)
plt.close()


# --------------------------------
# 4. Subject Average Chart
# --------------------------------

plt.figure(figsize=(8, 5))
plt.bar(
    summary["Subject"],
    summary["Average"]
)

plt.title("Subject-wise Average Marks")
plt.xlabel("Subject")
plt.ylabel("Average Marks")
plt.ylim(0, 100)
plt.tight_layout()

plt.savefig(
    os.path.join(output_folder, "subject_average.png")
)
plt.close()


# --------------------------------
# 5. Top Performers Chart
# --------------------------------

top_students = df.nlargest(10, "Average")

plt.figure(figsize=(10, 5))
plt.bar(
    top_students["name"],
    top_students["Average"]
)

plt.title("Top 10 Performers")
plt.xlabel("Student")
plt.ylabel("Average Marks")
plt.ylim(0, 100)
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(
    os.path.join(output_folder, "top_performers.png")
)
plt.close()


# --------------------------------
# Output
# --------------------------------

print("Files generated successfully:")
print("cleaned_marks.csv")
print("summary.csv")
print("grade_distribution.png")
print("subject_average.png")
print("top_performers.png")