import re
from textnode import TextNode, TextType
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def extract_markdown_images(text):
    """Extract markdown image syntax from text.
    
    Args:
        text (str): Text containing markdown image syntax
        
    Returns:
        list: List of tuples containing (alt_text, image_url)
    """
    pattern = r"!\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text):
    """Extract markdown link syntax from text.
    
    Args:
        text (str): Text containing markdown link syntax
        
    Returns:
        list: List of tuples containing (link_text, url)
    """
    alt_text = re.findall(r"\[(.*?)\]", text)
    link_text = re.findall(r"\((.*?)\)", text)
    matches = zip(alt_text, link_text)
    return list(matches)

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """Split text nodes based on a delimiter and convert delimited text to specified type.
    
    Args:
        old_nodes (list): List of TextNode objects
        delimiter (str): The delimiter to split on (e.g. "`" for code blocks)
        text_type (TextType): The type to convert delimited text to
    
    Returns:
        list: New list of TextNode objects with delimited text split into separate nodes
    """
    new_nodes = []
    
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
            
        parts = old_node.text.split(delimiter)
        
        if len(parts) == 1:
            new_nodes.append(old_node)
            continue
            
        for i, part in enumerate(parts):
            if i % 2 == 0:
                if part or i == len(parts) - 1:
                    new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))
    
    return new_nodes

def split_nodes_image(old_nodes):
    """Split text nodes containing markdown image syntax.
    
    Args:
        old_nodes (list): List of TextNode objects
        
    Returns:
        list: New list of TextNode objects with images split into separate nodes
    """
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1],
                )
            )
            original_text = sections[1]

        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    """Split text nodes containing markdown link syntax.
    
    Args:
        old_nodes (list): List of TextNode objects
        
    Returns:
        list: New list of TextNode objects with links split into separate nodes
    """
    new_nodes = []
    
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue

        for link in links:
            sections = original_text.split(f'[{link[0]}]({link[1]})', 1)
            if len(sections) != 2:
                raise ValueError('Invalid markdown, link section not closed')
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]

        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))

    return new_nodes 

def text_to_textnodes(text):
    """Convert a markdown text string into a list of TextNode objects.
    
    Args:
        text (str): Raw markdown text to convert
        
    Returns:
        list: List of TextNode objects representing the parsed markdown
        
    Example:
        Input: "This is **text** with an _italic_ word and a `code block`"
        Output: [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE)
        ]
    """
    # Start with a single text node
    nodes = [TextNode(text, TextType.TEXT)]
    
    # Split by bold text
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    
    # Split by italic text
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    
    # Split by code blocks
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    
    # Split by images
    nodes = split_nodes_image(nodes)
    
    # Split by links
    nodes = split_nodes_link(nodes)
    
    return nodes

def markdown_to_blocks(markdown):
    """Split markdown text into blocks.
    
    Args:
        markdown (str): Raw markdown text to split into blocks
        
    Returns:
        list: List of markdown blocks with whitespace stripped
        
    Example:
        Input: "# Heading\n\nParagraph\n\n- List item"
        Output: ["# Heading", "Paragraph", "- List item"]
    """
    # Split by double newlines
    blocks = markdown.split("\n\n")
    
    # Strip whitespace and filter out empty blocks
    filtered_blocks = []
    for block in blocks:
        stripped = block.strip()
        if stripped != "":
            filtered_blocks.append(stripped)
            
    return filtered_blocks

def block_to_block_type(block):
    """Determine the type of a markdown block.
    
    Args:
        block (str): A single block of markdown text
        
    Returns:
        BlockType: The type of the block
        
    Rules:
        - Headings start with 1-6 # characters, followed by a space
        - Code blocks start and end with 3 backticks
        - Quote blocks have every line starting with >
        - Unordered list blocks have every line starting with - and a space
        - Ordered list blocks have every line starting with a number, ., and a space
        - All other blocks are paragraphs
    """
    lines = block.split("\n")
    
    # Check for heading
    if re.match(r"^#{1,6}\s", block):
        return BlockType.HEADING
    
    # Check for code block
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    
    # Check for quote block
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    
    # Check for unordered list
    if all(re.match(r"^-\s", line) for line in lines):
        return BlockType.UNORDERED_LIST
    
    # Check for ordered list
    if all(re.match(r"^\d+\.\s", line) for line in lines):
        # Verify numbers start at 1 and increment by 1
        numbers = [int(re.match(r"^(\d+)\.", line).group(1)) for line in lines]
        if numbers == list(range(1, len(numbers) + 1)):
            return BlockType.ORDERED_LIST
    
    # Default to paragraph
    return BlockType.PARAGRAPH