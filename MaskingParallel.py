from PIL import Image
from utils_og import process_image
import os
import streamlit as st
import time
import shutil
import concurrent.futures

#------------------------------importing ends------------------------------

favicon = Image.open("UIDAI-logo.jpg")
st.set_page_config(page_title='Aadhaar Masking Tool', page_icon=favicon, layout="wide")  # Set app layout to wide mode

#------------------------------Page config ends------------------------------

def is_duplicate_page(page1, page2): 
    # for detecting duplicates 
    # Compare the pixel data of two pages
    return page1.tobytes() == page2.tobytes()

def redact_document(file_info): 
    # for redacting a single document
    file, output_dir, index = file_info
    redacted_files = []
    success_count = 0
    
    # Get the original filename
    filename = os.path.basename(file)

    # Process the uploaded image and get the redacted file name
    matched_word, truth, redacted_filename = process_image(file, index)

    # Open the multi-page TIFF image
    multi_page_tiff = Image.open(file)

    # Create a new list to store combined pages
    combined_pages = []
       
    # Append the first page directly to combined_pages
    combined_pages.append(multi_page_tiff)

    if truth == 0:
        success_count += 0;     
        masking_status = "unmasked"
        # If the truth value is 0, save the file as "originalname_unmasked.tif"
        unmasked_filename = f"{os.path.splitext(filename)[0]}_unmasked.tif"
        unmasked_filepath = os.path.join(output_dir, unmasked_filename)
        shutil.copy(file, unmasked_filepath)
        redacted_files.append(unmasked_filepath)
        os.remove(redacted_filename)

    elif truth == 1:
        # Redact the first page
        redacted_page = Image.open(redacted_filename).convert("RGBA")
        combined_pages[0] = redacted_page

        success_count += 1
        masking_status = "masked"

        # Iterate over the remaining pages in the multi-page TIFF image
        for j in range(1, multi_page_tiff.n_frames):
            multi_page_tiff.seek(j)
            current_page = multi_page_tiff.copy()

            # Check if the current page is a duplicate of any previously seen page
            is_duplicate = False
            for seen_page in combined_pages:
                if is_duplicate_page(seen_page, current_page):
                    is_duplicate = True
                    break

            if not is_duplicate:
                # Append unique pages to combined_pages
                combined_pages.append(current_page)

        if len(combined_pages) > 1:
            # Combine the modified pages and the first page into a single multi-page TIFF image
            combined_filename = f"{os.path.splitext(filename)[0]}_{masking_status}_{matched_word}.tif"
            combined_filepath = os.path.join(output_dir, combined_filename)
            combined_pages[0].save(str(combined_filepath), save_all=True, append_images=combined_pages[1:])
            redacted_files.append(combined_filepath)
            os.remove(redacted_filename)
        
        elif len(combined_pages) == 1:
            redacted_page = Image.open(redacted_filename).convert("RGBA")
            redacted_filename_single = f"{os.path.splitext(filename)[0]}_{masking_status}_{matched_word}.tif"
            redacted_filepath_single = os.path.join(output_dir, redacted_filename_single)
            redacted_page.save(redacted_filepath_single)
            os.remove(redacted_filename)
            redacted_files.append(redacted_filepath_single)
    

    return redacted_files, success_count


def redact_documents(file_list, output_dir, progress_bar): 
    # for redacting multiple documents using parallel processing
    redacted_files = []
    success_count = 0
    progress_text = st.empty()
    # Create a list of file information to pass to the redact_document function
    file_info_list = [(file, output_dir, i + 1) for i, file in enumerate(file_list)]
    total_files = len(file_info_list)

    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = executor.map(redact_document, file_info_list)

        for i, result in enumerate(results):
            files, count = result
            redacted_files.extend(files)
            success_count += count
            
            # Update progress
            progress = (i + 1) / total_files
            progress_bar.progress(progress)

            if total_files > 1:
                progress_text.text(f"Processed {i + 1} out of {total_files} files")
            else:
                progress_text.text(f"Processed {i + 1} out of {total_files} file")

    return redacted_files, success_count


#------------------------------Funtion definition ends------------------------------

def main():
    st.markdown('''
    <style>
    body {
        margin: 0px;
        font-family: helvetica;
        font-weight: 400;
        line-height: 1.6;
        color: rgb(20, 2, 2);
        background-color: white;
        text-size-adjust: 100%;
        -webkit-tap-highlight-color: rgba(0, 0, 0, 0);
        -webkit-font-smoothing: auto;
        primary-color: #C52319
    }

    h1 {
        font-family: helvetica;
        font-weight: 700;
        color: rgb(20, 2, 2);
        padding: 1.25rem 0px 1rem;
        margin: 0px;
        line-height: 1.2;
    }
    img[Attributes Style] {
        width: 160px;
        height: 90px;
       
    }
    
    img {
        overflow-clip-margin: content-box;
        overflow: clip;
        margin-left: 57px;
        width: 160px;
        height: 80px;
    }

    div[data-testid="stDecoration"] {
        position: absolute;
        top: 0px;
        right: 0px;
        left: 0px;
        height: 0.125rem;
        z-index: 0;
        visibility: hidden;
    }

    .st-bi {#progress bar
    background-color: rgb(24 192 82);
    }

    div[data-testid="stStatusWidget"] img{
    display:fixed;
    color: white;
    }
    
    div.[data-testid="stToolbar"] label {
     display: none;
    }

    div[data-testid="fileDeleteBtn"] svg{
    color:black;
    }
       
    
    section[data-testid="stFileUploadDropzone"]{#upload section
    display: flex;
    -webkit-box-align: center;
    align-items: center;
    padding: 1rem;
    # background-color: rgb(236, 234, 233);
    border-radius: 0.5rem;
    color: rgb(20, 2, 2);
    height: 13vh;
    # border: 1px solid black;
}

    div.uploadedFileName{
    display: flex;
    align-items: center;
    margin: 0px;
    }
    
    
    div[data-testid="block-container"] {#body 
    width: 100%;
    padding: 2rem 5rem 10rem;
    min-width: auto;
    max-width: initial;
    z-index:1;
}
    div.uploadedFileName{
    padding:5px;
    }

    div.uploadedFileData{
    display: flex;
    align-items: center;
    justify-content: space-between;
    }

    div.uploadedFile small{
        padding: 10px;
    }
    
    # .uploadedFile {display: none}

    div.stButton > button:first-child { 
        display: inline-flex;
        -webkit-box-align: center;
        align-items: center;
        -webkit-box-pack: center;
        justify-content: center;
        font-weight: 400;
        padding: 0.25rem 0.75rem;
        border-radius: 0.5rem;
        min-height: 38.4px;
        margin: 0px;
        line-height: 1.6;
        width: 100%;
        user-select: none;
        background-color: rgb(194, 27, 23);
        color: rgb(255, 255, 255);
        border: 1px solid rgb(194, 27, 23);
    }

    footer {#removing footer
        display: none;
    }
    @media (min-width: 576px)
    footer {
        padding-left: 5rem;
        padding-right: 5rem;
    }
   
    footer {
        color: rgba(20, 2, 2, 0.4);
        font-size: 14px;
        height: 2.5rem;
        min-width: auto;
        max-width: initial;
        padding: 0.5rem 1rem;
        width: 100%;
        display: none;
}
  
            <style>''',unsafe_allow_html=True)
    
#------------------------------CSS alteration ends------------------------------


    st.markdown("<h1 style='text-align: center;'>Aadhaar Masking Tool</h1>", unsafe_allow_html=True)
    input_files = st.file_uploader("Upload TIFF Files", accept_multiple_files=True,
                                   help="Click on the Browse button to select files from your system or drag and drop files here. \n\rOnly TIFF files are allowed",
                                   type=['tif', 'tiff'])
    total_files = 0

    if input_files:
        st.success('Upload complete!')
        output_dir = st.text_input("Output Directory", help="Specify the output directory path")
        process_button = st.button("Mask Documents", type="primary")
        
        

        if process_button and not output_dir:
            st.error("Enter the Output Directory")
            return

        if process_button and output_dir:
            output_dir += "\masking_output"
            start_time = time.time()

            # Remove the existing temporary directory if it exists
            shutil.rmtree("temp", ignore_errors=True)

            # Create the temporary directory if it doesn't exist
            os.makedirs("temp", exist_ok=True)

            file_list = []

            for file in input_files:
                # Save the uploaded file to the temporary directory
                temp_filepath = os.path.join("temp", file.name)
                with open(temp_filepath, "wb") as f:
                    f.write(file.getbuffer())
                file_list.append(temp_filepath)
            

            # Create the output directory
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            # Progress bar
            progress_bar = st.progress(0)

            # Process and redact the documents
            redacted_files, success_count = redact_documents(file_list, output_dir, progress_bar)

            # Clean up temporary files
            shutil.rmtree("temp")

            # Calculating the results
            total_files = len(file_list)
            end_time = time.time()
            total_time = end_time - start_time
            average_time = total_time / total_files if total_files > 0 else 0

            col1, col2 = st.columns(2)

            # Left column 
            with col1:
                if total_files > 0:
                    st.success(f"Output Directory: {output_dir}")
                    st.success(f"Aadhaar Documents Count: {total_files}")
                    st.success(f"Masked Documents Count: {success_count}")

            # Right column
            with col2:
                if total_files > 0:
                    st.success(f"Masking Success Rate: {(success_count / total_files) * 100:.2f}%")
                    st.success(f"Total Time Taken: {total_time:.2f} seconds")
                    st.success(f"Average Time Taken: {average_time:.2f} seconds")

if __name__ == "__main__":
    main()
