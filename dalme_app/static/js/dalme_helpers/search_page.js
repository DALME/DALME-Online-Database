function search_page_load() {
}

function search_page_init() {
  search_context = JSON.parse($('#search_context').text());
  $('#search-form').on('change', function() { $('#id_form-PAGE').val(1); });
  $('.search-text-container').each(init_show_more);
  $('.show-more').on('click', toggle_show_more);

  $('.clear-search').on('click', clear_search);

  $('#tooltip-toggle').on('change', toggle_tooltips);
  $('[data-toggle="tooltip"]').tooltip({ delay: { "show": 400, "hide": 50 } });
  $('[data-toggle="tooltip"]').tooltip('disable');

  $('#advanced-search').on('click', '.add', add_query_row);
  $('#advanced-search').on('click', '.remove', remove_query_row);
  $('#advanced-search').on('hide.bs.collapse', function() {
    clear_search();
    toggle_search_box();
  });
  $('#advanced-search').on('show.bs.collapse', toggle_search_box);
  $('#advanced-search').on('change', '.query_field select', change_on_field);

  $('#search-help-content').on('hide.bs.collapse show.bs.collapse', function() {
    $('#help-toggle').toggleClass('active');
  });

  $('select, input').on('click', function() {
    $('[data-toggle="tooltip"]').tooltip('hide');
  });

  $('.pagination').on('click', 'button', function(e) {
    let page = $(e.target).data('page');
    $('#id_form-PAGE').val(page);
    $('#search-form').submit();
  });
}

function init_show_more(i, el) {
  if ($(el).prop('scrollHeight') > $(el).outerHeight()) {
    $(el).find('.show-more').removeClass('d-none')
  }
}

function toggle_tooltips() {
  if ($('#tooltip-toggle').prop('checked')) {
    $('[data-toggle="tooltip"]').tooltip('enable');
  } else {
    $('[data-toggle="tooltip"]').tooltip('disable');
  }
}

function toggle_show_more(e) {
  if ($(e.target).text() == 'Show more') {
    $(e.target).parent().css({"maxHeight":"1000px"});
    $(e.target).text('Show less');
  } else {
    $(e.target).parent().css({"maxHeight":"84px"});
    $(e.target).text('Show more');
  }
}

function add_query_row() {
  let formset_manager = $('#id_form-TOTAL_FORMS');
  let idx = formset_manager.val();
  $('#advanced-search-sets').append($('#form_template').html().replace(/__prefix__/g, idx));
  formset_manager.val(parseInt(idx)+1);
}

function remove_query_row(e) {
  let formset_manager = $('#id_form-TOTAL_FORMS');
  let idx = formset_manager.val();
  $(e.target).parents('.advanced-search-row').remove();
  formset_manager.val(parseInt(idx)-1);
}

function toggle_search_box() {
    $('#search_box').toggleClass('d-none');
    $('#advanced-toggle').toggleClass('active');
    $('#id_form-0-query').val('');
}

function clear_search() {
  let formset_manager = $('#id_form-TOTAL_FORMS');
  $('#advanced-search-sets').html('<div class="help-heading"><small>Use multiple statements to build a complex search query.</small></div>');
  $('#advanced-search-sets').append($('#form_template').html().replace(/__prefix__/g, formset_manager.val() - 1));
  formset_manager.val(1);
  $('#advanced-search-sets .query_op').addClass('d-none');
  $('#advanced-search-sets .query_op_first').removeClass('d-none');
  $('#id_form-0-query').val('');
  $('#results-container').html('');
  $('.search-status div').html('<small>Enter a query to search.</small>');
  $('.search-status').removeClass('search-error');
  let payload = {}
  payload[search_context['session_var']] = false
  update_session(payload);
}

function change_on_field(e) {
  let field = $(e.target).val();
  let row = $(e.target).parent().parent();
  let type = search_context['fields'][field]['type'];
  let id = row.find('.query_input').children().first().attr('id');
  let name = row.find('.query_input').children().first().attr('name');
  let input = get_input(field, type, id, name);

  if (type == 'text') {
    row.find('.query_type').removeClass('d-none')
    row.find('.query_is').html(' contains ')
    row.find('.range_type').addClass('d-none')
    row.find('.query_input').addClass('grow');

  } else {
    row.find('.query_type').addClass('d-none');
    row.find('.query_is').html(' is ');
    if (type == 'keyword') {
      row.find('.query_input').removeClass('grow');
      row.find('.range_type').addClass('d-none');
    } else {
      row.find('.range_type').removeClass('d-none');
    }
  }

  row.find('.query_field_type input').val(type);
  row.find('.query_input').html(input);
}

function get_input(field, type, id, name) {
  if (type == 'keyword') {
    var input = $('<select/>').attr({
      id: id,
      name: name,
      class: 'form-control form-control-sm',
    })
    let opts = search_context['fields'][field]['options'];
    for (let i = 0, len = opts.length; i < len; ++i) {
      input.append(`<option value="${opts[i]['value']}">${opts[i]['label']}</option>`)
    }
  } else {
    var input = $('<input/>').attr({
      type: "search",
      name: name,
      placeholder: search_context['fields'][field]['placeholder'],
      autocomplete: "off",
      autocorrect: "off",
      autocapitalize: "off",
      spellcheck: "false",
      class: "form-control form-control-sm",
      id: id,
    });
  }
  return input
}
