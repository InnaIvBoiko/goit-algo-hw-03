import shutil
import argparse
import sys
from pathlib import Path


def parse_arguments():
    """Parse command line arguments for source and destination directories."""
    parser = argparse.ArgumentParser(
        description="Recursively copy files and organize them by extension"
    )
    parser.add_argument(
        "source", 
        help="Path to the source directory"
    )
    parser.add_argument(
        "destination", 
        nargs="?", 
        default="dist", 
        help="Path to the destination directory (default: dist)"
    )
    return parser.parse_args()


def copy_files_recursively(source_path: Path, destination_path: Path) -> None:
    """
    Recursively traverse the source directory and copy files to destination
    organized by file extensions.
    
    Args:
        source_path (Path): Path to the source directory
        destination_path (Path): Path to the destination directory
    """
    try:
        # Iterate through all items in the source directory
        for item in source_path.iterdir():
            try:
                if item.is_dir():
                    # If item is a directory, call function recursively
                    copy_files_recursively(item, destination_path)
                elif item.is_file():
                    # If item is a file, copy it to appropriate subdirectory
                    copy_file_by_extension(item, destination_path)
            except PermissionError:
                print(f"Permission denied: {item}")
            except Exception as e:
                print(f"Error processing {item}: {e}")
    except PermissionError:
        print(f"Permission denied accessing directory: {source_path}")
    except FileNotFoundError:
        print(f"Directory not found: {source_path}")
    except Exception as e:
        print(f"Error accessing directory {source_path}: {e}")


def ensure_directory_exists(directory_path: Path) -> bool:
    """
    Ensure that a directory exists, creating it if necessary.
    
    Args:
        directory_path (Path): Path to the directory to create
        
    Returns:
        bool: True if directory exists or was created successfully, False otherwise
    """
    try:
        directory_path.mkdir(parents=True, exist_ok=True)
        return True
    except PermissionError:
        print(f"Permission denied creating directory: {directory_path}")
        return False
    except Exception as e:
        print(f"Error creating directory {directory_path}: {e}")
        return False


def copy_file_by_extension(file_path: Path, destination_path: Path) -> None:
    """
    Copy a file to a subdirectory based on its extension.
    
    Args:
        file_path (Path): Path to the source file
        destination_path (Path): Path to the destination directory
    """
    try:
        # Get file extension (without the dot, lowercase)
        file_extension = file_path.suffix.lower().lstrip('.')
        
        # If file has no extension, use 'no_extension' as folder name
        if not file_extension:
            file_extension = 'no_extension'
        
        # Create subdirectory path based on file extension
        extension_dir = destination_path / file_extension
        
        # Ensure the subdirectory exists
        if not ensure_directory_exists(extension_dir):
            print(f"Failed to create directory for extension '{file_extension}', skipping file {file_path}")
            return
        
        # Define destination file path
        destination_file = extension_dir / file_path.name
        
        # Handle file name conflicts by adding a number suffix
        counter = 1
        original_stem = file_path.stem
        while destination_file.exists():
            new_name = f"{original_stem}_{counter}{file_path.suffix}"
            destination_file = extension_dir / new_name
            counter += 1
        
        # Copy the file
        shutil.copy2(file_path, destination_file)
        print(f"Copied: {file_path} -> {destination_file}")
        
    except PermissionError:
        print(f"Permission denied copying file: {file_path}")
    except shutil.Error as e:
        print(f"Error copying file {file_path}: {e}")
    except Exception as e:
        print(f"Unexpected error copying {file_path}: {e}")


def main():
    """Main function to execute the file copying process."""
    try:
        # Parse command line arguments
        args = parse_arguments()
        
        # Convert to Path objects
        source_path = Path(args.source)
        destination_path = Path(args.destination)
        
        # Validate source directory exists
        if not source_path.exists():
            print(f"Error: Source directory '{source_path}' does not exist.")
            sys.exit(1)
        
        if not source_path.is_dir():
            print(f"Error: '{source_path}' is not a directory.")
            sys.exit(1)
        
        # Create destination directory if it doesn't exist
        if not ensure_directory_exists(destination_path):
            print(f"Error: Failed to create destination directory '{destination_path}'")
            sys.exit(1)
        
        print(f"Destination directory: {destination_path.absolute()}")
        
        # Start the recursive copying process
        print(f"Starting to copy files from '{source_path}' to '{destination_path}'...")
        copy_files_recursively(source_path, destination_path)
        print("File copying completed successfully!")
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

# Run the script with the following command:
# python3 task-1.py test_source custom_dest
# python3 task-1.py test_source

