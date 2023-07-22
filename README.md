# Aadhar Masking Tool

## Description
The Aadhar Masking Tool is a Python application designed to mask sensitive information in Aadhar documents. It provides a user-friendly interface to process multiple tif files simultaneously and save the processed documents to a specified output directory.

## Prerequisites
Before running the Aadhar Masking Tool, ensure that you have the following software installed on your system:
- Python (version 3.6 or above)
- Streamlit, cv2, pytesseract, numpy, pillow (installed via pip or conda)
- You can install the dependencies using:

```
pip install opencv-python pytesseract numpy streamlit Pillow
```

## Usage
To launch the Aadhar Masking Tool, follow these steps:

1. Open a terminal or command prompt.
2. Navigate to the directory where the tool is located.
3. Run the following command:

```
streamlit run MaskingApp.py
```

## Instructions
Once the Aadhar Masking Tool is running, you can perform the following steps:

1. Drag and drop multiple tif files into the application.
2. Specify the output directory (eg: output_directory) where you want the processed documents to be saved.
3. The tool will create a file called `masking_output` in the specified output directory and save all the processed files there.

Please note that the Aadhar Masking Tool is designed to handle tif files specifically. Make sure the files you want to process are in the correct format.