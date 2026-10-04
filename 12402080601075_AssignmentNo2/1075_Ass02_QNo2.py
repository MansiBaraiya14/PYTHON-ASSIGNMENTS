import re


def normalize_price(price):
    # Remove ₹, $, commas, Rs., etc.
    numbers = re.sub(r'[^0-9.]', '', price)

    if numbers:
        return float(numbers)

    return 0


def extract_products(file_path):
    products = []

    with open(file_path, "r", encoding="utf-8") as file:
        html = file.read()

    # Extract product blocks
    blocks = re.findall(
        r'<div\s+class=["\']product["\']>(.*?)</div>',
        html,
        re.DOTALL | re.IGNORECASE
    )

    for block in blocks:

        # Extract name
        name_match = re.search(
            r'<span\s+class=["\']name["\']>(.*?)</span>',
            block,
            re.DOTALL | re.IGNORECASE
        )

        # Extract price
        price_match = re.search(
            r'<span\s+class=["\']price["\']>(.*?)</span>',
            block,
            re.DOTALL | re.IGNORECASE
        )

        # Extract rating
        rating_match = re.search(
            r'<span\s+class=["\']rating["\']>(.*?)</span>',
            block,
            re.DOTALL | re.IGNORECASE
        )

        if name_match and price_match and rating_match:

            name = name_match.group(1).strip()
            price = normalize_price(price_match.group(1).strip())

            try:
                rating = float(rating_match.group(1).strip())
            except ValueError:
                continue

            products.append((name, price, rating))

    return products


# ---------------- MAIN PROGRAM ----------------

p, k = map(int, input().split())

# Dictionary to remove duplicate products by name
products = {}

for _ in range(p):

    file_path = input().strip()

    extracted_products = extract_products(file_path)

    for name, price, rating in extracted_products:

        if name not in products:
            products[name] = (price, rating)

        else:
            old_price, old_rating = products[name]

            # Keep the better product according to ranking rules
            if rating > old_rating:
                products[name] = (price, rating)

            elif rating == old_rating and price < old_price:
                products[name] = (price, rating)


# Convert dictionary to list
product_list = []

for name, (price, rating) in products.items():
    product_list.append((name, price, rating))


# Sort:
# 1. Highest rating
# 2. Lowest price
# 3. Lexicographically smallest name
product_list.sort(
    key=lambda x: (-x[2], x[1], x[0])
)


# Print top K products
for name, price, rating in product_list[:k]:

    # Print integer price without .0
    if price.is_integer():
        price = int(price)

    print(name, price, rating)