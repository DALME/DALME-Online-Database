/* eslint-disable unused-imports/no-unused-vars */
// eslint-disable-next-line no-undef
const cite_app = new Vue({
  el: "#cite-container",
  delimiters: ["${", "}"],
  directives: {
    onClickaway: window.VueClickaway.directive,
  },
  created() {
    const Cite = require("citation-js");
    this.styles = this.citationData[0];
    this.config = Cite.plugins.config.get("@csl");
    this.loadTemplates().then(() => {
      this.citation = new Cite(this.citationData[1]);
      setTimeout(() => this.template = "chicago_16", 100);
    });
  },
  data: function() {
return {
    showCitePanel: false,
    showCopied: false,
    popoverPlacement: "right",
    format: "html",
    template: "apa",
    output_format: "bibliography",
    lang: "en-US",
    citation: null,
    config: null,
    styles: null
  };
},
  computed: {
    citationData() {
      const node = document.getElementById("citation_data");
      document.getElementsByTagName("BODY")[0].removeChild(node);
      return JSON.parse(node.textContent);
    },
    formatted_citation() {
      return this.citation.format(this.output_format, {
        format: this.format,
        template: this.template,
        lang: this.lang
      });
    }
  },
  methods: {
    async loadTemplates() {
      const that = this;
      await Promise.all(this.styles.map(style => {
        if (style.file) {
          var xhttp = new XMLHttpRequest();
          xhttp.onreadystatechange = function () {
            if (xhttp.readyState == 4 && xhttp.status == 200 && xhttp.responseXML !== null) {
              let xml_data = new XMLSerializer().serializeToString(xhttp.responseXML);
              that.config.templates.add(style.name, xml_data);
            }
          };
          xhttp.open("GET", `/static/web/citation_styles/${style.file}`, true);
          xhttp.send();
        }
      }));
    },
    downloadCitation(format) {
      const blob = new Blob([this.citation.format(this.output_format, {
        format: "text",
        template: this.template,
        lang: this.lang
      })], {
        encoding: "UTF-8",
        type: "text/plain;charset=UTF-8"
      });
      const link = document.createElement("a");
      link.href = URL.createObjectURL(blob);
      link.download = format == "bibtex" ? "citation.bib" : "citation.ris";
      link.click();
      URL.revokeObjectURL(link.href);
    },
    showCopiedTooltip() {
      this.showCitePanel = false;
      this.showCopied = true;
      setTimeout(() => this.showCopied = false, 800);
    },
    closeCitePanel() {
      this.showCitePanel = false;
    },
  }
});
