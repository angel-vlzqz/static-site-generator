from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """
    Split text nodes in old_nodes based on the delimiter and convert delimited text to the specified text_type.
    
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
            # If it's not a text node, keep it as is
            new_nodes.append(old_node)
            continue
            
        # Split the text by the delimiter
        parts = old_node.text.split(delimiter)
        
        # If there's no delimiter in the text, keep the node as is
        if len(parts) == 1:
            new_nodes.append(old_node)
            continue
            
        # Process each part
        for i, part in enumerate(parts):
            # Even indices are regular text, odd indices are delimited text
            if i % 2 == 0:
                # Include empty text nodes at the end
                if part or i == len(parts) - 1:
                    new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))
    
    return new_nodes