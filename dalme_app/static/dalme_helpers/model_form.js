function initializeFormHelper() {
  $('#parent_class_select').on('change', updateClass );
}

function updateClass() {
  if (model == 'dt_fields') {
    var table_url = "/api/dt_fields/?format=json";
    var url_prop = "&list=";
    var pc_url = "/api/dt_lists/";
    var info_skip = ['name', 'fields', 'content_types'];
  } else if (model == 'attribute_types') {
    var table_url = "/api/attribute_types/?format=json";
    var url_prop = "&content_type=";
    var pc_url = "/api/content_types/";
    var info_skip = ['name', 'attribute_types', 'content_class'];
  } else if (model == 'content_types') {
    var table_url = "/api/content_types/?format=json";
    var url_prop = "&class=";
    var pc_url = "/api/content_classes/";
    var info_skip = ['name'];
  };
  const value = $('#parent_class_select').children("option:selected").val();
  if (value !=0) {
      dt_table.ajax.url(table_url+url_prop+value).draw();
      $.ajax({
        method: "GET",
        url: pc_url+value+"/?format=json"
      }).done(function(data, textStatus, jqXHR) {
        current_class = data;
        $('#parent_class_info').empty();
        $('#parent_class_info').attr("data-editor-id", current_class.id);
        for (const prop in data) {
          if (data.hasOwnProperty(prop) && !info_skip.includes(prop) && data[prop] != '' && data[prop] != null) {
              if (typeof data[prop]['name'] !== 'undefined') {
                  var html = '<div class="model-attribute-container"><div class="model-attribute-label">'+ prop +'</div><div data-editor-field="'+ prop +'" class="model-attribute-value">'+ data[prop]['name'] +'</div></div>';
              } else {
                  var html = '<div class="model-attribute-container"><div class="model-attribute-label">'+ prop +'</div><div data-editor-field="'+ prop +'" class="model-attribute-value">'+ data[prop] +'</div></div>';
              };
              $('#parent_class_info').append(html);
          }
        };
      }).fail(function(jqXHR, textStatus, errorThrown) {
          alert('There was an error retrieving the data from the server: '+errorThrown);
      });
      $('#btn_class_edit').attr('disabled', false);
  } else {
      dt_table.ajax.url(table_url).draw();
      $('#parent_class_info').empty();
      $('#btn_class_edit').attr('disabled', true);
  };
  $(window).trigger('resize');
}

function addClassEntry() {
  if (model == 'dt_fields') {
    var option_lists = "content_types_list,attribute_types_list";
    var model_class_name = 'DT list'
  } else if (model == 'attribute_types') {
    var option_lists = "content_classes_list,attribute_types_list";
    var model_class_name = 'content type'
  };
  if (typeof option_lists !== 'undefined') {
    $.get("/api/options/?lists="+option_lists+"&format=json", function ( data ) {
        var modelClassForm = editorForm('create', data);
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
  } else {
    var modelClassForm = editorForm('create');
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
    modelClassForm.title('Create new content class').create();
  }
}

function editClassEntry() {
  if (model == 'dt_fields') {
    var option_lists = "content_types_list,attribute_types_list";
    var model_class_name = 'DT list';
  } else if (model == 'attribute_types') {
    var option_lists = "content_classes_list,attribute_types_list";
    var model_class_name = 'content type';
  };
  if (typeof option_lists !== 'undefined') {
    $.get("/api/options/?lists="+option_lists+"&format=json", function ( data ) {
        var modelClassForm = editorForm('edit', data);
        modelClassForm.on('postSubmit', function(e, json, data, action) {
            if (action == 'edit') {
                if (json.data && json.data !== "null" && typeof json.data !== "undefined" && json.data !== null) {
                  updateClass();
                }
            }
        });
        if (model == 'dt_fields') {
            var field_list = [];
            for (let i = 0, len = current_class.fields.length; i < len; ++i) {
              field_list.push(current_class.fields[i].field['value']);
            };
            modelClassForm.field('name').def(current_class.name);
            modelClassForm.field('fields').def(field_list);
            modelClassForm.field('content_types').def(current_class.content_types);
        } else if (model == 'attribute_types') {
            var att_list = [];
            for (let i = 0, len = current_class.attribute_types.length; i < len; ++i) {
              att_list.push(current_class.attribute_types[i].id);
            };
            modelClassForm.field('name').def(current_class.name);
            modelClassForm.field('content_class').def(current_class.content_class["value"]);
            modelClassForm.field('attribute_types').def(att_list);
        };
        modelClassForm.buttons([
          {
            text: "Delete",
            className: "btn btn-danger",
            action: function () {
              var conf = confirm("Are you sure you wish to delete this record?");
              if (conf == true) {
                modelClassForm2 = editorForm('remove');
                modelClassForm2.on('preSubmit', function (e, d) {
                    $('#parent_class_info').attr('data-editor-id', '');
                    d.data = current_class.id;
                });
                modelClassForm2.on('postSubmit', function(e, json, data, action) {
                        if (json.result == 'success') {
                          $('#parent_class_select option[value='+current_class.id+']').remove();
                          $('#parent_class_select').val(0);
                          current_class = '';
                          updateClass();
                        } else if (json.result == 'error') {
                          alert(json.error);
                        }
                });
                modelClassForm2.remove(current_class.id, false).submit();
                this.close();
              }
            }
          },
          {
            text: "Update",
            className: "btn btn-primary",
            action: function () { this.submit(); }
          }
        ]);
        modelClassForm.title('Edit '+model_class_name).edit(current_class.id);
    }, 'json');
  } else {
      var modelClassForm = editorForm('edit');
      modelClassForm.on('postSubmit', function(e, json, data, action) {
          if (action == 'edit') {
              if (json.data && json.data !== "null" && typeof json.data !== "undefined" && json.data !== null) {
                updateClass();
              }
          }
      });
      modelClassForm.field('name').def(current_class.name);
      modelClassForm.buttons([
        {
          text: "Delete",
          className: "btn btn-danger",
          action: function () {
            var conf = confirm("Are you sure you wish to delete this record?");
            if (conf == true) {
              modelClassForm2 = editorForm('remove');
              modelClassForm2.on('preSubmit', function (e, d) {
                  $('#parent_class_info').attr('data-editor-id', '');
                  d.data = current_class.id;
              });
              modelClassForm2.on('postSubmit', function(e, json, data, action) {
                      if (json.result == 'success') {
                        $('#parent_class_select option[value='+current_class.id+']').remove();
                        $('#parent_class_select').val(0);
                        current_class = '';
                        updateClass();
                      } else if (json.result == 'error') {
                        alert(json.error);
                      }
              });
              modelClassForm2.remove(current_class.id, false).submit();
              this.close();
            }
          }
        },
        {
          text: "Update",
          className: "btn btn-primary",
          action: function () { this.submit(); }
        }
      ]);
      modelClassForm.title('Edit content class').edit(current_class.id);
  };
}

function editorForm(action, data) {
    var fields;
    switch (model) {
        case 'dt_fields':
            var url = "/api/dt_lists/";
            if (action != 'remove') {
                fields = [
                  { label: "Name", name:  "name" },
                  { label: "Short Name", name:  "short_name" },
                  { label: "Description", name:  "description", type: "textarea" },
                  { label: "API URL", name:  "api_url" },
                  { label: "Helper/s", name:  "helpers", message: "A comma-separated list of js helpers for this list."},
                  { label: "Fields", name:  "fields", type: "chosen", attr: { multiple: true }, options: data.attribute_types_list },
                  { label: "Content Types", name:  "content_types", type: "chosen", attr: { multiple: true }, options: data.content_types_list }
                ];
            };
            break;
        case 'attribute_types':
            var url = "/api/content_types/";
            if (action != 'remove') {
                fields = [
                  { label: "Name", name:  "name" },
                  { label: "Short Name", name:  "short_name" },
                  { label: "Description", name:  "description", type: "textarea" },
                  { label: "Content Class", name:  "content_class", type: "chosen", opts: { disable_search: true}, options: data.content_classes_list },
                  { label: "Attribute Types", name:  "attribute_types", type: "chosen", attr: { multiple: true }, options: data.attribute_types_list }
                ];
            };
            break;
        case 'content_types':
            var url = "/api/content_classes/";
            if (action != 'remove') {
                fields = [
                  { label: "Name", name:  "name" },
                  { label: "Short Name", name:  "short_name" },
                  { label: "Description", name:  "description", type: "textarea" }
                ];
            };
    };
    switch (action) {
        case 'create':
            var method = "POST";
            break;
        case 'edit':
            var method = "PUT";
            url = url+"_id_/";
            break;
        case 'remove':
            var method = "DELETE";
            url = url+"_id_/";
    };
    var modelClassForm = new $.fn.dataTable.Editor( {
          ajax: {
              method: method,
              url: url,
              headers: { 'X-CSRFToken': getCookie("csrftoken") },
              data: function (data) { return { "data": JSON.stringify(data)};}
              },
          fields: fields
      });
    return modelClassForm
}

function toggleFieldEdit() {
  if (typeof edit_mode == 'undefined' || edit_mode == 'off') {
    edit_mode = 'on';
    $('#btn-field-edit').addClass('active');
    $('#dataTables-table').on('click', 'tbody td:not(:first-child)', function (e) {
          dt_editor.inline(dt_table.cell(this).index(), { onBlur: 'submit' });
      });
  } else {
    edit_mode = 'off';
    $('#btn-field-edit').removeClass('active');
    $('#dataTables-table').off();
  }
}
