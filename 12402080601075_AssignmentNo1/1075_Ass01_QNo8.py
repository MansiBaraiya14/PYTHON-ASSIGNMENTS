import os
import re
import pickle
import zipfile


def normalize_tokens(text):
    # Convert to lowercase and extract words
    return re.findall(r'[a-zA-Z0-9_]+', text.lower())


def build_index(folder_path, zip_name):

    index = {}

    total_files = 0
    total_lines = 0

    # Create temporary pickle file
    pickle_path = "index.pkl"

    # Scan all files in folder
    for file_name in os.listdir(folder_path):

        file_path = os.path.join(folder_path, file_name)

        # Only process files
        if not os.path.isfile(file_path):
            continue

        total_files += 1

        try:
            with open(file_path, "r", encoding="utf-8") as file:

                for line_number, line in enumerate(file, start=1):

                    total_lines += 1

                    tokens = normalize_tokens(line)

                    # Avoid storing same token twice
                    # for the same file and line
                    for token in set(tokens):

                        if token not in index:
                            index[token] = []

                        index[token].append(
                            (file_name, line_number)
                        )

        except (UnicodeDecodeError, OSError):
            continue

    # Save index using pickle
    with open(pickle_path, "wb") as file:
        pickle.dump(index, file)

    # Create ZIP file
    with zipfile.ZipFile(
        zip_name,
        "w",
        zipfile.ZIP_DEFLATED
    ) as archive:

        # Add original log files
        for file_name in os.listdir(folder_path):

            file_path = os.path.join(folder_path, file_name)

            if os.path.isfile(file_path):
                archive.write(
                    file_path,
                    arcname=os.path.join(
                        "logs",
                        file_name
                    )
                )

        # Add pickle index
        archive.write(
            pickle_path,
            arcname="index.pkl"
        )

    # Delete temporary pickle file
    os.remove(pickle_path)

    print("FILES", total_files)
    print("LINES", total_lines)
    print("TOKENS", len(index))


def search_index(pickle_path, queries):

    # Load pickle index
    with open(pickle_path, "rb") as file:
        index = pickle.load(file)

    for query in queries:

        token = query.lower()

        matches = index.get(token, [])

        print(token + ":")

        for file_name, line_number in matches:
            print(f"{file_name}:{line_number}")


# -----------------------------
# MAIN PROGRAM
# -----------------------------

try:

    first_line = input().strip()
    parts = first_line.split()

    mode = parts[0].upper()

    if mode == "BUILD":

        if len(parts) != 3:
            print("INVALID")
        else:
            folder_path = parts[1]
            zip_name = parts[2]

            build_index(folder_path, zip_name)

    elif mode == "SEARCH":

        if len(parts) != 2:
            print("INVALID")
        else:

            pickle_path = parts[1]

            q = int(input())

            queries = []

            for _ in range(q):
                queries.append(input().strip())

            search_index(pickle_path, queries)

    else:
        print("INVALID")

except Exception as e:
    print("ERROR")