# Aadhaar Masking Tool

## Description
The Aadhaar Masking Tool is a Python application designed to mask sensitive information in Aadhaar documents from Future Generali India Life Insurance Company. It provides a user-friendly interface to process multiple tif files simultaneously and save the processed documents to a specified output directory. I have attatched a template of the application form to display how it redacts the image. I would encourage you to look around in the utils_og and have a look at the functions and what they do. Currently, this tool only works on Future Generali's handwritten applications since that is what it was designed for but I will update it as I work to expand its usability.

## Prerequisites
Create a directory named `.streamlit` withing the present working directory and save the `config.toml` file there.
Before running the Aadhaar Masking Tool, ensure that you have the following software installed on your system:
- Python (version 3.6 or above)
- Tesseract (this has to be downloaded from https://github.com/UB-Mannheim/tesseract/wiki and added to PATH)
- Streamlit, OpenCV, Pytesseract, Numpy, Pillow, Tesseract (installed via pip or conda)
- You can install the dependencies using:

```
pip install opencv-python tesseract pytesseract numpy streamlit Pillow 
```

## Usage
To launch the Aadhaar Masking Tool, follow these steps:

1. Open a terminal or command prompt.
2. Navigate to the directory where the tool is located.
3. Run the following command:

```
streamlit run MaskingApp.py
```
Or run the follwing command to launch the version with the download button.
```
streamlit run MaskingDownload.py
```

## Instructions
Once the Aadhaar Masking Tool is running, you can perform the following steps:

1. Drag and drop multiple tif files into the application.
2. Specify the output directory (eg: output_directory) where you want the processed documents to be saved.
3. The tool will create a file called `masking_output` in the specified output directory and save all the processed files there.

Please note that the Aadhaar Masking Tool is designed to handle tif files specifically. Make sure the files you want to process are in the correct format.

##IMAGES

1. The image below shows the UI of MaskingApp.py and its performance with 19 multi-page tiff files.

2. The image below shows the UI of MaskingDownload.py and its performance with 19 multi-page tiff files.

3. The image below shows the UI of MaskingParallel.py and its performance with 19 multi-age tiff files.

