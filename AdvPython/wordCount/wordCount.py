import os
import wordcloud
import matplotlib.pyplot as plt

class CustomFileNotFoundError(Exception):
    def __init__(self, message="File not found. Please check the file path."):
        self.message = message
        super().__init__(self.message)

class InvalidDataError(Exception):
    def __init__(self, message="Data is invalid. Must be a non-empty string."):
        self.message = message
        super().__init__(self.message)

class OutputSizeExceededError(Exception):
    def __init__(self, message="Output size exceeds limit. Cannot write to file."):
        self.message = message
        super().__init__(self.message)

def validate_file_path(file_path):
    if not os.path.isfile(file_path):
        raise CustomFileNotFoundError(f"File '{file_path}' not found.")
    return file_path

def fetch_file_content(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        if not content.strip():
            raise InvalidDataError("The input file contains no valid data.")
        return content

def analyze_text(content):
    word_count = sum(1 for word in content.split())
    char_frequency = {char: content.count(char) for char in set(content)}
    word_cloud_text = " ".join(content.split())
    return word_count, char_frequency, word_cloud_text

def generate_and_show_wordcloud(content):
    wc = wordcloud.WordCloud().generate(content)
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")
    plt.savefig("WordCloudImage.png")

def verify_output_size(content, size_limit_mb=1):
    if len(content.encode('utf-8')) > size_limit_mb * 1024 * 1024:
        raise OutputSizeExceededError(f"Output exceeds {size_limit_mb} MB size limit.")

def save_results(output_path, word_count, char_frequency, word_cloud_text):
    output_content = f"Word Count: {word_count}\nCharacter Frequencies: {char_frequency}\nWord Cloud Text:\n{word_cloud_text}\n"
    verify_output_size(output_content)
    
    with open(output_path, 'w') as output_file:
        output_file.write(output_content)
    print(f"Results successfully written to '{output_path}'")

def main():
    input_file = input("Enter input file path: ")
    output_file = input("Enter output file path: ")

    try:
        file_path = validate_file_path(input_file)
        content = fetch_file_content(file_path)
        generate_and_show_wordcloud(content)
        word_count, char_frequency, word_cloud_text = analyze_text(content)
        save_results(output_file, word_count, char_frequency, word_cloud_text)
    except (CustomFileNotFoundError, InvalidDataError, OutputSizeExceededError) as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
