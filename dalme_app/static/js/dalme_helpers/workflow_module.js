function workflow_module_load() {

}

function workflow_module_init() {
  $.ajax({
    method: "POST",
    url: "/api/configs/get/",
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
      var container = $('<div class="btn-group dropdown"></div>');
      var dropdown = $('<div class="dropdown-menu wf-dropdown" aria-labelledby="workflow_button"></div>');
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
                  $(dropdown).append('<a class="dt-button dropdown-item" href="#" data-wf-query="' + item['query'] + '">'+ item['text'] +'</a>');
                  break;
              case 'item-select':
                  select_container = '<div class="dropdown-select dropdown-item">'
                  select_container += '<a class="dt-button dropdown-item-select mr-1" href="#" data-wf-query="' + item['query'] + '}">' + item['text'] + '</a>'
                  if (item['text'] != 'Ingestion') {
                    select_container += '<a class="dt-button dropdown-tag" href="#" data-wf-query="' + item['query'] + '-1, \'wf_status\': 3}">awaiting</a>'
                  }
                  select_container += '<a class="dt-button dropdown-tag" href="#" data-wf-query="' + item['query'] + ', \'wf_status\': 2}">in progress</a>'
                  select_container += '<a class="dt-button dropdown-item-select" href="#" data-wf-query="' + item['query'] + ', \'wf_status\': 3}"><i class="far fa-check-circle fa-fw"></i></a>'
                  select_container += '<a class="dt-button dropdown-item-select" href="#" data-wf-query="' + item['query'] + ', \'wf_status__not\': 3}"><i class="far fa-times-circle fa-fw"></i></i></a></div>'
                  $(dropdown).append(select_container);
          };
      };
      $(container).append('<button class="btn buttons-collection dropdown-toggle" id="workflow_button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false"><i class="fa fa-code-branch fa-sm"></i> Workflow</button>');
      $(container).append(dropdown);
      container.insertAfter($('.buttons-page-length').parent());
      $(container).on('click.dalme', 'a', function() {
          workflow_filter(this);
      });
  }).fail(function(jqXHR, textStatus, errorThrown) {
      toastr.error('The following error occured while attempting to retrieve the data for the Workflow menu: ' + errorThrown);
  });
}

function workflow_filter(el) {
  eval('var data = ' + $(el).data('wf-query'));
  if ($(el).hasClass('active')) {
    $(el).removeClass('active');
    if (!$(el).hasClass('dropdown-item')) {
      $(el).parent().removeClass('active');
    }
    filter_set(data, options=['clear']);
  } else {
    var current = $('.wf-dropdown').find('.active')
    if (current.length) {
      eval('var current_data = ' + current.data('wf-query'));
      for (const prop in current_data) {
        if (current_data.hasOwnProperty(prop)) {
          if (!data.hasOwnProperty(prop)) {
            data[prop] = 'clear';
          }
        }
      }
      current.removeClass('active');
    }
    $(el).addClass('active');
    if (!$(el).hasClass('dropdown-item')) {
      $(el).parent().addClass('active');
    }
    filter_set(data);
  }
  if ($('.wf-dropdown').find('.active').length) {
    $('#workflow_button').addClass('active');
  } else {
    $('#workflow_button').removeClass('active');
  }
}
