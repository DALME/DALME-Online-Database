function workflow_module_load() {

}

function workflow_module_init() {
  $.ajax({
    method: "POST",
    url: `${api_endpoint}/configs/get/`,
    xhrFields: { withCredentials: true },
    crossDomain: true,
    headers: {
      "Content-Type": "application/json",
      'X-CSRFToken': get_cookie("csrftoken")
    },
    data: JSON.stringify({
      'target': 'workflow_menu'
    })
  }).done(function(data, textStatus, jqXHR) {
      workflow_filter_on = false;
      var wf_menu = data[0];
      var container = $('<div class="btn-group dropdown" id="wf-menu-dropdown"></div>');
      var dropdown = $('<div class="dropdown-menu wf-dropdown" id="workflow-filters" aria-labelledby="workflow_button"></div>');

      var select_container = '';
      for (let i = 0, len = wf_menu.length; i < len; ++i) {
          let item = wf_menu[i];
          switch(item['type']) {
              case 'title':
                  $(dropdown).append('<div class="dropdown-title">' + item['text'] + '</div>');
                  break;
              case 'message':
                  $(dropdown).append('<div class="dropdown-text">' + item['text'] + '</div>');
                  break;
              case 'divider':
                  $(dropdown).append('<div class="dropdown-divider"></div>');
                  break;
              case 'item':
                  $(dropdown).append('<a class="dt-button dropdown-item dd-keep-open" href="#" data-wf-group="' + item['group'] + '" data-wf-query="' + item['query'] + '">'+ item['text'] +'</a>');
                  break;
              case 'item-select':
                  select_container = '<div class="dropdown-select dropdown-item">'
                  select_container += '<a class="dt-button dropdown-item-select dd-keep-open mr-1" href="#" data-wf-group="' + item['group'] + '" data-wf-query="' + item['query'] + '">' + item['text'] + '</a>'

                  if (item.hasOwnProperty('query-awaiting')) {
                    select_container += '<a class="dt-button dropdown-tag dd-keep-open" href="#" data-wf-group="' + item['group'] + '" data-wf-query="' + item['query-awaiting'] + '">awaiting</a>'
                  }
                  if (item.hasOwnProperty('query-in-progress')) {
                    select_container += '<a class="dt-button dropdown-tag dd-keep-open" href="#" data-wf-group="' + item['group'] + '" data-wf-query="' + item['query-in-progress'] + '">in progress</a>'
                  }
                  if (item.hasOwnProperty('query-done')) {
                   select_container += '<a class="dt-button dropdown-item-select dd-keep-open" href="#" data-wf-group="' + item['group'] + '" data-wf-query="' + item['query-done'] + '"><i class="far fa-check-circle fa-fw"></i></a>'
                  }
                  if (item.hasOwnProperty('query-not-done')) {
                    select_container += '<a class="dt-button dropdown-item-select dd-keep-open" href="#" data-wf-group="' + item['group'] + '" data-wf-query="' + item['query-not-done'] + '"><i class="far fa-times-circle fa-fw"></i></i></a></div>'
                  }

                  $(dropdown).append(select_container);
          };
      };

      $(dropdown).append('<div class="dropdown-divider"></div><a class="dt-button dropdown-item wf-action" href="#" data-action="clear">Clear All</a><a class="dt-button dropdown-item wf-action" href="#" data-action="submit">Submit Filter</a>');
      $(container).append('<button class="btn buttons-collection dropdown-toggle" id="workflow_button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false"><i class="fa fa-code-branch fa-sm"></i> Workflow</button>');
      $(container).append(dropdown);
      container.insertAfter($('.buttons-page-length').parent());

      $('#workflow-filters a').on('click', function(e) {
        if ($(this).hasClass('dd-keep-open')) {
            workflow_filter_toggle(this);
            e.stopPropagation();
        } else {
            let action = $(this).data('action')
            if (action == 'clear') {
              workflow_filter_clear()
              e.stopPropagation();
            } else if (action == 'submit') {
              workflow_filter_submit()
            }
        }
      });

  }).fail(function(jqXHR, textStatus, errorThrown) {
      toastr.error('The following error occured while attempting to retrieve the data for the Workflow menu: ' + errorThrown);
  });
}

function workflow_filter_submit() {
  let fields = ['wf_status',
                'help_flag',
                'is_public',
                'wf_stage',
                'ingestion_done',
                'transcription_done',
                'markup_done',
                'review_done',
                'parsing_done',
                'last_modified']
  let filters = {}
  let clear = []

  if ($('#workflow-filters').find('.active').length) {
    $('#workflow-filters').find('.active').each(function() {
      if (typeof $(this).data('wf-query') !== 'undefined') {
        el = $(this)
        eval('var query = ' + el.data('wf-query'));
        for (const prop in query) {
          if (query.hasOwnProperty(prop)) {
              filters[prop] = query[prop]
          }
        }
      }
    });
  }

  for (let i = 0, len = fields.length; i < len; ++i) {
    if (!filters.hasOwnProperty(fields[i])) {
      clear.push(fields[i])
    }
  }
  filter_set(filters, clear);
}

function workflow_filter_clear() {
  $('#workflow-filters').find('.active').each(function() {
    $(this).removeClass('active');
  })
  if ($('.wf-dropdown').find('.active').length) {
    $('#workflow_button').addClass('active');
  } else {
    $('#workflow_button').removeClass('active');
  }
}

function workflow_filter_toggle(el) {
  if ($(el).hasClass('active')) {
    $(el).removeClass('active');
    if (!$(el).hasClass('dropdown-item')) {
      $(el).parent().removeClass('active');
    }
  } else {
    if ($('#workflow-filters').find('[data-wf-group=' + $(el).data('wf-group') + ']').filter('.active').length) {
      $('#workflow-filters').find('[data-wf-group=' + $(el).data('wf-group') + ']').filter('.active').each(function() {
        $(this).removeClass('active');
        if (!$(this).hasClass('dropdown-item')) {
          $(this).parent().removeClass('active');
        }
      });
    }
    $(el).addClass('active');
    if (!$(el).hasClass('dropdown-item')) {
      $(el).parent().addClass('active');
    }
  }
  if ($('.wf-dropdown').find('.active').length) {
    $('#workflow_button').addClass('active');
  } else {
    $('#workflow_button').removeClass('active');
  }
}
