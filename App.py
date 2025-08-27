import io
import os
import sys
import tempfile
import zipfile

import streamlit as st
from PIL import Image

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Import functions from your modules
from Audio_Speech_Processing import analyse_pitch, text_to_speech
from Automation_Productivity import logging_setup, webpage_online_status
from File_Handling import (
    check_disk_usage,
    convert_pdf_to_images,
    convert_pdf_to_word,
    convert_word_doc_to_pdf,
    generate_file_tree,
    get_max_file_size,
    merge_pdfs_in_folder,
    recursively_unzip_and_delete,
    split_pdf,
)
from Git_Utilities import check_git_repo_status, get_github_repos
from HuggingFace_Utilities import delete_folder_on_hub
from Image_Processing import (
    compress_image_by_percentage,
    convert_and_display_grayscale,
    convert_image_format,
)
from Jupyter_Notebook_Utilities import (
    convert_notebook_to_clean_py,
    embed_youtube_video,
)
from Regex_Cheatsheet import (
    extract_dates,
    extract_hashtags,
    extract_urls,
    find_phone_numbers,
    remove_extra_spaces,
    validate_email,
)

# --- App Configuration ---

st.set_page_config(layout="wide", page_title="Useful Code Snippets", page_icon="🚀")

st.markdown("<h1 style='text-align: center;'>🚀 Useful Code Snippets Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'> "
            "A collection of practical and reusable code snippets for various everyday programming tasks.</p>",
            unsafe_allow_html=True
            )

# --- Sidebar Navigation ---

st.sidebar.title("Navigation")
selection = st.sidebar.radio(
    "Go to",
    [
        "Audio & Speech Processing",
        "Automation & Productivity",
        "File Handling",
        "Git Utilities",
        "Hugging Face Utilities",
        "Image Processing",
        "Jupyter Notebook Utilities",
        "Regex Cheatsheet",
    ],
)

# --- Page Content ---

# -----------------------------------------------------------------------------
# AUDIO & SPEECH PROCESSING
# -----------------------------------------------------------------------------
if selection == "Audio & Speech Processing":
    st.header("Audio & Speech Processing")

    st.subheader("🗣️ Text to Speech Conversion")
    text_to_convert = st.text_area(
        "Enter text to convert to speech:",
        "Hello, this is a text-to-speech conversion!",
    )
    is_male = st.selectbox("Select Voice:", ("Male", "Female"))
    speech_rate = st.slider("Speech Rate (words per minute):", 50, 300, 150)

    if st.button("Convert to Speech"):
        gender = 0 if is_male == "Male" else 1
        text_to_speech.text_to_speech(
            text=text_to_convert, is_male=gender, rate=speech_rate
        )
        st.success("Speech generated successfully!")

    st.subheader("🎤 Voice Pitch Analyser")
    st.info("This utility analyses the pitch of a voice from an audio file.")
    audio_file = st.file_uploader(
        "Upload an audio file (.wav, .mp3):", type=["wav", "mp3"]
    )

    if audio_file:
        if st.button("Analyse Pitch"):
            with tempfile.NamedTemporaryFile(
                    delete=False, suffix=f".{audio_file.type.split('/')[1]}"
            ) as tmp:
                tmp.write(audio_file.getvalue())
                stats = analyse_pitch.analyse_pitch(tmp.name)
                st.write("Pitch Analysis Results:")
                st.json(stats)


# -----------------------------------------------------------------------------
# AUTOMATION & PRODUCTIVITY
# -----------------------------------------------------------------------------
elif selection == "Automation & Productivity":
    st.header("Automation & Productivity")

    st.subheader("🌐 Website Online Status")
    url = st.text_input("Enter a URL to check its status:", "https://www.google.com")
    if st.button("Check Status"):
        if url:
            status = webpage_online_status.is_website_online(url)
            if status:
                st.success(f"{url} is online.")
            else:
                st.error(f"{url} is offline.")
        else:
            st.warning("Please enter a URL.")

    st.subheader("📝 Logging Setup")
    if st.button("Run Logging Setup"):
        logging_setup.setup_logging()
        st.success("Logging has been set up. Check your console for messages.")
        st.info(
            "This is a backend utility; output will appear in the terminal running Streamlit."
        )


# -----------------------------------------------------------------------------
# FILE HANDLING
# -----------------------------------------------------------------------------
elif selection == "File Handling":
    st.header("File Handling")

    st.subheader("📄 Convert PDF to Word Document")
    pdf_to_word_file = st.file_uploader(
        "Upload a PDF to convert to a Word document", type="pdf", key="pdf_to_word"
    )
    if pdf_to_word_file and st.button("Convert to Word"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
            tmp_pdf.write(pdf_to_word_file.getvalue())
            word_file_path = tmp_pdf.name.replace(".pdf", ".docx")
            convert_pdf_to_word.convert_pdf_to_word(tmp_pdf.name, word_file_path)
            with open(word_file_path, "rb") as f:
                st.download_button(
                    "Download Word Document", f, file_name="converted.docx"
                )

    st.subheader("🖼️ Convert PDF to Images")
    pdf_to_img_file = st.file_uploader(
        "Upload a PDF to convert to images", type="pdf", key="pdf_to_img"
    )
    if pdf_to_img_file and st.button("Convert to Images"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
            tmp_pdf.write(pdf_to_img_file.getvalue())
            images = convert_pdf_to_images.convert_pdf_to_images(tmp_pdf.name)
            for i, image in enumerate(images):
                st.image(image, caption=f"Page {i + 1}", use_container_width=True)

    st.subheader("🔄 Convert Word Document to PDF")
    word_to_pdf_file = st.file_uploader(
        "Upload a Word document to convert to PDF", type=["docx"], key="word_to_pdf"
    )
    if word_to_pdf_file and st.button("Convert to PDF"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp_word:
            tmp_word.write(word_to_pdf_file.getvalue())
            pdf_file_path = tmp_word.name.replace(".docx", ".pdf")
            convert_word_doc_to_pdf.convert_word_doc_to_pdf(tmp_word.name, pdf_file_path)
            with open(pdf_file_path, "rb") as f:
                st.download_button("Download PDF", f, file_name="converted.pdf")

    st.subheader("🗜️ Compress Files (ZIP)")
    uploaded_files = st.file_uploader(
        "Upload files to compress", accept_multiple_files=True, key="compress"
    )
    if uploaded_files and st.button("Compress Files"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as tmp_zip:
            with zipfile.ZipFile(tmp_zip.name, "w") as zf:
                for file in uploaded_files:
                    zf.writestr(file.name, file.getvalue())
            with open(tmp_zip.name, "rb") as f:
                st.download_button("Download ZIP", f, file_name="compressed.zip")

    st.subheader("🔓 Expand ZIP Files")
    zip_file = st.file_uploader("Upload a ZIP file to expand", type="zip")
    if zip_file and st.button("Decompress File"):
        with zipfile.ZipFile(zip_file, "r") as zf:
            for file_info in zf.infolist():
                st.write(f"File: {file_info.filename}")
                content = zf.read(file_info.filename)
                st.download_button(
                    f"Download {file_info.filename}",
                    content,
                    file_name=file_info.filename,
                )

    st.subheader("💾 Check Disk Usage")
    path_to_check = st.text_input("Enter path to check disk usage:", "/")
    st.info(
        "Note: This utility is most useful for local usage as it checks the disk usage of the machine running the Streamlit app.")
    if st.button("Check Disk Usage"):
        try:
            total, used, free = check_disk_usage.check_disk_usage(path_to_check)
            st.write(f"Total: {total // (1024 ** 3)} GB")
            st.write(f"Used: {used // (1024 ** 3)} GB")
            st.write(f"Free: {free // (1024 ** 3)} GB")
        except Exception as e:
            st.error(f"An error occurred while checking disk usage: {e}")

    st.subheader("📂 Get Max File Size in Directory")
    folder_to_scan = st.text_input(
        "Enter folder path to find the largest file:", "."
    )
    st.info(
        "Note: This utility is most useful for local usage as it scans the file system of the machine running the Streamlit app.")
    if st.button("Find Largest File"):
        max_size, max_file = get_max_file_size.get_max_file_size(folder_to_scan)
        st.write(f"The largest file is: {max_file}")
        st.write(f"Size: {max_size / (1024 * 1024):.2f} MB")

    st.subheader("🧩 Merge PDFs in Folder")
    uploaded_pdfs = st.file_uploader(
        "Upload PDFs to merge", accept_multiple_files=True, type="pdf", key="merge_pdfs"
    )
    if uploaded_pdfs and st.button("Merge PDFs"):
        with tempfile.TemporaryDirectory() as tmpdir:
            for uploaded_file in uploaded_pdfs:
                with open(os.path.join(tmpdir, uploaded_file.name), "wb") as f:
                    f.write(uploaded_file.getbuffer())

            output_pdf_path = os.path.join(tmpdir, "merged.pdf")
            merge_pdfs_in_folder.merge_pdfs_in_folder(tmpdir, output_pdf_path)

            with open(output_pdf_path, "rb") as f:
                st.download_button("Download Merged PDF", f, file_name="merged.pdf")

    st.subheader("🔓 Recursively Unzip and Delete ZIPs")
    st.info(
        "Note: This utility is most useful for local usage as it extracts all files from ZIPs and deletes the ZIP archives themselves.")
    zip_to_unzip = st.file_uploader(
        "Upload a zip file to recursively unzip", type="zip", key="unzip_recursive"
    )
    if zip_to_unzip and st.button("Unzip Recursively"):
        with tempfile.TemporaryDirectory() as tmpdir:
            zip_path = os.path.join(tmpdir, zip_to_unzip.name)
            with open(zip_path, "wb") as f:
                f.write(zip_to_unzip.getvalue())

            recursively_unzip_and_delete.unzip_and_delete(tmpdir)
            st.success(f"Unzipped all files in {zip_to_unzip.name}")

    st.subheader("🪓 Split PDF into Single Pages")
    pdf_to_split = st.file_uploader(
        "Upload a PDF to split", type="pdf", key="split_pdf"
    )
    if pdf_to_split and st.button("Split PDF"):
        with tempfile.TemporaryDirectory() as tmpdir:
            pdf_path = os.path.join(tmpdir, pdf_to_split.name)
            with open(pdf_path, "wb") as f:
                f.write(pdf_path.getvalue())
            split_pdf.split_pdf(pdf_path, tmpdir)
            st.success("PDF split successfully")

    st.subheader("🗂️ Generate File Tree")
    st.info(
        "Note: This utility is most useful for local usage as it generates the tree structure of directories on the machine running the Streamlit app.")
    path_to_tree = st.text_input(
        "Enter a directory path to generate its tree structure:", "."
    )
    if st.button("Generate Tree"):
        tree_structure = generate_file_tree.generate_file_tree(path_to_tree)
        st.code(tree_structure)


# -----------------------------------------------------------------------------
# GIT UTILITIES
# -----------------------------------------------------------------------------
elif selection == "Git Utilities":
    st.header("Git Utilities")

    st.subheader("✅ Check Git Repo Status")
    if st.button("Check Git Status"):
        st.info("Note: This utility is most useful for local usage and will not work on deployed websites.")
        if check_git_repo_status.is_git_repo_clean():
            st.success("Repository is clean.")
        else:
            st.warning("Repository has uncommitted changes.")

    st.subheader("🐱 Get GitHub Repos")
    github_token = st.text_input(
        "Enter your GitHub Personal Access Token:", type="password"
    )
    if st.button("Get Repos"):
        if github_token:
            repos = get_github_repos.get_all_repos(github_token)
            st.write(repos)
        else:
            st.warning("Please enter a GitHub token.")

    st.subheader("Useful Git Commands")
    with open("Git_Utilities/Useful Git Commands.md", "r") as f:
        st.markdown(f.read())


# -----------------------------------------------------------------------------
# HUGGING FACE UTILITIES
# -----------------------------------------------------------------------------
elif selection == "Hugging Face Utilities":
    st.header("Hugging Face Utilities")
    st.subheader("🗑️ Delete Folders From HuggingFace Repo")
    repo_id = st.text_input("Repo ID (e.g., 'username/my-dataset'):")
    path_in_repo = st.text_input("Folder path to delete in the repo:")
    repo_type = st.selectbox("Repo Type:", ("dataset", "model", "space"))
    hf_token = st.text_input("Hugging Face Token:", type="password")
    if st.button("Delete Folder"):
        if all([repo_id, path_in_repo, hf_token]):
            delete_folder_on_hub.delete_folder_on_hub(repo_id, path_in_repo, repo_type)
            st.success(
                f"Attempted to delete '{path_in_repo}' from '{repo_id}'. Check console for details."
            )
        else:
            st.warning("Please fill in all fields.")


# -----------------------------------------------------------------------------
# IMAGE PROCESSING
# -----------------------------------------------------------------------------
elif selection == "Image Processing":
    st.header("Image Processing")

    uploaded_image = st.file_uploader(
        "Upload a single image for processing", type=["png", "jpg", "jpeg"]
    )

    st.divider()

    # --- Convert to Grayscale ---
    st.subheader("🔳 Convert to Grayscale")
    if st.button("Convert to Grayscale", disabled=not uploaded_image):
        if uploaded_image:
            # Reread the buffer to avoid "closed file" errors
            uploaded_image.seek(0)
            img_bytes = uploaded_image.getvalue()

            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
                tmp_file.write(img_bytes)
                # This function needs a file path, so we create a temporary one
                gray_image_data = convert_and_display_grayscale.convert_and_display(tmp_file.name)

            col1, col2 = st.columns(2)
            with col1:
                st.image(uploaded_image, caption="Original Image", use_container_width=True)
            with col2:
                st.image(gray_image_data, caption="Grayscale Image", use_container_width=True)

    st.divider()

    # --- Compress Image by Percentage ---
    st.subheader("🗜️ Compress Image")
    percentage = st.slider("Select compression percentage", 1, 100, 85, disabled=not uploaded_image)
    if st.button("Compress", disabled=not uploaded_image):
        if uploaded_image:
            uploaded_image.seek(0)
            original_image = Image.open(uploaded_image)
            compressed_image = compress_image_by_percentage.compress_image_by_percentage(
                original_image, percentage
            )

            col1, col2 = st.columns(2)
            with col1:
                st.image(original_image, caption="Original Image", use_container_width=True)
            with col2:
                st.image(
                    compressed_image,
                    caption=f"Compressed by {percentage}%",
                    use_container_width=True,
                )

            # Prepare for download
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
                compressed_image.save(tmp_file.name, format="JPEG")
                with open(tmp_file.name, "rb") as f:
                    st.download_button(
                        "Download Compressed Image", f, file_name="compressed_image.jpg"
                    )

    st.divider()

    # --- Convert Image Format ---
    st.subheader("🎨 Convert Image Format")
    new_format = st.selectbox("Select new format:", ("JPEG", "PNG", "GIF"), disabled=not uploaded_image)
    if st.button("Convert Format", disabled=not uploaded_image):
        if uploaded_image:
            uploaded_image.seek(0)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_in:
                tmp_in.write(uploaded_image.getvalue())

                with tempfile.NamedTemporaryFile(delete=False, suffix=f".{new_format.lower()}") as tmp_out:
                    convert_image_format.convert_image_format(tmp_in.name, tmp_out.name, new_format)
                    converted_image = Image.open(tmp_out.name)

                    col1, col2 = st.columns(2)
                    with col1:
                        st.image(uploaded_image, caption="Original Image", use_container_width=True)
                    with col2:
                        st.image(converted_image, caption=f"Converted to {new_format}", use_container_width=True)

                    with open(tmp_out.name, "rb") as f:
                        st.download_button(
                            f"Download as {new_format}", f, file_name=f"converted.{new_format.lower()}"
                        )

    st.divider()

    # --- Resize all images in a folder ---
    st.subheader("🖼️ Resize all images in a folder")
    folder_images = st.file_uploader(
        "Upload multiple images to resize",
        accept_multiple_files=True,
        type=["png", "jpg", "jpeg"],
    )
    resize_percentage = st.slider(
        "Select resize percentage for folder:", 1, 100, 50, disabled=not folder_images
    )
    if st.button("Resize all images", disabled=not folder_images):
        if folder_images:
            with tempfile.TemporaryDirectory() as tmpdir:
                # Create a zip file in memory to download the resized images
                zip_buffer = io.BytesIO()
                with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
                    for image_file in folder_images:
                        # Process each image
                        img = Image.open(image_file)
                        new_size = (int(img.width * resize_percentage / 100), int(img.height * resize_percentage / 100))
                        resized_img = img.resize(new_size, Image.Resampling.LANCZOS)

                        # Save resized image to a buffer
                        img_byte_arr = io.BytesIO()
                        resized_img.save(img_byte_arr, format=img.format)
                        img_byte_arr = img_byte_arr.getvalue()

                        # Add the resized image to the zip file
                        zipf.writestr(image_file.name, img_byte_arr)

                st.success(f"{len(folder_images)} image(s) resized successfully!")
                st.download_button(
                    label="Download Resized Images as ZIP",
                    data=zip_buffer.getvalue(),
                    file_name="resized_images.zip",
                    mime="application/zip",
                )

# -----------------------------------------------------------------------------
# JUPYTER NOTEBOOK UTILITIES
# -----------------------------------------------------------------------------
elif selection == "Jupyter Notebook Utilities":
    st.header("Jupyter Notebook Utilities")

    st.subheader("🐍 Convert Notebook to Clean Python File")
    notebook_file = st.file_uploader(
        "Upload a Jupyter Notebook (.ipynb)", type="ipynb"
    )
    if notebook_file and st.button("Convert to Python"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".ipynb") as tmp_nb:
            tmp_nb.write(notebook_file.getvalue())
            py_file_path = convert_notebook_to_clean_py.convert_notebook_to_clean_py(
                tmp_nb.name
            )
            with open(py_file_path, "r") as f:
                st.download_button(
                    "Download Python Script", f.read(), file_name="converted_script.py"
                )

    st.subheader("📹 Embed a YouTube Video")
    video_id = st.text_input("Enter a YouTube Video ID:", "g91kQyy4G7E")
    if st.button("Embed Video"):
        embed_youtube_video.play_youtube_video(video_id)


# -----------------------------------------------------------------------------
# REGEX CHEATSHEET
# -----------------------------------------------------------------------------
elif selection == "Regex Cheatsheet":
    st.header("Regex Cheatsheet")
    text_to_search = st.text_area(
        "Enter text to apply regex on:",
        "Important dates: 12-05-2023, 03/11/2022. Visit https://example.com. Call 9876543210. #MachineLearning",
    )

    st.subheader("📅 Extract Dates")
    if st.button("Extract Dates"):
        st.write(extract_dates.extract_dates(text_to_search))

    st.subheader("#️⃣ Extract Hashtags")
    if st.button("Extract Hashtags"):
        st.write(extract_hashtags.extract_hashtags(text_to_search))

    st.subheader("🔗 Extract URLs")
    if st.button("Extract URLs"):
        st.write(extract_urls.extract_urls(text_to_search))

    st.subheader("📱 Find Phone Numbers")
    if st.button("Find Phone Numbers"):
        st.write(find_phone_numbers.find_phone_numbers(text_to_search))

    st.subheader("✉️ Validate Email")
    email_to_validate = st.text_input("Enter an email to validate:", "test@example.com")
    if st.button("Validate"):
        if validate_email.validate_email(email_to_validate):
            st.success("Valid email address.")
        else:
            st.error("Invalid email address.")

    st.subheader("🚫 Remove Extra Spaces")
    text_with_spaces = st.text_input(
        "Enter text with extra spaces:", "This   is  a    test."
    )
    if st.button("Remove Spaces"):
        st.write(remove_extra_spaces.remove_extra_spaces(text_with_spaces))
