import os
import shutil
from copy_static import copy_static
from page_generator import generate_pages_recursive

def main():
    # Get the project root directory
    root_dir = os.path.dirname(os.path.dirname(__file__))
    
    # Define paths
    static_dir = os.path.join(root_dir, "static")
    public_dir = os.path.join(root_dir, "public")
    content_dir = os.path.join(root_dir, "content")
    template_path = os.path.join(root_dir, "template.html")
    
    # Copy static files to public directory
    copy_static(static_dir, public_dir)
    
    # Generate all pages recursively
    generate_pages_recursive(content_dir, template_path, public_dir)

if __name__ == "__main__":
    main()
