const setExtent = (e) => {
  const tagName = e.tagName.slice(4);
  const reason = e.getAttribute("reason", false);

  let quantity = parseInt(e.getAttribute("quantity", "nope"));
  let unit = e.getAttribute("unit", null);
  let extent = e.getAttribute("extent", null);

  const fillers = {
    word: "___ ",
    char: "* ",
  };

  if (extent && !quantity && !unit) {
    let eTokens = extent.split(" ");
    if (eTokens.length === 2) {
      if (!isNaN(parseInt(eTokens[0]))) {
        quantity = parseInt(eTokens[0]);
      } else if (eTokens[0] === "full") {
        quantity = 1;
      } else if (eTokens[0].includes("-")) {
        let range = eTokens[0].split("-");
        quantity = Math.max(range);
      }
      unit = eTokens[1];
    }
  }

  if (unit && extent) {
    let content = "";
    let title = "";
    if (unit.startsWith("word") || unit.startsWith("char")) {
      if (quantity) {
        content = fillers[unit.slice(0, 4)].repeat(quantity).trim();
        title = `${quantity} missing ${unit}`;
        if (reason) title += ` (${reason})`;
      } else {
        content = extent;
        title = extent;
      }
      e.innerHTML = `[ ${content} ]`;
      let tooltip = document.createElement("div");
      // tooltip.setAttribute("title", title);
      tooltip.innerText = title;
      tooltip.setAttribute("class", "tei-tooltip");
      tooltip.setAttribute("data-toggle", "tooltip");
      e.appendChild(tooltip);
      console.log("added tooltip");
    } else if (unit.startsWith("line") || unit.startsWith("page")) {
      if (quantity) {
        let qual = tagName === "SPACE" ? " blank " : " ";
        content = reason ? `${quantity} ${unit} (${reason})` : `${quantity}${qual}${unit}`;
      } else {
        content = extent;
      }
      e.innerHTML = content;
      e.setAttribute("show", "block");
    }
  } else if (extent) {
    e.innerHTML = `[ ${extent} ]`;
  }

  return e;
};

const setTitle = (e) => {
  const tagName = e.tagName.slice(4);
  const reason = e.getAttribute("reason", false);
  const type = e.getAttribute("type", false);
  const lemma = e.getAttribute("lemma", false);
  const resp = e.getAttribute("resp", false);
  const titleStrings = {
    ADD: "addition",
    ABBR: `expanded ${e.getAttribute("type", "abbreviation")}`,
  };

  let tooltip = document.createElement("div");

  if (reason) {
    tooltip.innerText = `${tagName.toLowerCase()} (${reason})`;
  } else if (type && lemma) {
    tooltip.innerText = `${type} (${lemma})`;
  } else if (resp) {
    tooltip.innerText = `by ${resp}`;
  } else if (tagName in titleStrings) {
    tooltip.innerText = titleStrings[tagName];
  } else {
    tooltip.innerText = `${tagName.toLowerCase()}`;
  }

  tooltip.setAttribute("class", "tei-tooltip");
  tooltip.setAttribute("data-toggle", "tooltip");
  e.appendChild(tooltip);
  console.log("added tooltip");
  return e;
};

export const idaTeiBehaviours = {
  tei: {
    ab: [
      [
        "[type=column]",
        (e) => {
          const colNum = e.getAttribute("n");
          const content = document.createElement("div");
          content.className = "ab-content";
          content.setAttribute("n", colNum);
          content.innerHTML = e.innerHTML;
          const div = document.createElement("div");
          // eslint-disable-next-line max-len
          div.innerHTML = `<div><span class="label">C${colNum}</span><i class="fa fa-caret-down"></i><i class="fa fa-caret-right"></i></div>`;
          div.className = "ab-column-toggler";
          e.innerHTML = "";
          e.appendChild(div);
          e.appendChild(content);
        },
      ],
    ],
    gap: (e) => {
      setExtent(e);
    },
    space: (e) => {
      setExtent(e);
    },
    unclear: (e) => {
      setTitle(e);
    },
    supplied: (e) => {
      setTitle(e);
    },
    add: (e) => {
      setTitle(e);
    },
    abbr: (e) => {
      setTitle(e);
    },
    w: (e) => {
      setTitle(e);
    },
    quote: (e) => {
      setTitle(e);
    },
    g: (e) => {
      let ref = e.getAttribute("ref", false);
      if (ref) {
        e.innerText = String.fromCharCode(parseInt(ref, 16));
      }
    },
    hi: [
      [
        "[rend=superscript]",
        (e) => {
          if (e.innerText.length > 3) {
            e.setAttribute("rend-basic", 1);
          }
        },
      ],
    ],
    ref: [
      [
        "[target]",
        (e) => {
          let ref_id = e.getAttribute("target");
          if (ref_id.length > 1) {
            if (ref_id.startsWith("#")) {
              ref_id = ref_id.substring(1);
            }
            if (ref_id.startsWith("U-")) {
              ref_id = String.fromCharCode(parseInt(ref_id.substring(2), 16));
            }
          }
          e.innerText = ref_id;
        },
      ],
    ],
    note: [
      [
        "[type=marginal]",
        (e) => {
          e.innerHTML = `<div><i class="fas fa-caret-left"></i><i class="fas fa-sticky-note">\
            </i></div><div class="note_content">${e.innerHTML}</div>`;
        },
      ],
      [
        "[type=brace]",
        (e) => {
          let tooltip = document.createElement("div");
          tooltip.innerHTML = e.innerHTML;
          tooltip.setAttribute("class", "tei-tooltip");
          tooltip.setAttribute("data-toggle", "tooltip");
          tooltip.setAttribute("data-html", "true");
          /* eslint-disable */
          tooltip.setAttribute(
            "data-template",
            '<div class="tooltip note" role="tooltip"><div class="arrow"></div><div class="tooltip-inner"></div></div>'
          );
          e.innerHTML = '<i class="fas fa-sticky-note"></i>';
          e.appendChild(tooltip);
          /* eslint-enable */
        },
      ],
      [
        ":not([type]), [type=renvoi]",
        (e) => {
          e.setAttribute("class", "u-none");
        },
      ],
    ],
  },
};
