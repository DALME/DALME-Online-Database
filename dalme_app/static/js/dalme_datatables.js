function createDatatable(target, form_helper, callback) {
  if (typeof dt_editor_options !== 'undefined') {
    dt_editor_options['table'] = target;
    dt_editor = new $.fn.dataTable.Editor(dt_editor_options);
    if (form_helper != 'None') { initializeFormHelper(dt_editor); };
    if (typeof dt_editor_buttons !== 'undefined') {
      const buttons = dt_editor_buttons;
      for (let i = 0, len = buttons.length; i < len; ++i) {
        let dict = { 'extend': buttons[i].extend, 'text': buttons[i].text, 'editor': dt_editor};
        dt_options.buttons.push(dict);
      };
    };
  };
  dt_table = $(target).DataTable(dt_options);
  dt_table.on('init', function() {
    fix_dt_search();
    if (typeof callback !== 'undefined') {
      callback();
    }
  });
}

function addDtToolbarButton(button) {
  if (button == 'filters') {
    $('#dataTables-list_filter').parent().prepend('<button class="btn dt-btn buttons-collection" id="btn-filters" data-toggle="collapse" data-target="#filters-container" aria-expanded="false" aria-controls="filters-container" type="button" onclick="this.classList.toggle(\'active\')"><i class="fa fa-filter fa-sm"></i> Filters</button>');
    $('#dataTables-list_filter .form-control')[0].style.borderTopLeftRadius = "0";
    $('#dataTables-list_filter .form-control')[0].style.borderBottomLeftRadius = "0";
    $('#btn-filters').css("margin-right","-1px");
    resetFilters();
    $('#filters-container').on('click', '.add_filter', addFilter);
    $('#filters-container').on('click', '.remove_filter', removeFilter);
  } else if (button == 'preview') {
    $('.dt-buttons').append('<button class="btn dt-btn buttons-collection" id="btn-preview" onclick="togglePreview()"><i class="fa fa-eye fa-sm"></i> Preview</button>');
  }
}

function togglePreview() {
  if (typeof preview_state == 'undefined' || preview_state == 'off') {
      preview_state = 'on';
      maxWidth = $(window).width() - 422;
      $('#btn-preview').addClass('active');
      $('.panel-left').append('<div class="splitter-vertical ui-resizable-handle ui-resizable-e"></div>');
      $('.panel-container').append('<div class="panel-right"><div class="img-placeholder d-flex justify-content-center align-items-center"><i class="d-block fa fa-eye-slash fa-4x mt-5 mb-5"></i></div></div>');
      $('.panel-left').width('70%');
      $('.panel-right').width('30%');
      $('.panel-left').resizable({
          handles: {e: '.splitter-vertical'},
          maxWidth: maxWidth,
          minWidth: 400,
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
      initializePreviewHelper();
  } else {
      preview_state = 'off';
      $('#btn-preview').removeClass('active');
      $('.splitter-vertical').remove();
      $('.panel-right').remove();
      $('.panel-left').resizable('destroy');
      $('.panel-left').width('100%');
  }
}

function addFilter(event) {
  var filter = this.parentElement;
  if (filter.id == 'filter0') {
    $(this).html('<i class="fa fa-minus fa-sm"></i>');
    $(this).removeClass('add_filter')
    $(this).addClass('remove_filter')
    $(filter).append('<button class="btn filters-btn" type="button" onclick="applyFilters()">Apply</button><button class="btn filters-btn" type="button" onclick="saveFilterSet()">Save</button>')
  };
  filterNum++;
  var next_id = 'filter' + filterNum;
  var select_id = next_id+'_sel'
  var select = createSelect(filters, next_id, 'initial')
  var nextHtml = '<div class="table-filter clearfix" id="'+next_id+'">'+select+'\
  <button class="btn filters-btn add_filter" type="button" id="btn'+filterNum+'"><i class="fa fa-plus fa-sm"></i></button>\
  <button class="btn filters-btn remove_filter" type="button"><i class="fa fa-minus fa-sm"></i></button></div>';
  $(filter).after(nextHtml);
  $('#'+select_id).on('change', filterNext);
  filter_register[next_id] = [];
}

function filterNext() {
  const selected = this.options[this.selectedIndex].value;
  const filter_id = this.parentElement.id;
  const fe = filter_register[filter_id];
  //var index, len;
  for (let i = 0, len = fe.length; i < len; ++i) {
    let id = filter_id + '_el' + i
    $('#'+id).remove()
  };
  if (this.options[this.selectedIndex].text != 'Select filter') {
    if (filters[selected]['type'] == 'text') {
        var next_filter = createTextset(filters[selected]['lookups'], filter_id)
    } else if (filters[selected]['type'] == 'switch') {
        var next_filter = createSwitch(filter_id)
    } else if (filters[selected]['type'] == 'select') {
        var next_filter = createSelect(filters[selected]['options'], filter_id)
    } else if (filters[selected]['type'] == 'check') {
        var next_filter = createCheckboxes(filters[selected]['options'], filter_id)
    } else {
        var next_filter = 'There was an error processing this filter.'
    };
    $(this).after(next_filter);
  }
}

function removeFilter(event) {
  var filter = this.parentElement;
  if (filter.id == 'filter0') {
    resetFilters();
  } else {
    filter.remove();
    delete filter_register[filter.id];
  };
  if (Object.keys(filter_register).length == 1) {
    resetFilters();
  }
}

function resetFilters() {
  $('#filters-container').html('<div id="filter0" class="table-filter clearfix"><div class="filter_info">Filters</div><button class="btn filters-btn add_filter" type="button"><i class="fa fa-plus fa-sm"></i></button></div>');
  filterNum = 0;
  filter_register = { 'filter0': [], };
  updateTable('');
}

function applyFilters() {
  const fv = collectFilters();
  const filter_str = '&filters='+fv;
  updateTable(filter_str)
}

function updateTable(filters) {
  const dt = $('#dataTables-list').DataTable();
  const dt_url = removeParam('filters', dt.ajax.url())
  const new_url = dt_url + filters;
  dt.ajax.url(new_url).load();
}

function collectFilters() {
  var filtervalues = [];
  for (let i = 1, len = Object.keys(filter_register).length; i < len; ++i) {
    let filter_id = 'filter'+i;
    let i_select = document.getElementById(filter_id+'_sel');
    let selected = i_select.options[i_select.selectedIndex].value;
    let fdict = filters[selected];
    filtervalues = getFilterValues(filter_id, fdict, filtervalues);
  };
  var and_list = '';
  var or_list = '';
  for (let i = 0, len = filtervalues.length; i < len; ++i) {
    if (filtervalues[i][0] == 'and') {
      and_list += filtervalues[i][1]+',';
    } else {
      or_list += filtervalues[i][1]+',';
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
  var op = dict['operator'];
  var field = dict['field'];
  var lookup = typeof dict['lookup'] != 'undefined' ? dict['lookup'] : '';
  if (type == 'select') {
    var select = document.getElementById(filter_id+'_el0');
    var sel_v = select.options[select.selectedIndex].text;
    if (sel_v == 'Any') {
      var val = '{\''+field+'__isnull\':\'False\'}';
      filtervalues.push([op, val]);
    } else if (sel_v == 'None') {
      var val = '{\''+field+'__isnull\':\'True\'}';
      filtervalues.push([op, val]);
      val = '{\''+field+'__exact\':\'\'}';
      filtervalues.push([op, val]);
    } else {
      field = field + lookup;
      var val = '{\''+field+'\':\''+sel_v+'\'}';
      filtervalues.push([op, val]);
    }
  } else if (type == 'text') {
    var select = document.getElementById(filter_id+'_el0');
    var sel_v = select.options[select.selectedIndex].value;
    var txt_v = document.getElementById(filter_id+'_el1').value;
    field = field + '__' + sel_v;
    var val = '{\''+field+'\':\''+txt_v+'\'}';
    filtervalues.push([op, val]);
  } else if (type == 'check') {
    var cboxes = filter_register[filter_id];
    for (let i = 0, len = cboxes.length; i < len; ++i) {
      var cb = document.getElementById(cboxes[i]+'cb');
      if (cb.checked) {
        if (cb.value == 'None') {
          var val = '{\''+field+'__isnull\':\'True\'}';
        } else {
          field = field + lookup;
          var val = '{\''+field+'\':\''+cb.value+'\'}';
        };
        filtervalues.push([op, val]);
      };
    };
  } else if (type == 'switch') {
    if (document.getElementById(filter_id+'_el0cb').checked) {
      field = field + lookup;
      var val = '{\''+field+'\':\'1\'}';
      filtervalues.push([op, val]);
    };
  };
  return filtervalues
}

function saveFilterSet() {
  const data = dt_table.ajax.params();
  const url = dt_table.ajax.url();
  const filters = collectFilters();
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
          url: "../api/worksets/",
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
    }).title('Create new workset').create();
}

/*** utility functions for creating specific filter types ***/

function createSelect(dict, filter_id, type) {
  let id = filter_id + '_el0'
  if (type == 'initial') { id = filter_id + '_sel' };
  var select = '<select class="custom-select filter-select" id="'+id+'">'
  if (type == 'initial') { select += '<option selected>Select filter</option>'};
  //var index, len;
  for (let i = 0, len = dict.length; i < len; ++i) {
    if (dict[i]['label'] == 'divider') {
      select += '<option disabled>──────</option>';
    } else {
      select += '<option ';
      if (i == 0 && type != 'initial') { select += 'selected '};
      let s_val = i;
      if (type == 'textlookups') { s_val = dict[i]['lookup'] };
      select += 'value="'+s_val+'">'+dict[i]['label']+'</option>';
    }
  };
  select += '</select>';
  if (type != 'initial') { filter_register[filter_id].push(id) };
  return select;
}

function createSwitch(filter_id) {
  let id = filter_id + '_el0'
  let _switch = '<div class="custom-control custom-switch filter-switch" id="'+id+'">';
  _switch += '<input type="checkbox" class="custom-control-input" id="'+id+'cb'+'">';
  _switch += '<label class="custom-control-label" for="'+id+'cb'+'">Yes</label></div>';
  filter_register[filter_id].push(id)
  return _switch
}

function createCheckboxes(dict, filter_id) {
  let chkboxes = '';
  //var index, len;
  for (let i = 0, len = dict.length; i < len; ++i) {
      let cnt = i
      let id = filter_id+'_el'+cnt;
      chkboxes += '<div class="form-check form-check-inline filter-check" id="'+id+'">';
      chkboxes += '<input class="form-check-input" type="checkbox" value="'+dict[i]['label']+'" id="'+id+'cb'+'">';
      chkboxes += '<label class="form-check-label" for="'+id+'cb'+'">'+dict[i]['label']+'</label></div>';
      filter_register[filter_id].push(id)
  };
  return chkboxes
}

function createTextset(dict, filter_id) {
  let textset = createSelect(dict, filter_id, 'textlookups');
  let id = filter_id + '_el1'
  textset += '<input type="text" class="form-control filter-text" id="'+id+'">';
  filter_register[filter_id].push(id)
  return textset
}
