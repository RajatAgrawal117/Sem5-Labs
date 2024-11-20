from PIL import Image, ImageFilter, ImageEnhance
import matplotlib.pyplot as plt
import numpy as np

# Step 1: Image Loading and Display
def load_and_display_image(file_path):
    try:
        img = Image.open(file_path)
        img.show()  # Display the image
        print("Image loaded successfully.")
        return img
    except FileNotFoundError:
        print("Error: Image file not found.")
        return None

# Step 2: Image Manipulation Functions

# Apply a Gaussian blur filter
def apply_gaussian_blur(img, radius=2):
    return img.filter(ImageFilter.GaussianBlur(radius))

# Adjust brightness
def adjust_brightness(img, factor=1.0):
    enhancer = ImageEnhance.Brightness(img)
    return enhancer.enhance(factor)

# Convert to grayscale
def convert_to_grayscale(img):
    return img.convert("L")

# Resize image
def resize_image(img, width, height):
    return img.resize((width, height))

# Apply edge detection
def apply_edge_detection(img):
    return img.filter(ImageFilter.FIND_EDGES)

# Step 3: Histogram Analysis
def show_histogram(img):
    # Convert image to RGB if it isn't already
    if img.mode != 'RGB':
        img = img.convert('RGB')

    # Split the channels
    r, g, b = img.split()

    # Calculate histogram
    r_hist = np.array(r.histogram())
    g_hist = np.array(g.histogram())
    b_hist = np.array(b.histogram())

    # Plot histograms
    plt.figure(figsize=(10, 4))
    plt.subplot(1, 3, 1)
    plt.plot(r_hist, color='red')
    plt.title("Red Channel Histogram")
    plt.subplot(1, 3, 2)
    plt.plot(g_hist, color='green')
    plt.title("Green Channel Histogram")
    plt.subplot(1, 3, 3)
    plt.plot(b_hist, color='blue')
    plt.title("Blue Channel Histogram")
    plt.tight_layout()
    plt.show()

# Main Program Flow
def main():
    # Step 1: Load and display the image
    file_path = input("Enter the path of the image file: ")
    img = load_and_display_image(file_path)

    if img is None:
        return

    # Step 2: Image Manipulation options
    print("\nSelect an image manipulation option:")
    print("1. Apply Gaussian Blur")
    print("2. Adjust Brightness")
    print("3. Convert to Grayscale")
    print("4. Resize Image")
    print("5. Apply Edge Detection")
    choice = int(input("Enter choice (1-5): "))

    if choice == 1:
        radius = float(input("Enter blur radius: "))
        img = apply_gaussian_blur(img, radius)
    elif choice == 2:
        factor = float(input("Enter brightness factor (1.0 = original): "))
        img = adjust_brightness(img, factor)
    elif choice == 3:
        img = convert_to_grayscale(img)
    elif choice == 4:
        width = int(input("Enter new width: "))
        height = int(input("Enter new height: "))
        img = resize_image(img, width, height)
    elif choice == 5:
        img = apply_edge_detection(img)
    else:
        print("Invalid choice.")
        return

    # Display manipulated image
    img.show()

    # Step 3: Histogram Analysis
    print("\nDisplaying histogram for the manipulated image.")
    show_histogram(img)

if __name__ == "__main__":
    main()
