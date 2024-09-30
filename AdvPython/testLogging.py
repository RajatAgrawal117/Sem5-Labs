import logging

logging.basicConfig(filename='file_operations.log', level=logging.INFO)

def read_file(filename):
    try:
        with open(filename, "r") as file:
            content = file.read()
            logging.info(f"Read from {filename}: {content}")
    except Exception as e:
        logging.error(f"Error reading {filename}: {e}")

def write_file(filename, content):
    try:
        with open(filename, "w") as file:
            file.write(content)
            logging.info(f"Wrote to {filename}: {content}")
    except Exception as e:
        logging.error(f"Error writing to {filename}: {e}")

write_file("sample.txt", "Hello World!")
read_file("sample.txt")
import schedule, time
