var easy_read = {
  elements: {
    "front":{
      title:"contains any prefatory matter (headers, abstracts, title page, prefaces, dedications, etc) found at the start of a document, before the main body",
    },
    "body":{
      title:"contains the whole body of a single unitary text, excluding any front or back matter",
    },
    "back":{
      title:"contains any appendixes, etc. following the main part of a text"
    },
    "pb":{
      oneliner: true,
      collapsed: true,
      isReadOnly: true,
      title:"page break element used to denote the beginning of a folio. It should always mark the beginning of the text",
      attributes:{
        "n": {
          title:"used to state the page number or folio designation",
        },
        "facs": {
          title:"points to all or part of an image which corresponds with the content of the element. In this case the value should be a valid DALME DAM Resource ID",
        },
      }
    },
    "p":{
      title:"marks paragraphs in prose",
      hasText: true,
      isReadOnly: true,
    },
    "supplied":{
      title: "text supplied by the transcriber or editor for any reason; for example because the original cannot be read due to physical damage, or because of an obvious omission by the author or scribe",
      hasText: true,
      oneliner: true,
      collapsed: true,
      isReadOnly: true,
      attributes: {
        "reason": {
          title:"one or more words indicating why the text has had to be supplied",
        },
      }
    },
    "date":{
      title:"contains a date in any format",
      hasText: true,
      oneliner: true,
      collapsed: true,
      isReadOnly: true,
      attributes: {
        "when": {
          title:"supplies the value of the date or time in a standard form, eg yyyy-mm-dd",
        },
      }
    },
    "hi":{
      title:"marks a word or phrase as graphically distinct from the surrounding text",
      hasText: true,
      oneliner: true,
      collapsed: true,
      isReadOnly: true,
      attributes: {
        "rend": {
          title:"indicates how enclosed content should be rendered",
        }
      },
    },
    "del":{
      title:"contains a letter, word, or passage deleted, marked as deleted, or otherwise indicated as superfluous or spurious in the copy text by an author, scribe, or a previous annotator or corrector",
      hasText: true,
      oneliner: true,
      collapsed: true,
      isReadOnly: true,
      attributes: {
        "rend": {
          title:"indicates how enclosed content should be rendered",
        }
      },
    },
    "rs":{
      title:"contains a general purpose name or referring string",
      attributes: {
        "type": {
          title:"characterizes the element in some sense, using any convenient classification scheme or typology",
        },
        "subtype":{
          title:"provides a sub-categorization of the element, if needed",
        },
        "key":{
          title:"provides an externally-defined means of identifying the entity (or entities) being named, using a coded value of some kind",
        },
        "ref":{
          title:"provides an explicit means of locating a full definition or identity for the entity being named by means of one or more URIs",
        }
      },
      hasText: true,
      oneliner: true,
      collapsed: true,
      isReadOnly: true,
    },
    "unclear":{
      title:"contains a word, phrase, or passage which cannot be transcribed with certainty because it is illegible in the source",
      hasText: true,
      oneliner: true,
      collapsed: true,
      isReadOnly: true,
      attributes: {
        "reason": {
          title:"indicates why the material is hard to transcribe",
        },
      }
    },
    "gap":{
      title:"indicates a point where material has been omitted in a transcription, whether for editorial reasons described in the TEI header, as part of sampling practice, or because the material is illegible, invisible, or inaudible",
      oneliner: true,
      collapsed: true,
      isReadOnly: true,
      attributes: {
        "reason": {
          title:"gives the reason for omission",
        },
        "unit":{
          title:"unit used to measure the gap, e.g. words, or lines",
        },
        "quantity": {
          title:"number of units represented in the gap",
        },
        "extent": {
          title:"a description of the gap's extents",
        }
      },
    },
    "list":{
      title:"used to mark any kind of list: numbered, lettered, bulleted, or unmarked",
      hasText: true,
      isReadOnly: true,
      attributes: {
        "type": {
          title:"can be used to indicate the type of list, eg inventory, immobilia",
        },
        "rend":{
          title:"indicates how the list should be rendered, default is itemized",
        }
      },
    },
    "item":{
      title:"contains one component of a list",
      hasText: true,
      isReadOnly: true,
    },
    "num":{
      title:"contains a number, written in any form",
      hasText: true,
      oneliner: true,
      collapsed: true,
      isReadOnly: true,
      attributes: {
        "type": {
          title:"indicates the type of numeric value",
        },
        "value":{
          title:"supplies the value of the number in standard form",
        },
        "atLeast":{
          title:"gives a minimum estimated value for the approximate number",
        },
        "atMost":{
          title:"gives a maximum estimated value for the approximate number",
        }
      },
    },
    "measure":{
      title:"contains a word or phrase referring to some quantity of an object or commodity, usually comprising a number, a unit, and a commodity name",
      hasText: true,
      oneliner: true,
      collapsed: true,
      isReadOnly: true,
      attributes: {
        "type": {
          title:"specifies the type of measurement in any convenient typology",
        },
        "quantity": {
          title:"specifies the number of the specified units that comprise the measurement",
        },
        "unit": {
          title:"indicates the units used for the measurement, usually using the standard symbol for the desired units",
        },
        "commodity": {
          title:"indicates the substance that is being measured",
        },
      }
    },
    "pc":{
      title:"contains a character or string of characters regarded as constituting a single punctuation mark. Used to indicate hyphenation",
      hasText: true,
      oneliner: true,
      collapsed: true,
      isReadOnly: true,
      attributes: {
        "force": {
          title:"indicates the strength of the association between the punctuation mark and its adjacent word. Use the value strong to mark a hyphen that should be preserved during the tokenisation process, and weak for hyphens that should not be kept, e.g. split words at the end of lines",
        }
      }
    },
    "lb":{
      title:"marks the beginning of a new (typographic) line",
      hasText: false,
      oneliner: true,
      collapsed: true,
      isReadOnly: true,
    },
  }
};

var quick_edit = {
  elements: {
    "pb":{

    },
    "p":{
      hasText: true,
    },
    "supplied":{
      title: "text supplied by the transcriber or editor for any reason; for example because the original cannot be read due to physical damage, or because of an obvious omission by the author or scribe",
      hasText: true,
      oneliner: true,
      collapsed: true,
    },
    "date":{
      hasText: true,
      collapsible: false,
    },
    "hi":{
      hasText: true,
      collapsible: false
    },
    "del":{
      hasText: true,
      collapsible: false
    },
    "rs":{
      attributes: {
        "type": {
          asker: Xonomy.askPicklist,
          askerParameter: ["person", "place", "object"]
        }
      },
      hasText: true,
      collapsible: false
    },
    "unclear":{
      hasText: true,
      collapsible: false
    },
    "gap":{
      hasText: true,
      collapsible: false
    },
    "list":{
      hasText: true,
      collapsible: false
    },
    "item":{
      hasText: true,
      collapsible: false
    },
    "num":{
      hasText: true,
      collapsible: false
    },
    "measure":{
      hasText: true,
      collapsible: false
    },
    "pc":{
      hasText: true,
      collapsible: false
    },
    "lb":{
      hasText: false,
      collapsible: false,
      oneliner: false
    },
  }
};

var full_edit = {
  elements: {
    "front":{
      title:"contains any prefatory matter (headers, abstracts, title page, prefaces, dedications, etc) found at the start of a document, before the main body",
    },
    "body":{
      title:"contains the whole body of a single unitary text, excluding any front or back matter",
    },
    "back":{
      title:"contains any appendixes, etc. following the main part of a text"
    },
    "pb":{
      title:"page break element used to denote the beginning of a folio. It should always mark the beginning of the text",
      attributes:{
        "n": {
          title:"used to state the page number or folio designation",
          asker: Xonomy.askString,
        },
        "facs": {
          title:"points to all or part of an image which corresponds with the content of the element. In this case the value should be a valid DALME DAM Resource ID",
          asker: Xonomy.askString,
        },
      }
    },
    "p":{
      title:"marks paragraphs in prose",
      hasText: true,
      inlineMenu: [{
        caption: "mark as <supplied>",
        action: Xonomy.wrap,
        actionParameter: {template: "<supplied>$</supplied>", placeholder: "$"}
        },
        {
        caption: "mark as <unclear>",
        action: Xonomy.wrap,
        actionParameter: {template: "<unclear>$</unclear>", placeholder: "$"}
        },
        {
        caption: "mark as <item>",
        action: Xonomy.wrap,
        actionParameter: {template: "<item>$</item>", placeholder: "$"}
        }
      ]
    },
    "supplied":{
      title: "text supplied by the transcriber or editor for any reason; for example because the original cannot be read due to physical damage, or because of an obvious omission by the author or scribe",
      hasText: true,
      oneliner: true,
      attributes: {
        "reason": {
          title:"one or more words indicating why the text has had to be supplied",
          asker: Xonomy.askOpenPicklist,
          askerParameter: ["overbinding", "faded-ink", "lost-folio", "omitted-in-original"]
        },
      }
    },
    "date":{
      title:"contains a date in any format",
      hasText: true,
      attributes: {
        "when": {
          title:"supplies the value of the date or time in a standard form, eg yyyy-mm-dd",
          asker: Xonomy.askString,
        },
      }
    },
    "hi":{
      title:"marks a word or phrase as graphically distinct from the surrounding text",
      hasText: true,
      attributes: {
        "rend": {
          title:"indicates how enclosed content should be rendered",
          asker: Xonomy.askOpenPicklist,
          askerParameter: ["superscript", "subscript"]
        }
      },
    },
    "del":{
      title:"contains a letter, word, or passage deleted, marked as deleted, or otherwise indicated as superfluous or spurious in the copy text by an author, scribe, or a previous annotator or corrector",
      hasText: true,
      attributes: {
        "rend": {
          title:"indicates how enclosed content should be rendered",
          asker: Xonomy.askOpenPicklist,
          askerParameter: ["overstrike"]
        }
      },
    },
    "rs":{
      title:"contains a general purpose name or referring string",
      attributes: {
        "type": {
          title:"characterizes the element in some sense, using any convenient classification scheme or typology",
          asker: Xonomy.askOpenPicklist,
          askerParameter: ["person", "place", "object"]
        },
        "subtype":{
          title:"provides a sub-categorization of the element, if needed",
          asker: Xonomy.askString,
        },
        "key":{
          title:"provides an externally-defined means of identifying the entity (or entities) being named, using a coded value of some kind",
          asker: Xonomy.askString,
        },
        "ref":{
          title:"provides an explicit means of locating a full definition or identity for the entity being named by means of one or more URIs",
          asker: Xonomy.askString,
        }
      },
      hasText: true,
    },
    "unclear":{
      title:"contains a word, phrase, or passage which cannot be transcribed with certainty because it is illegible in the source",
      hasText: true,
      attributes: {
        "reason": {
          title:"indicates why the material is hard to transcribe",
          asker: Xonomy.askOpenPicklist,
          askerParameter: ["damage", "illegible","ink-blot"]
        },
      }
    },
    "gap":{
      title:"indicates a point where material has been omitted in a transcription, whether for editorial reasons described in the TEI header, as part of sampling practice, or because the material is illegible, invisible, or inaudible",
      hasText: true,
      attributes: {
        "reason": {
          title:"gives the reason for omission",
          asker: Xonomy.askOpenPicklist,
          askerParameter: ["damage", "illegible"]
        },
        "unit":{
          title:"unit used to measure the gap, e.g. words, or lines",
          asker: Xonomy.askOpenPicklist,
          askerParameter: ["letters","words","lines"]
        },
        "quantity": {
          title:"number of units represented in the gap",
          asker: Xonomy.askString,
        },
        "extent": {
          title:"a description of the gap's extents",
          asker: Xonomy.askLongString,
        }
      },
    },
    "list":{
      title:"used to mark any kind of list: numbered, lettered, bulleted, or unmarked",
      hasText: true,
      attributes: {
        "type": {
          title:"can be used to indicate the type of list, eg inventory, immobilia",
          asker: Xonomy.askOpenPicklist,
          askerParameter: ["inventory", "immobilia"]
        },
        "rend":{
          title:"indicates how the list should be rendered, default is itemized",
          asker: Xonomy.askOpenPicklist,
          askerParameter: ["inline"]
        }
      },
    },
    "item":{
      title:"contains one component of a list",
      hasText: true,
    },
    "num":{
      title:"contains a number, written in any form",
      hasText: true,
      attributes: {
        "type": {
          title:"indicates the type of numeric value",
          asker: Xonomy.askPicklist,
          askerParameter: ["cardinal", "ordinal", "fraction", "percentage"]
        },
        "value":{
          title:"supplies the value of the number in standard form",
          asker: Xonomy.askString,
        },
        "atLeast":{
          title:"gives a minimum estimated value for the approximate number",
          asker: Xonomy.askString,
        },
        "atMost":{
          title:"gives a maximum estimated value for the approximate number",
          asker: Xonomy.askString,
        }
      },
    },
    "measure":{
      title:"contains a word or phrase referring to some quantity of an object or commodity, usually comprising a number, a unit, and a commodity name",
      hasText: true,
      attributes: {
        "type": {
          title:"specifies the type of measurement in any convenient typology",
          asker: Xonomy.askOpenPicklist,
          askerParameter: ["volume", "weight", "currency", "other"]
        },
        "quantity": {
          title:"specifies the number of the specified units that comprise the measurement",
          asker: Xonomy.askString,
        },
        "unit": {
          title:"indicates the units used for the measurement, usually using the standard symbol for the desired units",
          asker: Xonomy.askString,
        },
        "commodity": {
          title:"indicates the substance that is being measured",
          asker: Xonomy.askString,
        },
      }
    },
    "pc":{
      title:"contains a character or string of characters regarded as constituting a single punctuation mark. Used to indicate hyphenation",
      hasText: true,
      attributes: {
        "force": {
          title:"indicates the strength of the association between the punctuation mark and its adjacent word. Use the value strong to mark a hyphen that should be preserved during the tokenisation process, and weak for hyphens that should not be kept, e.g. split words at the end of lines",
          asker: Xonomy.askPicklist,
          askerParameter: ["strong", "weak"]
        }
      }
    },
    "lb":{
      title:"marks the beginning of a new (typographic) line",
      hasText: false,
    },
  }
};
