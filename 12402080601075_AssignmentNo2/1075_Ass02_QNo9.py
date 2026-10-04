class Product:
    def __init__(self, product_id, name, stock, purchase_price, selling_price):
        self.product_id = product_id
        self.name = name
        self.stock = stock
        self.purchase_price = purchase_price
        self.selling_price = selling_price

    def total_value(self):
        return self.stock * self.selling_price


class Inventory:
    def __init__(self):
        self.products = {}

    # Add product
    def add_product(self, product):
        if product.product_id in self.products:
            return False

        self.products[product.product_id] = product
        return True

    # Delete product
    def delete_product(self, product_id):
        if product_id not in self.products:
            return False

        del self.products[product_id]
        return True

    # Update stock
    def update_stock(self, product_id, new_stock):
        if product_id not in self.products:
            return False

        self.products[product_id].stock = new_stock
        return True

    # Calculate total inventory value
    def total_value(self):
        return sum(
            product.total_value()
            for product in self.products.values()
        )

    # Compare inventories using total value
    def __lt__(self, other):
        return self.total_value() < other.total_value()

    def __eq__(self, other):
        return self.total_value() == other.total_value()

    # Merge two inventories using +
    def __add__(self, other):
        merged = Inventory()

        # Copy products from first inventory
        for product in self.products.values():
            merged.products[product.product_id] = Product(
                product.product_id,
                product.name,
                product.stock,
                product.purchase_price,
                product.selling_price
            )

        # Add products from second inventory
        for product in other.products.values():

            if product.product_id not in merged.products:
                merged.products[product.product_id] = Product(
                    product.product_id,
                    product.name,
                    product.stock,
                    product.purchase_price,
                    product.selling_price
                )

            else:
                existing = merged.products[product.product_id]

                # Merge stock
                existing.stock += product.stock

                # Lower purchase price
                existing.purchase_price = min(
                    existing.purchase_price,
                    product.purchase_price
                )

                # Higher selling price
                existing.selling_price = max(
                    existing.selling_price,
                    product.selling_price
                )

        return merged

    # Display inventory
    def display(self):
        for product_id in sorted(self.products):
            p = self.products[product_id]

            print(
                f"{p.product_id} {p.name} "
                f"stock={p.stock} "
                f"purchase={p.purchase_price} "
                f"selling={p.selling_price}"
            )

        print(f"Total valuation={self.total_value()}")


# -------------------------------
# Main Program
# -------------------------------

inventory_a = Inventory()
inventory_b = Inventory()

# Number of products in inventory A
n = int(input("Enter number of products in Inventory A: "))

for _ in range(n):
    product_id, name, stock, purchase, selling = input().split()

    inventory_a.add_product(
        Product(
            product_id,
            name,
            int(stock),
            int(purchase),
            int(selling)
        )
    )


# Number of products in inventory B
m = int(input("Enter number of products in Inventory B: "))

for _ in range(m):
    product_id, name, stock, purchase, selling = input().split()

    inventory_b.add_product(
        Product(
            product_id,
            name,
            int(stock),
            int(purchase),
            int(selling)
        )
    )


# Operations
q = int(input("Enter number of operations: "))

for _ in range(q):

    operation = input().split()

    if operation[0] == "ADD":
        _, inventory, product_id, name, stock, purchase, selling = operation

        product = Product(
            product_id,
            name,
            int(stock),
            int(purchase),
            int(selling)
        )

        target = inventory_a if inventory == "A" else inventory_b

        if target.add_product(product):
            print("ADD SUCCESS")
        else:
            print("ADD FAILED")

    elif operation[0] == "DELETE":
        _, inventory, product_id = operation

        target = inventory_a if inventory == "A" else inventory_b

        if target.delete_product(product_id):
            print("DELETE SUCCESS")
        else:
            print("DELETE FAILED")

    elif operation[0] == "UPDATE":
        _, inventory, product_id, stock = operation

        target = inventory_a if inventory == "A" else inventory_b

        if target.update_stock(product_id, int(stock)):
            print("UPDATE SUCCESS")
        else:
            print("UPDATE FAILED")

    elif operation[0] == "COMPARE":
        if inventory_a < inventory_b:
            print("Inventory B has higher value")
        elif inventory_a == inventory_b:
            print("Both inventories have equal value")
        else:
            print("Inventory A has higher value")

    elif operation[0] == "MERGE":
        merged = inventory_a + inventory_b

        print("MERGED INVENTORY")
        merged.display()