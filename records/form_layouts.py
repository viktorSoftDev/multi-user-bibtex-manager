from material import *


ARTICLE_LAYOUT = Layout(Fieldset("Required Fields [article]",
                'title',
                'author',
                'journal',
                'year',
                'volume'),
                Fieldset("Optional Fields [article]",
                'number',
                'pages',
                'month',
                'note',
                "key")
                )

BOOK_LAYOUT = Layout(Fieldset("Required Fields [book]",
                "title",
                "publisher",
                "year"),
                Fieldset("Provide Author AND/OR Editor",
                Row("author",
                "editor")),
                Fieldset("Optional Fields [book]",
                Row("volume", "number"),
                "address",
                "edition",
                "month",
                "note",
                "key",
                "url")
                )

BOOKLET_LAYOUT = Layout(Fieldset("Required Fields [booklet]",
                "title"),
                Fieldset("Optional Fields [booklet]",
                "author",
                "howpublished",
                "address",
                "month",
                "year",
                "note",
                "key")
                )

CONFERENCE_LAYOUT = Layout(Fieldset("Required Fields [conference]",
                "title",
                "author",
                "booktitle",
                "year",
                Fieldset("Optional Fields [conference]",
                "editor",
                Row("volume",
                "number"),
                "series",
                "pages",
                "address",
                "month",
                "organization",
                "publisher",
                "note",
                "key")
                ))

INBOOK_LAYOUT = Layout(Fieldset("Required Fields [inbook]",
                "title",
                "publisher",
                "year"),
                Fieldset("Provide Author AND/OR Editor and Chapter AND/OR Pages",
                Row("author", "editor"),Row("chapter", "pages")),
                Fieldset("Optional Fields [inbook]",
                "volume",
                "number",
                "series",
                "type",
                "address",
                "edition",
                "month",
                "note",
                "key")
                )

INCOLLECTIONS_LAYOUT = Layout(Fieldset("Required Fields [incollections]",
                    "title",
                    "author",
                    "booktitle",
                    "publisher",
                    "year"),
                    Fieldset("Optional Fields [incollections]",
                    "editor",
                    Row("volume", "number"),
                    "series",
                    "type",
                    "chapter",
                    "pages",
                    "address",
                    "edition",
                    "month",
                    "note",
                    "key")
                    )

INPROCEEDINGS_LAYOUT = Layout(Fieldset("Required Fields [inproceedings]",
                "title",
                "author",
                "booktitle",
                "year"),
                Fieldset("Optional Fields [inproceedings]",
                "editor",
                Row("volume", "number"),
                "series",
                "pages",
                "address",
                "month",
                "organization",
                "publisher",
                "note",
                "key")
                )

MANUAL_LAYOUT = Layout(Fieldset("Required Fields [manual]",
                "title"),
                Fieldset("Optional Fields [manual]",
                "author",
                "organization",
                "address",
                "edition",
                "month",
                "year",
                "note",
                "key")
                )

MASTERSTHESIS_LAYOUT = Layout(Fieldset("Required Fields [mastersthesis]",
                "title",
                "author",
                "school",
                "year"),
                Fieldset("Optional Fields [mastersthesis]",
                "type",
                "address",
                "month",
                "note",
                "key")
                )

MISC_LAYOUT = Layout(Fieldset("Optional Fields [misc]",
                "title",
                "author",
                "howpublished",
                "month",
                "year",
                "note",
                "key")
                )

PHDTHESIS_LAYOUT = Layout(Fieldset("Required Fields [phdthesis]",
                "title",
                "author",
                "school",
                "year"),
                Fieldset("Optional Fields [phdthesis]",
                "type",
                "address",
                "month",
                "note",
                "key")
                )

PROCEEDINGS_LAYOUT = Layout(Fieldset("Required Fields [proceedings]",
                "title",
                "year"),
                Fieldset("Optional Fields [proceedings]",
                "editor",
                Row("volume", "number"),
                "series",
                "address",
                "month",
                "publisher",
                "organization",
                "note",
                "key")
                )

TECHREPORT_LAYOUT = Layout(Fieldset("Required Fields [techreport]",
                "title",
                "author",
                "institution",
                "year"),
                Fieldset("Optional Fields [techreport]",
                "type",
                "number",
                "address",
                "month",
                "note",
                "key")
                )

UNPUBLISHED_LAYOUT = Layout(Fieldset("Required Fields [unpublished]",
                "title",
                "author",
                "note",
                Fieldset("Optional Fields [unpublished]",
                "month",
                "year",
                "key")
                ))


FORM_LAYOUT = {
    "article":ARTICLE_LAYOUT,
    "book":BOOK_LAYOUT,
    "booklet":BOOKLET_LAYOUT,
    "conference":CONFERENCE_LAYOUT,
    "inbook":INBOOK_LAYOUT,
    "incollections":INCOLLECTIONS_LAYOUT,
    "inproceedings":INPROCEEDINGS_LAYOUT,
    "manual":MANUAL_LAYOUT,
    "mastersthesis":MASTERSTHESIS_LAYOUT,
    "misc":MISC_LAYOUT,
    "phdthesis":PHDTHESIS_LAYOUT,
    "proceedings":PROCEEDINGS_LAYOUT,
    "techreport":TECHREPORT_LAYOUT,
    "unpublished":UNPUBLISHED_LAYOUT,
}
