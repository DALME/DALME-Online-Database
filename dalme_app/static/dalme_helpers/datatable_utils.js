function build_datatable(target, config) {
  $.ajax({
      method: "GET",
      url: "/api/configs/?path=datatables&target="+config+"&base=true"
  }).done(function(data, textStatus, jqXHR) {
      var config_data = data[0]['config']
      set_globals(config_data);
      var table_options = set_ajax_paras(_.merge(data[1].datatables.options, data[0].datatables.options));
      var editor_options = set_ajax_paras(_.merge(data[1].editor.options, data[0].editor.options));
      if (editor_options.hasOwnProperty('template')) {
          add_fields_to_template(config_data.template_field_container, Object.values(attribute_concordance));
      }
      get_dt_elements({
            type: 'field_defs',
            el_list: data[0].editor.fields,
            overrides: data[0].editor.overrides,
            endpoint: config_data.endpoint
      }).then(function(e_fields) {
          editor_options['fields'] = e_fields;
          editor_options['table'] = target;
          dt_editor = new $.fn.dataTable.Editor(editor_options);
          one_time_general_setup = false;
          dt_editor.on('open.dalme', general_form_setup);
          dt_editor.on('close.dalme', general_form_restore);
          dt_editor.on('postSubmit.dalme', function(e, json, data, action, xhr) {
              if (json != null && json.hasOwnProperty('fieldErrors')) {
                for (let i = 0, len = json['fieldErrors'].length; i < len; ++i) {
                  if (json['fieldErrors'][i].hasOwnProperty('name')) {
                      json['fieldErrors'][i]['name'] = attribute_concordance[json['fieldErrors'][i]['name']];
                  }
                }
              }
          });
          dt_editor.on('submitSuccess', function(e, json, data, action) { toastr.success(messages_list[action+'_success']) });
          get_dt_buttons(_.merge(data[1].datatables.buttons, data[0].datatables.buttons), data[0].editor.buttons, dt_editor)
          .then(function(buttons) {
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
                      if (Array.isArray(config_data.helpers) && config_data.helpers.length) {
                        for (let i = 0, len = config_data.helpers.length; i < len; ++i) { eval(config_data.helpers[i]+'_init()'); };
                      };
                    });
              });
          });
        });
  }).fail(function(jqXHR, textStatus, errorThrown) {
      toastr.error('There was an error communicating with the server: '+errorThrown);
  });
}

function set_ajax_paras(options) {
  if (options['ajax'].hasOwnProperty('url')) {
    options['ajax']['data'] = (function (data) { return { "data": JSON.stringify(data) }; });
  } else {
    for (const prop in options['ajax']) {
        if (options['ajax'].hasOwnProperty(prop) && ['create', 'edit', 'remove'].includes(prop)) {
            options['ajax'][prop]['headers']['X-CSRFToken'] = (get_cookie("csrftoken"));
            options['ajax'][prop]['data'] = (function (data) { return { "data": JSON.stringify(data) }; });
        }
    };
  }
  return options
}

function general_form_setup(e, mode, action) {
    if (!one_time_general_setup) {
      $('#header-button').insertAfter('.close');
      $('#header-button').remove();
      one_time_general_setup = true;
    }
    $('.close').remove();
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
    if (action == 'remove') {
      $('.modal-header').addClass('d-none');
      $('.DTE_Form_Buttons').appendTo($('.DTE_Body'));
      $('.DTE_Form_Buttons').addClass('remove-action-buttons');
      $('.modal-footer').addClass('d-none');
      $('.DTE_Form_Info').addClass('remove-action-info');
    }
    if (typeof on_open_function !== 'undefined') {
      eval(on_open_function + '(e, mode, action)');
    }
}

function general_form_restore(e) {
  $('.DTE_Form_Buttons').appendTo($('.DTE_Footer'));
  $('.DTE_Form_Buttons').removeClass('remove-action-buttons');
  $('.modal-header').removeClass('d-none');
  $('.modal-footer').removeClass('d-none');
  $('.DTE_Form_Info').removeClass('remove-action-info');
  if (typeof on_close_function !== 'undefined') {
    eval(on_close_function + '(e)');
  }
}

function add_fields_to_template(tag, fields) {
    for (let i = 0, len = fields.length; i < len; ++i) {
      $(tag).append('<div data-editor-template="' + fields[i] + '"></div>');
    }
}

function get_dt_elements({
  type = 'field_defs',
  el_list,
  overrides,
  endpoint
}) {
  return new Promise(function (resolve, reject) {
      let url = "/api/configs/?path=datatables," + type;
      if (typeof endpoint !== 'undefined') {
        url = url + "," + endpoint;
      }
      url = url + "&target=" + JSON.stringify(el_list);
      if (type == 'buttons') {
        url = url + "&buttons=true"
      }
      $.ajax({
          method: "GET",
          url: url
      }).done(function(data, textStatus, jqXHR) {
          process_dt_fields(type, data, overrides)
          .then(function(response) {
              resolve(response);
          });
      }).fail(function(jqXHR, textStatus, errorThrown) {
          toastr.error('There was an error communicating with the server: '+errorThrown);
      });
  });
}

function process_dt_fields(type, fields, overrides) {
  return new Promise(function (resolve, reject) {
      var key = type == "column_defs" ? 'data' : 'name';
      for (let i = 0, len = fields.length; i < len; ++i) {
          if (type == "column_defs") {
            fields[i]["targets"] = i;
            for (const prop in fields[i]) {
                if (fields[i].hasOwnProperty(prop) && prop == 'render') {
                    fields[i]['render'] = eval("(" + fields[i]['render'] + ")")
                }
            };
          }
          if (typeof overrides != "undefined" && overrides.hasOwnProperty(fields[i][key])) {
              let ov = overrides[fields[i][key]];
              for (const prop in ov) {
                  if (ov.hasOwnProperty(prop)) {
                    fields[i][prop] = ov[prop];
                  }
              }
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
                      fields[i]['opts']['load'] = eval("(function(query, callback) {$.ajax({url: \"" + opt_object['url'] + "\"\+ encodeURIComponent(query),type: 'GET',error: function() {callback();},success: function(res) {callback(res);}});})")
                      delete fields[i]['options'];
                }
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
                  resolve(t_buttons);
              });
          } else {
              resolve(t_buttons);
          }
      });
  });
}

function retrieve_field_options(url) {
  return new Promise(function (resolve, reject) {
      $.ajax({
          method: "GET",
          url: url
      }).done(function(data, textStatus, jqXHR) {
          resolve(data);
      }).fail(function(jqXHR, textStatus, errorThrown) {
          toastr.error('There was an error communicating with the server: '+errorThrown);
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

function filter_set(data, options=[]) {
  var param_list = []
  for (const prop in data) {
    if (data.hasOwnProperty(prop)) {
      param_list.push(prop)
    }
  }
  var url = remove_param(param_list, dt_table.ajax.url())
  if (!options.includes('clear')) {
    for (let i = 0, len = param_list.length; i < len; ++i) {
      if (data[param_list[i]] != 'clear') {
        url = url + '&' + param_list[i] + '=' + data[param_list[i]]
      }
    }
  }
  dt_table.ajax.url(url).load();
}

function set_globals(config) {
  if (config.hasOwnProperty('globals')) {
    for (const prop in config['globals']) {
        if (config['globals'].hasOwnProperty(prop)) {
          window[prop] = config['globals'][prop];
        }
    }
  }
}

function fix_dt_search() {
  $('.dataTables_filter label').contents().filter(function () { return this.nodeType == 3; }).remove();
}
