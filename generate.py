import markdown
import os
import re
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from jinja2 import Template

# HTML template with styling
TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>Teun van der Weij - AI Safety Researcher</title>
    <meta name="description" content="Teun van der Weij is a Member of Technical Staff at Apollo Research in Zürich, leading the RL Dynamics project. He works on making AI systems safer.">
    <link rel="icon" type="image/svg+xml" href="favicon.svg">
    <link rel="canonical" href="https://teunvanderweij.com/">
    <meta property="og:title" content="Teun van der Weij - AI Safety Researcher">
    <meta property="og:description" content="Member of Technical Staff at Apollo Research in Zürich, leading the RL Dynamics project.">
    <meta property="og:image" content="https://teunvanderweij.com/teun_apollo_2025.jpg">
    <meta property="og:url" content="https://teunvanderweij.com/">
    <meta property="og:type" content="website">
    <style>
        body {
            font-family: Georgia, 'Iowan Old Style', 'Times New Roman', serif;
            color: #1a1a1a;
            background-color: #ffffff;
            line-height: 1.6;
            margin: 0;
            padding: 0;
        }

        main {
            max-width: 68ch;
            margin: 0 auto;
            padding: 0 1.25rem 4rem;
        }

        header {
            margin: 3.5rem 0 3rem;
        }

        .monogram {
            width: 84px;
            height: 84px;
            flex-shrink: 0;
        }

        h1 {
            font-size: 2.3rem;
            font-weight: normal;
            margin: 0;
            letter-spacing: 0.01em;
        }

        .social {
            display: flex;
            align-items: center;
            gap: 1.1rem;
            margin-top: 0.8rem;
        }

        .social a {
            line-height: 0;
        }

        .social svg {
            width: 20px;
            height: 20px;
            fill: #666;
            transition: fill 0.15s;
        }

        .social a:hover svg {
            fill: #000;
        }

        nav {
            margin-top: 1.25rem;
            font-size: 0.95rem;
            color: #999;
        }

        nav a {
            color: #666;
            text-decoration: none;
            margin: 0 0.3rem;
        }

        nav a:hover {
            color: #1a1a1a;
            text-decoration: underline;
            text-underline-offset: 3px;
        }

        h2 {
            font-size: 1.45rem;
            font-weight: normal;
            margin: 3rem 0 1rem;
        }

        details,
        .plain-section {
            margin: 1.6rem -1.25rem 0;
            padding: 1.1rem 1.25rem;
            border-radius: 10px;
        }

        .plain-section h2 {
            margin: 0 0 1rem;
        }

        .tint-1 { background-color: #f7f5fb; }
        .tint-2 { background-color: #fbf4f6; }
        .tint-3 { background-color: #f2f7fb; }
        .tint-4 { background-color: #f3f8f4; }
        .tint-5 { background-color: #fbf7ef; }
        .tint-6 { background-color: #f5f5f9; }

        summary {
            cursor: pointer;
            list-style: none;
        }

        summary::-webkit-details-marker {
            display: none;
        }

        summary h2 {
            display: inline;
            margin: 0;
        }

        summary::before {
            content: "▸ ";
            color: #999;
            font-size: 1rem;
        }

        details[open] > summary::before {
            content: "▾ ";
        }

        .section-body {
            margin-top: 1rem;
        }

        .contact-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 1.5rem;
        }

        .contact-row p {
            margin: 0;
        }

        .photo-word {
            border-bottom: 1px dotted #999;
            cursor: pointer;
            position: relative;
        }

        .photo-word img {
            position: absolute;
            bottom: 1.7em;
            left: 50%;
            transform: translateX(-50%) rotate(-2deg);
            width: 240px;
            max-width: 70vw;
            opacity: 0;
            visibility: hidden;
            transition: opacity 0.2s ease, transform 0.2s ease;
            border: 5px solid #fff;
            box-shadow: 0 6px 24px rgba(0, 0, 0, 0.3);
            pointer-events: none;
            z-index: 10;
        }

        .photo-word:hover img,
        .photo-word.open img {
            opacity: 1;
            visibility: visible;
            transform: translateX(-50%) rotate(-2deg) translateY(-5px);
        }

        h3 {
            font-size: 1.1rem;
            margin: 1.9rem 0 0.15rem;
        }

        p {
            margin: 0 0 1rem;
        }

        a {
            color: #1a1a1a;
            text-decoration: underline;
            text-decoration-thickness: 1px;
            text-underline-offset: 2px;
        }

        a:hover {
            text-decoration-thickness: 2px;
        }

        .meta {
            color: #666;
            font-size: 0.92rem;
            margin: 0 0 0.6rem;
        }

        .subhead {
            text-transform: uppercase;
            letter-spacing: 0.08em;
            font-size: 0.85rem;
            color: #666;
            margin: 2.25rem 0 0.25rem;
        }

        .meta a {
            color: #666;
        }

        .about {
            display: flex;
            gap: 1.75rem;
            align-items: flex-start;
        }

        .about img {
            border-radius: 50%;
            flex-shrink: 0;
        }

        ul {
            padding-left: 1.25rem;
        }

        li {
            margin-bottom: 0.6rem;
        }

        @media (max-width: 640px) {
            .about {
                flex-direction: column-reverse;
                align-items: center;
                text-align: left;
            }

            header {
                margin: 2rem 0 2rem;
            }
        }
    </style>
</head>
<body>
    <main>
        <header>
            <h1>Teun van der Weij</h1>
            <div class="social">
                <a href="https://x.com/Teun_vd_Weij" aria-label="X (Twitter)" title="X"><svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M18.901 1.153h3.68l-8.04 9.19L24 22.846h-7.406l-5.8-7.584-6.638 7.584H.474l8.6-9.83L0 1.154h7.594l5.243 6.932ZM17.61 20.644h2.039L6.486 3.24H4.298Z"/></svg></a>
                <a href="https://www.linkedin.com/in/teun-van-der-weij/" aria-label="LinkedIn" title="LinkedIn"><svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.225 0z"/></svg></a>
                <a href="https://scholar.google.com/citations?hl=en&user=-fMmbSYAAAAJ" aria-label="Google Scholar" title="Google Scholar"><svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M5.242 13.769 0 9.5 12 0l12 9.5-5.242 4.269C17.548 11.249 14.978 9.5 12 9.5c-2.977 0-5.548 1.748-6.758 4.269zM12 10a7 7 0 1 0 0 14 7 7 0 0 0 0-14z"/></svg></a>            </div>
            <nav>
                <a href="#about-me">About</a> ·
                <a href="#work-experience">Work</a> ·
                <a href="#research-papers">Papers</a> ·
                <a href="#essays">Essays</a> ·
                <a href="#contact">Contact</a>
            </nav>
        </header>
        {{ content }}
    </main>
    <script>
        document.querySelectorAll('.photo-word').forEach(function (word) {
            word.addEventListener('click', function () { word.classList.toggle('open'); });
        });
    </script>
</body>
</html>
"""

def make_sections_collapsible(html_content):
    # Wrap each h2 section in <details open> so sections can be collapsed
    parts = re.split(r'(?=<h2)', html_content)
    sections = [parts[0]]
    for i, part in enumerate(parts[1:], start=1):
        match = re.match(r'(<h2[^>]*>.*?</h2>)(.*)', part, flags=re.S)
        header, body = match.group(1), match.group(2)
        if 'id="contact"' in header:
            sections.append(f'<div class="plain-section tint-{i}">\n{part}\n</div>')
            continue
        sections.append(
            f'<details open class="tint-{i}">\n<summary>{header}</summary>\n<div class="section-body">{body}</div>\n</details>'
        )
    return '\n'.join(sections)

def convert_markdown_to_html(markdown_content):
    # Convert markdown to HTML
    html_content = markdown.markdown(markdown_content, extensions=['extra'])
    html_content = make_sections_collapsible(html_content)

    # Render the template with the converted content
    template = Template(TEMPLATE)
    return template.render(content=html_content)

def update_html():
    try:
        # Read markdown content
        with open('main.md', 'r', encoding='utf-8') as f:
            markdown_content = f.read()

        # Convert to HTML
        html_content = convert_markdown_to_html(markdown_content)

        # Write the HTML file
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(html_content)

        print("Website updated successfully!")
    except Exception as e:
        print(f"Error updating website: {e}")

class MarkdownHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith('main.md'):
            print("Markdown file changed, updating website...")
            update_html()

def watch_markdown():
    event_handler = MarkdownHandler()
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=False)
    observer.start()
    print("Watching for changes in main.md...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\nStopped watching for changes.")

    observer.join()

if __name__ == "__main__":
    # Create main.md if it doesn't exist
    if not os.path.exists('main.md'):
        with open('main.md', 'w', encoding='utf-8') as f:
            f.write("# Your Website Content\n\nStart editing this file!")

    # Initial conversion
    update_html()

    # Start watching for changes
    watch_markdown()
