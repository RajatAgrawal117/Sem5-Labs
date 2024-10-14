import logging

# Set up logging configuration
logging.basicConfig(
    filename="banking_system.log",
    filemode="w",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.DEBUG
)


accounts = {}

def create_account(account_name, initial_balance):
    logging.info(f"Attempting to create a new account: {account_name}")

    try:
        if account_name in accounts:
            logging.warning(f"Account {account_name} already exists.")
            return "Account already exists."

        if initial_balance < 0:
            logging.warning(
                f"Cannot create account {account_name} with a negative balance.")
            return "Initial balance cannot be negative."

        accounts[account_name] = initial_balance
        logging.debug(
            f"Account {account_name} created successfully with balance {initial_balance}.")
        return f"Account {account_name} created successfully."

    except Exception as e:
        logging.error(f"Error creating account {account_name}: {str(e)}")
        raise




def withdraw_money(account_name, amount):
    logging.info(
        f"Attempting to withdraw {amount} from account: {account_name}")

    try:
        if account_name not in accounts:
            logging.warning(f"Account {account_name} does not exist.")
            return "Account does not exist."

        if amount <= 0:
            logging.warning(f"Invalid withdrawal amount: {amount}")
            return "Withdrawal amount must be greater than zero."

        if accounts[account_name] < amount:
            logging.warning(
                f"Insufficient funds in account {account_name}. Available balance: {accounts[account_name]}.")
            return "Insufficient funds."

        accounts[account_name] -= amount
        logging.debug(
            f"Withdrawal of {amount} from account {account_name} successful. Remaining balance: {accounts[account_name]}.")
        return f"Withdrawal of {amount} successful. Remaining balance: {accounts[account_name]}."

    except Exception as e:
        logging.error(f"Error withdrawing money from {account_name}: {str(e)}")
        raise


def main():
    logging.info("Banking system started")

    try:
        # Create accounts
        print(create_account("Alice", 100))
        print(create_account("Bob", -50))  # This should trigger a warning
        print(create_account("Alice", 200))  # This should trigger a warning

        # Withdraw money
        print(withdraw_money("Alice", 30))
        print(withdraw_money("Bob", 50))  # This should trigger a warning
        # This should trigger a warning for insufficient funds
        print(withdraw_money("Alice", 150))

    except Exception as e:
        logging.error(f"Application encountered an error: {str(e)}")

    logging.info("Banking system finished")


if __name__ == "__main__":
    main()
