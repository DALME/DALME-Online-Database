if (typeof(window.reference_dialogue) == "undefined") {
  window.reference_dialogue = function (target, entityId) {
    const selector = $(target).select2({
      placeholder: "Type to search bibliography...",
      width: "100%",
      dropdownParent: $(".modal"),
      ajax: {
        url: `${window.APIURL}/library/`,
        datatype: "json",
        delay: 500,
        processResults: function (data) {
          return {results: data.map((entry) => {
            const citation = new window.cite(entry);
            return {
              id: entry.id.split("/")[1],
              text: citation.format("citation", { format: "text", template: "apa", lang: "en-US" }),
              html: $(citation.format("bibliography", { format: "html", template: "apa", lang: "en-US" })),
            };
          })};
        },
        data: function (params) {
          return {
            search: params.term,
            limit: 10,
            content: "csljson",
            format: "json"
          }
        }
      },
      templateResult: (entry) => entry.html,
    });

    if (entityId) {
      fetch(`${window.APIURL}/library/${entityId}/?content=csljson&format=json`)
        .then(response => response.json())
        .then(data => {
          const citation = new window.cite(data[0]);
          const option = new Option(
            citation.format("citation", { format: "text", template: "apa", lang: "en-US" }),
            data[0].id.split("/")[1],
            true,
            true,
          );
          selector.append(option).trigger("change");
        });
    }
    return selector;
  };
}
