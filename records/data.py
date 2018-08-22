"""
This file contains data structures defining fields and types
that are used to render the correct forms in records/forms.py

The information has been gathered from:
wikipedia

"""

FIELDS = [
    "address",      #0
    "annote",       #1
    "author",       #2
    "booktitle",    #3
    "chapter",      #4
    "crossref",     #5
    "edition",      #6
    "editor",       #7
    "howpublished", #8
    "institution",  #9
    "journal",      #10
    "key",          #11
    "month",        #12
    "note",         #13
    "number",       #14
    "organization", #15
    "pages",        #16
    "publisher",    #17
    "school",       #18
    "series",       #19
    "title",        #20
    "type",         #21
    "volume",       #22
    "year",         #23
    "url"

]

"""
Here follows the specific fields that are required and optional
for each specific entry which can all be accessed through
ENTRY_TYPE_FIELDS["entry_type"][x] where x = 0 gives a list of
required fields and x = 1 gives the optional fields
"""
ARTICLE_FIELDS = [
    [
        "title",
        "author",
        "journal",
        "year",
        "volume",
    ],
    [
        "number",
        "pages",
        "month",
        "note",
        "key"
    ]
]

BOOK_FIELDS = [
    [
        "title",
        "publisher",
        "year",
    ],
    [
        "author",
        "editor",
        "volume",
        "number",
        "address",
        "edition",
        "month",
        "note",
        "key",
        "url"
    ]
]

BOOKLET_FIELDS = [
    [
        "title"
    ],
    [
        "author",
        "howpublished",
        "address",
        "month",
        "year",
        "note",
        "key"
    ]
]

CONFERENCE_FIELDS = [
    [
        "title",
        "author",
        "booktitle",
        "year"
    ],
    [
        "editor",
        "volume",
        "number",
        "series",
        "pages",
        "address",
        "month",
        "organization",
        "publisher",
        "note",
        "key"
    ]
]
INBOOK_FIELDS =  [
    [
        "title",
        "publisher",
        "year",
    ],
    [
        "author",
        "editor",
        "chapter",
        "pages",
        "volume",
        "number",
        "series",
        "type",
        "address",
        "edition",
        "month",
        "note",
        "key"
    ]
]

INCOLLECTION_FIELDS = [
    [
        "title",
        "author",
        "booktitle",
        "publisher",
        "year"
    ],
    [
        "editor",
        "volume",
        "number",
        "series",
        "type",
        "chapter",
        "pages",
        "address",
        "edition",
        "month",
        "note",
        "key"
    ]
]

INPROCEEDINGS_FIELDS = [
    [
        "title",
        "author",
        "booktitle",
        "year"
    ],
    [
        "editor",
        "volume",
        "number",
        "series",
        "pages",
        "address",
        "month",
        "organization",
        "publisher",
        "note",
        "key"
    ]
]

MANUAL_FIELDS =[
    [
        "title"
    ],
    [
        "author",
        "organization",
        "address",
        "edition",
        "month",
        "year",
        "note",
        "key"
    ]
]

MASTERSTHESIS_FIELDS = [
    [
        "title",
        "author",
        "school",
        "year"
    ],
    [
        "type",
        "address",
        "month",
        "note",
        "key"
    ]
]

MISC_FIELDS = [
    [

    ],
    [
        "title",
        "author",
        "howpublished",
        "month",
        "year",
        "note",
        "key"
    ]
]

PHDTHESIS_FIELDS = [
    [
        "title",
        "author",
        "school",
        "year"
    ],
    [
        "type",
        "address",
        "month",
        "note",
        "key"
    ]
]

PROCEEDINGS_FIELDS = [
    [
        "title",
        "year"
    ],
    [
        "editor",
        "volume",
        "number",
        "series",
        "address",
        "publisher",
        "note",
        "month",
        "organization",
        "key"
    ]
]

TECHREPORT_FIELDS = [
    [
        "title",
        "author",
        "institution",
        "year"
    ],
    [
        "type",
        "number",
        "address",
        "month",
        "note",
        "key"
    ]
]

UNPUBLISHED_FIELDS = [
    [
        "title",
        "author",
        "note"
    ],
    [
        "month",
        "year",
        "key"
    ]
]

ENTRY_TYPES = {
    1:"article",
    2:"book",
    3:"booklet",
    4:"conference",
    5:"inbook",
    6:"incollections",
    7:"inproceedings",
    8:"manual",
    9:"mastersthesis",
    10:"misc",
    11:"phdthesis",
    12:"proceedings",
    13:"techreport",
    14:"unpublished",
}

ENTRY_TYPE_FIELDS = {
    "article":ARTICLE_FIELDS,
    "book":BOOK_FIELDS,
    "booklet":BOOKLET_FIELDS,
    "conference":CONFERENCE_FIELDS,
    "inbook":INBOOK_FIELDS,
    "incollection":INCOLLECTION_FIELDS,
    "inproceedings":INPROCEEDINGS_FIELDS,
    "manual":MANUAL_FIELDS,
    "mastersthesis":MASTERSTHESIS_FIELDS,
    "misc":MISC_FIELDS,
    "phdthesis":PHDTHESIS_FIELDS,
    "proceedings":PROCEEDINGS_FIELDS,
    "techreport":TECHREPORT_FIELDS,
    "unpublished":UNPUBLISHED_FIELDS,
}
