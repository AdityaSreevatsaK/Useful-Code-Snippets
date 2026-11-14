import io
import os
import re
import sys
import tempfile
import zipfile
from pathlib import Path

import streamlit as st
from PIL import Image
from File_Handling.archive_safety import validate_archive

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
)
from Regex_Cheatsheet import (
    convert_text_to_lower_case,
    convert_text_to_upper_case,
    convert_text_to_sentence_case,
    extract_dates,
    extract_hashtags,
    extract_urls,
    find_phone_numbers,
    remove_extra_spaces,
    validate_email,
)

# Server-side operations and personal tokens are deliberately disabled on hosted instances.
# Set ENABLE_LOCAL_OPERATIONS=1 only when running Streamlit on a trusted machine.
LOCAL_TOOLS_ENABLED = os.environ.get("ENABLE_LOCAL_OPERATIONS") == "1"
MAX_UPLOAD_BYTES = 20 * 1024 * 1024


def upload_is_valid(upload) -> bool:
    if upload.size > MAX_UPLOAD_BYTES:
        st.error("File exceeds the 20 MiB upload limit.")
        return False
    return True


def safe_upload_name(name: str) -> str:
    """Never incorporate paths supplied by a browser into server filenames."""
    return name.replace("\\", "/").split("/")[-1] or "file"


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
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                output = str(Path(tmpdir) / "speech.wav")
                gender = 0 if is_male == "Male" else 1
                text_to_speech.text_to_speech(
                    text=text_to_convert, is_male=gender, rate=speech_rate,
                    output_path=output,
                )
                data = Path(output).read_bytes()
                if not data:
                    raise RuntimeError("Speech engine returned empty audio")
                st.audio(data, format="audio/wav")
                st.download_button("Download Speech", data, file_name="speech.wav")
        except Exception as exc:
            st.error(f"Speech generation unavailable: {exc}")

    st.subheader("🎤 Voice Pitch Analyser")
    st.info("This utility analyses the pitch of a voice from an audio file.")
    audio_file = st.file_uploader(
        "Upload an audio file (.wav, .mp3):", type=["wav", "mp3"]
    )

    if audio_file and st.button("Analyse Pitch"):
        if upload_is_valid(audio_file):
            try:
                with tempfile.TemporaryDirectory() as tmpdir:
                    suffix = Path(safe_upload_name(audio_file.name)).suffix.lower()
                    path = Path(tmpdir) / ("recording" + suffix)
                    path.write_bytes(audio_file.getvalue())
                    stats = analyse_pitch.analyse_pitch(str(path))
                    st.write("Pitch Analysis Results:")
                    st.json(stats)
                    report = path.with_suffix(".pitch.txt")
                    st.download_button(
                        "Download Pitch Report", report.read_bytes(),
                        file_name="pitch_report.txt",
                    )
            except Exception as exc:
                st.error(f"Could not analyse recording: {exc}")


# -----------------------------------------------------------------------------
# AUTOMATION & PRODUCTIVITY
# -----------------------------------------------------------------------------
elif selection == "Automation & Productivity":
    st.header("Automation & Productivity")
    if not LOCAL_TOOLS_ENABLED:
        st.info("Server-side tools are available only when running locally with ENABLE_LOCAL_OPERATIONS=1.")

    st.subheader("🌐 Website Online Status")
    url = st.text_input("Enter a URL to check its status:", "https://www.google.com")
    if st.button("Check Status", disabled=not LOCAL_TOOLS_ENABLED):
        if url:
            status = webpage_online_status.is_website_online(url)
            if status:
                st.success(f"{url} is online.")
            else:
                st.error(f"{url} is offline.")
        else:
            st.warning("Please enter a URL.")

    st.subheader("📝 Logging Setup")
    if st.button("Run Logging Setup", disabled=not LOCAL_TOOLS_ENABLED):
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
    if pdf_to_word_file and st.button("Convert to Word") and upload_is_valid(pdf_to_word_file):
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                source = Path(tmpdir) / "input.pdf"
                target = Path(tmpdir) / "converted.docx"
                source.write_bytes(pdf_to_word_file.getvalue())
                convert_pdf_to_word.convert_pdf_to_word(str(source), str(target))
                st.download_button("Download Word Document", target.read_bytes(),
                                   file_name="converted.docx")
        except Exception as exc:
            st.error(f"PDF conversion failed: {exc}")

    st.subheader("🖼️ Convert PDF to Images")
    pdf_to_img_file = st.file_uploader(
        "Upload a PDF to convert to images", type="pdf", key="pdf_to_img"
    )
    if pdf_to_img_file and st.button("Convert to Images") and upload_is_valid(pdf_to_img_file):
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                source = Path(tmpdir) / "input.pdf"
                source.write_bytes(pdf_to_img_file.getvalue())
                images = convert_pdf_to_images.convert_pdf_to_images(str(source))
                for i, image in enumerate(images):
                    st.image(image, caption=f"Page {i + 1}", use_container_width=True)
                output = io.BytesIO()
                with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as zipped:
                    for i, image in enumerate(images, 1):
                        page_data = io.BytesIO()
                        image.save(page_data, format="PNG")
                        zipped.writestr(f"page_{i}.png", page_data.getvalue())
                st.download_button("Download Images as ZIP", output.getvalue(),
                                   file_name="pdf_images.zip")
        except Exception as exc:
            st.error(f"PDF-to-image conversion failed: {exc}")

    st.subheader("🔄 Convert Word Document to PDF")
    word_to_pdf_file = st.file_uploader(
        "Upload a Word document to convert to PDF", type=["docx"], key="word_to_pdf"
    )
    if word_to_pdf_file and st.button("Convert to PDF") and upload_is_valid(word_to_pdf_file):
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                source = Path(tmpdir) / "input.docx"
                target = Path(tmpdir) / "converted.pdf"
                source.write_bytes(word_to_pdf_file.getvalue())
                convert_word_doc_to_pdf.convert_word_doc_to_pdf(str(source), str(target))
                st.download_button("Download PDF", target.read_bytes(),
                                   file_name="converted.pdf")
        except Exception as exc:
            st.error(f"Word-to-PDF conversion failed: {exc}")

    st.subheader("🗜️ Compress Files (ZIP)")
    uploaded_files = st.file_uploader(
        "Upload files to compress", accept_multiple_files=True, key="compress"
    )
    if uploaded_files and st.button("Compress Files"):
        if len(uploaded_files) <= 100 and all(upload_is_valid(item) for item in uploaded_files):
            output = io.BytesIO()
            with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as zf:
                for index, item in enumerate(uploaded_files, 1):
                    zf.writestr(f"{index:03d}_{safe_upload_name(item.name)}", item.getvalue())
            st.download_button("Download ZIP", output.getvalue(), file_name="compressed.zip")
        else:
            st.error("Select at most 100 files.")

    st.subheader("🔓 Expand ZIP Files")
    zip_file = st.file_uploader("Upload a ZIP file to expand", type="zip")
    if zip_file and st.button("Decompress File") and upload_is_valid(zip_file):
        try:
            with zipfile.ZipFile(zip_file, "r") as zf:
                members = validate_archive(zf)
                for index, (info, name) in enumerate(members):
                    if info.is_dir():
                        continue
                    st.download_button(
                        f"Download {name}", zf.read(info),
                        file_name=safe_upload_name(name), key=f"expanded_{index}",
                    )
        except (ValueError, zipfile.BadZipFile, RuntimeError) as exc:
            st.error(f"Unsafe or invalid ZIP: {exc}")

    st.subheader("💾 Check Disk Usage")
    path_to_check = st.text_input("Enter path to check disk usage:", "/")
    st.info(
        "Note: This utility is most useful for local usage as it checks the disk usage of the machine running the Streamlit app.")
    if st.button("Check Disk Usage", disabled=not LOCAL_TOOLS_ENABLED):
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
    if st.button("Find Largest File", disabled=not LOCAL_TOOLS_ENABLED):
        try:
            max_size, max_file = get_max_file_size.get_max_file_size(folder_to_scan)
            if max_file is None:
                st.warning("No files were found.")
            else:
                st.write(f"The largest file is: {max_file}")
                st.write(f"Size: {max_size / (1024 * 1024):.2f} MB")
        except Exception as exc:
            st.error(f"Scan failed: {exc}")

    st.subheader("🧩 Merge PDFs in Folder")
    uploaded_pdfs = st.file_uploader(
        "Upload PDFs to merge", accept_multiple_files=True, type="pdf", key="merge_pdfs"
    )
    if uploaded_pdfs and st.button("Merge PDFs"):
        if len(uploaded_pdfs) > 30 or not all(upload_is_valid(p) for p in uploaded_pdfs):
            st.error("Select up to 30 PDFs, each no larger than 20 MiB.")
        else:
            try:
                with tempfile.TemporaryDirectory() as tmpdir:
                    for index, upload in enumerate(uploaded_pdfs, 1):
                        (Path(tmpdir) / f"{index:03d}.pdf").write_bytes(upload.getvalue())
                    merged = Path(tmpdir) / "merged.pdf"
                    merge_pdfs_in_folder.merge_pdfs_in_folder(tmpdir, str(merged))
                    st.download_button("Download Merged PDF", merged.read_bytes(),
                                       file_name="merged.pdf")
            except Exception as exc:
                st.error(f"PDF merge failed: {exc}")

    st.subheader("🔓 Recursively Unzip and Delete ZIPs")
    st.info(
        "Note: This utility is most useful for local usage as it extracts all files from ZIPs and deletes the ZIP archives themselves.")
    zip_to_unzip = st.file_uploader(
        "Upload a zip file to recursively unzip", type="zip", key="unzip_recursive"
    )
    if zip_to_unzip and st.button("Unzip Recursively") and upload_is_valid(zip_to_unzip):
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                source = Path(tmpdir) / "uploaded.zip"
                source.write_bytes(zip_to_unzip.getvalue())
                extracted = recursively_unzip_and_delete.unzip_and_delete(tmpdir)
                result = io.BytesIO()
                with zipfile.ZipFile(result, "w", zipfile.ZIP_DEFLATED) as zf:
                    for extracted_file in extracted:
                        path = Path(extracted_file)
                        zf.write(path, path.relative_to(tmpdir).as_posix())
                st.success(f"Extracted {len(extracted)} files.")
                st.download_button("Download Extracted Files", result.getvalue(),
                                   file_name="extracted_files.zip")
        except (ValueError, zipfile.BadZipFile, OSError) as exc:
            st.error(f"Archive extraction refused: {exc}")

    st.subheader("🪓 Split PDF into Single Pages")
    pdf_to_split = st.file_uploader(
        "Upload a PDF to split", type="pdf", key="split_pdf"
    )
    if pdf_to_split and st.button("Split PDF") and upload_is_valid(pdf_to_split):
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                source = Path(tmpdir) / "input.pdf"
                pages = Path(tmpdir) / "pages"
                source.write_bytes(pdf_to_split.getvalue())
                output_paths = split_pdf.split_pdf(str(source), str(pages))
                output = io.BytesIO()
                with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as zf:
                    for page in output_paths:
                        zf.write(page, Path(page).name)
                st.success(f"Split into {len(output_paths)} pages.")
                st.download_button("Download Split Pages", output.getvalue(),
                                   file_name="split_pages.zip")
        except Exception as exc:
            st.error(f"PDF split failed: {exc}")

    st.subheader("🗂️ Generate File Tree")
    st.info(
        "Note: This utility is most useful for local usage as it generates the tree structure of directories on the machine running the Streamlit app.")
    path_to_tree = st.text_input(
        "Enter a directory path to generate its tree structure:", "."
    )
    if st.button("Generate Tree", disabled=not LOCAL_TOOLS_ENABLED):
        tree_structure = generate_file_tree.generate_file_tree(path_to_tree)
        st.code(tree_structure)


# -----------------------------------------------------------------------------
# GIT UTILITIES
# -----------------------------------------------------------------------------
elif selection == "Git Utilities":
    st.header("Git Utilities")
    if not LOCAL_TOOLS_ENABLED:
        st.warning("Git commands and access tokens are disabled on hosted instances.")

    st.subheader("✅ Check Git Repo Status")
    if st.button("Check Git Status", disabled=not LOCAL_TOOLS_ENABLED):
        st.info("Note: This utility is most useful for local usage and will not work on deployed websites.")
        if check_git_repo_status.is_git_repo_clean():
            st.success("Repository is clean.")
        else:
            st.warning("Repository has uncommitted changes.")

    st.subheader("🐱 Get GitHub Repos")
    github_token = (st.text_input(
        "Enter your GitHub Personal Access Token:", type="password"
    ) if LOCAL_TOOLS_ENABLED else "")
    if st.button("Get Repos", disabled=not LOCAL_TOOLS_ENABLED):
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
    if not LOCAL_TOOLS_ENABLED:
        st.warning("Destructive operations and personal tokens are disabled on hosted instances.")
    st.subheader("🗑️ Delete Folders From HuggingFace Repo")
    repo_id = st.text_input("Repo ID (e.g., 'username/my-dataset'):")
    path_in_repo = st.text_input("Folder path to delete in the repo:")
    repo_type = st.selectbox("Repo Type:", ("dataset", "model", "space"))
    hf_token = (st.text_input("Hugging Face Token:", type="password")
                if LOCAL_TOOLS_ENABLED else "")
    confirm_delete = st.checkbox("I understand this will delete the selected folder",
                                 disabled=not LOCAL_TOOLS_ENABLED)
    if st.button("Delete Folder", disabled=not (LOCAL_TOOLS_ENABLED and confirm_delete)):
        if all([repo_id, path_in_repo, hf_token]):
            success, message = delete_folder_on_hub.delete_folder_on_hub(repo_id, path_in_repo, repo_type, hf_token)
            if success:
                st.success(message)
            else:
                st.error(f"Failed to delete '{path_in_repo}' from '{repo_id}'. \n{message}")
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

            if not upload_is_valid(uploaded_image):
                st.stop()
            with tempfile.TemporaryDirectory() as tmpdir:
                original = Path(tmpdir) / "input.png"
                original.write_bytes(img_bytes)
                gray_image_data = convert_and_display_grayscale.convert_and_display(
                    str(original), str(Path(tmpdir) / "grayscale.png")
                )

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

            # JPEG cannot preserve alpha; use a white backdrop for transparent uploads.
            jpg = compressed_image.convert("RGBA")
            background = Image.new("RGB", jpg.size, "white")
            background.paste(jpg, mask=jpg.getchannel("A"))
            buffer = io.BytesIO()
            background.save(buffer, format="JPEG")
            st.download_button("Download Compressed Image", buffer.getvalue(),
                               file_name="compressed_image.jpg")

    st.divider()

    # --- Convert Image Format ---
    st.subheader("🎨 Convert Image Format")
    new_format = st.selectbox("Select new format:", ("JPEG", "PNG", "GIF"), disabled=not uploaded_image)
    if st.button("Convert Format", disabled=not uploaded_image):
        if uploaded_image:
            uploaded_image.seek(0)
            if not upload_is_valid(uploaded_image):
                st.stop()
            try:
                with tempfile.TemporaryDirectory() as tmpdir:
                    source = Path(tmpdir) / "input.png"
                    target = Path(tmpdir) / f"converted.{new_format.lower()}"
                    source.write_bytes(uploaded_image.getvalue())
                    convert_image_format.convert_image_format(str(source), str(target), new_format)
                    image_data = target.read_bytes()
                    col1, col2 = st.columns(2)
                    with col1:
                        st.image(uploaded_image, caption="Original Image", use_container_width=True)
                    with col2:
                        st.image(image_data, caption=f"Converted to {new_format}",
                                 use_container_width=True)
                    st.download_button(f"Download as {new_format}", image_data,
                                       file_name=target.name)
            except Exception as exc:
                st.error(f"Image conversion failed: {exc}")

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
                    for index, image_file in enumerate(folder_images, 1):
                        if not upload_is_valid(image_file):
                            st.stop()
                        # Process each image
                        img = Image.open(image_file)
                        new_size = (max(1, round(img.width * resize_percentage / 100)), max(1, round(img.height * resize_percentage / 100)))
                        resized_img = img.resize(new_size, Image.Resampling.LANCZOS)

                        # Save resized image to a buffer
                        img_byte_arr = io.BytesIO()
                        resized_img.save(img_byte_arr, format=img.format)
                        img_byte_arr = img_byte_arr.getvalue()

                        # Add the resized image to the zip file
                        zipf.writestr(f"{index:03d}_{safe_upload_name(image_file.name)}", img_byte_arr)

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
    if notebook_file and st.button("Convert to Python") and upload_is_valid(notebook_file):
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                source = Path(tmpdir) / "input.ipynb"
                source.write_bytes(notebook_file.getvalue())
                path = convert_notebook_to_clean_py.convert_notebook_to_clean_py(str(source))
                st.download_button("Download Python Script", Path(path).read_bytes(),
                                   file_name="converted_script.py")
        except Exception as exc:
            st.error(f"Notebook conversion failed: {exc}")

    st.subheader("📹 Embed a YouTube Video")
    video_id = st.text_input("Enter a YouTube Video ID:", "g91kQyy4G7E")
    if st.button("Embed Video"):
        if re.fullmatch(r"[A-Za-z0-9_-]{11}", video_id):
            st.video(f"https://www.youtube.com/watch?v={video_id}")
        else:
            st.error("Enter a valid YouTube video ID.")


# -----------------------------------------------------------------------------
# REGEX CHEATSHEET
# -----------------------------------------------------------------------------
elif selection == "Regex Cheatsheet":
    st.header("Regex Cheatsheet")
    text_to_search = st.text_area(
        "Enter text to apply regex on:",
        "Important dates: 12-05-2023, 03/11/2022. Visit https://example.com. Call 9876543210. #MachineLearning",
    )

    st.subheader("⬆️ Capitalise text")
    if st.button("Capitalise"):
        st.write(convert_text_to_upper_case.to_upper_case(text_to_search))

    st.subheader("⬇️ Convert text to lower case")
    if st.button("Convert to lower case"):
        st.write(convert_text_to_lower_case.to_lower_case(text_to_search))

    st.subheader("✍🏻 Convert text to sentence case")
    if st.button("Convert to sentence case"):
        st.write(convert_text_to_sentence_case.to_sentence_case(text_to_search))

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
    if st.button("Find"):
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
