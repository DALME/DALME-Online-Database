function addDtToolbarButton(button) {
  if (button == 'filters') {
    filters_btn_container = document.getElementById("filters-button-ct");
    filters_container = document.getElementById("filters-container");
    filters_btn_container.innerHTML = '<button class="btn btn-secondary buttons-collection" id="btn-filters" data-toggle="collapse" data-target="#filters-container" aria-expanded="false" aria-controls="filters-container" type="button" onclick="this.classList.toggle(\'active\')"><i class="fa fa-filter fa-sm"></i> Filters</button>';
    var search_box = document.getElementById("dataTables-list_filter").getElementsByClassName("form-control")[0];
    search_box.style.borderTopRightRadius = "0";
    search_box.style.borderBottomRightRadius = "0";
    filters_container.innerHTML = '<div id="filter0" class="table-filter clearfix"><div class="filter_info">Filter: DAM Images</div><button class="btn filters-btn add_filter" type="button" id="btn0"><i class="fa fa-plus fa-sm"></i></button></div>';
    filterNum = 0;
    filter_register = { 'filter0': [], };
    $('#filters-container').on('click', '.add_filter', addFilter);
    $('#filters-container').on('click', '.remove_filter', removeFilter);
  }
}

function saveFilterSet() {
  alert('save search triggered');
}

function applyFilters() {
  var fv = collectFilters();
  alert(JSON.stringify(fv));
  //get datatables ajax url
  var dt = $('#dataTables-list').DataTable();
  var filter_str = '&filters="'+JSON.stringify(fv)+'"'
  var dt_url = dt.ajax.url();
  //add filters to url in a way the API will recognize
  var new_url = dt_url + filter_str;
  //push url to datatables and force redraw -> ajax.url().load()
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
    var fvalues = getFilterValues(filter_id, fdict);
    filtervalues.push(fvalues)
  };
  return filtervalues
}

function getFilterValues( filter_id, dict ) {
  var type = dict['type'];
  if (type == 'select') {
    var select = document.getElementById(filter_id+'_el0');
    var sel_v = select.options[select.selectedIndex].text;
    var field = dict['field'];
    //var val = '&'+field + '="' + sel_v + '"';
    var val = [field,sel_v];
  } else if (type == 'text') {
    var select = document.getElementById(filter_id+'_el0');
    var sel_v = select.options[select.selectedIndex].value;
    var txt_v = document.getElementById(filter_id+'_el1').value;
    var field = dict['field'] + '__' + sel_v;
    //var val = '&'+field+'__'+sel_v+'="' + txt_v + '"';
    var val = [field,txt_v];
  } else if (type == 'check') {
    var cboxes = filter_register[filter_id];
    var index, len;
    var val = [];
    for (index = 0, len = cboxes.length; index < len; ++index) {
      var cb = document.getElementById(cboxes[index]+'cb');
      if (cb.checked) {
        //val += '&' + dict['field'] + '="' + cb.value + '"';
        val.push([dict['field'],cb.value]);
      };
    };
  } else if (type == 'switch') {
    if (document.getElementById(filter_id+'_el0cb').checked) {
      //var val = '&'+dict['field'] + '=' + "1";
      var val = [dict['field'],1];
    } else {
      var val = [];
    };
  } else {
    var val = [];
  };
  return val
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
    filters_container.innerHTML = '<div id="filter0" class="table-filter clearfix"><div class="filter_info">Filter: DAM Images</div><button class="btn filters-btn add_filter" type="button"><i class="fa fa-plus fa-sm"></i></button><button class="btn filters-btn" type="button" onclick="filtersSaveSearch()">Save</button></div>';
    filterNum = 0;
  } else {
    filter.remove();
  }
}

function createSelect(dict, filter_id, type) {
  var id = filter_id + '_el0'
  if (type == 'initial') { id = filter_id + '_sel' };
  var select = '<select class="custom-select filter-select" id="'+id+'">'
  if (type == 'initial') { select += '<option selected>Select filter</option>'};
  var index, len;
  for (index = 0, len = dict.length; index < len; ++index) {
    select += '<option ';
    if (index == 0 && type != 'initial') { select += 'selected '};
    s_val = index;
    if (type == 'textlookups') { s_val = dict[index]['lookup'] };
    select += 'value="'+s_val+'">'+dict[index]['label']+'</option>';
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
