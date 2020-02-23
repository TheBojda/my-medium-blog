import os
from html.parser import HTMLParser


class TitleExtractor(HTMLParser):
    inHeading = False
    inSubHeading = False
    title = ''
    subtitle = ''

    def handle_starttag(self, tag, attrs):
        if tag == 'h1':
            self.inHeading = True
        if tag == 'section':
            for name, value in attrs:
                if name == 'data-field' and value == 'subtitle':
                    self.inSubHeading = True

    def handle_data(self, data):
        if self.inHeading:
            self.title = data
        if self.inSubHeading:
            self.subtitle = data

    def handle_endtag(self, tag):
        if tag == 'h1':
            self.inHeading = False
        if tag == 'section':
            self.inSubHeading = False

    def get_title(self):
        return self.title

    def get_subtitle(self):
        if len(self.subtitle) > 100:
            return ''
        return self.subtitle


readme_file = open('README.md', 'w')
readme_file.write('''
# My Medium Blog

This is a backup of my Medium blog. [https://medium.com/@thebojda](https://medium.com/@thebojda)
 
''')

files = os.listdir('posts')
files.sort()
for post in files:
    file = open('posts/' + post)
    html = file.read()
    file.close()
    parser = TitleExtractor()
    parser.feed(html)
    readme_file.write(
        '[' + parser.get_title() + ' ' + parser.get_subtitle() + '](' + 'https://thebojda.github.io/my-medium-blog/posts/' + post + ')\n\n')

readme_file.close()
