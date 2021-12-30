function config_editor_init() {
  $.ajax({
      method: "GET",
      xhrFields: { withCredentials: true },
      crossDomain: true,
      headers: { 'X-CSRFToken': get_cookie("csrftoken") },
      url: `${api_endpoint}/configs/`
  }).done(function(data, textStatus, jqXHR) {
      $('#config-tree').bstreeview({data: data});
      const container = document.getElementById("config-editor-panel");
      cnf_editor_changed = false;
      cnf_editor_filename = null;
      cnf_editor_path = null;
      editor = new JSONEditor(container, {
        onChange: function() {cnf_editor_changed = true},
        onError: function(error) {toastr.error(error)},
        onModeChange: function(newMode, oldMode) {expand_tree(newMode)},
        escapeUnicode: false,
        sortObjectKeys: false,
        limitDragging: true,
        history: true,
        mode: 'tree',
        modes: ['tree', 'form', 'code'],
        indentation: 4,
        mainMenuBar: true,
        navigationBar: true,
        statusBar: true,
        enableSort: false,
        enableTransform: false,
      });

  }).fail(function(jqXHR, textStatus, errorThrown) {
      toastr.error(`There was an error communicating with the server: ${errorThrown}`);
  });
}

function load_config_file(path, filename) {
  $.ajax({
    method: "POST",
    url: `${api_endpoint}/configs/get/`,
    xhrFields: { withCredentials: true },
    crossDomain: true,
    headers: {
      "Content-Type": "application/json",
      'X-CSRFToken': get_cookie("csrftoken")
    },
    data: JSON.stringify({
      'target': filename,
      'path': path
    })
  }).done(function(data, textStatus, jqXHR) {
      cnf_editor_filename = filename;
      cnf_editor_path = path;
      cnf_editor_changed = false;

      editor.set(data[0]);
      expand_tree(editor.getMode());

      let pre = path.length > 0 ? `${path}\\` : '';
      $('.config-editor-title').text(`Editing ${pre}${filename}.json`)

  }).fail(function(jqXHR, textStatus, errorThrown) {
      toastr.error(`There was an error communicating with the server: ${errorThrown}`);
  });
}

function expand_tree(mode) {
  if (['tree', 'view', 'form'].includes(mode)) {
    editor.expandAll();
  };
}

function save_config_file() {
    editor.validate().then(function(results) {
      if (results.length) {
        for (let i = 0, len = results.length; i < len; ++i) {
          toastr.error(
            results[i].message
              .replaceAll('&', '&amp;')
              .replaceAll('<', '&lt;')
              .replaceAll('>', '&gt;')
              .replaceAll('"', '&quot;')
              .replaceAll("'", '&#039;'),
            '',
            {
              closeButton: true,
              timeOut: 0,
              extendedTimeOut: 0,
              progressBar: false,
            }
          );
        }
      } else {
        $.ajax({
          method: "POST",
          url: `${api_endpoint}/configs/save/`,
          xhrFields: { withCredentials: true },
          crossDomain: true,
          headers: {
            "Content-Type": "application/json",
            'X-CSRFToken': get_cookie("csrftoken")
          },
          data: JSON.stringify({
            'target': cnf_editor_filename,
            'path': cnf_editor_path,
            'payload': editor.get()
          })
        }).done(function(data, textStatus, jqXHR) {
            toastr.success('Configuration file saved succesfully.');
            cnf_editor_changed = false;
        }).fail(function(jqXHR, textStatus, errorThrown) {
            toastr.error(`There was an error communicating with the server: ${errorThrown}`);
        });
      }
    });
}
