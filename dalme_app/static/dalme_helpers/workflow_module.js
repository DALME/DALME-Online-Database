function workflow_module_load() {

}

function workflow_module_init() {
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
