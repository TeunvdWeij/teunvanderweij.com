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
    
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-08RF5E3N61"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());

      gtag('config', 'G-08RF5E3N61');
    </script>
    
    <style>
        body {
            font-family: 'Arial', sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 0;
            background-color: #f4f4f4;
            color: #333;
        }

        .layout-wrapper {
            display: flex;
            min-height: 100vh;
        }

        .sidebar {
            width: 250px;
            background-color: #fff;
            padding: 2rem 1.5rem;
            box-shadow: 2px 0 5px rgba(0,0,0,0.1);
            position: fixed;
            height: 100vh;
            overflow-y: auto;
            border-right: 3px solid #3498db;
        }

        .sidebar h3 {
            color: #2c3e50;
            margin-bottom: 1rem;
            font-size: 1.1rem;
            border-bottom: 2px solid #3498db;
            padding-bottom: 0.5rem;
        }

        .sidebar ul {
            list-style: none;
            padding: 0;
            margin: 0;
        }

        .sidebar li {
            margin-bottom: 0.8rem;
        }

        .sidebar a {
            color: #34495e;
            text-decoration: none;
            display: block;
            padding: 0.5rem 0.75rem;
            border-radius: 4px;
            transition: all 0.3s ease;
            border-left: 3px solid transparent;
        }

        .sidebar a:hover {
            background-color: #f8f9fa;
            border-left-color: #3498db;
            color: #2c3e50;
            transform: translateX(5px);
        }

        .main-content {
            flex: 1;
            margin-left: 250px;
            padding: 2rem;
        }

        .container {
            max-width: 900px;
            margin: 0 auto;
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

        /* Mobile responsiveness */
        @media (max-width: 768px) {
            .sidebar {
                width: 200px;
            }
            
            .main-content {
                margin-left: 200px;
                padding: 1rem;
            }
        }

        @media (max-width: 640px) {
            .layout-wrapper {
                flex-direction: column;
            }
            
            .sidebar {
                position: relative;
                width: 100%;
                height: auto;
                border-right: none;
                border-bottom: 3px solid #3498db;
            }
            
            .main-content {
                margin-left: 0;
            }
        }
    </style>
</head>
<body>
    <div class="layout-wrapper">
        <!-- Sidebar with Table of Contents -->
        <div class="sidebar">
            <h3>Table of Contents</h3>
            <ul>
                <li><a href="#about-me">About me</a></li>
                <li><a href="#work-experience">Work experience</a></li>
                <li><a href="#research-papers">Research papers</a></li>
                <li><a href="#essays">Essays</a></li>
                <li><a href="#education">Education</a></li>
                <li><a href="#activity-highlights">Activity highlights</a></li>
                <li><a href="#outside-of-work">Outside of work</a></li>
                <li><a href="#contact">Contact</a></li>
            </ul>
        </div>

        <!-- Main Content -->
        <div class="main-content">
            <div class="container">
                {{ content }}
            </div>
        </div>
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