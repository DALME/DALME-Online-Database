function createDatatable(target, helper) {
  if (typeof dt_editor_options !== 'undefined') {
    dt_editor_options['table'] = target;
    dt_editor = new $.fn.dataTable.Editor(dt_editor_options);
    if (helper != 'None') { initializeHelper(dt_editor); };
    if (typeof dt_editor_buttons !== 'undefined') {
      var buttons = dt_editor_buttons;
      var index, len;
      for (index = 0, len = buttons.length; index < len; ++index) {
        var dict = { 'extend': buttons[index].extend, 'text': buttons[index].text, 'editor': dt_editor};
        dt_options.buttons.push(dict);
      };
    };
  };
  dt_table = $(target).DataTable(dt_options);
}

function addDtToolbarButton(button) {
  if (button == 'filters') {
    filters_btn_container = document.getElementById("filters-button-ct");
    filters_container = document.getElementById("filters-container");
    filters_btn_container.innerHTML = '<button class="btn btn-secondary buttons-collection" id="btn-filters" data-toggle="collapse" data-target="#filters-container" aria-expanded="false" aria-controls="filters-container" type="button" onclick="this.classList.toggle(\'active\')"><i class="fa fa-filter fa-sm"></i> Filters</button>';
    var search_box = document.getElementById("dataTables-list_filter").getElementsByClassName("form-control")[0];
    search_box.style.borderTopRightRadius = "0";
    search_box.style.borderBottomRightRadius = "0";
    resetFilters();
    $('#filters-container').on('click', '.add_filter', addFilter);
    $('#filters-container').on('click', '.remove_filter', removeFilter);
  }
}

function saveFilterSet() {
  alert('save search triggered');
}

function applyFilters() {
  var fv = collectFilters();
  var filter_str = '&filters='+fv
  updateTable(filter_str)
}

function updateTable(filters) {
  var dt = $('#dataTables-list').DataTable();
  var dt_url = removeParam('filters', dt.ajax.url())
  var new_url = dt_url + filters;
  dt.ajax.url(new_url).load();
}

function collectFilters() {
  var filtervalues = [];
  var index, len;
  for (index = 1, len = Object.keys(filter_register).length; index < len; ++index) {
    var filter_id = 'filter'+index;
    var i_select = document.getElementById(filter_id+'_sel');
    var selected = i_select.options[i_select.selectedIndex].value;
    var fdict = filters[selected];
    var filtervalues = getFilterValues(filter_id, fdict, filtervalues);
  };
  //process filtervalues
  var and_list = '';
  var or_list = '';
  for (index = 0, len = filtervalues.length; index < len; ++index) {
    if (filtervalues[index][0] == 'and') {
      and_list += filtervalues[index][1]+',';
    } else {
      or_list += filtervalues[index][1]+',';
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
  if (type == 'select') {
    var select = document.getElementById(filter_id+'_el0');
    var sel_v = select.options[select.selectedIndex].text;
    var field = dict['field'];
    if (sel_v == 'Any') {
      var val = '{\''+field+'__isnull\':\'False\'}';
      filtervalues.push([op, val]);
    } else if (sel_v == 'None') {
      var val = '{\''+field+'__isnull\':\'True\'}';
      filtervalues.push([op, val]);
      val = '{\''+field+'__exact\':\'\'}';
      filtervalues.push([op, val]);
    } else {
      var val = '{\''+field+'\':\''+sel_v+'\'}';
      filtervalues.push([op, val]);
    }

  } else if (type == 'text') {
    var select = document.getElementById(filter_id+'_el0');
    var sel_v = select.options[select.selectedIndex].value;
    var txt_v = document.getElementById(filter_id+'_el1').value;
    var field = dict['field'] + '__' + sel_v;
    var val = '{\''+field+'\':\''+txt_v+'\'}';
    filtervalues.push([op, val]);
  } else if (type == 'check') {
    var cboxes = filter_register[filter_id];
    var index, len;
    for (index = 0, len = cboxes.length; index < len; ++index) {
      var cb = document.getElementById(cboxes[index]+'cb');
      if (cb.checked) {
        if (cb.value == 'None') {
          var val = '{\''+dict['field']+'__isnull\':\'True\'}';
        } else {
          var val = '{\''+dict['field']+'\':\''+cb.value+'\'}';
        };
        filtervalues.push([op, val]);
      };
    };
  } else if (type == 'switch') {
    if (document.getElementById(filter_id+'_el0cb').checked) {
      var val = '{\''+dict['field']+'\':\'1\'}';
      filtervalues.push([op, val]);
    };
  };
  return filtervalues
}

function addFilter(event) {
  var filter = this.parentElement;
  if (filter.id == 'filter0') {
    this.innerHTML = '<i class="fa fa-minus fa-sm"></i>';
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
  //alert(JSON.stringify(filter_register))
}

function filterNext() {
  var selected = this.options[this.selectedIndex].value;
  var filter_id = this.parentElement.id;
  var fe = filter_register[filter_id];
  var index, len;
  for (index = 0, len = fe.length; index < len; ++index) {
    var id = filter_id + '_el' + index
    $('#'+id).remove()
  };
  if (this.options[this.selectedIndex].text != 'Select filter') {
    if (filters[selected]['type'] == 'text') {
        next_filter = createTextset(filters[selected]['lookups'], filter_id)
    } else if (filters[selected]['type'] == 'switch') {
        next_filter = createSwitch(filter_id)
    } else if (filters[selected]['type'] == 'select') {
        next_filter = createSelect(filters[selected]['options'], filter_id)
    } else if (filters[selected]['type'] == 'check') {
        next_filter = createCheckboxes(filters[selected]['options'], filter_id)
    } else {
        next_filter = 'There was an error processing this filter.'
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
  filters_container.innerHTML = '<div id="filter0" class="table-filter clearfix"><div class="filter_info">Filter: DAM Images</div><button class="btn filters-btn add_filter" type="button"><i class="fa fa-plus fa-sm"></i></button></div>';
  filterNum = 0;
  filter_register = { 'filter0': [], };
  updateTable('');
}

function createSelect(dict, filter_id, type) {
  var id = filter_id + '_el0'
  if (type == 'initial') { id = filter_id + '_sel' };
  var select = '<select class="custom-select filter-select" id="'+id+'">'
  if (type == 'initial') { select += '<option selected>Select filter</option>'};
  var index, len;
  for (index = 0, len = dict.length; index < len; ++index) {
    if (dict[index]['label'] == 'divider') {
      select += '<option disabled>──────</option>';
    } else {
      select += '<option ';
      if (index == 0 && type != 'initial') { select += 'selected '};
      s_val = index;
      if (type == 'textlookups') { s_val = dict[index]['lookup'] };
      select += 'value="'+s_val+'">'+dict[index]['label']+'</option>';
    }
  };
  select += '</select>';
  if (type != 'initial') { filter_register[filter_id].push(id) };
  return select;
}

function createSwitch(filter_id) {
  var id = filter_id + '_el0'
  var _switch = '<div class="custom-control custom-switch filter-switch" id="'+id+'">';
  _switch += '<input type="checkbox" class="custom-control-input" id="'+id+'cb'+'">';
  _switch += '<label class="custom-control-label" for="'+id+'cb'+'">Yes</label></div>';
  filter_register[filter_id].push(id)
  return _switch
}

function createCheckboxes(dict, filter_id) {
  var chkboxes = '';
  var index, len;
  for (index = 0, len = dict.length; index < len; ++index) {
      var cnt = index
      var id = filter_id+'_el'+cnt;
      chkboxes += '<div class="form-check form-check-inline filter-check" id="'+id+'">';
      chkboxes += '<input class="form-check-input" type="checkbox" value="'+dict[index]['label']+'" id="'+id+'cb'+'">';
      chkboxes += '<label class="form-check-label" for="'+id+'cb'+'">'+dict[index]['label']+'</label></div>';
      filter_register[filter_id].push(id)
  };
  return chkboxes
}

function createTextset(dict, filter_id) {
  var textset = createSelect(dict, filter_id, 'textlookups');
  var id = filter_id + '_el1'
  textset += '<input type="text" class="form-control filter-text" id="'+id+'">';
  filter_register[filter_id].push(id)
  return textset
}
