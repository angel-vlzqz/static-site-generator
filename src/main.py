import os
import sys
import shutil
from copy_static import copy_static
from page_generator import generate_pages_recursive

def main():
    # Get the project root directory
    root_dir = os.path.dirname(os.path.dirname(__file__))
    
    # Get basepath from CLI args or default to "/"
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    
    # Define paths
    static_dir = os.path.join(root_dir, "static")
    docs_dir = os.path.join(root_dir, "docs")
    content_dir = os.path.join(root_dir, "content")
    template_path = os.path.join(root_dir, "template.html")
    
    # Copy static files to docs directory
    copy_static(static_dir, docs_dir)
    
    # Generate all pages recursively
    generate_pages_recursive(content_dir, template_path, docs_dir, basepath)

if __name__ == "__main__":
    main()
