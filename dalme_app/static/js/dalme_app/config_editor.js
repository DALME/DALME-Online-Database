function config_editor_load() {
  $.ajax({
      method: "GET",
      xhrFields: { withCredentials: true },
      crossDomain: true,
      headers: { 'X-CSRFToken': get_cookie("csrftoken") },
      url: `${api_endpoint}/configs/`
  }).done(function(data, textStatus, jqXHR) {
      $('#config-tree').bstreeview({
        data: data,
      });
  });
}
