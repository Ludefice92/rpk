from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def handle_comment(self, data):
        # Check if the comment is multi-line or single-line
        if "\n" in data:
            print(">>> Multi-line Comment")
        else:
            print(">>> Single-line Comment")
        print(data)

    def handle_data(self, data):
        # Avoid printing empty or newline-only data
        if data.strip():
            print(">>> Data")
            print(data)

# Read input
n = int(input())
html_snippet = "\n".join(input() for _ in range(n))

# Create an instance of the parser and feed the HTML snippet
parser = MyHTMLParser()
parser.feed(html_snippet)
parser.close()
