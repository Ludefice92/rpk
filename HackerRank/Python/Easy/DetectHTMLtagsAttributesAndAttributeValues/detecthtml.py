from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print(tag)
        for attr, value in attrs:
            print(f"-> {attr} > {value}")
    
    def handle_startendtag(self, tag, attrs):
        print(tag)
        for attr, value in attrs:
            print(f"-> {attr} > {value}")

    def handle_endtag(self, tag):
        # We don't need to process end tags for this task
        pass

# Read input
n = int(input())
html_snippet = "\n".join(input() for _ in range(n))

# Create an instance of the parser and feed the HTML snippet
parser = MyHTMLParser()
parser.feed(html_snippet)
