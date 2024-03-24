if (typeof(window.cite) == 'undefined') {
  window.cite = require('citation-js');
}

window.format_reference = (data) => {
  const citation = new window.cite(entry);
  const output = document.createElement("div");
  output.dataset.label = citation.format('citation', { format: 'text', template: 'apa', lang: 'en-US' });
  output.innerText = citation.format('bibliography', { format: 'html', template: 'apa', lang: 'en-US' });
  return output;
} 
