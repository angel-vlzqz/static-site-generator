import unittest
from markdown_parser import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
    markdown_to_blocks,
    block_to_block_type,
    BlockType,
    markdown_to_html_node,
    extract_title,
)
from textnode import TextNode, TextType

class TestMarkdownParser(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)"
        expected = [
            ("image", "https://i.imgur.com/zjjcJKZ.png"),
            ("second image", "https://i.imgur.com/3elNhQu.png")
        ]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_links(self):
        text = "This is text with a [link](https://www.boot.dev) and [another link](https://www.youtube.com)"
        expected = [
            ("link", "https://www.boot.dev"),
            ("another link", "https://www.youtube.com")
        ]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_split_nodes_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_nodes_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_nodes_link(self):
        node = TextNode(
            "This is text with a [link](https://www.boot.dev) and [another link](https://www.youtube.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another link", TextType.LINK, "https://www.youtube.com"),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(text_to_textnodes(text), expected) 

    def test_markdown_to_blocks(self):
        markdown = """# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item"""
        
        expected = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
            "- This is the first list item in a list block\n- This is a list item\n- This is another list item"
        ]
        
        self.assertListEqual(markdown_to_blocks(markdown), expected)
        
    def test_markdown_to_blocks_with_extra_newlines(self):
        markdown = """# This is a heading



This is a paragraph of text. It has some **bold** and _italic_ words inside of it.




- This is the first list item in a list block
- This is a list item
- This is another list item"""
        
        expected = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
            "- This is the first list item in a list block\n- This is a list item\n- This is another list item"
        ]
        
        self.assertListEqual(markdown_to_blocks(markdown), expected)

    def test_block_to_block_type(self):
        # Test headings
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## Heading 2"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)
        
        # Test code blocks
        self.assertEqual(
            block_to_block_type("```\ncode block\n```"),
            BlockType.CODE
        )
        self.assertEqual(
            block_to_block_type("```python\nprint('hello')\n```"),
            BlockType.CODE
        )
        
        # Test quote blocks
        self.assertEqual(
            block_to_block_type("> Quote line 1\n> Quote line 2"),
            BlockType.QUOTE
        )
        
        # Test unordered lists
        self.assertEqual(
            block_to_block_type("- List item 1\n- List item 2\n- List item 3"),
            BlockType.UNORDERED_LIST
        )
        
        # Test ordered lists
        self.assertEqual(
            block_to_block_type("1. List item 1\n2. List item 2\n3. List item 3"),
            BlockType.ORDERED_LIST
        )
        
        # Test paragraphs
        self.assertEqual(
            block_to_block_type("This is a paragraph"),
            BlockType.PARAGRAPH
        )
        self.assertEqual(
            block_to_block_type("This is a paragraph\nwith multiple lines"),
            BlockType.PARAGRAPH
        )
        
    def test_block_to_block_type_edge_cases(self):
        # Test invalid heading (no space after #)
        self.assertEqual(block_to_block_type("#Heading"), BlockType.PARAGRAPH)
        
        # Test invalid code block (missing closing backticks)
        self.assertEqual(block_to_block_type("```\ncode"), BlockType.PARAGRAPH)
        
        # Test invalid quote block (some lines don't start with >)
        self.assertEqual(
            block_to_block_type("> Quote line 1\nNot a quote line"),
            BlockType.PARAGRAPH
        )
        
        # Test invalid unordered list (missing space after -)
        self.assertEqual(
            block_to_block_type("-List item 1\n-List item 2"),
            BlockType.PARAGRAPH
        )
        
        # Test invalid ordered list (wrong numbering)
        self.assertEqual(
            block_to_block_type("1. List item 1\n3. List item 2"),
            BlockType.PARAGRAPH
        )
        
        # Test invalid ordered list (wrong format)
        self.assertEqual(
            block_to_block_type("1 List item 1\n2 List item 2"),
            BlockType.PARAGRAPH
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain\nthe **same** even with inline stuff\n```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_simple_title(self):
        markdown = "# My Title"
        self.assertEqual(extract_title(markdown), "My Title")

    def test_title_with_extra_spaces(self):
        markdown = "#   My Title"
        self.assertEqual(extract_title(markdown), "My Title")

    def test_title_with_multiple_hashes(self):
        markdown = "### My Title"
        self.assertEqual(extract_title(markdown), "My Title")

    def test_no_title(self):
        markdown = "This is not a title"
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "no title in markdown found")

    def test_empty_string(self):
        markdown = ""
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "no title in markdown found")

    def test_title_with_content_after(self):
        markdown = "# My Title\nSome content after"
        self.assertEqual(extract_title(markdown), "My Title\nSome content after")