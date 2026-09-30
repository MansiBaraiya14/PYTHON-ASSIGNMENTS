class BankError(Exception):
    pass


class AccountNotFoundError(BankError):
    pass


class InsufficientFundsError(BankError):
    pass


class InvalidAmountError(BankError):
    pass


class Account:
    def __init__(self, account_id, balance):
        self._account_id = account_id
        self._balance = balance
        self._history = []

    @property
    def account_id(self):
        return self._account_id

    @property
    def balance(self):
        return self._balance

    @property
    def history(self):
        return self._history

    def deposit(self, amount):
        if amount <= 0:
            raise InvalidAmountError("Invalid amount")

        self._balance += amount
        self._history.append(("DEPOSIT", amount))

    def withdraw(self, amount):
        if amount <= 0:
            raise InvalidAmountError("Invalid amount")

        if amount > self._balance:
            raise InsufficientFundsError("Insufficient funds")

        self._balance -= amount
        self._history.append(("WITHDRAW", amount))


class Transaction:
    def __init__(self, operation, acc1, acc2=None, amount=0):
        self.operation = operation
        self.acc1 = acc1
        self.acc2 = acc2
        self.amount = amount


class Bank:
    def __init__(self):
        self.accounts = {}
        self.transactions = []

    def add_account(self, account):
        self.accounts[account.account_id] = account

    def get_account(self, account_id):
        if account_id not in self.accounts:
            raise AccountNotFoundError("Account not found")

        return self.accounts[account_id]

    def deposit(self, account_id, amount):
        account = self.get_account(account_id)
        account.deposit(amount)

    def withdraw(self, account_id, amount):
        account = self.get_account(account_id)
        account.withdraw(amount)

    def transfer(self, from_id, to_id, amount):
        sender = self.get_account(from_id)
        receiver = self.get_account(to_id)

        sender.withdraw(amount)
        receiver.deposit(amount)

        self.transactions.append(
            Transaction("TRANSFER", from_id, to_id, amount)
        )

    def execute(self, operation):
        parts = operation.split()

        command = parts[0]

        if command == "DEPOSIT":
            if len(parts) != 3:
                raise BankError("Invalid operation")

            acc = parts[1]
            amount = int(parts[2])

            self.deposit(acc, amount)

        elif command == "WITHDRAW":
            if len(parts) != 3:
                raise BankError("Invalid operation")

            acc = parts[1]
            amount = int(parts[2])

            self.withdraw(acc, amount)

        elif command == "TRANSFER":
            if len(parts) != 4:
                raise BankError("Invalid operation")

            from_acc = parts[1]
            to_acc = parts[2]
            amount = int(parts[3])

            self.transfer(from_acc, to_acc, amount)

        else:
            raise BankError("Invalid operation")


# -----------------------------
# MAIN PROGRAM
# -----------------------------

try:
    bank = Bank()

    # Number of accounts
    n = int(input())

    # Read accounts
    for _ in range(n):
        account_id, balance = input().split()

        bank.add_account(
            Account(account_id, int(balance))
        )

    # Number of operations
    q = int(input())

    batch_active = False
    batch_number = 0
    failed_batches = []

    # Used to restore balances if a batch fails
    batch_backup = {}

    for _ in range(q):
        operation = input().strip()

        if operation == "BATCH_BEGIN":

            if batch_active:
                raise BankError("Nested batch not allowed")

            batch_active = True
            batch_number += 1

            # Save current balances
            batch_backup = {
                acc_id: account.balance
                for acc_id, account in bank.accounts.items()
            }

        elif operation == "BATCH_END":

            if not batch_active:
                raise BankError("BATCH_END without BATCH_BEGIN")

            batch_active = False
            batch_backup = {}

        else:

            try:
                bank.execute(operation)

            except Exception:

                # Operation failed
                if batch_active:

                    # Roll back entire batch
                    for acc_id, old_balance in batch_backup.items():
                        bank.accounts[acc_id]._balance = old_balance

                    failed_batches.append(batch_number)

                    batch_active = False
                    batch_backup = {}

                # If operation is outside a batch,
                # simply ignore the failed operation
                continue

    # Final output
    for acc_id in sorted(bank.accounts):
        print(acc_id, bank.accounts[acc_id].balance)

    for number in failed_batches:
        print("FAILED", number)

except Exception as e:
    print("ERROR")