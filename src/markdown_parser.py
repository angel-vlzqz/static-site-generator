import re
from textnode import TextNode, TextType

def extract_markdown_images(text):
    """Extract markdown image syntax from text.
    
    Args:
        text (str): Text containing markdown image syntax
        
    Returns:
        list: List of tuples containing (alt_text, image_url)
    """
    alt_text = re.findall(r"\[(.*?)\]", text)
    link_text = re.findall(r"\((.*?)\)", text)
    matches = zip(alt_text, link_text)
    return list(matches)

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