import os
from html.parser import HTMLParser


class TitleExtractor(HTMLParser):
    inHeading = False
    title = ''

    def handle_starttag(self, tag, attrs):
        if tag == 'h1':
            self.inHeading = True

    def handle_data(self, data):
        if self.inHeading:
            self.title = data

    def handle_endtag(self, tag):
        if tag == 'h1':
            self.inHeading = False

    def get_title(self):
        return self.title


readme_file = open('README.md', 'w')
readme_file.write('''
# My Medium Blog

This is a backup of my Medium blog. [https://medium.com/@thebojda](https://medium.com/@thebojda)
 
''')

parser = TitleExtractor()
files = os.listdir('posts')
files.sort()
for post in files:
    file = open('posts/' + post)
    html = file.read()
    file.close()
    parser.feed(html)
    readme_file.write(
        '[' + parser.get_title() + '](' + 'https://thebojda.github.io/my-medium-blog/posts/' + post + ')\n\n')

readme_file.close()
