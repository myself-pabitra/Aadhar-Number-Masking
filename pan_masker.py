from pytesseract import Output
import pytesseract
import cv2
import numpy as np


class PanMasker:
    def __init__(self, source_file):
        self.image = self.process_image(source_file)
        self.image_data = self.get_image_data()

    def preprocess_image(self, img):
        blurred = cv2.medianBlur(img, 5)
        return blurred

    def process_image(self, source_file):
        contents = source_file.read()
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        processed_img = self.preprocess_image(img)
        return processed_img

    def check_pan_number(self, text):

        return len(text) == 10 and text[:5].isalpha() and text[5:9].isdigit() and text[9].isalpha()

        # This will work for samarjit
        # return len(text) == 10 and text[:5].isalpha() and text[5:9].isdigit() 

    def get_image_data(self):
        rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        custom_config = r'--oem 3 --psm 6'
        res = pytesseract.image_to_data(rgb, output_type=Output.DICT, config=custom_config)
        return res

    def get_pan_details(self):
        text_data = self.image_data['text']

        # Clean up the text by removing empty strings and irrelevant characters
        cleaned_text = [text.strip() for text in text_data if text.strip()]
        print(cleaned_text)
        pan_details = []

        for i in range(len(cleaned_text)):
            current_text = cleaned_text[i]
            if self.check_pan_number(current_text):
                print(current_text)
                # Assume the PAN number is a 10-character alphanumeric code
                pan_number = current_text
                for j in range(1, 9):
                    next_text = cleaned_text[i + j] if i + j < len(cleaned_text) else ""
                    if len(next_text) == 1 and (next_text.isalpha() or next_text.isdigit()):
                        pan_number += next_text
                    else:
                        break

                if len(pan_number) == 10:
                    pan_details.append(pan_number)
                    break

        if len(pan_details) != 1:
            return False, None
        else:
            return True, pan_details

    def mask_pan_number(self, pan_data, output_file):
        # Find the index of the first character of the PAN number in the OCR output
        pan_char_index = self.image_data['text'].index(pan_data[0])

        # Calculate the width for first 6 digits assuming equal width per character
        char_width = int(self.image_data['width'][pan_char_index] / 5)

        # Adjust the rectangle coordinates to cover only the first 6 digits
        x = self.image_data['left'][pan_char_index]
        w = char_width * 3
        y = self.image_data['top'][pan_char_index]
        h = self.image_data['height'][pan_char_index]

        # Draw a rectangle to mask only the first 6 digits
        cv2.rectangle(self.image, (x, y), (x + w, y + h), (80, 80, 80), -1)

        # Write the modified image to the output file
        cv2.imwrite(output_file.name, self.image)




    def mask_pan(self, output_file):
        success, pan_data = self.get_pan_details()

        if success:
            self.mask_pan_number(pan_data, output_file)
            return True
        else:
            return False
