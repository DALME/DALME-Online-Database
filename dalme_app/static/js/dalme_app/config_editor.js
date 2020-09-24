function config_editor_load() {
  $.ajax({
      method: "GET",
      url: "/api/configs/"
  }).done(function(data, textStatus, jqXHR) {
      $('#config-tree').bstreeview({
        data: data,
      });
  });
}
