function initializeFormHelper() {
  $('#parent_class_select').on('change', updateClass );
}

function updateClass() {
  const value = $('#parent_class_select').children("option:selected").val();
  if (value !=0) {
      dt_table.ajax.url("/api/fields/?format=json&list=" +value).draw();
      $.ajax({
        method: "GET",
        url: "/api/lists/"+value+"/?format=json"
      }).done(function(data, textStatus, jqXHR) {
        current_class = data;
        $('#parent_class_info').empty();
        $('#parent_class_info').attr("data-editor-id", current_class.id);
        var skip = ['name', 'fields', 'content_types'];
        for (const prop in data) {
          if (data.hasOwnProperty(prop) && prop != 'name' && prop != 'fields' && prop != 'content_types' && data[prop] != '' && data[prop] != null) {
              let html = '<div class="model-attribute-container"><div class="model-attribute-label">'+ prop +'</div><div data-editor-field="'+ prop +'" class="model-attribute-value">'+ data[prop] +'</div></div>';
              $('#parent_class_info').append(html);
          }
        };
      }).fail(function(jqXHR, textStatus, errorThrown) {
          alert('There was an error retrieving the data for this list from the server: '+errorThrown);
      });
      $('#btn_class_edit').attr('disabled', false);
      window.dispatchEvent(new Event('resize'));
  } else {
      dt_table.ajax.url("/api/fields/?format=json").draw();
      $('#parent_class_info').empty();
      $('#btn_class_edit').attr('disabled', true);
      window.dispatchEvent(new Event('resize'));
  }
}

function addClassEntry() {
  $.get("/api/options/?form=modelslist&format=json", function ( data ) {
      const content_types = data.content_types;
      const fields = data.fields;
      const model_class_name = 'list';
      var modelClassForm = editorForm('create', content_types, fields);
      modelClassForm.on('postSubmit', function(e, json, data, action) {
          if (json.data) {
            $('#parent_class_select').append(new Option(json.data.name, json.data.id));
            $('#parent_class_select').val(json.data.id);
            updateClass();
          }
      });
      modelClassForm.buttons(
        {
          text: "Create",
          className: "btn btn-primary",
          action: function () { this.submit(); }
        }
      );
      modelClassForm.title('Create new '+model_class_name).create();
  }, 'json');
}

function editClassEntry() {
  $.get("/api/options/?form=modelslist&format=json", function ( data ) {
      const content_types = data.content_types;
      const fields = data.fields;
      const model_class_name = 'list';
      var modelClassForm = editorForm('edit', content_types, fields);
      modelClassForm.on('postSubmit', function(e, json, data, action) {
          if (action == 'edit') {
              if (json.data && json.data !== "null" && typeof json.data !== "undefined" && json.data !== null) {
                $('#parent_class_select').append(new Option(json.data.name, json.data.id));
                $('#parent_class_select').val(json.data.id);
                updateClass();
              }
          } else if (action == 'remove') {
              if (json.result == 'success') {
                $('#parent_class_select option[value='+current_class.id+']').remove();
                $('#parent_class_select').val(0);
                current_class = '';
                updateClass();
              } else if (json.result == 'error') {
                alert(json.error);
              }
          }
      });
      var field_list = [];
      for (let i = 0, len = current_class.fields.length; i < len; ++i) {
        field_list.push(current_class.fields[i].field);
      };
      modelClassForm.field('name').def(current_class.name);
      modelClassForm.field('fields').def(field_list);
      modelClassForm.field('content_types').def(current_class.content_types);
      modelClassForm.buttons([
        {
          text: "Delete",
          className: "btn btn-danger",
          action: function () {
            //this.remove(current_class.id).submit();
            modelClassForm2 = editorForm('remove');
            modelClassForm2.on('preSubmit', function (e, d) {
                //delete d.data;
                d.data['id'] = current_class.id;
            });
            modelClassForm2.remove(current_class.id).submit();
            this.close()
          }
        },
        {
          text: "Save",
          className: "btn btn-primary",
          action: function () { this.submit(); }
        }
      ]);
      modelClassForm.title('Edit '+model_class_name).edit(current_class.id);
  }, 'json');
}

function editorForm(action, content_types, fields) {
    if (action == 'create') {
        var method = "POST";
        var url = "/api/lists/";
    } else if (action == 'edit') {
        var method = "PUT";
        var url = "/api/lists/_id_/";
    } else if (action == 'remove') {
        var method = "DELETE";
        var url = "/api/lists/_id_/";
    };
    var modelClassForm = new $.fn.dataTable.Editor( {
          ajax: {
            method: method,
            url: url,
            headers: { 'X-CSRFToken': getCookie("csrftoken") },
            data: function (d) {
              return { "data": JSON.stringify(d)};
            }
          },
          fields: [
            {
              label: "Name",
              name:  "name"
            },
            {
              label: "Short name",
              name:  "short_name"
            },
            {
              label: "Description",
              name:  "description",
              type: "textarea"
            },
            {
              label: "API URL",
              name:  "api_url",
            },
            {
              label: "Form helper",
              name:  "form_helper",
            },
            {
              label: "Preview helper",
              name:  "preview_helper",
            },
            {
              label: "Fields",
              name:  "fields",
              type: "chosen",
              attr: { multiple: true },
              options: fields
            },
            {
              label: "Content types",
              name:  "content_types",
              type: "chosen",
              attr: { multiple: true },
              options: content_types
            }
          ]
      });
      return modelClassForm
}

function toggleFieldEdit() {
  if (typeof edit_mode == 'undefined' || edit_mode == 'off') {
    edit_mode = 'on';
    $('#btn-field-edit').addClass('active');
    $('#dataTables-table').on('click', 'tbody td:not(:first-child)', function (e) {
          dt_editor.inline(this);
      });
  } else {
    edit_mode = 'off';
    $('#btn-field-edit').removeClass('active');
    $('#dataTables-table').off();
  }
}
