function setExtent(e) {
  const tag_name = e.tagName.slice(4,);
  const reason = e.getAttribute('reason', false);
  var quantity = parseInt(e.getAttribute('quantity', 'nope'));
  var unit = e.getAttribute('unit', null);
  var extent = e.getAttribute('extent', null);
  const fillers = {
    word: '___ ',
    char: '* ',
  }
  if (extent && !quantity && !unit) {
    let e_tokens = extent.split(' ');
    if (e_tokens.length == 2) {
      if (parseInt(e_tokens[0]) !== NaN) {
        quantity = parseInt(e_tokens[0]);
      } else if (e_tokens[0] == 'full') {
        quantity = 1;
      } else if (e_tokens[0].includes('-')) {
        let range = e_tokens[0].split('-');
        quantity = Math.max(range);
      }
      unit = e_tokens[1];
    }
  }
  if (unit && extent) {
    var content = '';
    var title = '';
    if (unit.startsWith('word') || unit.startsWith('char')) {
      if (quantity) {
        content = fillers[unit.slice(0,4)].repeat(quantity).trim();
        title = `${quantity} missing ${unit}`;
        if (reason) title += ` (${reason})`;
      } else {
        content = extent;
        title = extent;
      }
      e.innerHTML = `[ ${content} ]`;
      e.setAttribute('title', title);
      e.setAttribute('data-toggle', 'tooltip');
    } else if (unit.startsWith('line') || unit.startsWith('page')) {
      if (quantity) {
        let qual = tag_name == 'SPACE' ? ' blank ' : ' ';
        content = reason ? `${quantity} ${unit} (${reason})` : `${quantity}${qual}${unit}`;
      } else {
        content = extent;
      }
      e.innerHTML = content;
      e.setAttribute('show', 'block');
    }
  } else if (extent) {
    e.innerHTML = `[ ${extent} ]`;
  }
  return e
}

function setTitle(e) {
  const tag_name = e.tagName.slice(4,);
  const reason = e.getAttribute('reason', false);
  const type = e.getAttribute('type', false);
  const lemma = e.getAttribute('lemma', false);
  const resp = e.getAttribute('resp', false);
  const title_strings = {
    'ADD': 'addition',
    'ABBR': `expanded ${e.getAttribute('type', 'abbreviation')}`,
    'NUM': e.getAttribute('value', 'number'),
    'EXPAN': 'expansion',
  }
  if (reason) {
    e.setAttribute('title', `${tag_name.toLowerCase()} (${reason})`);
  } else if (type && lemma) {
    e.setAttribute('title', `${type} (${lemma})`);
  } else if (resp) {
    e.setAttribute('title', `by ${resp}`);
  } else if (tag_name in title_strings) {
    e.setAttribute('title', title_strings[tag_name]);
  } else if (tag_name == 'RS' && type) {
    e.setAttribute('title', type);
  } else if (tag_name == 'W' && type == 'elision') {
    e.setAttribute('title', 'elision');
  } else {
    e.setAttribute('title', `${tag_name.toLowerCase()}`);
  }
  e.setAttribute('data-toggle', 'tooltip');
  return e
}

const dalmeTeiBehaviours = {
  'tei': {
    'ab': [
      ['[type=column]', function(e) {
         const colNum = e.getAttribute('n');
         const content = document.createElement('div');
         content.className = 'ab-content';
         content.setAttribute('n', colNum);
         content.innerHTML = e.innerHTML;
         const div = document.createElement('div');
         div.innerHTML = `<div><span class="label">C${colNum}</span><i class="fa fa-caret-down"></i><i class="fa fa-caret-right"></i></div>`;
         div.className = 'ab-column-toggler';
         e.innerHTML = '';
         e.appendChild(div);
         e.appendChild(content);
     }],
    ],
    'del': function(e) {
      let rend_att = e.getAttribute('rend', false);
      let content = '';
      if (rend_att) {
        content += `${rend_att}: `
      }
      content += e.innerText;
      e.setAttribute('title', content);
      e.setAttribute('data-toggle', 'tooltip');
    },
    'expan': function(e) { e = setTitle(e); },
    'gap': function(e) { e = setExtent(e); },
    'sic': function(e) { 
      e.setAttribute('title', 'sic');
      e.setAttribute('data-toggle', 'tooltip');
     },
    'handShift': function(e) {
      let content = 'hand shift';
      e.getAttributeNames().forEach((att_name) => {
        if (['scribe', 'medium', 'script'].includes(att_name)) {
          content += ` | ${att_name}: ${e.getAttribute(att_name)}`;
        }
      });
      e.setAttribute('title', content);
      e.setAttribute('data-toggle', 'tooltip');
     },
    'space': function(e) { e = setExtent(e); },
    'unclear': function(e) { e = setTitle(e); },
    'supplied': function(e) { e = setTitle(e); },
    'add': function(e) { e = setTitle(e); },
    'abbr': function(e) { e = setTitle(e); },
    'w': function(e) { e = setTitle(e); },
    'quote': function(e) { e = setTitle(e); },
    'num': function(e) { e = setTitle(e); },
    'g': function(e) {
      let ref = e.getAttribute('ref', false);
      if (ref) e.innerText = String.fromCharCode(parseInt(ref, 16));
    },
    'gloss': function(e) { e.setAttribute('class', 'd-none'); },
    'hi': [
      ['[rend=superscript]', function(e) {
        if (e.innerText.length > 3) {
          e.setAttribute('rend-basic', 1);
        }
      }],
      ['[rend=center], [rend=right]', function(e) {
        const wrapper = document.createElement('div');
        wrapper.style.display = 'inline-block';
        wrapper.innerHTML = e.innerHTML;
        e.innerHTML = '';
        e.appendChild(wrapper);
      }]
    ],
    'ref': [
      [':not([rend]), [rend=footnote]', function(e) {
        let ref_id = e.getAttribute('target');
        if (ref_id.length > 1) {
          if (ref_id.startsWith('#')) {
            ref_id = ref_id.substring(1);
          }
          if (ref_id.startsWith('U-')) {
            ref_id = String.fromCharCode(parseInt(ref_id.substring(2), 16));
          }
        }
        e.innerText = ref_id;
      }]
    ],
    'rs': [
      ['[type]', function(e) { e = setTitle(e); }]
    ],
    'note': [
      ['[type=marginal]', function(e) {
        e.innerHTML = `<div><i class="fas fa-sticky-note"></i></div><div class="note_content">${e.innerHTML}</div>`;
      }],
      ['[type=brace]', function(e) {
        e.setAttribute('title', 'Note');
        e.setAttribute('data-content', e.innerHTML);
        e.setAttribute('data-toggle', 'popover');
        e.setAttribute('data-template', '<div class="popover" role="tooltip"><div class="arrow"></div><div class="popover-header-wrapper"><h3 class="popover-header"></h3><div class="popover-header-closer"></div></div><div class="popover-body"></div></div>');
        e.innerHTML = '<i class="fas fa-sticky-note"></i>';
      }],
      [':not([type]), [type=renvoi], [type=gloss], [type=footnote]', function(e) {
        e.setAttribute('class', 'd-none');
      }]
    ],
  }
};
