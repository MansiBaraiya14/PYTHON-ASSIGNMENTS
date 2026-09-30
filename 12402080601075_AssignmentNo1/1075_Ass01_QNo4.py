import csv
from datetime import datetime
from collections import defaultdict
import os


# Get input CSV file path
file_path = input("Enter CSV file path: ").strip()

balance = defaultdict(float)

try:
    with open(file_path, "r", newline="") as infile:

        reader = csv.DictReader(infile)

        # Check required columns
        required_columns = {
            "tid", "acc", "type", "amount", "time"
        }

        if not reader.fieldnames or not required_columns.issubset(
            set(reader.fieldnames)
        ):
            print("Invalid CSV header")
            exit()

        # Create output files
        with open("credit.csv", "w", newline="") as credit_file, \
             open("debit.csv", "w", newline="") as debit_file, \
             open("error.csv", "w", newline="") as error_file:

            credit_writer = csv.writer(credit_file)
            debit_writer = csv.writer(debit_file)
            error_writer = csv.writer(error_file)

            # Headers
            credit_writer.writerow(
                ["tid", "acc", "type", "amount", "time"]
            )

            debit_writer.writerow(
                ["tid", "acc", "type", "amount", "time"]
            )

            error_writer.writerow(
                ["tid", "acc", "type", "amount", "time", "reason"]
            )

            # Process every row
            for row in reader:

                try:
                    tid = row["tid"].strip()
                    acc = row["acc"].strip()
                    trans_type = row["type"].strip().upper()
                    amount_text = row["amount"].strip()
                    timestamp = row["time"].strip()

                    # Validate empty fields
                    if not tid or not acc or not amount_text or not timestamp:
                        raise ValueError("Missing field")

                    # Validate transaction type
                    if trans_type not in ("CREDIT", "DEBIT"):
                        raise ValueError("Invalid transaction type")

                    # Validate amount
                    try:
                        amount = float(amount_text)
                    except ValueError:
                        raise ValueError("Amount is not numeric")

                    if amount <= 0:
                        raise ValueError("Amount must be greater than 0")

                    # Validate timestamp
                    try:
                        datetime.strptime(
                            timestamp,
                            "%Y-%m-%dT%H:%M:%S"
                        )
                    except ValueError:
                        raise ValueError("Invalid timestamp")

                    # Original row
                    output_row = [
                        tid,
                        acc,
                        trans_type,
                        amount_text,
                        timestamp
                    ]

                    # Store valid transaction
                    if trans_type == "CREDIT":
                        credit_writer.writerow(output_row)
                        balance[acc] += amount

                    else:
                        debit_writer.writerow(output_row)
                        balance[acc] -= amount

                except Exception as e:

                    error_writer.writerow([
                        row.get("tid", ""),
                        row.get("acc", ""),
                        row.get("type", ""),
                        row.get("amount", ""),
                        row.get("time", ""),
                        str(e)
                    ])

                    # Continue with next row
                    continue

    # Print account-wise summary
    print("\nAccount-wise balance changes:")

    sorted_balance = sorted(
        balance.items(),
        key=lambda x: abs(x[1]),
        reverse=True
    )

    for account, amount in sorted_balance:
        if amount.is_integer():
            amount = int(amount)

        print(account, amount)

    print("\nFiles created:")
    print("credit.csv")
    print("debit.csv")
    print("error.csv")

except FileNotFoundError:
    print("File not found.")

except Exception as e:
    print("Error:", e)