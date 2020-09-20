function language_forms_load() {
}

function language_forms_init() {

}

function change_form(e, mode, action) {
  if (e.type == 'open') {
    if (action == 'edit') {
      let editor_fields = dt_editor.order()
      let populated_list = []
      for (let i = 0, len = editor_fields.length; i < len; ++i) {
        if (dt_editor.field(editor_fields[i]).val() != '') {
          populated_list.push(editor_fields[i])
        }
      }
      toggle_fields(populated_list);
      dt_editor.field('type.id').input().on('change.dalme', change_on_type);
    }
    if (action == 'create') {
      toggle_fields(required_list);
      dt_editor.field('type.id').input().on('change.dalme', change_on_type);
    }
  } else if (e.type == 'close') {
      $(dt_editor.field('type.id').node()).find('input').off('change.dalme');
  }
}


function change_on_type() {
  if (dt_editor.field('type.id').val() == "2") {
    toggle_fields('parent.id', 'show');
  } else {
    toggle_fields('parent.id', 'hide');
  }
}
