"""
This file contains data structures defining fields and types
that are used to render the correct forms in records/forms.py

The information has been gathered from:
http://bib-it.sourceforge.net/help/fieldsAndEntryTypes.php

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
    "publisher",    #18
    "school",       #19
    "series",       #20
    "title",        #21
    "type",         #22
    "volume",       #23
    "year",         #24

]

"""
Here follows the specific fields that are required and optional
for each specific entry which can all be accessed through
ENTRY_TYPES("entry_type")[x] where x = 0 gives a list of
required fields and x = 1 gives the optional fields
"""
ARTICLE_FIELDS = [
    [
        "title",
        "author",
        "journal",
        "year",
    ],
    [
        "volume",
        "number",
        "pages",
        "month",
        "note",
    ]
]

BOOK_FIELDS = [
    [
        "title",
        "author",
        "editor",
        "publisher",
        "year",
    ],
    [
        "volume",
        "number",
        "address",
        "edition",
        "month",
        "month",
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
        "note"
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
        "note"
    ]
]
INBOOK_FIELDS =  [
    [
        "author",
        "editor",
        "title",
        "chapter",
        "pages",
        "publisher",
        "year",
    ],
    [
        "volume",
        "number",
        "series",
        "type",
        "address",
        "edition",
        "month",
        "note"
    ]
]

INCOLLECTIONS_FIELDS = [
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
        "note"
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
        "note"
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
        "note"
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
        "note"
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
        "note"
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
        "note"
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
        "organization"
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
        "note"
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
        "year"
    ]
]

ENTRY_TYPES = {
    "article":ARTICLE_FIELDS,
    "book":BOOK_FIELDS,
    "booklet":BOOKLET_FIELDS,
    "conference":CONFERENCE_FIELDS,
    "inbook":INBOOK_FIELDS,
    "incollections":INCOLLECTIONS_FIELDS,
    "inproceedings":INPROCEEDINGS_FIELDS,
    "manual":MANUAL_FIELDS,
    "mastersthesis":MASTERSTHESIS_FIELDS,
    "misc":MISC_FIELDS,
    "phdthesis":PHDTHESIS_FIELDS,
    "proceedings":PROCEEDINGS_FIELDS,
    "techreport":TECHREPORT_FIELDS,
    "unpublished":UNPUBLISHED_FIELDS,
}
