function set_forms_load() {
}

function set_forms_init() {
}

function open_sets_form(e, action) {
  if (action == 'edit') {
    let editor_fields = dt_editor.order()
    let populated_list = []

    for (let i = 0, len = editor_fields.length; i < len; ++i) {
      if (dt_editor.field(editor_fields[i]).val() != '') {
        populated_list.push(editor_fields[i])
      }
    }

    toggle_fields(populated_list);


    change_on_set_type();
    dt_editor.field('set_type.value').input().on('change.dalme', change_on_set_type);

  } else if (action == 'create') {
    toggle_fields(required_list);
    dt_editor.hide(['is_public', 'has_landing', 'dataset_usergroup.id', 'owner.id']);
    dt_editor.field('set_type.value').input().on('change.dalme', change_on_set_type);

  }
}

function close_set_forms(e) {
  dt_editor.field('set_type.value').input().off('change.dalme');
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
