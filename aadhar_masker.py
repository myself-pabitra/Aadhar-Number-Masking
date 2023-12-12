from pytesseract import Output
import pytesseract
import cv2
import numpy as np


class AadharMasker:
    def __init__(self, source_file):
        self.image = self.process_image(source_file)
        self.image_data = self.get_image_data()
    
    def preprocess_image(self, img):
        # blurred = cv2.GaussianBlur(img, (5, 5), 0)
        blurred = cv2.medianBlur(img,5)
        return blurred

    def process_image(self, source_file):
        contents = source_file.read()
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        processed_img = self.preprocess_image(img)
        
        return processed_img
        # return img


    def check_aadhar_num(self, text):
        return len(text) == 4 and text.isdigit()
    
    def get_image_data(self):
        rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        # Experiment with additional OCR configurations
        custom_config = r'--oem 3 --psm 6'
        res = pytesseract.image_to_data(rgb, output_type=Output.DICT, config=custom_config)
        return res



    def get_uid_details(self):
        """
            UID number has three components all are numbers , 
            the function assumes pytesseract reads all three components serially.
            Return : success/failure, uid_details
        """
        text_data = self.image_data['text']
        print(text_data)
        uid = []
        print(uid)
        for i in range(len(text_data)):
            if self.check_aadhar_num(text_data[i]):
                if len(text_data) < i + 2:
                    return (False, None)
                if self.check_aadhar_num(text_data[i + 1]) and self.check_aadhar_num(text_data[i + 2]):
                    uid.extend((i, i+1, i+2))
                    break
        
        if len(uid) != 3:
            return False, None
        else:
            return True, uid

    def mask_aadhar(self, output_file):
        success, uid = self.get_uid_details()

        if success:
            self.mask_uid_number(uid, output_file)
            return True
        else:
            return False

    def mask_uid_number(self, aadhar_data, output_file):
        for i in range(len(aadhar_data)):
            if i == 2:
                break
            d = aadhar_data[i]
            x = self.image_data['left'][d]
            y = self.image_data['top'][d]
            w = self.image_data['width'][d]
            h = self.image_data['height'][d]
                                    
            cv2.rectangle(self.image, (x, y), (x + w, y + h), (80, 80, 80), -1)
        
        cv2.imwrite(output_file.name, self.image)