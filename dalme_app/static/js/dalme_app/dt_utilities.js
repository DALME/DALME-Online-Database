function initialize_dt(config, editor, target) {
  $.ajax({
    method: "POST",
    url: "/api/configs/get/",
    headers: {
      "Content-Type": "application/json",
      'X-CSRFToken': get_cookie("csrftoken")
    },
    data: JSON.stringify({
      'target': config,
      'path': 'datatables',
      'base': true
    })

  }).done(function(data, textStatus, jqXHR) {
      if (data[0]['config'].hasOwnProperty('globals')) {
        for (const prop in data[0]['config']['globals']) {
            if (data[0]['config']['globals'].hasOwnProperty(prop)) {
              window[prop] = data[0]['config']['globals'][prop];
            }
        }
      }

      if (editor && data[0].hasOwnProperty('editor')) {
        build_editor(data, target);
      } else {
        build_datatables(data, target, false);
      }

  }).fail(function(jqXHR, textStatus, errorThrown) {
      toastr.error('There was an error communicating with the server: ' + errorThrown);
  });
}

function build_editor(data, target) {
  var config_data = data[0]['config']

  attribute_concordance_rev = {}
  for (key in attribute_concordance)
    attribute_concordance_rev[attribute_concordance[key]] = key;

  get_dt_elements({
        type: 'field_defs',
        el_list: data[0].editor.fields,
        overrides: data[0].editor.overrides,
        endpoint: config_data.endpoint

  }).then(function(e_fields) {
      var editor_options = _.merge(data[1].editor.options, data[0].editor.options);
      one_time_general_setup = false;

      for (const prop in editor_options['ajax']) {
          if (editor_options['ajax'].hasOwnProperty(prop) && ['create', 'edit', 'remove'].includes(prop)) {
              editor_options['ajax'][prop]['headers']['X-CSRFToken'] = (get_cookie("csrftoken"));
              editor_options['ajax'][prop]['data'] = (function (data) { return { "data": JSON.stringify(data) }; });
          }
      };

      let fields = Object.values(attribute_concordance)

      for (let i = 0, len = fields.length; i < len; ++i) {
        if (required_list.includes(fields[i])) {
          $('#form-field-container').append('<div class="flex-row-reverse" data-editor-template="' + fields[i]
              + '"></div>');
        } else {
          $('#form-field-container').append('<div class="flex-row-reverse" data-editor-template="' + fields[i]
              + '"><i class="fas fa-times-circle field_clear_button"></i></div>');}
      }

      editor_options['fields'] = e_fields;
      if (typeof target != 'undefined') { editor_options['table'] = target }

      dt_editor = new $.fn.dataTable.Editor(editor_options);

      dt_editor.on('initEdit.dalme', function(e, node, data, items, type) {
          return new Promise(function (resolve, reject) {
              let url_components = dt_editor.ajax()['edit']['url'].split('/')
              $.ajax({
                  method: "POST",
                  url: "/api/" + url_components[2] + "/" + data.id + "/has_permission/",
                  headers: { 'X-CSRFToken': get_cookie("csrftoken") },
              }).done(function(response, textStatus, jqXHR) {
                  resolve();
              }).fail(function(jqXHR, textStatus, errorThrown) {
                  dt_editor.on('preOpen.dalme', function(e, mode, action) { return false });
                  toastr.error('Permission denied.');
                  resolve();
              });
          });
      });

      dt_editor.on('open.dalme', general_form_setup);

      dt_editor.on('close.dalme', general_form_restore);

      dt_editor.on('postSubmit.dalme', function(e, json, data, action, xhr) {
          if (json != null) {
            let error_list = []
            if (json.hasOwnProperty('fieldErrors')) {
                for (let i = 0, len = json['fieldErrors'].length; i < len; ++i) {
                  if (json['fieldErrors'][i].hasOwnProperty('name')) {
                      let name = json['fieldErrors'][i]['name'];
                      console.log('name = ' + name)
                      if (name == 'non_field_errors') {
                          error_list.push(`General error: ${json['fieldErrors'][i]['status']}`);
                          delete json['fieldErrors'][i]
                      } else {
                          if (name.includes('.non_field_errors')) {
                            name = name.replace('.non_field_errors', '');
                          }
                          if (attribute_concordance.hasOwnProperty(name)) {
                            json['fieldErrors'][i]['name'] = attribute_concordance[name];
                          } else {
                            error_list.push(`${json['fieldErrors'][i]['name']} failed to validate with status ${json['fieldErrors'][i]['status']}`);
                            delete json['fieldErrors'][i]
                          }
                      }
                  }
                  if (json['fieldErrors'][0] == null) {
                    delete json['fieldErrors'];
                  }
                }
              } else if (json.hasOwnProperty('data') && json['data'].hasOwnProperty('detail')) {
                  toastr.error(json['data']['detail']);
                  dt_editor.close()
              }
              if (json.hasOwnProperty('error')) {
                error_list.push(`General error: ${json['error']}`);
              }
              if (error_list.length) {
                console.log(JSON.stringify(error_list))
                let error = '<ul>'
                for (let i = 0, len = error_list.length; i < len; ++i) {
                  error += `<li>${error_list[i]}</li>`
                }
                error += '</ul>'
                json['error'] = error;
              }
            console.log(JSON.stringify(json))
          }
      });

      dt_editor.on('submitSuccess', function(e, json, data, action) { toastr.success(messages_list[action+'_success']) });

      if (typeof target != 'undefined') {
        build_datatables(data, target, true);
      } else {
        init_helpers(config_data);
      }
  });
}

function build_datatables(data, target, editor) {
  var config_data = data[0]['config']

  var table_options = _.merge(data[1].datatables.options, data[0].datatables.options);
  table_options['ajax']['data'] = (function (data) { return { "data": JSON.stringify(data) }; });

  let editor_buttons = editor ? data[0].editor.buttons : []
  let editor_instance = editor ? dt_editor : null

  get_dt_buttons(
    _.merge(data[1].datatables.buttons, data[0].datatables.buttons),
    editor_buttons,
    editor_instance

  ).then(function(buttons) {
    table_options['buttons'] = buttons;

    get_dt_elements({
      type: 'column_defs',
      el_list: data[0].datatables.columns,
      overrides: data[0].datatables.overrides,
      endpoint: config_data.endpoint

    }).then(function(t_columns) {
        table_options['columnDefs'] = t_columns;

        dt_table = $(target).DataTable(table_options);

        dt_table.on('init', function() {
          fix_dt_search();
          dt_table.on('preXhr.dt', function (e, settings, data) { update_dt_url(data); });
          dt_table.on('draw.dalme', function() {
              dt_table.columns.adjust();
              dt_table.responsive.recalc();
              window.dispatchEvent(new Event('resize'));
          });
          dt_table.on('column-visibility.dalme', function() {
              dt_table.columns.adjust();
              dt_table.responsive.recalc();
              window.dispatchEvent(new Event('resize'));
          });
        });

        init_helpers(config_data);
      });
  });
}

function init_helpers(config_data) {
  if (Array.isArray(config_data.helpers) && config_data.helpers.length) {
    for (let i = 0, len = config_data.helpers.length; i < len; ++i) {
      eval(config_data.helpers[i]+'_init()');
    };
  };
}

function general_form_setup(e, mode, action) {
    if (!one_time_general_setup) {
      $('#header-button').insertAfter('.close');
      $('#header-button').remove();
      one_time_general_setup = true;
    }

    $('.DTE_Header').children('.close').remove();
    $('.DTE_Header_Content').html('<div class="form_title_text">' + dt_editor.title() + '</div>')
    $('[data-dte-e="form_error"]').appendTo($('.DTE_Body'));
    $('.DTE_Footer_Content').append($('#form-button-container').html());
    $('#form-button-container').remove();
    $('.DTE_Form_Content').find('.col-lg-4').removeClass('col-lg-4').addClass('col-lg-12');
    $('.DTE_Form_Content').find('.col-lg-8').removeClass('col-lg-8').addClass('col-lg-12');

    $('.DTE_Field').each(function() {
      if (!$(this).find('[data-dte-e="msg-info"]').is(':empty') ) {
        let info = $(this).find('[data-dte-e="msg-info"]').html();
        $(this).find('[data-dte-e="msg-label"]').html(info);
        $(this).find('[data-dte-e="msg-info"]').html('');
      }
    });

    $('.field_clear_button').each( function(i, el) {
      let field = $(el).parent().data('editor-template')
      $(el).popover({
          toggle: 'popover',
          placement: 'right',
          html: true,
          title: '',
          content: '<a href="#" id="' + field + '" class="btn btn-sm btn-danger clear-field mr-1">\
              Remove</a><a href="#" class="btn btn-sm btn-primary">Cancel</a>',
        })
    })

    $(document).on("click.dalme", ".popover .btn-primary" , function() {
        $(this).parents(".popover").popover('hide');
    });

    $(document).on("click.dalme", ".popover .clear-field" , function() {
        toggle_fields($(this).attr('id'), 'hide');
        $(this).parents(".popover").popover('hide');
    });

    if (action == 'remove') {
      $('.modal-header').addClass('d-none');
      $('.DTE_Form_Buttons').appendTo($('.DTE_Body'));
      $('.DTE_Form_Buttons').addClass('remove-action-buttons');
      $('.modal-footer').addClass('d-none');
      $('.DTE_Form_Info').addClass('remove-action-info');
    }

    if (typeof on_open_function !== 'undefined') {
      eval(on_open_function + '(e, mode, action)');
    } else {
      if (action == 'create') {
        toggle_fields(required_list);
      } else if (action == 'edit') {
        let editor_fields = dt_editor.order()
        let populated_list = []

        for (let i = 0, len = editor_fields.length; i < len; ++i) {
          if (dt_editor.field(editor_fields[i]).val() != '') {
            populated_list.push(editor_fields[i])
          }
        }

        toggle_fields(populated_list);
      }
    }
}

function general_form_restore(e) {
  $('.DTE_Form_Buttons').appendTo($('.DTE_Footer'));
  $('.DTE_Form_Buttons').removeClass('remove-action-buttons');
  $('.modal-header').removeClass('d-none');
  $('.modal-footer').removeClass('d-none');
  $('.DTE_Form_Info').removeClass('remove-action-info');

  $('#add-attribute-button').off('click.dalme');
  $('.field_clear_button').popover('dispose');
  $(document).off("click.dalme", ".popover .btn-primary");
  $(document).off("click.dalme", ".popover .clear-field");

  if (typeof on_close_function !== 'undefined') {
    eval(on_close_function + '(e)');
  }
}

function toggle_fields(target, action) {
  if (Array.isArray(target) && target.length) {
    let editor_fields = Object.values(attribute_concordance);
    let add_menu_list = [];

    for (let i = 0, len = editor_fields.length; i < len; ++i) {
      if (target.includes(editor_fields[i])) {
        toggle_fields(editor_fields[i], 'show')
      } else {
        toggle_fields(editor_fields[i], 'hide')
        add_menu_list.push(editor_fields[i]);
      }
    }
    if (add_menu_list.length) {
      let clean_menu_list = []
      add_menu_list.forEach((x) => { clean_menu_list.push(attribute_concordance_rev[x])});
      clean_menu_list.sort();

      $('#add-attribute-menu-container').html('');

      for (let i = 0, len = clean_menu_list.length; i < len; ++i) {
          $('#add-attribute-menu-container').append('<a class="dropdown-item" href="#" data-menu-field="'
            + attribute_concordance[clean_menu_list[i]] + '">'
            + clean_menu_list[i].replace('_', ' ').replace(/^\w/, (c) => c.toUpperCase()) + '</a>');
      }
      $('#add-attribute-button').removeClass('d-none');
      $('#add-attribute-menu-container').on('click.dalme', '.dropdown-item', function () {
        toggle_fields($(this).data('menu-field'), 'show');
      });

    } else {
      $('#add-attribute-button').addClass('d-none');
    }

  } else if (typeof action != 'undefined') {

    switch (action) {

      case 'hide':
        dt_editor.field(target).val('');
        dt_editor.hide(target);

        if ($(dt_editor.field(target).node()).parent().find('.field_clear_button').length) {
          $(dt_editor.field(target).node()).parent().find('.field_clear_button').addClass('d-none');
        }

        if (!$('#add-attribute-menu-container').find('[data-menu-field="' + target + '"]').length) {
          $('#add-attribute-menu-container').append('<a class="dropdown-item" href="#" data-menu-field="' + target + '">'
              + attribute_concordance_rev[target].replace('_', ' ').replace(/^\w/, (c) => c.toUpperCase()) + '</a>');

          $('#add-attribute-menu-container').find('dropdown_item').sort(function(a, b) {
              return $(a).text().toLowerCase().localeCompare($(b).text().toLowerCase());
            }).each(function() {
              $('#add-attribute-menu-container').append(this);
          });
        }

        if ($('#add-attribute-button').hasClass('d-none')) {
          $('#add-attribute-button').removeClass('d-none');
        }

        break;

      case 'show':
        dt_editor.show(target);

        if ($(dt_editor.field(target).node()).parent().find('.field_clear_button').length) {
          $(dt_editor.field(target).node()).parent().find('.field_clear_button').removeClass('d-none');
        }

        if ($('#add-attribute-menu-container').find('[data-menu-field="' + target + '"]').length > 0) {
          $('#add-attribute-menu-container').find('[data-menu-field="' + target + '"]').remove()

          if ($('#add-attribute-menu-container').children().length < 1) {
            $('#add-attribute-button').addClass('d-none');
          }
        }
    }
  }
}

function get_dt_elements({
  type = 'field_defs',
  el_list,
  overrides,
  endpoint,
  process=true
}) {
  return new Promise(function (resolve, reject) {
      let payload = { 'target': el_list }

      if (type == 'buttons') {
        payload['buttons'] = true;
        payload['path'] = 'datatables,' + type
      } else {
        payload['path'] = 'datatables,' + type + ',' + endpoint
      }

      $.ajax({
        method: "POST",
        url: "/api/configs/get/",
        headers: {
          "Content-Type": "application/json",
          'X-CSRFToken': get_cookie("csrftoken")
        },
        data: JSON.stringify(payload)

      }).done(function(data, textStatus, jqXHR) {
          if (process) {
            process_dt_fields(type, data, overrides)
            .then(function(response) {
                resolve(response);
            });
          } else {
            resolve(data);
          }

      }).fail(function(jqXHR, textStatus, errorThrown) {
          toastr.error('There was an error communicating with the server: '+errorThrown);
      });
  });
}

function process_dt_fields(type, fields, overrides) {
  return new Promise(function (resolve, reject) {
      var keys = ['name', 'data']

      for (let i = 0, len = fields.length; i < len; ++i) {
          if (typeof overrides != "undefined") {
            for (let j = 0, len = keys.length; j < len; ++j) {
              if (overrides.hasOwnProperty(fields[i][keys[j]])) {
                let ov = overrides[fields[i][keys[j]]];
                for (const prop in ov) {
                    if (ov.hasOwnProperty(prop)) {
                      fields[i][prop] = ov[prop];
                    }
                }
              }
            }
          }

          if (type == "column_defs") {
            fields[i]["targets"] = i;

            for (const prop in fields[i]) {
                if (fields[i].hasOwnProperty(prop) && prop == 'render') {
                    fields[i]['render'] = eval("(" + fields[i]['render'] + ")")
                }
            };
          }

          if (type == "field_defs") {
            if (fields[i].hasOwnProperty('options')) {
              if (typeof fields[i]['options'] == 'object' && fields[i]['options'] != null) {
                var opt_object = fields[i]['options'];

                switch (opt_object['type']) {

                  case 'list':
                      fields[i]['options'] = eval(opt_object['list']);
                      break;

                  case 'api_call':
                      fields[i]['opts']['load'] = eval("(function(query, callback) {$.ajax({url: \"" + opt_object['url'] +
                          "\"\+ encodeURIComponent(query),type: 'GET',error: function() {callback();},success: function(res) {callback(res);}});})")
                      delete fields[i]['options'];
                      break;

                  case 'api_call_x':
                      fields[i]['opts']['load'] = eval("(function(query, callback) {$.ajax({url: \"" + opt_object['url'] +
                          "\"\+ encodeURIComponent(query),type: 'GET',error: function() {callback();},success: function(res) {callback(res);}});})")
                      fields[i]['opts']['render'] = eval("(" + opt_object['render'] + ")")
                      delete fields[i]['options'];
                }
              }
            }

            if (fields[i]['type'] == "upload") {
              fields[i]['ajax'] = {
                method: 'POST',
                url: '/api/attachments/',
                headers: { 'X-CSRFToken': get_cookie("csrftoken") },
              };
              fields[i]['display'] = eval("(function(file) { return file.filename })")
            }

            if (required_list.includes(fields[i]['name'])) {
              if (fields[i].hasOwnProperty('attr')) {
                  fields[i]['attr']['required'] = true
              } else {
                  fields[i]['attr'] = { required: true }
              }

            }
          }
      };
      resolve(fields);
  });
}

function get_dt_buttons(table_button_list, editor_button_list, editor) {
  return new Promise(function (resolve, reject) {
      get_dt_elements({
        type: 'buttons',
        el_list: table_button_list

      }).then(function(t_buttons) {
          if (Array.isArray(editor_button_list) && editor_button_list.length) {
              get_dt_elements({
                type: 'buttons',
                el_list: editor_button_list

              }).then(function(e_buttons) {
                  if (e_buttons.length > 0) {
                    for (let i = 0, len = e_buttons.length; i < len; ++i) {
                      e_buttons[i]['editor'] = editor;

                      if (e_buttons[i].hasOwnProperty('formButtons')) {
                        for (let j = 0, len = e_buttons[i]['formButtons'].length; j < len; ++j) {
                          for (const prop in e_buttons[i]['formButtons'][j]) {
                              if (e_buttons[i]['formButtons'][j].hasOwnProperty(prop) && prop == 'action') {
                                  e_buttons[i]['formButtons'][j]['action'] = eval('(' + e_buttons[i]['formButtons'][j]['action'] + ')');
                              }
                          };
                        }
                      }
                    };
                    let button_wrapper = {
                        'extend': 'collection',
                        'text': '<i class="fa fa-bars fa-fw"></i> Actions',
                        'autoClose': 'true',
                        'buttons': e_buttons
                        };
                    t_buttons.push(button_wrapper);
                  }
                  resolve(t_buttons);
              });
          } else {
              resolve(t_buttons);
          }
      });
  });
}

function update_dt_url(data) {
  data = JSON.parse(data['data'])
  var url = remove_param(['search', 'ordering'], dt_table.ajax.url())

  if (data['order'].length) {
    var ordering = [];

    for (let i = 0, len = data['order'].length; i < len; ++i) {
      let column = data['order'][i]['dir'] == 'asc' ? '' : '-'
      column = column + data['columns'][data['order'][i]['column']]['data']
      ordering.push(column)
    }

    url = url + '&ordering=' + ordering.join(',')
  }

  if (data['search']['value'] != '') {
    url = url + '&search=' + data['search']['value']
  }

  dt_table.ajax.url(url)
}

function filter_set(set, clear=[]) {
  console.log('clear = ' + JSON.stringify(clear))
  console.log('set = ' + JSON.stringify(set))
  for (const prop in set) {
    if (set.hasOwnProperty(prop)) {
      clear.push(prop)
    }
  }
  console.log('compiled clear = ' + JSON.stringify(clear))
  var url = remove_param(clear, dt_table.ajax.url())
  console.log('clean url = ' + url)
  for (const prop in set) {
    if (set.hasOwnProperty(prop)) {
      url = url + '&' + prop + '=' + set[prop]
    }
  }
  console.log('request url = ' + url)
  dt_table.ajax.url(url).load();
}
