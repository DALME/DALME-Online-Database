function set_form() {
  $(document).ready(function () {
    dt_editor.on('open.dalme', function(e, mode, action) { change_set_form(e, action) });
    dt_editor.on('submitSuccess.dalme', function(e, json, data, action) { location.reload(); });
  });
}

function change_set_form(e, action) {
  if (e.type == 'open') {
    if (action == 'edit') {
      change_on_set_type();
      dt_editor.field('set_type.value').input().on('change.dalme', change_on_set_type);
    } else if (action == 'create') {
      dt_editor.hide(['is_public', 'has_landing', 'dataset_usergroup.id', 'owner.id']);
      dt_editor.field('set_type.value').input().on('change.dalme', change_on_set_type);
    }
  } else if (e.type == 'close') {
    dt_editor.field('set_type.value').input().off('change.dalme');
  }
}

function change_on_set_type(callback='undefined') {
  var stype = dt_editor.get('set_type.value');
  dt_editor.hide(['is_public', 'has_landing', 'dataset_usergroup.id']);
  if (stype == "2") {
    dt_editor.show(['is_public', 'has_landing']);
  } else if (stype == "3") {
    dt_editor.show('dataset_usergroup.id');
  }
}
