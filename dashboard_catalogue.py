"""Framework-independent catalogue powering Utility Shelf Dashboard v2."""

from dataclasses import dataclass


CATEGORIES = ("Audio & Speech Processing", "Automation & Productivity", "File Handling", "Git Utilities", "Hugging Face Utilities", "Image Processing", "Jupyter Notebook Utilities", "Regex Cheatsheet",)


@dataclass(frozen=True, slots=True)
class Tool:
    category: str
    slug: str
    title: str
    icon: str
    description: str
    source: str
    tags: str
    local_only: bool = False


TOOLS = (
    Tool("Audio & Speech Processing", "text-to-speech", "Text to speech", "🔊", "Turn text into a downloadable WAV recording", "Audio_Speech_Processing/text_to_speech.py", "audio speech wav voice", False),
    Tool("Audio & Speech Processing", "pitch-analysis", "Voice pitch analyser", "🎙️", "Measure pitch and duration from an audio recording", "Audio_Speech_Processing/analyse_pitch.py", "audio pitch voice wav mp3", False),
    Tool("Automation & Productivity", "website-status", "Website status check", "🌐", "Check whether a website is responding", "Automation_Productivity/webpage_online_status.py", "url website http monitor", True),
    Tool("Automation & Productivity", "logging-setup", "Logging setup", "🧾", "Configure local logging for your Python scripts", "Automation_Productivity/logging_setup.py", "logs debugging local", True),
    Tool("File Handling", "pdf-to-word", "PDF to Word", "📑", "Convert a PDF into an editable DOCX", "File_Handling/convert_pdf_to_word.py", "pdf docx convert office", False),
    Tool("File Handling", "pdf-to-images", "PDF to images", "🖼️", "Export PDF pages as PNG image files", "File_Handling/convert_pdf_to_images.py", "pdf png render image", False),
    Tool("File Handling", "word-to-pdf", "Word to PDF", "📄", "Turn a Word document into a PDF", "File_Handling/convert_word_doc_to_pdf.py", "docx pdf office", False),
    Tool("File Handling", "create-zip", "Create ZIP archive", "🗜️", "Package uploaded files into a ZIP", "File_Handling/compress_expand_files.py", "zip compress pack archive", False),
    Tool("File Handling", "extract-zip", "Extract ZIP archive", "🗃️", "Extract a ZIP safely for download", "File_Handling/compress_expand_files.py", "zip decompress unpack", False),
    Tool("File Handling", "disk-usage", "Disk usage", "💾", "Inspect free and used storage on a local disk", "File_Handling/check_disk_usage.py", "storage disk local", True),
    Tool("File Handling", "largest-file", "Find largest file", "📦", "Locate the biggest file in a directory tree", "File_Handling/get_max_file_size.py", "file size folder local", True),
    Tool("File Handling", "merge-pdfs", "Merge PDFs", "🧩", "Combine multiple PDFs into one", "File_Handling/merge_pdfs_in_folder.py", "pdf merge combine", False),
    Tool("File Handling", "recursive-unzip", "Recursive ZIP extraction", "🪄", "Unpack nested archives into a ZIP bundle", "File_Handling/recursively_unzip_and_delete.py", "zip nested recursive", False),
    Tool("File Handling", "split-pdf", "Split PDF", "✂️", "Export PDF pages into separate documents", "File_Handling/split_pdf.py", "split pdf pages", False),
    Tool("File Handling", "file-tree", "Generate directory tree", "🌳", "Create a text diagram of a local folder", "File_Handling/generate_file_tree.py", "folder tree filesystem local", True),
    Tool("Git Utilities", "git-status", "Git status", "✅", "Check your local Git working tree", "Git_Utilities/check_git_repo_status.py", "git local status", True),
    Tool("Git Utilities", "github-repos", "List GitHub repositories", "🐙", "List repositories using a local personal token", "Git_Utilities/get_github_repos.py", "github git token api", True),
    Tool("Git Utilities", "git-commands", "Git command reference", "⌘", "Browse useful Git commands", "Git_Utilities/Useful Git Commands.md", "git commands reference", False),
    Tool("Hugging Face Utilities", "hf-delete-folder", "Delete Hugging Face folder", "🛡️", "Delete a Hub folder with explicit confirmation", "HuggingFace_Utilities/delete_folder_on_hub.py", "huggingface folder delete", True),
    Tool("Image Processing", "grayscale-image", "Convert to greyscale", "◐", "Preview an image in greyscale", "Image_Processing/convert_and_display_grayscale.py", "image black white grayscale", False),
    Tool("Image Processing", "compress-image", "Compress image", "🪶", "Preview and download a compressed JPEG", "Image_Processing/compress_image_by_percentage.py", "image jpeg compress size", False),
    Tool("Image Processing", "convert-image", "Convert image format", "🎨", "Convert to JPEG PNG or GIF", "Image_Processing/convert_image_format.py", "image convert png jpeg gif", False),
    Tool("Image Processing", "resize-images", "Resize image batch", "↔️", "Resize multiple images in one go", "Image_Processing/resize_all_images_in_folder.py", "image resize batch zip", False),
    Tool("Jupyter Notebook Utilities", "notebook-to-python", "Notebook to Python", "📓", "Export a clean Python script from a notebook", "Jupyter_Notebook_Utilities/convert_notebook_to_clean_py.py", "notebook ipynb python", False),
    Tool("Jupyter Notebook Utilities", "embed-youtube", "Embed YouTube video", "▶️", "Preview YouTube videos by video ID", "Jupyter_Notebook_Utilities/embed_youtube_video.py", "jupyter youtube video", False),
    Tool("Regex Cheatsheet", "upper-case", "Uppercase text", "🔠", "Turn text into uppercase", "Regex_Cheatsheet/convert_text_to_upper_case.py", "text uppercase case", False),
    Tool("Regex Cheatsheet", "lower-case", "Lowercase text", "🔡", "Turn text into lowercase", "Regex_Cheatsheet/convert_text_to_lower_case.py", "text lowercase case", False),
    Tool("Regex Cheatsheet", "sentence-case", "Sentence case", "✍️", "Capitalise sentence beginnings", "Regex_Cheatsheet/convert_text_to_sentence_case.py", "text sentence capitalise", False),
    Tool("Regex Cheatsheet", "extract-dates", "Extract dates", "📅", "Find dates in a text passage", "Regex_Cheatsheet/extract_dates.py", "text date regex", False),
    Tool("Regex Cheatsheet", "extract-hashtags", "Extract hashtags", "#️⃣", "Find hashtags in text", "Regex_Cheatsheet/extract_hashtags.py", "text hashtag regex", False),
    Tool("Regex Cheatsheet", "extract-urls", "Extract URLs", "🔗", "Extract website links from text", "Regex_Cheatsheet/extract_urls.py", "url links regex", False),
    Tool("Regex Cheatsheet", "find-phone-numbers", "Find phone numbers", "📱", "Find ten digit numbers in text", "Regex_Cheatsheet/find_phone_numbers.py", "phone digits regex", False),
    Tool("Regex Cheatsheet", "validate-email", "Validate email syntax", "✉️", "Check the structure of an email address", "Regex_Cheatsheet/validate_email.py", "email address format", False),
    Tool("Regex Cheatsheet", "remove-spaces", "Normalise spaces", "🧹", "Remove excess whitespace", "Regex_Cheatsheet/remove_extra_spaces.py", "text whitespace spaces", False),
)
TOOL_BY_SLUG = {tool.slug: tool for tool in TOOLS}


def category_tools(category: str) -> tuple[Tool, ...]:
    return tuple(tool for tool in TOOLS if tool.category == category)


def search_tools(query: str = "", category: str | None = None) -> tuple[Tool, ...]:
    """Case-insensitive, all-words matching across names, descriptions and tags."""
    words = query.strip().casefold().split()
    return tuple(
        tool
        for tool in TOOLS
        if (category is None or tool.category == category)
        and all(
            word in f"{tool.title} {tool.description} {tool.category} {tool.tags}".casefold()
            for word in words
        )
    )
