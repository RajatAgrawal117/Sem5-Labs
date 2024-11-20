import hashlib
import json
import os
import logging

# Directory and file paths
BASE_DIR = r"Practical 10"
USER_DATA_FILE = os.path.join(BASE_DIR, "users.json")
LOG_FILE = os.path.join(BASE_DIR, "user_activity.log")

# Ensure the directory exists
os.makedirs(BASE_DIR, exist_ok=True)

# Configure logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)


def load_user_data():
    """Load user data from a JSON file."""
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r") as file:
            return json.load(file)
    else:
        return {}


def save_user_data(user_data):
    """Save user data to a JSON file."""
    with open(USER_DATA_FILE, "w") as file:
        json.dump(user_data, file, indent=4)


def hash_password(password):
    """Hash a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()


def register_user(username, password):
    """Register a new user with a hashed password and log the activity."""
    user_data = load_user_data()
    
    if username in user_data:
        print("Username already exists. Please choose a different username.")
        return False
    
    user_data[username] = hash_password(password)
    save_user_data(user_data)
    print("Sign up successful.")
    logging.info(f"User '{username}' registered successfully.")
    return True


def login_user(username, password):
    """Log in an existing user by checking the hashed password and log the activity."""
    user_data = load_user_data()
    
    if username not in user_data:
        print("Username not found.")
        logging.warning(f"Unsuccessful login attempt by '{username}' (username not found).")
        return False
    
    hashed_password = hash_password(password)
    if user_data[username] == hashed_password:
        print("Log in successful.")
        logging.info(f"User '{username}' logged in successfully.")
        return True
    else:
        print("Incorrect password.")
        logging.warning(f"Unsuccessful login attempt by '{username}' (incorrect password).")
        return False


def main():
    print("USER MANAGEMENT SYSTEM")
    while True:
        print("\nMenu:")
        print("1. Sign Up")
        print("2. Log In")
        print("3. Exit")
        
        choice = input("Enter choice: ").strip()
        
        if choice == "1":
            username = input("Enter username: ").strip()
            if not username:
                print("Username cannot be empty.")
                continue
            password = input("Enter password: ").strip()
            if not password:
                print("Password cannot be empty.")
                continue
            register_user(username, password)
        
        elif choice == "2":
            username = input("Enter username: ").strip()
            password = input("Enter password: ").strip()
            login_user(username, password)
        
        elif choice == "3":
            print("Exiting the program.")
            break
        
        else:
            print("Invalid option. Please choose 1, 2, or 3.")


if __name__ == "__main__":
    main()
