import os
import shutil
import logging

# Define file type categories and their corresponding extensions
FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp", ".svg", ".heic"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".xls", ".xlsx", ".ppt", ".pptx", ".csv"],
    "Videos": [".mp4", ".mov", ".avi", ".mkv", ".wmv", ".flv", ".webm"],
    "Audio": [".mp3", ".wav", ".aac", ".ogg", ".flac", ".m4a"],
    "Archives": [".zip", ".rar", ".tar", ".gz", ".7z"],
    "Executables": [".exe", ".msi", ".bat", ".sh"],
    "Scripts": [".py", ".js", ".html", ".css", ".php", ".java", ".c", ".cpp"],
    "Presentations": [".ppt", ".pptx", ".key", ".odp"],
    "Spreadsheets": [".xls", ".xlsx", ".ods", ".csv"],
    "TextFiles": [".txt", ".md", ".log"],
    "Others": []  # For files that don't fit any other category
}

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_target_directory():
    """
    Prompts the user to enter the target directory path and validates it.

    Returns:
        str: The validated absolute path to the target directory.
             Returns None if the input is invalid or the user cancels.
    """
    while True:
        target_dir = input("Enter the full path to the directory you want to organise: ").strip()
        if not target_dir:
            logging.warning("No directory entered. Exiting.")
            return None
        if os.path.isdir(target_dir):
            return os.path.abspath(target_dir) # Return absolute path
        else:
            logging.error(f"Error: The path '{target_dir}' is not a valid directory or does not exist.")
            choice = input("Try again? (y/n): ").lower()
            if choice != 'y':
                return None

def organise_files(directory_path):
    """
    organises files in the specified directory into subfolders based on their extensions.

    Args:
        directory_path (str): The absolute path to the directory to organise.
    """
    if not directory_path:
        return

    logging.info(f"Starting to organise files in: {directory_path}")
    organised_count = 0
    skipped_count = 0

    # Iterate over each item in the target directory
    for item_name in os.listdir(directory_path):
        item_path = os.path.join(directory_path, item_name)

        # Skip if it's a directory or if it's one of the category folders we might create
        if os.path.isdir(item_path) or item_name in FILE_CATEGORIES.keys():
            logging.debug(f"Skipping directory or category folder: {item_name}")
            continue

        # Get file extension
        _, file_extension = os.path.splitext(item_name)
        file_extension = file_extension.lower() # Normalize to lowercase

        if not file_extension:
            logging.info(f"Skipping file without extension: {item_name}")
            skipped_count += 1
            continue

        # Determine the category for the file
        target_folder_name = None
        for category, extensions in FILE_CATEGORIES.items():
            if file_extension in extensions:
                target_folder_name = category
                break

        if not target_folder_name:
            target_folder_name = "Others" # Default to "Others" if no specific category found
            logging.debug(f"File '{item_name}' (extension: {file_extension}) will be moved to 'Others'.")


        # Create the target category folder if it doesn't exist
        target_folder_path = os.path.join(directory_path, target_folder_name)
        if not os.path.exists(target_folder_path):
            try:
                os.makedirs(target_folder_path)
                logging.info(f"Created folder: {target_folder_path}")
            except OSError as e:
                logging.error(f"Error creating directory {target_folder_path}: {e}")
                skipped_count += 1
                continue # Skip this file if folder creation fails

        # Move the file
        destination_path = os.path.join(target_folder_path, item_name)

        # Check for name conflicts
        if os.path.exists(destination_path):
            # Simple name conflict resolution: append a number
            base, ext = os.path.splitext(item_name)
            counter = 1
            while os.path.exists(destination_path):
                new_name = f"{base}_{counter}{ext}"
                destination_path = os.path.join(target_folder_path, new_name)
                counter += 1
            logging.warning(f"File '{item_name}' already exists in '{target_folder_name}'. Renaming to '{os.path.basename(destination_path)}'.")
            item_name = os.path.basename(destination_path) # update item_name for logging

        try:
            shutil.move(item_path, destination_path)
            logging.info(f"Moved '{item_name}' to '{target_folder_name}' folder.")
            organised_count += 1
        except Exception as e:
            logging.error(f"Error moving file {item_name}: {e}")
            skipped_count += 1

    logging.info("--------------------------------------------------")
    logging.info("File organization complete.")
    logging.info(f"Total files processed (attempted to move): {organised_count + skipped_count}")
    logging.info(f"Files successfully organised: {organised_count}")
    logging.info(f"Files skipped (due to errors or no extension): {skipped_count}")
    logging.info("--------------------------------------------------")


if __name__ == "__main__":
    print("==============================================")
    print("          PYTHON FILE organiseR             ")
    print("==============================================")
    print("This script will organise files in a directory")
    print("by moving them into subfolders based on type.")
    print("----------------------------------------------\n")

    target_dir = get_target_directory()

    if target_dir:
        confirm = input(f"Are you sure you want to organise files in '{target_dir}'? (y/n): ").lower()
        if confirm == 'y':
            organise_files(target_dir)
        else:
            logging.info("Organization cancelled by user.")
    else:
        logging.info("No valid directory selected. Exiting program.")

    print("\nExiting program.")