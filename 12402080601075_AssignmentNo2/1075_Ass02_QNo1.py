import re

# Regex for valid email addresses
pattern = re.compile(
    r'[A-Za-z0-9+._-]+@[A-Za-z0-9-]+\.(?:com|edu|org)'
)

def extract_emails(file_path):

    # Dictionary to store unique emails for each domain
    domain_emails = {}

    # Read file line by line
    with open(file_path, "r", encoding="utf-8") as file:

        for line in file:

            # Find all email addresses in the current line
            emails = pattern.findall(line)

            for email in emails:

                # Extract domain
                domain = email.split("@")[1]

                # Create a set for a new domain
                if domain not in domain_emails:
                    domain_emails[domain] = set()

                # Add email to set
                domain_emails[domain].add(email)

    # Print domains in lexicographic order
    for domain in sorted(domain_emails):

        emails = domain_emails[domain]

        # Find smallest email
        smallest_email = min(emails)

        print(domain, len(emails), smallest_email)


# Take file path from user
file_path = input("Enter file path: ")

extract_emails(file_path)