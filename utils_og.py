import cv2
import pytesseract
import numpy as np
import os

def thick_font_2(image):
    import numpy as np
    image = cv2.bitwise_not(image)
    kernel = np.ones((2,1),np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    image = cv2.bitwise_not(image)
    return (image)

def thick_font(image):
    import numpy as np
    image = cv2.bitwise_not(image)
    kernel = np.ones((2,2),np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    image = cv2.bitwise_not(image)
    return (image)


def thin_font(image):
    import numpy as np
    image = cv2.bitwise_not(image)
    kernel = np.ones((2,2),np.uint8) # kernel will determine how much is eroded or dilated, small kernel , small erosion or dilation
    image = cv2.erode(image, kernel, iterations=1)
    image = cv2.bitwise_not(image)
    return (image)



def detect_boxes(image):
    
    #Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(image, (5,5), 0)

    h = image.shape[0]
    w = image.shape[1]
    
    # Perform Canny edge detection
    edges = cv2.Canny(blurred, 50, 150)
   
    # Find contours of the detected edges
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda x: cv2.boundingRect(x)[0])
    
    # Iterate over the contours and filter boxes based on size criteria
    detected_boxes = []
    for contour in contours:
        x, y, width, height = cv2.boundingRect(contour)
        if width > int(w/15) and height > int(h/100) and width < int(h/5.4) and height < int(w/40) and y <= (h//2) :
            detected_boxes.append((x, y, width, height))
            cv2.rectangle(image, (x, y), (x + width, y + height), (0, 255, 0), 2)
            
    # cv2.imwrite("temp/textbox.png",image) 
    
    return detected_boxes

def detect_boxes_rest(image):
    
    #Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(image, (5,5), 0)

    h = image.shape[0]
    w = image.shape[1]
    
    # Perform Canny edge detection
    edges = cv2.Canny(blurred, 50, 150)
   
    # Find contours of the detected edges
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda x: cv2.boundingRect(x)[0])
    
    # Iterate over the contours and filter boxes based on size criteria
    detected_boxes = []
    for contour in contours:
        x, y, width, height = cv2.boundingRect(contour)
        if width > int(w/15) and height > int(h/100) and width < int(h/5.4) and height < int(w/40) and y >= int(h/2.2) :
            detected_boxes.append((x, y, width, height))
            cv2.rectangle(image, (x, y), (x + width, y + height), (0, 255, 0), 2)
            
    # cv2.imwrite("temp/textbox.png",image)
    return detected_boxes

    

def noise_removal(image):
    import numpy as np
    kernell = np.ones((2, 2), np.uint8)
    image = cv2.dilate(image, kernell, iterations=1)
    image = cv2.erode(image, kernell, iterations=1)
    image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernell)
    image = cv2.medianBlur(image, 3)
    return (image)
    

def redact_area_aadhar(image, bbox):
    bbox_x,bbox_y,bbox_w,bbox_h = bbox
    redacted_image = image.copy()
    h=image.shape[0]
    w=image.shape[1]
    # Draw a filled rectangle to redact the area
    cv2.rectangle(redacted_image, (bbox_x + bbox_w + (w//200), bbox_y), (bbox_x + bbox_w + (w//200) + (w//3) , bbox_y + bbox_h), (0, 0, 0), -1)
    return redacted_image
    
def redact_area_pan(image,bbox):
    bbox_x,bbox_y,bbox_w,bbox_h = bbox
    redacted_image = image.copy()
    h = image.shape[0]
    w = image.shape[1]
    # Draw a filled rectangle to redact the area
    cv2.rectangle(redacted_image, (bbox_x - (w // 3) - (w//200) , bbox_y+bbox_h -56), (bbox_x - (w // 200) - 35, bbox_y +bbox_h ), (0, 0, 0), -1)
    return redacted_image




def ocr_boxes(no_noise, detected_boxes,image_index,original_img):
    # Convert the image to grayscale
    gray = cv2.cvtColor(no_noise, cv2.COLOR_BGR2GRAY)

    filename = f"{image_index}.png"

    target_word1 = ["Aadhar", "ar Card", "har Nu"]
    target_word2 = ["(PAN)"," Permanent Acc", " Acco", "count "]
    target_word3 = ["er (P"]
    target_word4 = [" Aad","Aadhaar","aar Nu"] 
        
    # Perform OCR on each detected box
    ocr_results = []
    truth = 0
    for bbox in detected_boxes:
        bbox_x, bbox_y, bbox_w, bbox_h = bbox
        box_image = gray[bbox_y:bbox_y+bbox_h, bbox_x:bbox_x+bbox_w]

        # Apply additional preprocessing if necessary (e.g., thresholding, denoising)

        # Perform OCR on the box image
        text = pytesseract.image_to_string(box_image)
        
        # if len(text) == 0 or text.isspace():
        #     continue
        
        matched_words = ["No matchced word"]

        matched_words = [target_word for target_word in target_word1 if target_word in text]
        if matched_words:
            truth = 1
            # print("Target Found! in " + filename)
            # Add the OCR result to the list along with the box coordinates
            ocr_results.append((bbox, text))
            # print("Box Detected:", text)
            redacted_image = redact_area_aadhar(original_img, bbox)
            filename = f"redacted_image_{image_index}.tif"
            cv2.imwrite(filename,redacted_image)
            break


        matched_words = [target_word for target_word in target_word2 if target_word in text]
        if matched_words:
            truth = 1
            # print("Target Found! in " + filename)
            # Add the OCR result to the list along with the box coordinates
            ocr_results.append((bbox, text))
            # print("Box Detected:", text)
            redacted_image = redact_area_pan(original_img, bbox)
            filename = f"redacted_image_{image_index}.tif"
            cv2.imwrite(filename,redacted_image)
            break


        matched_words = [target_word for target_word in target_word3 if target_word in text]
        if matched_words:
            truth = 1
            # print("Target Found! in " + filename)
            # Add the OCR result to the list along with the box coordinates
            ocr_results.append((bbox, text))
            # print("Box Detected:", text)
            redacted_image = redact_area_pan(original_img, bbox)
            filename = f"redacted_image_{image_index}.tif"
            cv2.imwrite(filename,redacted_image)
            break


        matched_words = [target_word for target_word in target_word4 if target_word in text]
        if matched_words:
            truth = 1
            # print("Target Found! in " + filename)
            # Add the OCR result to the list along with the box coordinates
            ocr_results.append((bbox, text))
            # print("Box Detected:", text)
            redacted_image = redact_area_aadhar(original_img, bbox)
            filename = f"redacted_image_{image_index}.tif"
            cv2.imwrite(filename,redacted_image)
            break
    
   
    # Print the location of the bounding box
    if truth == 1:
        # print("Bounding Box Location:", (bbox_x, bbox_y, bbox_w, bbox_h))
        return matched_words[0],1,filename
    else:
        redacted_image = original_img.copy()
        filename = f"redacted_image_{image_index}.tif"
        cv2.imwrite(filename,redacted_image)
        return "No matched words",0,filename



def process_image(image_path,image_index):
    
    img = cv2.imread(image_path)
   
    img_copy = img.copy()
    
    # cv2.imwrite("temp/copyy.jpg",img_copy)
    # img_copy = cv2.imread("temp/copyy.jpg")

    dilated_image1 = thick_font(img_copy)
    
    eroded_image = thin_font(dilated_image1)
   
    dilated_image = thick_font(eroded_image)
    
    # Detect boxes based on the criteria

    detected_boxes = detect_boxes(dilated_image)
    
    no_noise = noise_removal(img)
    no_noise = thick_font_2(no_noise)
    # cv2.imwrite("temp/no_noise.png", no_noise)
    
    matched_word,truth,redacted_filename = ocr_boxes(no_noise, detected_boxes,image_index,img)

    if truth == 0:
        detected_boxes = detect_boxes_rest(dilated_image)
        matched_word,truth,redacted_filename = ocr_boxes(no_noise,detected_boxes,image_index,img)
        # if truth == 0:
            # print("Target word not found!")

    

    return matched_word,truth, redacted_filename