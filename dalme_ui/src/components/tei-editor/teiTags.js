export const teiTags = [
  {
    name: "Note",
    type: "sc",
    section: "annotation",
    help: "Add additional comment out of the main textual stream.",
    link: "#Marginal_Notes_and_Insertions_via_renvoi",
    tagName: "note",
    attributes: [
      {
        name: "type",
        label: "Type",
        type: "choice",
        message: "<b>Type</b> of note",
        options: ["marginal", "renvoi", "brace"],
      },
      {
        name: "target",
        label: "Target",
        message: ", <b>target</b> id to be used if renvoi",
        type: "text",
      },
      {
        name: "text",
        label: "Text",
        message: ", and the actual <b>text</b> of the note",
        type: "text",
      },
    ],
  },
  {
    name: "Brace",
    type: "w",
    section: "annotation",
    help: "Vertical element used to show groupings of lines that function as a unit.",
    link: "#Braces",
    tagName: "seg",
    attributeName: "type",
    attributeValue: "brace",
    attributes: [
      {
        name: "text",
        label: "Text",
        message: "<b>Text</b> to be associated with the lines",
        type: "text",
      },
      {
        name: "rend",
        label: "Rend",
        message: ", indication of how the brace is <b>rend</b>ered on the page",
        type: "text",
        options: ["curly bracket", "C-shaped", "line", "L-shaped"],
      },
      {
        name: "target",
        label: "Target",
        message:
          ", and <b>target</b> id to be used to link the brace and the note (<i>e.g.</i> note_01)",
        type: "text",
      },
    ],
  },
  {
    name: "Paraphrase",
    type: "w",
    section: "annotation",
    help: "Wrap text that has been paraphrased",
    link: "#Paraphrasing",
    tagName: "quote",
    attributes: [
      {
        name: "resp",
        label: "Author",
        message: "<b>Person responsible</b> for the paraphrased text",
        type: "text",
      },
    ],
  },
  {
    name: "Highlight",
    type: "w",
    section: "annotation",
    help: "Wrap a word or phrase to mark it as graphically distinct from the surrounding text.",
    link: "#Indentations.2C_Superscripts.2C_and_Subscripts",
    tagName: "hi",
    attribute: "rend",
    menu: [
      "subscript",
      "superscript",
      "underscore",
      "center",
      "indent",
      "indent1",
      "indent2",
      "indent3",
      "indent4",
    ],
  },
  {
    name: "Abbreviation",
    type: "w",
    section: "editorial",
    help: "Wrap abbreviation",
    link: "#Abbreviations_and_Expansions",
    tagName: "abbr",
    attributes: [
      {
        name: "type",
        label: "Type",
        type: "text",
        message: "<b>Type</b> of abbreviation",
        options: ["title", "initial", "acronym"],
      },
    ],
  },
  {
    name: "Addition",
    type: "w",
    section: "editorial",
    help: "Wrap text inserted in the source text",
    link: "#Additions.2C_Deletions.2C_Substitutions.2C_and_Restorations",
    tagName: "add",
    attributes: [
      {
        name: "place",
        label: "Place",
        type: "text",
        message:
          "<b>Place</b> where the addition is located with reference to the main text",
        options: ["above", "below"],
      },
    ],
  },
  {
    name: "Deletion",
    type: "w",
    section: "editorial",
    help: "Wrap text deleted, marked as deleted, or otherwise indicated as superfluous.",
    link: "#Additions.2C_Deletions.2C_Substitutions.2C_and_Restorations",
    tagName: "del",
    attributes: [
      {
        name: "rend",
        label: "Rend",
        type: "text",
        message: "How the deletion is <b>rend</b>ered on the page",
        options: ["overstrike"],
      },
    ],
  },
  {
    name: "Elision",
    type: "w",
    section: "editorial",
    help: "Wrap elided word.",
    link: "#Elisions",
    tagName: "w",
    attributeName: "type",
    attributeValue: "elision",
    attributes: [
      {
        name: "lemma",
        label: "Lemma",
        message:
          "The <b>lemma</b> (<i>i.e.</i> non-elided version of the word)",
        type: "text",
      },
      {
        name: "join",
        label: "Join",
        type: "choice",
        message:
          ", or the side on which the word should be <b>join</b> another",
        options: ["left", "right"],
      },
    ],
  },
  {
    name: "Expansion",
    type: "w",
    section: "editorial",
    help: "Wrap text that has been expanded from an abbreviation.",
    link: "#Abbreviations_and_Expansions",
    tagName: "expan",
  },
  {
    name: "Hyphenation",
    type: "w",
    section: "editorial",
    help: "Wrap a hyphen and indicate its type/function.",
    link: "#Hyphenation",
    tagName: "pc",
    attributes: [
      {
        name: "force",
        label: "Force",
        type: "choice",
        message:
          "<b>Force</b> of the association: <b>strong</b> for hyphen that should be preserved during tokenisation, <b>weak</b> for hyphen that should not be kept, <i>e.g.</i> split words at the end of lines",
        options: ["weak", "strong"],
      },
    ],
  },
  {
    name: "Omission/Gap",
    type: "sc",
    section: "editorial",
    help: "Mark a gap or omission in the transcription.",
    link: "#Omissions",
    tagName: "gap",
    attributes: [
      {
        name: "reason",
        label: "Reason",
        type: "text",
        message:
          "<b>Reason</b> for the omission/gap, including type of content omitted",
        options: ["damage", "script", "ink", "image"],
      },
      {
        name: "extent",
        label: "Extent",
        message: ", <b>extent</b> of the gap, <i>e.g.</i> 1 word, 3 paragraphs",
        type: "text",
      },
    ],
  },
  {
    name: "Supplied",
    type: "w",
    section: "editorial",
    help: "Wrap text supplied by the transcriber",
    link: "#Supplied_Text",
    tagName: "supplied",
    attributes: [
      {
        name: "reason",
        label: "Reason",
        message: "<b>Reason</b> why the text had to be supplied",
        type: "text",
        options: ["damage", "script", "ink", "image"],
      },
    ],
  },
  {
    name: "Unclear",
    type: "w",
    section: "editorial",
    help: "Wrap text that cannot be transcribed with certainty.",
    link: "#Unclear_Text",
    tagName: "unclear",
    attributes: [
      {
        name: "reason",
        label: "Reason",
        message: "<b>Reason</b> why the material is hard to transcribe",
        type: "text",
        options: ["damage", "script", "ink", "image"],
      },
    ],
  },
  {
    name: "Blank space",
    type: "sc",
    section: "other",
    help: "Mark <b>unusual space</b> in the source text.",
    link: "#Blank_Space",
    tagName: "space",
    attributes: [
      {
        name: "extent",
        label: "Extent",
        message:
          "Description of the <b>extent</b> of the blank, <i>e.g.</i> 7 words",
        type: "text",
      },
    ],
  },
  {
    name: "Columns Layout",
    type: "w",
    section: "other",
    help: "Wraps a section of text that is laid out as columns. The columns themselves must be tagged individually.",
    link: "#Columns",
    tagName: "layout",
    attributes: [
      {
        name: "columns",
        label: "Columns",
        message:
          "<b>Number of columns</b> in which the selected section is divided.",
        type: "text",
      },
    ],
  },
  {
    name: "Column",
    type: "w",
    section: "other",
    help: "Wraps a column of text. Must be inside a <b>Columns Layout</b> tag.",
    link: "#Columns",
    tagName: "ab",
    attributeName: "type",
    attributeValue: "column",
    attributes: [
      {
        name: "n",
        label: "Number",
        message:
          "<b>Number of the column</b> on the page, <i>e.g.</i> 1, 2, etc",
        type: "text",
      },
    ],
  },
  {
    name: "Named entity",
    type: "w",
    section: "other",
    help: "Wrap text that refers to a person, place, room, etc.",
    link: "#Named_Entities_.28Persons.2FLocations.2FOrganizations.29",
    tagName: "rs",
    attributes: [
      {
        name: "type",
        label: "Type",
        type: "text",
        message: "<b>Type</b> of entity",
        options: ["object", "organization", "person", "place", "locus"],
      },
      {
        name: "key",
        label: "Key",
        message:
          ", and <b>key</b> to an externally-defined means of identifying the entity, <i>e.g.</i> a database UUID",
        type: "text",
      },
    ],
  },
  {
    name: "Leader",
    type: "sc",
    section: "other",
    help: "Typographical mark used to connect items on the page that might be separated by considerable horizontal distance.",
    link: "#Leaders",
    tagName: "metamark",
    attributeName: "function",
    attributeValue: "leader",
    attributes: [
      {
        name: "rend",
        label: "Rend",
        type: "text",
        message: "How the leader is <b>rend</b>ered on the page",
        options: ["dots", "line", "dashes", "none"],
      },
    ],
  },
];