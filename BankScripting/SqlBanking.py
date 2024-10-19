import sqlite3

class Account:
    def _init_(self, account_number, name, initial_balance=0):
        self.account_number = account_number
        self.name = name
        self.balance = initial_balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            print(f"Deposited {amount} into account {self.account_number}")
        else:
            print("Deposit amount must be positive.")

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            print(f"Withdrew {amount} from account {self.account_number}")
        else:
            print("Invalid withdrawal amount or insufficient funds.")

    def check_balance(self):
        print(f"Account {self.account_number}, Balance: {self.balance}")

class Bank:
    def __init__(self):
        # Connect to SQLite database (or create it if it doesn't exist)
        self.conn = sqlite3.connect('bank.db')
        self.create_accounts_table()

    def create_accounts_table(self):
        # Create a table for storing account details if it doesn't exist
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS accounts (
                    account_number TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    balance REAL NOT NULL
                )
            ''')

    def create_account(self, account_number, name, initial_balance):
        with self.conn:
            # Check if the account already exists
            if self.get_account(account_number):
                print(f"Account {account_number} already exists.")
            else:
                self.conn.execute('''
                    INSERT INTO accounts (account_number, name, balance)
                    VALUES (?, ?, ?)
                ''', (account_number, name, initial_balance))
                print(f"Created account for {name} with account number {account_number}")

    def get_account(self, account_number):
        cursor = self.conn.execute('''
            SELECT account_number, name, balance FROM accounts
            WHERE account_number = ?
        ''', (account_number,))
        row = cursor.fetchone()
        if row:
            return Account(row[0], row[1], row[2])
        return None

    def update_balance(self, account_number, new_balance):
        with self.conn:
            self.conn.execute('''
                UPDATE accounts SET balance = ? WHERE account_number = ?
            ''', (new_balance, account_number))

def main():
    bank = Bank()

    while True:
        print("\nBanking System")
        print("1. Create an account")
        print("2. Deposit money")
        print("3. Withdraw money")
        print("4. Check balance")
        print("5. Quit")

        choice = input("Enter your choice: ")

        if choice == '1':
            account_number = input("Enter a new account number: ")
            name = input("Enter account holder's name: ")
            initial_balance = float(input("Enter the initial balance: "))
            bank.create_account(account_number, name, initial_balance)
        elif choice == '2':
            account_number = input("Enter the account number: ")
            account = bank.get_account(account_number)
            if account:
                amount = float(input("Enter the amount to deposit: "))
                account.deposit(amount)
                bank.update_balance(account.account_number, account.balance)
            else:
                print("Account not found.")
        elif choice == '3':
            account_number = input("Enter the account number: ")
            account = bank.get_account(account_number)
            if account:
                amount = float(input("Enter the amount to withdraw: "))
                account.withdraw(amount)
                bank.update_balance(account.account_number, account.balance)
            else:
                print("Account not found.")
        elif choice == '4':
            account_number = input("Enter the account number: ")
            account = bank.get_account(account_number)
            if account:
                account.check_balance()
            else:
                print("Account not found.")
        elif choice == '5':
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == '__main__':
    main()