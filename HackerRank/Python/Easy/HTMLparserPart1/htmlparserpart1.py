from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print(f"Start : {tag}")
        for attr, value in attrs:
            print(f"-> {attr} > {value if value else 'None'}")

    def handle_endtag(self, tag):
        print(f"End   : {tag}")

    def handle_startendtag(self, tag, attrs):
        print(f"Empty : {tag}")
        for attr, value in attrs:
            print(f"-> {attr} > {value if value else 'None'}")

# Read input
n = int(input())
html_snippet = "\n".join(input() for _ in range(n))

# Create an instance of the parser and feed the HTML snippet
parser = MyHTMLParser()
parser.feed(html_snippet)
