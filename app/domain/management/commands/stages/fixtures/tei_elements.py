"""TEI elements."""

TEI_ATTRIBUTE_OPTIONS = [
    {
        'key': 'languages',
        'name': 'TEI language list',
        'payload_type': 'db_records',
        'description': 'List of languages for TEI elements.',
        'payload': {
            'app': 'domain',
            'model': 'LanguageReference',
            'filters': {'iso6393__in': ['eng', 'fra', 'spa', 'deu', 'ita']},
            'concordance': {
                'label': 'name',
                'value': 'iso6393',
            },
        },
    },
    {
        'key': 'named_entity_kinds',
        'name': 'TEI list of named entity kinds',
        'payload_type': 'static_list',
        'description': 'List of named entity kinds for TEI elements.',
        'payload': [
            {'label': 'Object', 'value': 'object'},
            {'label': 'Organization', 'value': 'organization'},
            {'label': 'Person', 'value': 'person'},
            {'label': 'Place', 'value': 'place'},
            {'label': 'Locus', 'value': 'locus'},
        ],
    },
    {
        'key': 'brace_types',
        'name': 'TEI list of brace types',
        'payload_type': 'static_list',
        'description': 'List of brace types for TEI elements.',
        'payload': [
            {'label': 'Curly bracket', 'value': 'curly bracket'},
            {'label': '"C"-shaped', 'value': 'c_shaped'},
            {'label': 'Vertical line', 'value': 'line'},
            {'label': '"L"-shaped', 'value': 'l_shaped'},
        ],
    },
    {
        'key': 'renvoi_rendering',
        'name': 'TEI list of renderings for renvoi',
        'payload_type': 'static_list',
        'description': 'List of renderings for TEI renvoi element.',
        'payload': [
            {'label': 'Superscript', 'value': 'superscript'},
            {'label': 'Subscript', 'value': 'subscript'},
            {'label': 'Bold', 'value': 'bold'},
            {'label': 'Oversized', 'value': 'oversized'},
        ],
    },
    {
        'key': 'abbreviation_types',
        'name': 'TEI list of abbreviation types',
        'payload_type': 'static_list',
        'description': 'List of types for TEI abbreviation element.',
        'payload': [
            {'label': 'Acronym', 'value': 'acronym'},
            {'label': 'Initial', 'value': 'initial'},
            {'label': 'Title', 'value': 'title'},
        ],
    },
    {
        'key': 'addition_placements',
        'name': 'TEI list of addition placements',
        'payload_type': 'static_list',
        'description': 'List of placements for TEI addition element.',
        'payload': [
            {'label': 'Above the line', 'value': 'above'},
            {'label': 'Below the line', 'value': 'below'},
            {'label': 'Inline', 'value': 'inline'},
            {'label': 'Inline block', 'value': 'inline-block'},
        ],
    },
    {
        'key': 'deletion_renderings',
        'name': 'TEI list of deletion renderings',
        'payload_type': 'static_list',
        'description': 'List of renderings for TEI deletion element.',
        'payload': [
            {'label': 'Overstrike', 'value': 'overstrike'},
            {'label': 'Rubout', 'value': 'rubout'},
        ],
    },
    {
        'key': 'elision_joins',
        'name': 'TEI list of elision joins',
        'payload_type': 'static_list',
        'description': 'List of join types for TEI elision element.',
        'payload': [
            {'label': 'Join left', 'value': 'left'},
            {'label': 'Join right', 'value': 'right'},
        ],
    },
    {
        'key': 'hyphenation_force',
        'name': 'TEI list of hyphenation force types',
        'payload_type': 'static_list',
        'description': 'List of force types for TEI hyphenation element.',
        'payload': [
            {'label': 'Strong', 'value': 'strong', 'description': 'Preserved during tokeneization.'},
            {'label': 'Weak', 'value': 'weak', 'description': 'Ignored during tokeneization.'},
        ],
    },
    {
        'key': 'gap_reasons',
        'name': 'TEI list of reasons for gaps',
        'payload_type': 'static_list',
        'description': 'List of reasons for TEI gap element.',
        'payload': [
            {'label': 'Contains context', 'value': 'context'},
            {'label': 'Damaged medium', 'value': 'damage'},
            {'label': 'Image unreadable', 'value': 'image'},
            {'label': 'Ink blot', 'value': 'ink'},
            {'label': 'Script undecipherable', 'value': 'script'},
        ],
    },
    {
        'key': 'supplied_reasons',
        'name': 'TEI list of reasons for supplied words',
        'payload_type': 'static_list',
        'description': 'List of reasons for TEI supplied element.',
        'payload': [
            {'label': 'Contains antecedent', 'value': 'antecedent'},
            {'label': 'Damaged medium', 'value': 'damage'},
            {'label': 'Image unreadable', 'value': 'image'},
            {'label': 'Ink blot', 'value': 'ink'},
            {'label': 'Script undecipherable', 'value': 'script'},
        ],
    },
    {
        'key': 'unclear_reasons',
        'name': 'TEI list of reasons for unclear words',
        'payload_type': 'static_list',
        'description': 'List of reasons for TEI unclear element.',
        'payload': [
            {'label': 'Damaged medium', 'value': 'damage'},
            {'label': 'Image unreadable', 'value': 'image'},
            {'label': 'Ink blot', 'value': 'ink'},
            {'label': 'Script undecipherable', 'value': 'script'},
        ],
    },
    {
        'key': 'alignment_options',
        'name': 'TEI list of alignment options',
        'payload_type': 'static_list',
        'description': 'List of options for TEI alignment element.',
        'payload': [
            {'label': 'Center', 'value': 'center'},
            {'label': 'Right', 'value': 'right'},
            {'label': 'Justify', 'value': 'justify'},
        ],
    },
    {
        'key': 'baseline_options',
        'name': 'TEI list of baseline options',
        'payload_type': 'static_list',
        'description': 'List of options for TEI baseline element.',
        'payload': [
            {'label': 'Subscript', 'value': 'subscript'},
            {'label': 'Superscript', 'value': 'superscript'},
        ],
    },
    {
        'key': 'decoration_options',
        'name': 'TEI list of decoration options',
        'payload_type': 'static_list',
        'description': 'List of options for TEI decoration element.',
        'payload': [
            {'label': 'Underscore/Underline', 'value': 'underscore'},
            {'label': 'Overline', 'value': 'overline'},
        ],
    },
    {
        'key': 'indentation_options',
        'name': 'TEI list of indentation options',
        'payload_type': 'static_list',
        'description': 'List of options for TEI indentation element.',
        'payload': [
            {'label': 'Level 1', 'value': 'indent'},
            {'label': 'Level 2', 'value': 'indent1'},
            {'label': 'Level 3', 'value': 'indent2'},
            {'label': 'Level 4', 'value': 'indent3'},
            {'label': 'Level 5', 'value': 'indent4'},
        ],
    },
    {
        'key': 'leader_renderings',
        'name': 'TEI list of leader renderings',
        'payload_type': 'static_list',
        'description': 'List of renderings for TEI leader element.',
        'payload': [
            {'label': 'Dashed line', 'value': 'dashes'},
            {'label': 'Dotted line', 'value': 'dots'},
            {'label': 'Ellipsis (three dots)', 'value': 'ellipsis'},
            {'label': 'Solid line', 'value': 'line'},
            {'label': 'Spacing only', 'value': 'none'},
        ],
    },
    {
        'key': 'mute_types',
        'name': 'TEI list of mute tag types',
        'payload_type': 'static_list',
        'description': 'List of types for TEI mute element.',
        'payload': [
            {'label': 'Named agents', 'value': 'named_agents_wrapper'},
        ],
    },
    {
        'key': 'table_renderings',
        'name': 'TEI list of table renderings',
        'payload_type': 'static_list',
        'description': 'List of renderings for TEI table element.',
        'payload': [
            {
                'label': 'Horizontal header',
                'value': 'hor_header',
                'description': 'Use the contents of the first row as headers.',
            },
            {
                'label': 'Vertical header',
                'value': 'vert_header',
                'description': 'Use the contents of the first column as headers.',
            },
            {
                'label': 'Table border',
                'value': 'boxed',
                'description': 'Adds a border around the table.',
            },
            {'label': 'Row dividers', 'value': 'hdiv', 'description': 'Adds dividers between rows.'},
            {
                'label': 'Column dividers',
                'value': 'vdiv',
                'description': 'Adds dividers between columns.',
            },
        ],
    },
    {
        'key': 'glyph_options',
        'name': 'TEI list of glyph options',
        'payload_type': 'static_list',
        'description': 'List of options for TEI glyph element.',
        'payload': [
            {'value': '22B6', 'label': 'Barbell right'},
            {'value': '22B7', 'label': 'Barbell left'},
            {'value': '25CB', 'label': 'Circle'},
            {'value': '2655', 'label': 'Crown'},
            {'value': '2720', 'label': 'Maltese cross'},
            {'value': '261A', 'label': 'Manicule pointing left'},
            {'value': '261B', 'label': 'Manicule pointing right'},
            {
                'value': '00BD',
                'label': 'fraction - half',
                'description': {'parent': 'num', 'attributes': {'type': 'fraction', 'value': 0.5}},
            },
            {
                'value': '2153',
                'label': 'fraction - third',
                'description': {'parent': 'num', 'attributes': {'type': 'fraction', 'value': 0.33}},
            },
            {
                'value': '00BC',
                'label': 'fraction - quarter',
                'description': {'parent': 'num', 'attributes': {'type': 'fraction', 'value': 0.25}},
            },
        ],
    },
    {
        'key': 'table_row_roles',
        'name': 'TEI list of table row roles',
        'payload_type': 'static_list',
        'description': 'List of roles for TEI table rows.',
        'payload': [
            {'label': 'Label', 'value': 'label'},
            {'label': 'Data', 'value': 'data'},
        ],
    },
]

TEI_ELEMENTS = [
    {
        'label': 'Gloss',
        'description': 'Add a gloss or translation for a term.',
        'kb_reference': '#Glosses',
        'compound': True,
        'in_context_menu': False,
        'in_toolbar': False,
        'icon': 'fa-solid fa-language',
        'section': 'annotation',
        'tags': [
            {
                'name': 'term',
                'kind': 'enclosing',
                'placeholder': 'WORD',
                'icon': 'fa-solid fa-info',
                'attributes': [
                    {
                        'value': 'xml:id',
                        'label': 'Id',
                        'editable': False,
                        'required': True,
                        'default': 'auto',
                        'kind': 'string',
                    },
                ],
            },
            {
                'name': 'noteGrp',
                'kind': 'grouping',
                'icon': 'mdi-note-multiple-outline',
            },
            {
                'name': 'note',
                'kind': 'supplied',
                'parent': 'noteGrp',
                'icon': 'merge mdi-note-outline mdi-translate',
                'attributes': [
                    {
                        'value': 'type',
                        'label': 'Type',
                        'editable': False,
                        'required': True,
                        'default': 'gloss',
                        'kind': 'string',
                    },
                    {'value': 'text', 'label': 'Note', 'editable': True, 'required': True, 'kind': 'textarea'},
                    {
                        'value': 'xml:id',
                        'label': 'Id',
                        'editable': False,
                        'required': True,
                        'default': 'auto',
                        'kind': 'string',
                    },
                ],
            },
            {
                'name': 'gloss',
                'kind': 'supplied',
                'parent': 'noteGrp',
                'icon': 'mdi-translate',
                'attributes': [
                    {
                        'value': 'target',
                        'label': 'Target',
                        'editable': False,
                        'required': True,
                        'default': 'auto',
                        'kind': 'string',
                    },
                    {
                        'value': 'lang',
                        'label': 'Language',
                        'editable': True,
                        'required': True,
                        'kind': 'choice',
                        'default': 'ENG',
                        'options': 'languages',
                    },
                    {'value': 'text', 'label': 'Note', 'editable': True, 'required': True, 'kind': 'textarea'},
                ],
            },
        ],
    },
    {
        'label': 'Marginal note',
        'description': 'Adds a note to the margin aligned with the point of insertion.',
        'kb_reference': '#Marginal_Notes_and_Insertions_via_renvoi',
        'compound': False,
        'in_context_menu': True,
        'in_toolbar': True,
        'icon': 'fa-solid fa-note-sticky',
        'section': 'annotation',
        'tags': [
            {
                'name': 'note',
                'kind': 'supplied',
                'attributes': [
                    {
                        'value': 'type',
                        'label': 'Type',
                        'editable': False,
                        'required': True,
                        'default': 'marginal',
                        'kind': 'string',
                    },
                    {'value': 'text', 'label': 'Note', 'editable': True, 'required': True, 'kind': 'textarea'},
                ],
            }
        ],
    },
    {
        'label': 'Mute',
        'description': 'Indicates that the enclosed section of the text should be hidden and ignored for all processing purposes.',
        'kb_reference': '#Marginal_Notes_and_Insertions_via_renvoi',
        'compound': False,
        'in_context_menu': False,
        'in_toolbar': False,
        'icon': 'fa-solid fa-bell-slash',
        'section': 'annotation',
        'tags': [
            {
                'name': 'mute',
                'kind': 'enclosing',
                'placeholder': 'CONTENT TO MUTE',
                'attributes': [
                    {
                        'value': 'type',
                        'label': 'Type',
                        'editable': True,
                        'required': False,
                        'kind': 'choice',
                        'options': 'mute_types',
                    }
                ],
            }
        ],
    },
    {
        'label': 'Named entity',
        'description': 'Wrap text that refers to a person, place, room, etc.',
        'kb_reference': '#Named_Entities_.28Persons.2FLocations.2FOrganizations.29',
        'compound': False,
        'in_context_menu': False,
        'in_toolbar': False,
        'icon': 'fa-solid fa-tag',
        'section': 'annotation',
        'tags': [
            {
                'name': 'rs',
                'kind': 'enclosing',
                'placeholder': 'NAMED ENTITY',
                'attributes': [
                    {
                        'value': 'type',
                        'label': 'Type',
                        'editable': True,
                        'required': True,
                        'kind': 'choice',
                        'options': 'named_entity_kinds',
                    },
                    {
                        'value': 'key',
                        'label': 'Key',
                        'editable': True,
                        'required': False,
                        'kind': 'string',
                        'description': 'An externally-defined means of identifying the entity, <i>e.g.</i> a database UUID.',
                    },
                ],
            }
        ],
    },
    {
        'label': 'Note with brace',
        'description': 'Note with a vertical element that indicates the lines it refers to.',
        'kb_reference': '#Braces',
        'compound': True,
        'in_context_menu': True,
        'in_toolbar': False,
        'icon': 'mdi-code-braces',
        'section': 'annotation',
        'tags': [
            {
                'name': 'seg',
                'kind': 'enclosing',
                'placeholder': 'CONTENT\nTO ENCLOSE\nWITH BRACE',
                'icon': 'mdi-code-braces',
                'attributes': [
                    {
                        'value': 'type',
                        'label': 'Type',
                        'editable': False,
                        'required': True,
                        'default': 'brace',
                        'kind': 'string',
                    },
                    {
                        'value': 'target',
                        'label': 'Target',
                        'editable': False,
                        'required': True,
                        'default': 'auto',
                        'kind': 'string',
                    },
                    {
                        'value': 'rend',
                        'label': 'Rendering',
                        'editable': True,
                        'required': True,
                        'default': 'curly bracket',
                        'kind': 'choice',
                        'options': 'brace_types',
                    },
                ],
            },
            {
                'name': 'note',
                'kind': 'supplied',
                'icon': 'merge mdi-note-outline mdi-code-braces',
                'attributes': [
                    {
                        'value': 'type',
                        'label': 'Type',
                        'editable': False,
                        'required': True,
                        'default': 'brace',
                        'kind': 'string',
                    },
                    {
                        'value': 'xml:id',
                        'label': 'Id',
                        'editable': False,
                        'required': True,
                        'default': 'auto',
                        'kind': 'string',
                    },
                    {'value': 'text', 'label': 'Note', 'editable': True, 'required': True, 'kind': 'textarea'},
                ],
            },
        ],
    },
    {
        'label': 'Note with renvoi',
        'description': 'Adds comments outside of the main textual stream, using a mark to indicate a specific point in the text.',
        'kb_reference': '#Marginal_Notes_and_Insertions_via_renvoi',
        'compound': True,
        'in_context_menu': True,
        'in_toolbar': False,
        'section': 'annotation',
        'tags': [
            {
                'name': 'ref',
                'kind': 'enclosing',
                'placeholder': '*',
                'icon': 'mdi-asterisk-circle-outline',
                'attributes': [
                    {
                        'value': 'target',
                        'label': 'Target',
                        'editable': False,
                        'required': True,
                        'default': 'auto',
                        'kind': 'string',
                    },
                    {
                        'value': 'rend',
                        'label': 'Rendering',
                        'editable': True,
                        'required': True,
                        'default': 'superscript',
                        'kind': 'multichoice',
                        'options': 'renvoi_rendering',
                    },
                ],
            },
            {
                'name': 'note',
                'kind': 'supplied',
                'icon': 'merge mdi-note-outline mdi-asterisk-circle-outline',
                'attributes': [
                    {
                        'value': 'type',
                        'label': 'Type',
                        'editable': False,
                        'required': True,
                        'default': 'renvoi',
                        'kind': 'string',
                    },
                    {'value': 'text', 'label': 'Note', 'editable': True, 'required': True, 'kind': 'textarea'},
                    {
                        'value': 'xml:id',
                        'label': 'Id',
                        'editable': False,
                        'required': True,
                        'default': 'auto',
                        'kind': 'string',
                    },
                ],
            },
        ],
    },
    {
        'label': 'Paraphrase',
        'description': 'Wrap text that has been paraphrased',
        'kb_reference': '#Paraphrasing',
        'compound': False,
        'in_context_menu': False,
        'in_toolbar': True,
        'icon': 'fa-solid fa-quote-left',
        'section': 'annotation',
        'tags': [
            {
                'name': 'quote',
                'kind': 'enclosing',
                'placeholder': 'PARAPHRASED CONTENT',
                'attributes': [
                    {
                        'value': 'resp',
                        'label': 'Author',
                        'editable': True,
                        'required': False,
                        'kind': 'string',
                        'description': 'Person responsible for the paraphrased text.',
                    }
                ],
            }
        ],
    },
    {
        'label': 'Abbreviation',
        'description': 'Wrap abbreviation',
        'kb_reference': '#Abbreviations_and_Expansions',
        'compound': False,
        'in_context_menu': False,
        'in_toolbar': False,
        'icon': 'fa-solid fa-signature',
        'section': 'editorial',
        'tags': [
            {
                'name': 'abbr',
                'kind': 'enclosing',
                'placeholder': 'ABBREVIATION',
                'attributes': [
                    {
                        'value': 'type',
                        'label': 'Type',
                        'editable': True,
                        'required': False,
                        'kind': 'choice',
                        'options': 'abbreviation_types',
                    }
                ],
            }
        ],
    },
    {
        'label': 'Addition',
        'description': 'Wrap text inserted in the source text',
        'kb_reference': '#Additions.2C_Deletions.2C_Substitutions.2C_and_Restorations',
        'compound': False,
        'in_context_menu': True,
        'in_toolbar': False,
        'icon': 'fa-solid fa-arrows-turn-to-dots',
        'section': 'editorial',
        'tags': [
            {
                'name': 'add',
                'kind': 'enclosing',
                'placeholder': 'INSERTED CONTENT',
                'attributes': [
                    {
                        'value': 'place',
                        'label': 'Place',
                        'editable': True,
                        'required': False,
                        'kind': 'choice',
                        'description': 'Location of the addition with reference to the main text.',
                        'options': 'addition_placements',
                    }
                ],
            }
        ],
    },
    {
        'label': 'Deletion',
        'description': 'Wrap text deleted, marked as deleted, or otherwise indicated as superfluous.',
        'kb_reference': '#Additions.2C_Deletions.2C_Substitutions.2C_and_Restorations',
        'compound': False,
        'in_context_menu': True,
        'in_toolbar': False,
        'icon': 'mdi-eraser',
        'section': 'editorial',
        'tags': [
            {
                'name': 'del',
                'kind': 'enclosing',
                'placeholder': 'DELETED CONTENT',
                'attributes': [
                    {
                        'value': 'rend',
                        'label': 'Rendering',
                        'editable': True,
                        'required': True,
                        'default': 'overstrike',
                        'kind': 'choice',
                        'options': 'deletion_renderings',
                    }
                ],
            }
        ],
    },
    {
        'label': 'Elision',
        'description': 'Wrap elided word.',
        'kb_reference': '#Elisions',
        'compound': False,
        'in_context_menu': False,
        'in_toolbar': False,
        'icon': 'fa-solid fa-comment-dots',
        'section': 'editorial',
        'tags': [
            {
                'name': 'w',
                'kind': 'enclosing',
                'placeholder': 'ELIDED WORD',
                'attributes': [
                    {
                        'value': 'type',
                        'label': 'Type',
                        'editable': False,
                        'required': True,
                        'default': 'elision',
                        'kind': 'string',
                    },
                    {
                        'value': 'lemma',
                        'label': 'Lemma',
                        'editable': True,
                        'required': True,
                        'kind': 'string',
                        'description': 'The non-elided version of the word.',
                    },
                    {
                        'value': 'join',
                        'label': 'Join',
                        'editable': True,
                        'required': True,
                        'kind': 'choice',
                        'description': 'Side on which the word should be joined.',
                        'options': 'elision_joins',
                    },
                ],
            }
        ],
    },
    {
        'label': 'Expansion',
        'description': 'Wrap text that has been expanded from an abbreviation.',
        'kb_reference': '#Abbreviations_and_Expansions',
        'compound': False,
        'in_context_menu': False,
        'in_toolbar': False,
        'icon': 'fa-solid fa-left-right',
        'section': 'editorial',
        'tags': [
            {
                'name': 'expan',
                'kind': 'enclosing',
                'placeholder': 'EXPANDED WORD',
            }
        ],
    },
    {
        'label': 'Hand shift',
        'description': 'Mark the beginning of a sequence of text written in a new hand, a change of writing style, character, or ink.',
        'kb_reference': '#Hyphenation',
        'compound': False,
        'in_context_menu': False,
        'in_toolbar': False,
        'icon': 'fa-solid fa-user-pen',
        'section': 'editorial',
        'tags': [
            {
                'name': 'handShift',
                'kind': 'standalone',
                'attributes': [
                    {
                        'value': 'scribe',
                        'label': 'Scribe',
                        'editable': True,
                        'required': False,
                        'kind': 'string',
                        'description': 'Scribe value or ID (can be relative to document) if hand is attributable.',
                    },
                    {
                        'value': 'script',
                        'label': 'Script',
                        'editable': True,
                        'required': False,
                        'kind': 'string',
                        'description': 'Writing style, <i>e.g. secretary, copperplate, smaller, lighter, rough</i>.',
                    },
                    {
                        'value': 'medium',
                        'label': 'Medium',
                        'editable': True,
                        'required': False,
                        'kind': 'string',
                        'description': 'Tint or type of ink or writing medium, <i>e.g. black ink, greenish ink, pencil</i>.',
                    },
                ],
            }
        ],
    },
    {
        'label': 'Hyphenation',
        'description': 'Wrap a hyphen and indicate its type/function.',
        'kb_reference': '#Hyphenation',
        'compound': False,
        'in_context_menu': False,
        'in_toolbar': True,
        'icon': 'fa-solid fa-minus',
        'section': 'editorial',
        'tags': [
            {
                'name': 'pc',
                'kind': 'enclosing',
                'placeholder': '-',
                'attributes': [
                    {
                        'value': 'force',
                        'label': 'Force',
                        'editable': True,
                        'required': True,
                        'default': 'weak',
                        'kind': 'choice',
                        'options': 'hyphenation_force',
                    }
                ],
            }
        ],
    },
    {
        'label': 'Omission/Gap',
        'description': 'Mark a gap or omission in the transcription.',
        'kb_reference': '#Omissions',
        'compound': False,
        'in_context_menu': True,
        'in_toolbar': False,
        'icon': 'fa-solid fa-arrows-left-right-to-line',
        'section': 'editorial',
        'tags': [
            {
                'name': 'gap',
                'kind': 'standalone',
                'attributes': [
                    {
                        'value': 'reason',
                        'label': 'Reason',
                        'editable': True,
                        'required': True,
                        'kind': 'choice',
                        'options': 'gap_reasons',
                    },
                    {
                        'value': 'extent',
                        'label': 'Extent',
                        'editable': True,
                        'required': False,
                        'description': 'Extent of the gap, <i>e.g.</i> 1 word, 3 paragraphs',
                        'kind': 'string',
                    },
                ],
            }
        ],
    },
    {
        'label': 'Supplied',
        'description': 'Wrap text supplied by the transcriber',
        'kb_reference': '#Supplied_Text',
        'compound': False,
        'in_context_menu': True,
        'in_toolbar': False,
        'icon': 'fa-solid fa-hand-holding-medical',
        'section': 'editorial',
        'tags': [
            {
                'name': 'supplied',
                'kind': 'enclosing',
                'placeholder': 'SUPPLIED WORD',
                'attributes': [
                    {
                        'value': 'reason',
                        'label': 'Reason',
                        'editable': True,
                        'required': False,
                        'description': 'Reason why the text had to be supplied',
                        'kind': 'choice',
                        'options': 'supplied_reasons',
                    }
                ],
            }
        ],
    },
    {
        'label': 'Unclear',
        'description': 'Wrap text that cannot be transcribed with certainty.',
        'kb_reference': '#Unclear_Text',
        'compound': False,
        'in_context_menu': True,
        'in_toolbar': False,
        'icon': 'fa-solid fa-circle-question',
        'section': 'editorial',
        'tags': [
            {
                'name': 'unclear',
                'kind': 'enclosing',
                'placeholder': 'UNCLEAR WORD',
                'attributes': [
                    {
                        'value': 'reason',
                        'label': 'Reason',
                        'editable': True,
                        'required': False,
                        'description': 'Reason why the material is hard to transcribe',
                        'kind': 'choice',
                        'options': 'unclear_reasons',
                    }
                ],
            }
        ],
    },
    {
        'label': 'Alignment',
        'description': 'Wrap a word or phrase to indicate a change in alignment.',
        'kb_reference': '#Indentations.2C_Superscripts.2C_and_Subscripts',
        'compound': False,
        'in_context_menu': False,
        'in_toolbar': True,
        'icon': 'fa-solid fa-align-center',
        'section': 'formatting',
        'tags': [
            {
                'name': 'hi',
                'kind': 'enclosing',
                'placeholder': 'CONTENT TO ALIGN',
                'attributes': [
                    {
                        'value': 'rend',
                        'label': 'Rendering',
                        'editable': True,
                        'required': True,
                        'kind': 'choice',
                        'options': 'alignment_options',
                    }
                ],
            }
        ],
    },
    {
        'label': 'Baseline',
        'description': 'Wrap a word or phrase to alter its baseline.',
        'kb_reference': '#Indentations.2C_Superscripts.2C_and_Subscripts',
        'compound': False,
        'in_context_menu': False,
        'in_toolbar': True,
        'icon': 'fa-solid fa-superscript',
        'section': 'formatting',
        'tags': [
            {
                'name': 'hi',
                'kind': 'enclosing',
                'placeholder': 'TARGET CONTENT',
                'attributes': [
                    {
                        'value': 'rend',
                        'label': 'Rendering',
                        'editable': True,
                        'required': True,
                        'kind': 'choice',
                        'options': 'baseline_options',
                    }
                ],
            }
        ],
    },
    {
        'label': 'Decoration',
        'description': 'Wrap a word or phrase and indicate a type of decoration.',
        'kb_reference': '#Indentations.2C_Superscripts.2C_and_Subscripts',
        'compound': False,
        'in_context_menu': False,
        'in_toolbar': True,
        'icon': 'fa-solid fa-underline',
        'section': 'formatting',
        'tags': [
            {
                'name': 'hi',
                'kind': 'enclosing',
                'placeholder': 'CONTENT TO DECORATE',
                'attributes': [
                    {
                        'value': 'rend',
                        'label': 'Rendering',
                        'editable': True,
                        'required': True,
                        'kind': 'choice',
                        'options': 'decoration_options',
                    }
                ],
            }
        ],
    },
    {
        'label': 'Indentation',
        'description': 'Wrap a word or phrase to assign a level of indentation to it.',
        'kb_reference': '#Indentations.2C_Superscripts.2C_and_Subscripts',
        'compound': False,
        'in_context_menu': True,
        'in_toolbar': True,
        'icon': 'fa-solid fa-indent',
        'section': 'formatting',
        'tags': [
            {
                'name': 'hi',
                'kind': 'enclosing',
                'placeholder': 'CONTENT TO INDENT',
                'attributes': [
                    {
                        'value': 'rend',
                        'label': 'Rendering',
                        'editable': True,
                        'required': True,
                        'kind': 'choice',
                        'options': 'indentation_options',
                    }
                ],
            }
        ],
    },
    {
        'label': 'Format Quotation',
        'description': 'Formats wrapped text as directly quoted, e.g. from a manuscript. Mainly for use in notes.',
        'kb_reference': '#Paraphrasing',
        'compound': False,
        'in_context_menu': False,
        'in_toolbar': False,
        'icon': 'fa-solid fa-quote-left',
        'section': 'formatting',
        'tags': [
            {
                'name': 'quotation',
                'kind': 'enclosing',
                'placeholder': 'QUOTED CONTENT',
            }
        ],
    },
    {
        'label': 'Blank space',
        'description': 'Mark <b>unusual space</b> in the source text.',
        'kb_reference': '#Blank_Space',
        'compound': False,
        'in_context_menu': False,
        'in_toolbar': False,
        'icon': 'fa-solid fa-up-down',
        'section': 'layout',
        'tags': [
            {
                'name': 'space',
                'kind': 'standalone',
                'attributes': [
                    {
                        'value': 'extent',
                        'label': 'Extent',
                        'editable': True,
                        'required': True,
                        'description': 'Description of the <b>extent</b> of the blank, <i>e.g.</i> 7 words',
                        'kind': 'string',
                    }
                ],
            }
        ],
    },
    {
        'label': 'Columns',
        'description': 'Adds a set of columns to the page.',
        'kb_reference': '#Columns',
        'compound': True,
        'in_context_menu': False,
        'in_toolbar': False,
        'icon': 'mdi-table-column',
        'section': 'layout',
        'tags': [
            {
                'name': 'layout',
                'kind': 'grouping',
                'icon': 'mdi-format-columns',
                'attributes': [
                    {
                        'value': 'columns',
                        'label': 'Number of columns',
                        'editable': True,
                        'required': True,
                        'kind': 'string',
                    }
                ],
            },
            {
                'name': 'ab',
                'kind': 'enclosing',
                'parent': 'layout',
                'placeholder': 'COLUMN CONTENT',
                'icon': 'mdi-table-column',
                'attributes': [
                    {
                        'value': 'type',
                        'label': 'Type',
                        'editable': False,
                        'required': True,
                        'default': 'column',
                        'kind': 'string',
                    },
                    {
                        'value': 'n',
                        'label': 'Column no.',
                        'editable': True,
                        'required': True,
                        'kind': 'string',
                    },
                ],
            },
        ],
    },
    {
        'label': 'Horizontal rule',
        'description': 'Adds a horizontal line accross the page.',
        'kb_reference': '#Leaders',
        'compound': False,
        'in_context_menu': False,
        'in_toolbar': False,
        'icon': 'fa-regular fa-window-minimize',
        'section': 'layout',
        'tags': [
            {
                'name': 'metamark',
                'kind': 'standalone',
                'attributes': [
                    {
                        'value': 'function',
                        'label': 'Function',
                        'editable': False,
                        'required': True,
                        'default': 'hr',
                        'kind': 'string',
                    }
                ],
            }
        ],
    },
    {
        'label': 'Partial rule',
        'description': 'Adds a partial, unindented horizontal line.',
        'kb_reference': '#Leaders',
        'compound': False,
        'in_context_menu': False,
        'in_toolbar': False,
        'icon': 'fa-solid fa-minus',
        'section': 'layout',
        'tags': [
            {
                'name': 'metamark',
                'kind': 'standalone',
                'attributes': [
                    {
                        'value': 'function',
                        'label': 'Function',
                        'editable': False,
                        'required': True,
                        'default': 'hhr',
                        'kind': 'string',
                    }
                ],
            }
        ],
    },
    {
        'label': 'Leader',
        'description': 'Typographical mark used to connect items on the page that might be separated by considerable horizontal distance.',
        'kb_reference': '#Leaders',
        'compound': False,
        'in_context_menu': False,
        'in_toolbar': False,
        'icon': 'mdi-form-textbox-password',
        'section': 'layout',
        'tags': [
            {
                'name': 'metamark',
                'kind': 'standalone',
                'attributes': [
                    {
                        'value': 'function',
                        'label': 'Function',
                        'editable': False,
                        'required': True,
                        'default': 'leader',
                        'kind': 'string',
                    },
                    {
                        'value': 'rend',
                        'label': 'Rendering',
                        'editable': True,
                        'required': True,
                        'kind': 'choice',
                        'description': 'How the leader is <b>rend</b>ered on the page',
                        'options': 'leader_renderings',
                    },
                ],
            }
        ],
    },
    {
        'label': 'Table',
        'description': 'Adds a tabular structure to the page. If applied to a comma/tab-separated block of content, the structure is parsed automatically, otherwise a skeleton table is added.',
        'kb_reference': '#Leaders',
        'compound': True,
        'in_context_menu': False,
        'in_toolbar': False,
        'icon': 'mdi-table',
        'section': 'layout',
        'tags': [
            {
                'name': 'table',
                'kind': 'grouping',
                'icon': 'mdi-table',
                'attributes': [
                    {
                        'value': 'rend',
                        'label': 'Rendering',
                        'editable': True,
                        'required': False,
                        'kind': 'multichoice',
                        'options': 'table_renderings',
                    },
                    {
                        'value': 'rows',
                        'label': 'Rows',
                        'editable': True,
                        'required': False,
                        'kind': 'string',
                        'description': 'Number of rows if creating an empty table.',
                    },
                    {
                        'value': 'cols',
                        'label': 'Columns',
                        'editable': True,
                        'required': False,
                        'kind': 'string',
                        'description': 'Number of columns if creating an empty table.',
                    },
                ],
            },
            {
                'name': 'row',
                'kind': 'grouping',
                'parent': 'table',
                'icon': 'mdi-table-row',
                'attributes': [
                    {
                        'value': 'role',
                        'label': 'Role',
                        'editable': True,
                        'required': False,
                        'kind': 'string',
                        'default': 'data',
                        'options': 'table_row_roles',
                    },
                ],
            },
            {
                'name': 'cell',
                'kind': 'enclosing',
                'icon': 'fa-regular fa-rectangle-list',
                'parent': 'row',
                'placeholder': 'CELL CONTENT',
            },
        ],
    },
    {
        'label': 'Ditto',
        'description': 'Mark to indicate that the words or figures above it are to be repeated',
        'kb_reference': '#Indentations.2C_Superscripts.2C_and_Subscripts',
        'compound': False,
        'in_context_menu': False,
        'in_toolbar': False,
        'icon': 'from-char 〃',
        'section': 'marks',
        'tags': [
            {
                'name': 'metamark',
                'kind': 'standalone',
                'attributes': [
                    {
                        'value': 'function',
                        'label': 'Function',
                        'editable': False,
                        'required': True,
                        'default': 'ditto',
                        'kind': 'string',
                    }
                ],
            }
        ],
    },
    {
        'label': 'Ellipsis',
        'description': 'Mark to indicates the intentional omission of text without altering its original meaning',
        'kb_reference': '#Indentations.2C_Superscripts.2C_and_Subscripts',
        'compound': False,
        'in_context_menu': False,
        'in_toolbar': False,
        'icon': 'fa-solid fa-ellipsis',
        'section': 'marks',
        'tags': [
            {
                'name': 'metamark',
                'kind': 'standalone',
                'attributes': [
                    {
                        'value': 'function',
                        'label': 'Function',
                        'editable': False,
                        'required': True,
                        'kind': 'string',
                        'default': 'ellipsis',
                    }
                ],
            }
        ],
    },
    {
        'label': 'Glyph',
        'description': 'Add a non-standard character (e.g. manicule, cross, fraction, etc.)',
        'kb_reference': '#Indentations.2C_Superscripts.2C_and_Subscripts',
        'compound': True,
        'in_context_menu': False,
        'in_toolbar': True,
        'icon': 'fa-brands fa-glide-g',
        'section': 'marks',
        'tags': [
            {
                'name': 'g',
                'kind': 'standalone',
                'icon': 'fa-brands fa-glide-g',
                'attributes': [
                    {
                        'value': 'ref',
                        'label': 'Value',
                        'editable': True,
                        'required': True,
                        'kind': 'compound',
                        'options': 'glyph_options',
                    }
                ],
            },
            {
                'name': 'num',
                'kind': 'grouping',
                'icon': 'fa-solid fa-hashtag',
                'attributes': [
                    {
                        'value': 'type',
                        'label': 'Type',
                        'editable': False,
                        'required': True,
                        'default': 'auto',
                        'kind': 'string',
                    },
                    {
                        'value': 'value',
                        'label': 'Value',
                        'editable': False,
                        'required': True,
                        'default': 'auto',
                        'kind': 'string',
                    },
                ],
            },
        ],
    },
]
