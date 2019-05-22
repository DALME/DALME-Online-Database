function createDatatable(target, helpers, modules) {
  if (typeof dt_editor_options !== 'undefined') {
    dt_editor_options['table'] = target;
    dt_editor = new $.fn.dataTable.Editor(dt_editor_options);
    if (helpers != 'None') {
      helpers = JSON.parse(helpers.replace(/'/g, '"'));
      for (let i = 0, len = helpers.length; i < len; ++i) { eval(helpers[i]+'()'); };
    };
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
    if (modules != 'None') {
      modules = JSON.parse(modules.replace(/'/g, '"'));
      for (let i = 0, len = modules.length; i < len; ++i) { initModule(modules[i]); };
    };
    if (typeof action !== 'undefined') {
      performAction(action);
    };
  });
}

function performAction(action) {
  eval(action['action']+'(['+action['data']+'])');
}

function initModule(mod) {
  switch(mod) {
    case 'filters':
        $('#dataTables-list_filter').parent().prepend('<button class="btn dt-btn buttons-collection" id="btn-filters" data-toggle="collapse" data-target="#filters-container" aria-expanded="false" aria-controls="filters-container" type="button" onclick="this.classList.toggle(\'active\')"><i class="fa fa-filter fa-sm"></i> Filters</button>');
        $('#dataTables-list_filter .form-control')[0].style.borderTopLeftRadius = "0";
        $('#dataTables-list_filter .form-control')[0].style.borderBottomLeftRadius = "0";
        $('#btn-filters').css("margin-right","-1px");
        resetFilters();
        $('#filters-container').on('click', '.add_filter', addFilter);
        $('#filters-container').on('click', '.remove_filter', removeFilter);
        break;
    case 'preview':
        $('.dt-buttons').append('<button class="btn dt-btn buttons-collection" id="btn-preview" onclick="togglePreview()"><i class="fa fa-eye fa-sm"></i> Preview</button>');
        break;
    case 'fieldsets':
        var button_html = '<div class="btn-group dropdown"><button class="btn buttons-collection dropdown-toggle" id="fieldsets_button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false"><i class="fa fa-swatchbook fa-sm"></i> Fieldsets</button><div class="dropdown-menu" aria-labelledby="fieldsets_button">';
        for (const prop in dt_fieldsets) {
            if (dt_fieldsets.hasOwnProperty(prop)) { button_html += '<a class="dt-button dropdown-item" href="#" onclick="toggleColumns(this)"><span>'+ prop +'</span></a>'; }
        };
        button_html += '</div></div>';
        $('.dt-buttons').append(button_html);
        break;
    case 'form':
        dt_editor.on('open.dalme', source_form_on);
        dt_editor.on('close.dalme', source_form_off);
  }
}

function toggleInlineEdit() {
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

function toggleColumns(button) {
  $(button).parent().find('.active').removeClass('active');
  $(button).toggleClass('active');
  var range = dt_fieldsets[$(button).text()];
  for (let i = 3; i < dt_table.columns().count(); ++i) {
    range.includes(i) ? dt_table.column(i).visible(true) : dt_table.column(i).visible(false);
  };
  dt_table.columns.adjust().draw();
  window.dispatchEvent(new Event('resize'));
}

function togglePreview() {
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

function addFilter(event) {
  var filter = $(this).parent().parent();
  filterNum++;
  var next_id = 'filter' + filterNum;
  var nextHtml = '<div class="table-filter" id="'+next_id+'">';
  if ($(filter).attr('id') == 'filter0') {
    $(this).html('<i class="fa fa-minus fa-sm"></i>');
    $(this).removeClass('add_filter');
    $(this).addClass('remove_filter');
    $(this).parent().prepend('<button class="btn filters-btn" onclick="saveFilterSet()">Save</button><button class="btn filters-btn" onclick="applyFilters()">Apply</button>');
  } else {
    var op_select = createSelect(filters, next_id, 'operator');
    nextHtml += op_select;
  };
  var select_id = next_id+'_sel';
  var select = createSelect(filters, next_id, 'initial');
  nextHtml += select;
  nextHtml += '<div class="filter_buttons"><button class="btn filters-btn remove_filter" type="button"><i class="fa fa-minus fa-sm"></i></button>';
  nextHtml += '<button class="btn filters-btn add_filter" type="button" id="btn'+filterNum+'"><i class="fa fa-plus fa-sm"></i></button></div></div>';
  $(filter).after(nextHtml);
  $('#'+select_id).on('change.dalme', filterNext);
  filter_register[next_id] = [];
}

function filterNext() {
  var selected = $(this).children("option:selected").val();
  var filter_id = $(this).parent().attr('id');
  $(this).parent().attr('data-filter-type', filters[selected]['type']);
  var fe = filter_register[filter_id];
  var fields_with_lookups = ['text', 'integer', 'date', 'datetime'];
  for (let i = 0, len = fe.length; i < len; ++i) {
    $('#'+filter_id+'_el'+i).remove()
  };
  if ($(this).children("option:selected").text() != 'Select filter') {
    if (fields_with_lookups.includes(filters[selected]['type'])) {
        var next_filter = createSelect(filters[selected]['lookups'], filter_id, 'lookups');
        next_filter += '<input type="text" class="form-control filter-text" id="'+filter_id+'_el1">';
        filter_register[filter_id].push(filter_id+'_el1');
        if (filters[selected]['type'] == 'text') {
          next_filter += '<div class="form-check form-check-inline filter-check" id="'+filter_id+'_el2">';
          filter_register[filter_id].push(filter_id+'_el2');
          next_filter += '<input class="form-check-input" type="checkbox" value="1" id="'+filter_id+'_el2cb'+'">';
          next_filter += '<label class="form-check-label" for="'+filter_id+'_el2cb'+'">Ignore case</label></div>';
        }
    } else if (filters[selected]['type'] == 'switch') {
        var next_filter = createSwitch(filter_id);
    } else if (filters[selected]['type'] == 'select') {
        var next_filter = createSelect(filters[selected]['options'], filter_id);
    } else if (filters[selected]['type'] == 'check') {
        var next_filter = createCheckboxes(filters[selected]['options'], filter_id);
    } else {
        var next_filter = 'There was an error processing this filter.';
    };
    $('#'+filter_id+'_sel').after(next_filter);
    if (fields_with_lookups.includes(filters[selected]['type'])) {
      $('#'+filter_id+'_el0').on('change.dalme', function() {
        createTextset($(this).parent().attr('id'));
      });
    }
  }
}

function removeFilter(event) {
  var filter = $(this).parent().parent();
  if (filter.attr('id') == 'filter0') {
    resetFilters();
  } else {
    $('#'+filter.attr('id')+'_sel').off('change.dalme');
    filter.remove();
    delete filter_register[filter.attr('id')];
  };
  if (Object.keys(filter_register).length == 1) {
    resetFilters();
  }
}

function resetFilters() {
  $('#filters-container').html('<div id="filter0" class="table-filter"><div class="filter_info">Filters</div><div class="filter_buttons"><button class="btn filters-btn add_filter" type="button"><i class="fa fa-plus fa-sm"></i></button></div></div>');
  filterNum = 0;
  filter_register = { 'filter0': [], };
  updateTable('');
}

function applyFilters() {
  const fv = collectFilters();
  const filter_str = '&filters='+fv;
  updateTable(filter_str);
}

function updateTable(filters) {
  var dt = $('#dataTables-list').DataTable();
  var dt_url = removeParam('filters', dt.ajax.url())
  var new_url = dt_url + filters;
  dt.ajax.url(new_url).load();
}

function collectFilters() {
  var and_list = '';
  var or_list = '';
  for (let i = 1, len = Object.keys(filter_register).length; i < len; ++i) {
    let filterop = $('#filter'+i+'_op').children("option:selected").val() || 'and';
    let selected = $('#filter'+i+'_sel').children("option:selected").val();
    let fdict = filters[selected];
    let filtervalues = [];
    filtervalues = getFilterValues('filter'+i, fdict, filtervalues);
    if (filterop == 'and') {
      and_list += filtervalues+',';
    } else {
      or_list += filtervalues+',';
    };
  };
  var fv = '{';
  if (and_list !== '') { fv += '\'and_list\':['+and_list+'],' };
  if (or_list !== '') { fv += '\'or_list\':['+or_list+'],' };
  fv += '}';
  return fv
}

function getFilterValues(filter_id, dict, filtervalues) {
  var type = dict['type'];
  var field = dict['field'];
  //var lookup = typeof dict['lookup'] != 'undefined' ? dict['lookup'] : '';
  if (type == 'select') {
      var sel_v = $('#'+filter_id+'_el0').children("option:selected").val();
      // var select = document.getElementById(filter_id+'_el0');
      // var sel_v = select.options[select.selectedIndex].text;
      if (sel_v == 'any') {
        var val = '{\''+field+'__isnull\':\'False\'}';
        filtervalues.push(val);
      } else if (sel_v == 'none') {
        var val = '{\''+field+'__isnull\':\'True\'}';
        filtervalues.push(val);
        val = '{\''+field+'__exact\':\'\'}';
        filtervalues.push(val);
      } else {
        var val = '{\''+field+'\':\''+sel_v+'\'}';
        filtervalues.push(val);
      }
  } else if (type == 'text' || type == 'integer') {
      var lookup = $('#'+filter_id+'_el0').children("option:selected").val();
      if (lookup == 'isnull') {
          var val = '{\''+field+'__isnull\':\'True\'}';
          filtervalues.push(val);
          val = '{\''+field+'__exact\':\'\'}';
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
            var val = '{\''+field+'__isnull\':\'True\'}';
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

function saveFilterSet() {
  var data = JSON.parse(dt_table.ajax.params().data);
  var url = dt_table.ajax.url();
  var filters = collectFilters();
  var query = {
    'order_field': data.columns[data.order[0].column].data,
    'order_dir': data.order[0].dir,
    'filters': filters,
    'api': url.split("/")[2]
  };
  if (typeof data.search.value != 'undefined') {
    query['search'] = data.search.value;
  };
  saveFilterForm(query);
}

function saveFilterForm(query) {
  filterForm = new $.fn.dataTable.Editor( {
        ajax: {
          method: "POST",
          url: "/api/worksets/",
          headers: { 'X-CSRFToken': getCookie("csrftoken") },
          data: { 'query': JSON.stringify(query) },
        },
        fields: [{
                label: "Name:",
                name:  "name"
              }, {
                label: "Description:",
                name:  "description",
                type: "textarea"
              }]
    });
    filterForm.buttons({
      text: "Save",
      className: "btn btn-primary",
      action: function () { this.submit(); }
    }).title('Create New Workset').create();
}

/*** utility functions for creating specific filter types ***/
function createSelect(dict, filter_id, type) {
  if (type == 'operator') {
    let id = filter_id + '_op'
    var select = '<select class="custom-select filter-select" id="'+id+'">'
    select += '<option selected value="and">and</option>';
    select += '<option value="or">or</option></select>';
  } else {
      let id = filter_id + '_el0'
      if (type == 'initial') { id = filter_id + '_sel' };
      var select = '<select class="custom-select filter-select" id="'+id+'">'
      if (type == 'initial') { select += '<option selected>Select filter</option>'};
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
      select += '</select>';
      if (type != 'initial') { filter_register[filter_id].push(id) };
  };
  return select
}

function createSwitch(filter_id) {
  let id = filter_id + '_el0'
  let _switch = '<div class="custom-control custom-switch filter-switch" id="'+id+'">';
  _switch += '<input type="checkbox" class="custom-control-input" id="'+id+'cb'+'">';
  _switch += '<label class="custom-control-label" for="'+id+'cb'+'"></label></div>';
  filter_register[filter_id].push(id)
  return _switch
}

function createCheckboxes(dict, filter_id) {
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

function createTextset(filter_id) {
  var lookup = $('#'+filter_id+'_el0').children("option:selected").val();
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
