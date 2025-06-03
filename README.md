# Static Site Generator

A custom-built static site generator that converts Markdown content into a beautiful, responsive website. This project was built as part of the [Boot.dev](https://boot.dev) course.

## Live Demo

Visit the live site: [Tolkien Fan Club](https://angel-vlzqz.github.io/static-site-generator/)

## Features

- Converts Markdown files to HTML
- Supports nested directory structures
- Handles static assets (CSS, JavaScript, images)
- Responsive design
- GitHub Pages integration
- Custom template system

## Project Structure

```
static-site-generator/
├── content/           # Markdown content files
├── docs/             # Generated site (served by GitHub Pages)
├── static/           # Static assets (CSS, JS, images)
│   ├── css/
│   ├── js/
│   └── images/
├── src/              # Python source code
│   ├── main.py       # Main entry point
│   ├── page_generator.py
│   └── copy_static.py
├── template.html     # HTML template
└── build.sh          # Build script
```

## Usage

1. Clone the repository
2. Add your content in Markdown format to the `content/` directory
3. Add static assets to the `static/` directory
4. Run the build script:
   ```bash
   ./build.sh
   ```
5. The generated site will be in the `docs/` directory

## Development

The site generator is written in Python and uses:
- Markdown parsing for content
- HTML templating for layout
- Static file management for assets

## License

This project is open source and available under the MIT License.