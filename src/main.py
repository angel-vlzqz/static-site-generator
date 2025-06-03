from textnode import TextNode, TextType
from copy_static import copy_static
import os

def main():
    # Copy static files to public directory
    static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
    public_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "public")
    copy_static(static_dir, public_dir)

if __name__ == "__main__":
    main()
