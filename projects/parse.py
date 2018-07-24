from pylatexenc.latex2text import LatexNodes2Text
from pylatexenc.latexencode import utf8tolatex

import bibtexparser

from django.shortcuts import get_object_or_404


def importBib(file):
    """
    open a file and get all the entries in a list of dictionaries.
    ID corresponds to cite_key and ENTRYTYPE to entry_type.

    The format might still be latex and hence LatexNodes2Text needs to be used
    in order to get the UTF8 text to store in the mubm models
    """
    try:
        with open(filename) as bibtex_file:
            bibtex_database = bibtexparser.load(bibtex_file)
            print(bibtex_database.entries)
            return bibtex_database.entries
    except FileNotFoundError:
        print("broken file or filepath")



# def exportBib(filename, slug):
#     project = get_object_or_404(Project, slug=slug)
#     bib_string = ""
#     for records in project.records:
#         # entry type
#         # cite Key
#         # iterator or model to dict?
#
#             # bib string += field : value


# latex = r"""\textbf{Hi there!} Here is \emph{an equation}:
# \begin{equation}
# \zeta = x + i y
# \end{equation}
# where $i$ is the imaginary unit.
# """
# utf = LatexNodes2Text().latex_to_text(latex)
# print(utf)
#
#
# latex_again = utf8tolatex(utf)
#
# print(latex_again)
