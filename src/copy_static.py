import os
import shutil
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def copy_static(source_dir: str, dest_dir: str) -> None:
    """Recursively copy all files from source_dir to dest_dir.
    
    Args:
        source_dir (str): Source directory path
        dest_dir (str): Destination directory path
    """
    # Delete destination directory if it exists
    if os.path.exists(dest_dir):
        logger.info(f"Deleting existing directory: {dest_dir}")
        shutil.rmtree(dest_dir)
    
    # Create destination directory
    logger.info(f"Creating directory: {dest_dir}")
    os.mkdir(dest_dir)
    
    # Get all files and directories in source
    for item in os.listdir(source_dir):
        source_path = os.path.join(source_dir, item)
        dest_path = os.path.join(dest_dir, item)
        
        # If it's a file, copy it
        if os.path.isfile(source_path):
            logger.info(f"Copying file: {source_path} -> {dest_path}")
            shutil.copy(source_path, dest_path)
        # If it's a directory, recursively copy it
        else:
            logger.info(f"Copying directory: {source_path} -> {dest_path}")
            copy_static(source_path, dest_path) 