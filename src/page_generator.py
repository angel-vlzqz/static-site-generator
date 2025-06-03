import os
from markdown_parser import markdown_to_html_node, extract_title

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
    
    # Create destination directory if it doesn't exist
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    # Write the generated HTML to the destination file
    with open(dest_path, "w") as f:
        f.write(html_page) 