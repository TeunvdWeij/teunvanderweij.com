import markdown
import os
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
    <style>
        body {
            font-family: 'Arial', sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 0;
            background-color: #f4f4f4;
            color: #333;
        }

        .container {
            max-width: 900px;
            margin: 0 auto;
            padding: 2rem;
        }

        h1 {
            color: #2c3e50;
            text-align: center;
            padding: 2rem;
            background-color: #fff;
            margin-top: 0;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }

        h2 {
            color: #2c3e50;
            border-bottom: 2px solid #2c3e50;
            padding-bottom: 0.5rem;
            margin-top: 2rem;
        }

        h3 {
            color: #34495e;
        }

        a {
            color: #3498db;
            text-decoration: none;
        }

        a:hover {
            text-decoration: underline;
        }

        p {
            margin-bottom: 1rem;
        }

        ul {
            padding-left: 2rem;
        }

        li {
            margin-bottom: 0.5rem;
        }

        /* Style for the contact section */
        #contact {
            background-color: #fff;
            padding: 2rem;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            margin-top: 2rem;
        }

        /* Style for the skills section */
        .skills {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1rem;
            margin-top: 1rem;
        }

        .skill-category {
            background-color: #fff;
            padding: 1rem;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }

        /* Style for papers list */
        .papers-list li {
            margin-bottom: 1rem;
            padding-left: 1rem;
            border-left: 3px solid #2c3e50;
        }

        em {
            color: #666;
            font-style: normal;
        }
    </style>
</head>
<body>
    <div class="container">
        {{ content }}
    </div>
</body>
</html>
"""

def convert_markdown_to_html(markdown_content):
    # Convert markdown to HTML
    html_content = markdown.markdown(markdown_content, extensions=['extra'])
    
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