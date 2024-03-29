import xml.etree.ElementTree as ET
import sys

def opml_to_html(opml_file, html_file):
    # Parse OPML file
    tree = ET.parse(opml_file)
    root = tree.getroot()

    # Find the outline element in a case-insensitive manner
    element = next((outline for outline in root.findall(".//outline") if outline.get('text') and outline.get('text').lower() == sys.argv[3]), None)

    if element is None:
        print("Error: " + sys.argv[3] + " outline element not found.")
        sys.exit(1)

    # Get children of the outline element and sort them alphabetically by title
    sorted_children = sorted(element.findall('./outline'), key=lambda x: x.get('text').lower())

    # Create HTML file and write header
    with open(html_file, 'w', encoding='utf-8') as html:
        html.write('<!DOCTYPE html>\n<html>\n<head>\n<title>OPML to HTML</title>\n</head>\n<body>\n')

        # Write the list and traverse sorted children of the outline element
        html.write('<ul>\n')
        for outline in sorted_children:
            title = outline.get('title')
            text = outline.get('text')
            url = outline.get('htmlUrl')

            # Write HTML list item with link
            if title and url:
                html.write(f'<li><a href="{url}" title="{title}">{text}</a></li>\n')

        # Write closing tags for HTML
        html.write('</ul>\n</body>\n</html>\n')

if __name__ == "__main__":
    if len(sys.argv) != 4 or sys.argv[1] in ['-h', '--help']:
        print("Usage: python script_name.py <opml_file_path> <html_file_path> <category element name>")
        print("Converts children of the category element in an OPML file to a valid HTML file, sorted alphabetically.")
        sys.exit(1)

    opml_file_path = sys.argv[1]
    html_file_path = sys.argv[2]

    opml_to_html(opml_file_path, html_file_path)

    print(f"Conversion complete. HTML file saved at: {html_file_path}")
