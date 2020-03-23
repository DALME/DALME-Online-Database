function create_datatable(target, helpers, modules) {
  if (typeof dt_editor_options !== 'undefined') {
    dt_editor_options['table'] = target;
    dt_editor = new $.fn.dataTable.Editor(dt_editor_options);
    if (typeof dt_editor_buttons !== 'undefined') {
      buttons = dt_editor_buttons
      for (let i = 0, len = buttons.length; i < len; ++i) {
        buttons[i]['editor'] = dt_editor;
      };
      dt_options.buttons.push({ 'extend': 'collection', 'text': '<i class="fa fa-bars fa-fw"></i> Actions', 'autoClose': 'true', 'buttons': buttons });
    };
  };
  dt_table = $(target).DataTable(dt_options);
  dt_table.on('init', function() {
    fix_dt_search();
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
    if (helpers != 'None') {
      helpers = JSON.parse(helpers.replace(/'/g, '"'));
      for (let i = 0, len = helpers.length; i < len; ++i) { eval(helpers[i]+'()'); };
    };
    if (modules != 'None') {
      modules = JSON.parse(modules.replace(/'/g, '"'));
      for (let i = 0, len = modules.length; i < len; ++i) { init_module(modules[i]); };
    };
    if (typeof action !== 'undefined') {
      perform_action(action);
    };
  });
}

function perform_action(action) {
  eval(action['action']+'(['+action['data']+'])');
}

function init_module(mod) {
  switch(mod) {
    case 'filters':
        $('#dataTables-list_filter').parent().prepend('<button class="btn dt-btn buttons-collection" id="btn-filters" data-toggle="collapse" data-target="#filters-container"\
                                                      aria-expanded="false" aria-controls="filters-container" type="button" onclick="this.classList.toggle(\'active\')">\
                                                      <i class="fa fa-filter fa-sm"></i> Filters</button>');
        $('#dataTables-list_filter .form-control')[0].style.borderTopLeftRadius = "0";
        $('#dataTables-list_filter .form-control')[0].style.borderBottomLeftRadius = "0";
        $('#btn-filters').css("margin-right","-1px");
        reset_filters();
        $('#filters-container').on('click', '.add_filter', add_filter);
        $('#filters-container').on('click', '.remove_filter', remove_filter);
        break;
    case 'preview':
        $('.dt-buttons').append('<button class="btn dt-btn buttons-collection" id="btn-preview" onclick="toggle_preview()"><i class="fa fa-eye fa-sm"></i> Preview</button>');
        break;
    case 'fieldsets':
        var button_html = '<div class="btn-group dropdown"><button class="btn buttons-collection dropdown-toggle" id="fieldsets_button" data-toggle="dropdown" aria-haspopup="true"\
                          aria-expanded="false"><i class="fa fa-swatchbook fa-sm"></i> Fieldsets</button><div class="dropdown-menu" aria-labelledby="fieldsets_button">';
        for (const prop in dt_fieldsets) {
            if (dt_fieldsets.hasOwnProperty(prop)) { button_html += '<a class="dt-button dropdown-item" href="#" onclick="toggle_columns(this)"><span>'+ prop +'</span></a>'; }
        };
        button_html += '</div></div>';
        $('.dt-buttons').append(button_html);
        break;
    case 'workflow':
        $.ajax({
            method: "GET",
            url: "/api/options/?target=json_file&name=workflow_menu&format=json"
        }).done(function(data, textStatus, jqXHR) {
            var wf_menu = data.json_file;
            var button_html = '<div class="btn-group dropdown"><button class="btn buttons-collection dropdown-toggle" id="workflow_button" data-toggle="dropdown" aria-haspopup="true"\
                              aria-expanded="false"><i class="fa fa-code-branch fa-sm"></i> Workflow</button><div class="dropdown-menu wf-dropdown" aria-labelledby="workflow_button">';
            for (let i = 0, len = wf_menu.length; i < len; ++i) {
              switch(wf_menu[i]['type']) {
                case 'title':
                    button_html += '<div class="dropdown-title">'+ wf_menu[i]['text'] +'</div>';
                    break;
                case 'message':
                    button_html += '<div class="dropdown-text">'+ wf_menu[i]['text'] +'</div>';
                    break;
                case 'divider':
                    button_html += '<div class="dropdown-divider"></div>';
                    break;
                case 'item':
                    button_html += '<a class="dt-button dropdown-item" href="#" onclick="workflow_filter(this, \''+ wf_menu[i]['query'] +'\')">'+ wf_menu[i]['text'] +'</a>';
                    break;
                case 'item-select':
                    button_html += '<div class="dropdown-select dropdown-item">\
                                    <a class="dt-button dropdown-item-select mr-1" href="#" onclick="workflow_filter(this, \''+ wf_menu[i]['query'] +'-all\')">'+ wf_menu[i]['text'] +'</a>';
                    if (wf_menu[i]['text'] != 'Ingestion') { button_html += '<a class="dt-button dropdown-tag" href="#" onclick="workflow_filter(this, \''+ wf_menu[i]['query'] +'-awaiting\')">awaiting</a>' };
                    button_html += '<a class="dt-button dropdown-tag" href="#" onclick="workflow_filter(this, \''+ wf_menu[i]['query'] +'-progress\')">in progress</a>\
                                    <a class="dt-button dropdown-item-select" href="#" onclick="workflow_filter(this, \''+ wf_menu[i]['query'] +'-done\')"><i class="far fa-check-circle fa-fw"></i></a>\
                                    <a class="dt-button dropdown-item-select" href="#" onclick="workflow_filter(this, \''+ wf_menu[i]['query'] +'-not_done\')"><i class="far fa-times-circle fa-fw"></i></i></a>\
                                    </div>';
              };
            };
            button_html += '</div></div>';
            $('.dt-buttons').append(button_html);
        }).fail(function(jqXHR, textStatus, errorThrown) {
            toastr.error('The following error occured while attempting to retrieve the data for the Workflow menu: '+errorThrown);
        });
  }
}

function workflow_filter(menu, query) {
  $('.wf-dropdown').find('.active').removeClass('active');
  $(menu).addClass('active');
  if (!$(menu).hasClass('dropdown-item')) { $(menu).parent().addClass('active'); };
  if (query.includes('timedelta')) {
      if (query == 'timedelta-older') {
          var val = '{\'workflow__last_modified__lt\': \'timedelta-365\'}';
      } else {
          var val = '{\'workflow__last_modified__gte\': \''+query+'\'}';
      }
  } else if ($.isNumeric(query.slice(0,1))) {
      var stage_dict = { '1': 'ingestion', '2': 'transcription', '3': 'markup', '4':'review', '5':'parsing' };
      var q_list = query.split('-');
      switch (q_list[1]) {
          case 'all':
              var val = '{\'workflow__stage\': '+q_list[0]+'}';
              break;
          case 'awaiting':
              const stage = q_list[0] - 1;
              var val = '{\'workflow__stage\': '+stage+'},{\'workflow__'+stage_dict[stage]+'_done\': 1}';
              break;
          case 'progress':
              var val = '{\'workflow__stage\': '+q_list[0]+'},{\'workflow__'+stage_dict[q_list[0]]+'_done\': 0}';
              break;
          case 'done':
              var val = '{\'workflow__'+stage_dict[q_list[0]]+'_done\': 1}';
              break;
          case 'not_done':
              var val = '{\'workflow__'+stage_dict[q_list[0]]+'_done\': 0}';
      }
  } else {
      switch (query) {
          case 'processed':
              var val = '{\'workflow__wf_status\':3}';
              break;
          case 'assessing':
              var val = '{\'workflow__wf_status\':1}';
              break;
          case 'help':
              var val = '{\'workflow__help_flag\':1}';
              break;
          case 'public':
              var val = '{\'workflow__is_public\':1}';
      }
  };
  if (typeof val != 'undefined') {
      wf_filters = val;
  } else {
      wf_filters = undefined;
  };
  apply_filters();
}

function toggle_inline_edit() {
  if (typeof edit_mode == 'undefined' || edit_mode == 'off') {
    edit_mode = 'on';
    $('.inline-edit-toggle').addClass('active');
    dt_table.on('click.dalme', 'tbody td:not(:first-child)', function (e) {
          dt_editor.inline(dt_table.cell(this).index(), { onBlur: 'submit' });
      });
  } else {
    edit_mode = 'off';
    $('.inline-edit-toggle').removeClass('active');
    dt_table.off('click.dalme');
  }
}

function toggle_columns(button) {
  $(button).parent().find('.active').removeClass('active');
  $(button).toggleClass('active');
  var range = dt_fieldsets[$(button).text()];
  for (let i = 3; i < dt_table.columns().count(); ++i) {
    range.includes(i) ? dt_table.column(i).visible(true) : dt_table.column(i).visible(false);
  };
  dt_table.columns.adjust().draw();
  window.dispatchEvent(new Event('resize'));
}

function toggle_preview() {
  if (typeof preview_state == 'undefined' || preview_state == 'off') {
      preview_state = 'on';
      maxWidth = $(window).width() - 522;
      $('#btn-preview').addClass('active');
      $('.panel-left').append('<div class="splitter-vertical ui-resizable-handle ui-resizable-e"></div>');
      $('.panel-container').append('<div class="panel-right panel-preview"><div class="img-placeholder d-flex justify-content-center align-items-center"><i class="d-block fa fa-eye-slash fa-4x mt-5 mb-5"></i></div></div>');
      $('.panel-left').width('70%');
      $('.panel-right').width('30%');
      $('.panel-left').resizable({
          handles: {e: '.splitter-vertical'},
          maxWidth: maxWidth,
          minWidth: 600,
          resize: function(e, ui) {
              const parent = ui.element.parent();
              const remainingSpace = parent.width() - ui.element.outerWidth();
              const divTwo = ui.element.next();
              const divTwoWidth = (remainingSpace - (divTwo.outerWidth() - divTwo.width()));
              const divTwoPercent = divTwoWidth/parent.width()*100+"%";
              divTwo.width(divTwoPercent);
              //$(editor_container).height(divTwoHeight - 56);
              },
          stop: function (e, ui) {
            const parent = ui.element.parent();
            ui.element.css({ width: ui.element.width()/parent.width()*100+"%", });
            window.dispatchEvent(new Event('resize'));
            }
      });
      set_preview('on');
  } else {
      preview_state = 'off';
      set_preview('off');
      $('#btn-preview').removeClass('active');
      $('.splitter-vertical').remove();
      $('.panel-right').remove();
      $('.panel-left').resizable('destroy');
      $('.panel-left').width('100%');
      window.dispatchEvent(new Event('resize'));
  }
}

function add_filter(event) {
  var filter = $(this).parent().parent();
  filterNum++;
  var next_id = 'filter' + filterNum;
  var nextHtml = '<div class="table-filter" id="'+next_id+'">';
  if ($(filter).attr('id') == 'filter0') {
    $(this).html('<i class="fa fa-minus fa-sm"></i>');
    $(this).removeClass('add_filter');
    $(this).addClass('remove_filter');
    $(this).parent().prepend('<button class="btn filters-btn" onclick="save_filter_set()">Save</button><button class="btn filters-btn" onclick="apply_filters()">Apply</button>');
  } else {
    var op_select = create_select(filters, next_id, 'operator');
    nextHtml += op_select;
  };
  var select_id = next_id+'_sel';
  var select = create_select(filters, next_id, 'initial');
  nextHtml += select;
  nextHtml += '<div class="filter_buttons"><button class="btn filters-btn remove_filter" type="button"><i class="fa fa-minus fa-sm"></i></button>';
  nextHtml += '<button class="btn filters-btn add_filter" type="button" id="btn'+filterNum+'"><i class="fa fa-plus fa-sm"></i></button></div></div>';
  $(filter).after(nextHtml);
  if ($(filter).attr('id') != 'filter0') {
    $('#'+next_id+'_op').selectize();
    $('#'+next_id+'_op').parent().find('.selectize-input').css('min-width', '30px');
  }
  let swidth = $('#'+select_id).width();
  $('#'+select_id).selectize().on('change.dalme', filter_next);
  $('#'+select_id).parent().find('.selectize-input').css('min-width', swidth);
  filter_register[next_id] = [];
}

function filter_next() {
  var selected = $(this).val();
  var container = $(this).parent();
  var filter_id = container.parent().attr('id');
  container.parent().attr('data-filter-type', filters[selected]['type']);
  var fe = filter_register[filter_id];
  var fields_with_lookups = ['text', 'integer', 'date', 'datetime'];
  for (let i = 0, len = fe.length; i < len; ++i) {
    $('#'+filter_id+'_el'+i).remove()
  };
  if ($(this).text() != 'Select filter') {
    if (fields_with_lookups.includes(filters[selected]['type'])) {
        var next_filter = create_select(filters[selected]['lookups'], filter_id, 'lookups');
        next_filter += '<input type="text" class="form-control filter-text" id="'+filter_id+'_el1">';
        filter_register[filter_id].push(filter_id+'_el1');
        if (filters[selected]['type'] == 'text') {
          next_filter += '<div class="form-check form-check-inline filter-check" id="'+filter_id+'_el2">';
          filter_register[filter_id].push(filter_id+'_el2');
          next_filter += '<input class="form-check-input" type="checkbox" value="1" id="'+filter_id+'_el2cb'+'">';
          next_filter += '<label class="form-check-label" for="'+filter_id+'_el2cb'+'">Ignore case</label></div>';
        }
    } else if (filters[selected]['type'] == 'switch') {
        var next_filter = create_switch(filter_id);
    } else if (filters[selected]['type'] == 'select') {
        var next_filter = create_select(filters[selected]['options'], filter_id);
    } else if (filters[selected]['type'] == 'check') {
        var next_filter = create_checkboxes(filters[selected]['options'], filter_id);
    } else {
        var next_filter = 'There was an error processing this filter.';
    };
    $('#'+filter_id+'_sel').parent().after(next_filter);
    if (fields_with_lookups.includes(filters[selected]['type'])) {
      $('#'+filter_id+'_el0').find('select').selectize().on('change.dalme', function() {
        create_text_set(container.parent().attr('id'));
      });
      $('#'+filter_id+'_el0').find('.selectize-input').css('min-width', '150px');
    };
    if (filters[selected]['type'] == 'select') {
        let swidth = $('#'+filter_id+'_el0').find('select').width();
        $('#'+filter_id+'_el0').find('select').selectize();
        $('#'+filter_id+'_el0').find('.selectize-input').css('min-width', swidth);
    }
  }
}

function remove_filter(event) {
  var filter = $(this).parent().parent();
  if (filter.attr('id') == 'filter0') {
    reset_filters();
  } else {
    $('#'+filter.attr('id')+'_sel').off('change.dalme');
    filter.remove();
    delete filter_register[filter.attr('id')];
  };
  if (Object.keys(filter_register).length == 1) {
    reset_filters();
  }
}

function reset_filters() {
  $('#filters-container').html('<div id="filter0" class="table-filter"><div class="filter_info">Filters</div><div class="filter_buttons"><button class="btn filters-btn add_filter" type="button"><i class="fa fa-plus fa-sm"></i></button></div></div>');
  filterNum = 0;
  filter_register = { 'filter0': [], };
  apply_filters();
}

function apply_filters() {
  const fv = collect_filters();
  if (fv != '{}') {
    update_table('&filters='+fv);
  } else {
    update_table();
  }
}

function update_table(query_data) {
  var url = remove_param('filters', dt_table.ajax.url());
  if (typeof query_data != 'undefined') { url = url + query_data; };
  dt_table.ajax.url(url).load();
}

function collect_filters() {
  var and_list = '';
  var or_list = '';
  for (let i = 1, len = Object.keys(filter_register).length; i < len; ++i) {
    let filterop = $('#filter'+i+'_op').children("option:selected").val() || 'and';
    let selected = $('#filter'+i+'_sel').children("option:selected").val();
    let fdict = filters[selected];
    let filtervalues = [];
    filtervalues = get_filter_values('filter'+i, fdict, filtervalues);
    if (filterop == 'and') {
      and_list += filtervalues+',';
    } else {
      or_list += filtervalues+',';
    };
  };
  var fv = '{';
  if (and_list !== '' || typeof wf_filters != 'undefined') {
      fv += '\'and_list\':[';
      if (and_list !== '') { fv += and_list };
      if (typeof wf_filters != 'undefined') { fv += wf_filters };
      fv += '],'
  };
  if (or_list !== '') { fv += '\'or_list\':['+or_list+'],' };
  fv += '}';
  return fv
}

function get_filter_values(filter_id, dict, filtervalues) {
  var type = dict['type'];
  if (typeof dict['lookup'] != 'undefined') {
    var field = dict['lookup'];
  } else {
    var field = dict['field'];
  };
  if (type == 'select') {
      var sel_v = $('#'+filter_id+'_el0').find('select').children("option:selected").val();
      if (sel_v == 'any') {
        var val = '{\''+field+'__isnull\':False}';
        filtervalues.push(val);
      } else if (sel_v == 'none') {
        var val = '{\''+field+'__isnull\':True}';
        filtervalues.push(val);
      } else {
        var val = '{\''+field+'\':\''+sel_v+'\'}';
        filtervalues.push(val);
      }
  } else if (type == 'text' || type == 'integer') {
      var lookup = $('#'+filter_id+'_el0').find('select').children("option:selected").val();
      if (lookup == 'isnull') {
          var val = '{\''+field+'__isnull\':True}';
          filtervalues.push(val);
      } else if (lookup == 'range') {
          var txt_v1 = $('#'+filter_id+'_el1').val();
          var txt_v2 = $('#'+filter_id+'_el3').val();
          var val = '{\''+field+'__range\':\'('+txt_v1+','+txt_v2+')\'}';
          filtervalues.push(val);
      } else if (lookup == 'in') {
          var txt_v = $('#'+filter_id+'_el1').val();
          txt_v = txt_v.split(',');
          var val = '{\''+field+'__in\':\''+txt_v+'\'}';
          filtervalues.push(val);
      } else {
          if ($('#'+filter_id+'_el2cb').prop('checked')) { lookup = 'i'+lookup; };
          var txt_v = $('#'+filter_id+'_el1').val();
          var val = '{\''+field+'__'+lookup+'\':\''+txt_v+'\'}';
          filtervalues.push(val);
      };
  } else if (type == 'check') {
      var cboxes = filter_register[filter_id];
      for (let i = 0, len = cboxes.length; i < len; ++i) {
        if ($('#'+cboxes[i]+'cb').is(':checked')) {
          if ($('#'+cboxes[i]+'cb').val() == 'none') {
            var val = '{\''+field+'__isnull\':True}';
          } else {
            var val = '{\''+field+'\':\''+$('#'+cboxes[i]+'cb').val()+'\'}';
          };
          filtervalues.push(val);
        };
      };
  } else if (type == 'switch') {
      if ($('#'+filter_id+'_el0cb').is(':checked')) {
        var val = '{\''+field+'\':\'1\'}';
        filtervalues.push(val);
      };
  };
  return filtervalues
}

function save_filter_set() {
  var url_params = dt_table.ajax.url().split("/");
  $.ajax({
    method: "GET",
    url: "/"+url_params[1]+"/"+url_params[2]+"/get_workset/"+url_params[3],
    data: dt_table.ajax.params()
  }).done(function(data, textStatus, jqXHR) {
        save_filter_form(data.data, url_params[2]);
  }).fail(function(jqXHR, textStatus, errorThrown) {
        toastr.error('There was an error communicating with the server: '+errorThrown);
  });
}

function save_filter_form(qset, endpoint) {
    filterForm = new $.fn.dataTable.Editor( {
          ajax: {
            method: "POST",
            url: "/api/sets/",
            headers: { 'X-CSRFToken': get_cookie("csrftoken") },
            data: { 'qset': JSON.stringify(qset), 'endpoint': endpoint, 'type': 4 },
          },
          fields: [
                {
                  label: "Name:",
                  name:  "name"
                },
                {
                  label: "Description:",
                  name:  "description",
                  type: "textarea"
                },
                {
                  label: "Permissions:",
                  name:  "set_permissions",
                  type: "selectize",
                  options: [
                    { label: "Private", value: "1" },
                    { label: "Others: view", value: "2" },
                    { label: "Others: view|add", value: "3" },
                    { label: "Others: view|add|delete", value: "4" },
                  ],
                }
          ]
    });
    filterForm.on('submitSuccess', function(e, json, data, action) { toastr.success('The set was saved successfully.') });
    filterForm.buttons({
      text: "Save",
      className: "btn btn-primary",
      action: function () { this.submit(); }
    }).title('Create New Workset').create();
}

/*** utility functions for creating specific filter types ***/
function create_select(dict, filter_id, type) {
  if (type == 'operator') {
    let id = filter_id + '_op'
    var select = '<div class="sel_container"><select id="'+id+'">'
    select += '<option selected value="and">and</option>';
    select += '<option value="or">or</option></select></div>';
  } else {
      if (type == 'initial') {
        var select = '<div class="sel_container"><select id="'+filter_id+'_sel"><option selected>Select filter</option>';
      } else {
        var select = '<div id="'+filter_id+'_el0"><select>';
      };
      for (let i = 0, len = dict.length; i < len; ++i) {
        if (dict[i]['label'] == 'divider') {
          select += '<option disabled>──────</option>';
        } else {
          select += '<option ';
          if (i == 0 && type != 'initial') { select += 'selected '};
          s_value = dict[i]['value'];
          if (type == 'initial') { s_value = i };
          select += 'value="'+s_value+'">'+dict[i]['label']+'</option>';
        }
      };
      select += '</select></div>';
      if (type != 'initial') { filter_register[filter_id].push(filter_id+'_el0') };
  };
  return select
}

function create_switch(filter_id) {
  let id = filter_id + '_el0'
  let _switch = '<div class="custom-control custom-switch filter-switch" id="'+id+'">';
  _switch += '<input type="checkbox" class="custom-control-input" id="'+id+'cb'+'">';
  _switch += '<label class="custom-control-label" for="'+id+'cb'+'"></label></div>';
  filter_register[filter_id].push(id)
  return _switch
}

function create_checkboxes(dict, filter_id) {
  let chkboxes = '';
  for (let i = 0, len = dict.length; i < len; ++i) {
      let cnt = i
      let id = filter_id+'_el'+cnt;
      chkboxes += '<div class="form-check form-check-inline filter-check" id="'+id+'">';
      chkboxes += '<input class="form-check-input" type="checkbox" value="'+dict[i]['value']+'" id="'+id+'cb'+'">';
      chkboxes += '<label class="form-check-label" for="'+id+'cb'+'">'+dict[i]['label']+'</label></div>';
      filter_register[filter_id].push(id)
  };
  return chkboxes
}

function create_text_set(filter_id) {
  var lookup = $('#'+filter_id+'_el0').find('select').children("option:selected").val();
  var i_lookups = ['exact', 'contains','startswith','endswith', 'regex'];
  const fe = filter_register[filter_id];
  for (let i = 1, len = fe.length; i < len; ++i) {
    $('#'+filter_id+'_el'+i).remove()
  };
  if (lookup != 'isnull') {
      var id = 1;
      var textset = '<input type="text" class="form-control filter-text" id="'+filter_id+'_el1">';
      id = id+1;
      filter_register[filter_id].push(filter_id+'_el1');
      if (lookup == 'range') {
        textset += '<div class="filter-inline-text" id="'+filter_id+'_el2">to</div><input type="text" class="form-control filter-text" id="'+filter_id+'_el3">';
        filter_register[filter_id].push(filter_id+'_el2');
        filter_register[filter_id].push(filter_id+'_el3');
        id = id+2;
      }
      if ($('#'+filter_id).attr('data-filter-type') == 'text' && i_lookups.includes(lookup)) {
        textset += '<div class="form-check form-check-inline filter-check" id="'+filter_id+'_el'+id+'">';
        filter_register[filter_id].push(filter_id+'_el'+id);
        textset += '<input class="form-check-input" type="checkbox" value="1" id="'+filter_id+'_el'+id+'cb'+'">';
        textset += '<label class="form-check-label" for="'+filter_id+'_el'+id+'cb'+'">Ignore case</label></div>';
      }
      $('#'+filter_id+'_el0').after(textset);
      if (lookup == 'date') {
        $('#'+filter_id+'_el1').datepicker({dateformat:"YYYY-MM-DD"})
      };
      if (lookup == 'time') {
        $('#'+filter_id+'_el1').datepicker({dateformat:"HH:MM"})
      };
  }
}
