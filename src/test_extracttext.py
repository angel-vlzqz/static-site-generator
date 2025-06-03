import unittest
from extracttext import extract_markdown_images, extract_markdown_links

class TestExtractText(unittest.TestCase):
  def test_extract_markdown_images(self):
    matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
    )
    self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
  
  def test_extract_markdown_links(self):
    matches = extract_markdown_links(
        "This is text with an [link](https://i.imgur.com/zjjcJKZ.png)"
    )
    self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png")], matches)

  def test_extract_markdown_images_multiple(self):
    matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and ![image2](https://i.imgur.com/zjjcJKZ.png)"
    )
    self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png"), ("image2", "https://i.imgur.com/zjjcJKZ.png")], matches)

  def test_extract_markdown_links_multiple(self):
    matches = extract_markdown_links(
        "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and [link2](https://i.imgur.com/zjjcJKZ.png)"
    )
    self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png"), ("link2", "https://i.imgur.com/zjjcJKZ.png")], matches)

  def test_extract_markdown_images_multiple_with_text(self):
    matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and ![image2](https://i.imgur.com/zjjcJKZ.png) and ![image3](https://i.imgur.com/zjjcJKZ.png)"
    )
    self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png"), ("image2", "https://i.imgur.com/zjjcJKZ.png"), ("image3", "https://i.imgur.com/zjjcJKZ.png")], matches)
  
