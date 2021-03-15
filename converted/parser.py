import TexSoup

# text
# textbf
# underline
# textit
# tableofcontents
# section
# label
# BraceGroup
# longtable
# includegraphics
# enumerate
# footnote
# subsection
# itemize
# subsubsection
# textsc
# textsuperscript
# textgreater
# quote
# paragraph
# section*


class TexConverter:
    def __init__(self, tree: TexSoup.data.TexNode) -> None:
        'Initialise the values and pass the tree to the parser.'
        self.section_counter = 1
        self.subsection_counter = 1
        self.subsubsection_counter = 1
        self.paragrash_counter = 1
        self.result = []
        self.parse(tree)

    def emit(self, *args):
        'Redirects tokens to the output stream.'
        for arg in args:
            self.result.append(arg)

    def parse(self, tree: TexSoup.data.TexNode) -> None:
        for child in tree.children:
            self.emit(child.name)

    def get_string(self):
        return '\n'.join(self.result)


# def section(emit, with_asterisk: False):


# def textless(emit, with_asterisk: False):
#     if with_asterisk:
#         emit('<', '*')
#     else:
#         emit('<')


# def textgreater(emit, with_asterisk: False):
#     if with_asterisk:
#         emit('>', '*')
#     else:
#         emit('>')


if __name__ == '__main__':
    with open('coordination_pekelis_20130125_final_cleaned.tex', 'r', encoding='utf-8') as inp:
        converter = TexConverter(TexSoup.TexSoup(inp.read()))
    print(converter.get_string())
