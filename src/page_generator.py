import os
from markdown_parser import markdown_to_html_node, extract_title

def convert_links_to_relative(html_content, from_path, dest_path):
    """Convert absolute paths in HTML content to relative paths.
    
    Args:
        html_content (str): The HTML content to process
        from_path (str): The path of the source markdown file
        dest_path (str): The path where the HTML will be saved
    
    Returns:
        str: HTML content with relative paths
    """
    # Get the relative path from the destination file to the public root
    dest_dir = os.path.dirname(dest_path)
    rel_path = os.path.relpath("public", dest_dir)
    if rel_path == ".":
        rel_path = ""
    else:
        rel_path = rel_path + "/"
    
    # Replace absolute paths with relative paths
    html_content = html_content.replace('href="/', f'href="{rel_path}')
    html_content = html_content.replace('src="/', f'src="{rel_path}')
    
    return html_content

def generate_page(from_path, template_path, dest_path):
    """Generate an HTML page from a markdown file using a template.
    
    Args:
        from_path (str): Path to the markdown file to convert
        template_path (str): Path to the HTML template file
        dest_path (str): Path where the generated HTML file should be saved
    """
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    # Read the markdown file
    with open(from_path, "r") as f:
        markdown = f.read()
    
    # Read the template file
    with open(template_path, "r") as f:
        template = f.read()
    
    # Convert markdown to HTML
    html_node = markdown_to_html_node(markdown)
    html_content = html_node.to_html()
    
    # Extract title from markdown
    title = extract_title(markdown)
    
    # Replace placeholders in template
    html_page = template.replace("{{ Title }}", title)
    html_page = html_page.replace("{{ Content }}", html_content)
    
    # Convert absolute paths to relative paths
    html_page = convert_links_to_relative(html_page, from_path, dest_path)
    
    # Create destination directory if it doesn't exist
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    # Write the generated HTML to the destination file
    with open(dest_path, "w") as f:
        f.write(html_page)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    """Recursively generate HTML pages from markdown files in a directory.
    
    Args:
        dir_path_content (str): Path to the content directory containing markdown files
        template_path (str): Path to the HTML template file
        dest_dir_path (str): Path to the destination directory where HTML files will be written
    """
    # Create destination directory if it doesn't exist
    os.makedirs(dest_dir_path, exist_ok=True)
    
    # Walk through the content directory
    for root, dirs, files in os.walk(dir_path_content):
        # Calculate the relative path from content directory
        rel_path = os.path.relpath(root, dir_path_content)
        
        # Create corresponding directory in destination
        dest_path = os.path.join(dest_dir_path, rel_path)
        os.makedirs(dest_path, exist_ok=True)
        
        # Process each file in the current directory
        for file in files:
            if file.endswith(".md"):
                # Get the full path of the markdown file
                md_path = os.path.join(root, file)
                
                # Create the corresponding HTML file path
                html_file = os.path.splitext(file)[0] + ".html"
                html_path = os.path.join(dest_path, html_file)
                
                # Generate the HTML page
                generate_page(md_path, template_path, html_path) 