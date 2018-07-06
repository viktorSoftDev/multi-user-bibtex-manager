from material import Layout, Row, Fieldset


ARTICLE_LAYOUT = Layout(Fieldset("Required Fields [article]",
                'title',
                'author',
                'journal',
                'year'),
                Fieldset("Optional Fields [article]",
                'volume',
                'number',
                'pages',
                'month',
                'note')
                )
BOOK_LAYOUT = Layout(Fieldset("Required Fields [book]",
                "title",
                "author",
                "editor",
                "publisher",
                "year",
                Fieldset("Optional Fields [book]",
                "volume",
                "number",
                "address",
                "edition",
                "month")
                ))

BOOKLET_LAYOUT = Layout(Fieldset("Required Fields [booklet]",
                "title",
                Fieldset("Optional Fields [booklet]",
                "author",
                "howpublished",
                "address",
                "month",
                "year",
                "note")
                ))

CONFERENCE_LAYOUT = Layout(Fieldset("Required Fields [conference]",
                "title",
                "author",
                "booktitle",
                "year",
                Fieldset("Optional Fields [conference]",
                "editor",
                "volume",
                "number",
                "series",
                "pages",
                "address",
                "month",
                "organization",
                "publisher",
                "note")
                ))

INBOOK_LAYOUT = Layout(Fieldset("Required Fields [inbook]",
                "author",
                "editor",
                "title",
                "chapter",
                "pages",
                "publisher",
                "year",
                Fieldset("Optional Fields [inbook]",
                "volume",
                "number",
                "series",
                "type",
                "address",
                "edition",
                "month",
                "note")
                ))

INCOLLECTIONS_LAYOUT = Layout(Fieldset("Required Fields [incollections]",
                    "title",
                    "author",
                    "booktitle",
                    "publisher",
                    "year",
                    Fieldset("Optional Fields",
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
                    "note")
                    ))

INPROCEEDINGS_LAYOUT = Layout(Fieldset("Required Fields [inproceedings]",
                "title",
                "author",
                "booktitle",
                "year",
                Fieldset("Optional Fields [inproceedings]",
                "editor",
                "volume",
                "number",
                "series",
                "pages",
                "address",
                "month",
                "organization",
                "publisher",
                "note")
                ))

MANUAL_LAYOUT = Layout(Fieldset("Required Fields [manual]",
                "title",
                Fieldset("Optional Fields [manual]",
                "author",
                "organization",
                "address",
                "edition",
                "month",
                "year",
                "note")
                ))

MASTERSTHESIS_LAYOUT = Layout(Fieldset("Required Fields [mastersthesis]",
                "title",
                "author",
                "school",
                "year",
                Fieldset("Optional Fields [mastersthesis]",
                "type",
                "address",
                "month",
                "note")
                ))

MISC_LAYOUT = Layout(Fieldset("Optional Fields [misc]",
                "title",
                "author",
                "howpublished",
                "month",
                "year",
                "note")
                )

PHDTHESIS_LAYOUT = Layout(Fieldset("Required Fields [phdthesis]",
                "title",
                "author",
                "school",
                "year",
                Fieldset("Optional Fields [phdthesis]",
                "type",
                "address",
                "month",
                "note")
                ))

PROCEEDINGS_LAYOUT = Layout(Fieldset("Required Fields [proceedings]",
                "title",
                "year",
                Fieldset("Optional Fields [proceedings]",
                "editor",
                "volume",
                "number",
                "series",
                "address",
                "publisher",
                "note",
                "month",
                "organization")
                ))

TECHREPORT_LAYOUT = Layout(Fieldset("Required Fields [techreport]",
                "title",
                "author",
                "institution",
                "year",
                Fieldset("Optional Fields [techreport]",
                "type",
                "number",
                "address",
                "month",
                "note")
                ))

UNPUBLISHED_LAYOUT = Layout(Fieldset("Required Fields [unpublished]",
                "title",
                "author",
                "note",
                Fieldset("Optional Fields [unpublished]",
                "month",
                "year")
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
