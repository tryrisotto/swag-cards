import csv
import qrcode
from PIL import Image
import os

def generate_qr_on_image(url, filename, background_image_path):
    # Create a QR code instance
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    # Add URL to the QR code
    qr.add_data(url)
    qr.make(fit=True)

    # Create an image from the QR code instance
    qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGBA')

    # Resize QR code to a fixed size (e.g., 390x390)
    qr_img_resized = qr_img.resize((1850, 1850))

    # Open the background image
    background = Image.open(background_image_path)

    # Set QR code position in pixels
    x_position = int(479.5)  # Rounding to the nearest pixel
    y_position = int(401.5)

    # Paste the QR code onto the background image
    background.paste(qr_img_resized, (x_position, y_position), qr_img_resized)

    # Save the modified image
    background.save(filename)

def process_csv(file_path, background_image_path):
    # Open the CSV file
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for index, row in enumerate(reader):
            url = row[0].strip()  # Assuming the URL is in the first column
            filename = f"combined_qr_{index + 1}.png"
            generate_qr_on_image(url, filename, background_image_path)

    print("QR codes generated successfully and placed on images for all URLs.")

# Path to the CSV file and background image
csv_file_path = 'urls.csv'
background_image_path = 'background.png'  # Change this to your actual background image path

# Check if the CSV file and the background image exist
if os.path.exists(csv_file_path) and os.path.exists(background_image_path):
    process_csv(csv_file_path, background_image_path)
else:
    print("The specified CSV file or background image does not exist.")
