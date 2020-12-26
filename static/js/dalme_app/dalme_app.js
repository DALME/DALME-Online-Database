/* custom JavaScript functions used by dalme.app */
function dalme_startup(helpers) {
  $('[data-toggle="tooltip"]').tooltip({
    container: 'body',
    trigger: 'hover'
  });

  $('[data-toggle="tooltip"]').tooltip('disable');

  toastr.options = {
      "closeButton": false,
      "debug": false,
      "newestOnTop": true,
      "progressBar": true,
      "positionClass": "toast-top-right",
      "preventDuplicates": false,
      "onclick": function() { toastr.clear() },
      "showDuration": "300",
      "hideDuration": "1000",
      "timeOut": "5000",
      "extendedTimeOut": "1000",
      "showEasing": "swing",
      "hideEasing": "linear",
      "showMethod": "fadeIn",
      "hideMethod": "fadeOut"
  };

  if ($('#user-preferences').length) {
    user_prefs = JSON.parse($('#user-preferences').text());
  }

  if (typeof helpers != 'undefined' && helpers != 'None') {
    helpers = JSON.parse(helpers.replace(/'/g, '"'));
    for (let i = 0, len = helpers.length; i < len; ++i) { eval(helpers[i]+'_load()'); };
  };

  // SB Admin 2 handlers:
  // Toggle the side navigation
  $("#sidebarToggle, #sidebarToggleTop").on('click', function(e) {
    $("body").toggleClass("sidebar-toggled");
    $(".sidebar").toggleClass("toggled");
    if ($(".sidebar").hasClass("toggled")) {
      $('.sidebar .collapse').collapse('hide');
    };
  });

  // Close any open menu accordions when window is resized below 768px
  $(window).resize(function() {
    if ($(window).width() < 768) {
      $('.sidebar .collapse').collapse('hide');
    };
  });

  // Prevent the content wrapper from scrolling when the fixed side navigation hovered over
  $('body.fixed-nav .sidebar').on('mousewheel DOMMouseScroll wheel', function(e) {
    if ($(window).width() > 768) {
      var e0 = e.originalEvent,
        delta = e0.wheelDelta || -e0.detail;
      this.scrollTop += (delta < 0 ? 1 : -1) * 30;
      e.preventDefault();
    }
  });

  // Scroll to top button appear
  $(document).on('scroll', function() {
    var scrollDistance = $(this).scrollTop();
    if (scrollDistance > 100) {
      $('.scroll-to-top').fadeIn();
    } else {
      $('.scroll-to-top').fadeOut();
    }
  });

  // Smooth scrolling using jQuery easing
  $(document).on('click', 'a.scroll-to-top', function(e) {
    var $anchor = $(this);
    $('html, body').stop().animate({
      scrollTop: ($($anchor.attr('href')).offset().top)
    }, 1000, 'easeInOutExpo');
    e.preventDefault();
  });
}

function toggle_tooltips(el) {
  if ($(el).text() == 'Enable Tooltips') {
    $('[data-toggle="tooltip"]').tooltip('enable');
    $(el).html('<i class="fas fa-comment-alt fa-fw mr-2 text-gray-400"></i> Disable Tooltips');
  } else {
    $('[data-toggle="tooltip"]').tooltip('disable');
    $(el).html('<i class="fas fa-comment-alt fa-fw mr-2 text-gray-400"></i> Enable Tooltips');
  }
}

function update_workflow(action, code=0) {
    $.ajax({
        method: "PATCH",
        url: `${api_endpoint}/workflow/${source_id}/change_state/`,
        xhrFields: { withCredentials: true },
        crossDomain: true,
        headers: {
          "Content-Type": "application/json",
          'X-CSRFToken': get_cookie("csrftoken")
        },
        data: JSON.stringify({ "action": action, "code": code })
    }).done(function(data, textStatus, jqXHR) {
        if (action == 'toggle_help') {
            $('#wf-manager-help').toggleClass("wf-help_flag-on");
        } else if (action == 'toggle_public') {
            $('#wf-manager-public').toggleClass("wf-public_flag-on");
        } else {
            $('.wf-manager-status-container').html(data['status_html']);
            $('.wf-manager-info').html(data['mod_html']);
            if (action == 'stage_done') {
              $('#' + data['prev_stage_name']).find('i').removeClass('far').removeClass('fa-square').addClass('fas').addClass('fa-check');
            };
            if (action == 'begin_stage') {
              $('#' + data['stage_name']).find('i').removeClass('far').removeClass('fa-square').addClass('fas').addClass('fa-hammer');
            };
            if (action == 'change_status') {
              if (code == 1) {
                $('#assessment_menu').remove();
                $('#wf_menu').append('<a id="processing_menu" class="dropdown-item" href="#" onclick="update_workflow(\'change_status\', 2)">\
                  <i class="fas fa-clipboard-list fa-fw mr-2 text-gray-400"></i> Resume processing</a>');
              } else {
                $('#processing_menu').remove();
                $('#wf_menu').append('<a id="assessment_menu" class="dropdown-item" href="#" onclick="update_workflow(\'change_status\', 1)">\
                  <i class="fas fa-clipboard-check fa-fw mr-2 text-gray-400"></i> Place under assessment</a>');
              }
            }
        };
    }).fail(function(jqXHR, textStatus, errorThrown) {
        if (errorThrown == "Forbidden") {
          toastr.error("You do not have the required permissions to change the workflow status on this item.");
        } else {
          toastr.error('There was an error communicating with the server: '+errorThrown);
        }
    });
}

function create_task_list() {
  $.ajax({
    method: "GET",
    url: `${api_endpoint}/options/?target=user_groups&format=json`,
    xhrFields: { withCredentials: true },
    crossDomain: true,
    headers: {
      "Content-Type": "application/json",
      'X-CSRFToken': get_cookie("csrftoken")
    },
  }).done(function(data, textStatus, jqXHR) {
    const groups = data.user_groups;
    taskListForm = new $.fn.dataTable.Editor( {
          ajax: {
            method: "POST",
            url: `${api_endpoint}/tasklists/`,
            xhrFields: { withCredentials: true },
            crossDomain: true,
            headers: {
              "Content-Type": "application/json",
              'X-CSRFToken': get_cookie("csrftoken")
            },
            data: function (data) { return { "data": JSON.stringify( data ) }; }
          },
          fields: [
            {
              label: "List name",
              name: "name",
              fieldInfo: "Name of the list to be created"
            },
            {
              label: "Group",
              name:  "group",
              fieldInfo: "Group of users that will utilize the list",
              type: "selectize",
              opts: {'placeholder': "Select user group"},
              options: groups
            },
          ]
      });

      taskListForm.on('open.dalme', function(e, mode, action) {
        editor_form_setup(e, mode, action, taskListForm)
      });

      taskListForm.on('close.dalme', function(e) {
        editor_form_restore(e, taskListForm)
      });

      taskListForm.on('submitSuccess', function(e, json, data, action) {
        toastr.success('The task list was created successfully.');
        if (typeof table_lists != 'undefined') {
          table_lists.ajax.reload();
        }
      });

      taskListForm.buttons({
        text: "Create",
        className: "btn btn-primary",
        action: function () { this.submit(); }
      }).title('Create New Task List').create();
  });
}

function create_task() {
  $.ajax({
    method: "GET",
    url: `${api_endpoint}/options/?target=active_staff,user_worksets,user_task_lists&format=json`,
    xhrFields: { withCredentials: true },
    crossDomain: true,
    headers: {
      "Content-Type": "application/json",
      'X-CSRFToken': get_cookie("csrftoken")
    },
  }).done(function(data, textStatus, jqXHR) {
    const staff = data.active_staff;
    const worksets = data.user_worksets;
    const lists = data.user_task_lists;
    taskForm = new $.fn.dataTable.Editor( {
          ajax: {
            method: "POST",
            url: `${api_endpoint}/tasks/`,
            xhrFields: { withCredentials: true },
            crossDomain: true,
            headers: {
              "Content-Type": "application/json",
              'X-CSRFToken': get_cookie("csrftoken")
            },
            data: function (data) { return { "data": JSON.stringify( data ) }; }
          },
          fields: [
              {
                label: "Task",
                name:  "title"
              },
              {
                label: "Description",
                name:  "description",
                type: "textarea"
              },
              {
                label: "List",
                name:  "task_list",
                type: "selectize",
                opts: {'placeholder': "Select list"},
                fieldInfo: "Task list to which the task should be added",
                options: lists
              },
              {
                label: "Assigned to",
                name:  "assigned_to",
                type: "selectize",
                opts: {'placeholder': "Select user"},
                options: staff
              },
              {
                label: "Due date",
                name:  "due_date",
                type: "datetime",
                format: "YYYY-MM-DD"
              },
              {
                label: "Workset",
                name:  "workset",
                fieldInfo: "Workset to be used for the task, if applicable",
                type: "selectize",
                opts: {'placeholder': "Select workset"},
                options: worksets
              },
              {
                label: "URL",
                name:  "url",
                fieldInfo: "URL related to the task, if applicable",
                type: "text"
              },
              {
                label: "Attachment",
                name:  "file",
                fieldInfo: "A file to be attached to the task ",
                type: "upload",
                ajax: {
                  method: "POST",
                  url: `${api_endpoint}/attachments/`,
                  headers: {
                    "Content-Type": "application/json",
                    'X-CSRFToken': get_cookie("csrftoken")
                  },
                },
                display: function ( fileId ) {
                  return taskForm.file('Attachment', fileId ).filename;
                },
                clearText: "Remove File",
                dragDrop: 'true',
                dragDropText: "Drag file here",
                uploadText: "Choose file..."
              }
          ]
    });
    taskForm.on('submitSuccess', function(e, json, data, action) {
      toastr.success('The task was created successfully.');
      if (typeof table_tasks != 'undefined') {
        table_tasks.ajax.reload().draw();
      }
    });
    taskForm.buttons({
        text: "Create",
        className: "btn btn-primary",
        action: function () { this.submit(); }
      }).title('Create New Task').create();
  });
}

function task_set_state(task, state) {
    if (state == 'True' || state == true || state == 'true' || state == 1 || state == '1') {
      var action = 'mark_undone';
    } else {
      var action = 'mark_done';
    };
    $.ajax({
      method: "PATCH",
      url: `${api_endpoint}/tasks/${task}/set_state/`,
      xhrFields: { withCredentials: true },
      crossDomain: true,
      headers: {
        "Content-Type": "application/json",
        'X-CSRFToken': get_cookie("csrftoken")
      },
      data: JSON.stringify({ "action": action })
    }).done(function(data, textStatus, jqXHR) {
        if ( $('#task_'+task).length ) {
          switch (action) {
            case 'mark_undone':
              $('#task_'+task).html('<i class="far fa-square fa-lg"></i>');
              break;
            case 'mark_done':
              $('#task_'+task).html('<i class="far fa-check-square fa-lg"></i>');
          }
        }
    }).fail(function(jqXHR, textStatus, errorThrown) {
      if (errorThrown == "Forbidden") {
        toastr.error("You do not have the required permissions to change the status on this task.");
      } else {
        toastr.error('There was an error communicating with the server: '+errorThrown);
      }
    });
}

function create_ticket() {
    ticketForm = new $.fn.dataTable.Editor( {
          ajax: {
            method: "POST",
            url: `${api_endpoint}/tickets/`,
            xhrFields: { withCredentials: true },
            crossDomain: true,
            headers: {
              "Content-Type": "application/json",
              'X-CSRFToken': get_cookie("csrftoken")
            },
            data: function (data) { return { "data": JSON.stringify( data ) };}
          },
          fields: [
              {
                label: "Subject",
                name:  "subject"
              },
              {
                label: "Description",
                name:  "description",
                type: "textarea"
              },
              {
                label: "Tags",
                name:  "tags",
                type: "selectize",
                opts: {'maxItems': 10, 'plugins': ["remove_button"], 'placeholder': "Tag ticket"},
                options: [
                  {"label": "bug", "value": "bug"},
                  {"label": "feature", "value": "feature"},
                  {"label": "documentation", "value": "documentation"},
                  {"label": "question", "value": "question"},
                  {"label": "content", "value": "content"}
                ]
              },
              {
                label: "URL",
                name:  "url",
                fieldInfo: "A URL related to the ticket, if applicable",
                type: "text"
              },
              {
                label: "Attachment",
                name:  "file",
                fieldInfo: "A file to be attached to the ticket, <i>e.g. a screenshot</i>",
                type: "upload",
                ajax: {
                  method: "POST",
                  url: `${api_endpoint}/attachments/`,
                  headers: {
                    "Content-Type": "application/json",
                    'X-CSRFToken': get_cookie("csrftoken")
                  },
                },
                display: function ( fileId ) {
                  return ticketForm.file('Attachment', fileId ).filename;
                },
                dragDrop: 'true',
                dragDropText: "Drag file here",
                uploadText: "Choose file..."
              }
          ]
    });
    ticketForm.on('submitSuccess', function(e, json, data, action) {
      toastr.success('The ticket was created successfully.');
      if (typeof table_tickets != 'undefined') {
        table_tickets.ajax.reload().draw();
      }
    });
    ticketForm.buttons({
        text: "Create",
        className: "btn btn-primary",
        action: function () { this.submit(); }
      }).title('Create New Issue Ticket').create();
}

function full_screen_mode(action) {
  if (action == 'on') {
    const elem = document.documentElement;
    if (elem.requestFullscreen) {
        elem.requestFullscreen();
      } else if (elem.mozRequestFullScreen) { /* Firefox */
        elem.mozRequestFullScreen();
      } else if (elem.webkitRequestFullscreen) { /* Chrome, Safari and Opera */
        elem.webkitRequestFullscreen();
      } else if (elem.msRequestFullscreen) { /* IE/Edge */
        elem.msRequestFullscreen();
      };
    document.getElementById('fullScreenToggle').innerHTML = '<a class="nav-link" href="#" role="button" onclick="full_screen_mode(\'off\')"><i class="fas fa-compress fa-g"></i></a>';
    window.dispatchEvent(new Event('resize'));
  } else {
    if (document.exitFullscreen) {
      document.exitFullscreen();
    } else if (document.mozCancelFullScreen) { /* Firefox */
      document.mozCancelFullScreen();
    } else if (document.webkitExitFullscreen) { /* Chrome, Safari and Opera */
      document.webkitExitFullscreen();
    } else if (document.msExitFullscreen) { /* IE/Edge */
      document.msExitFullscreen();
    };
    document.getElementById("fullScreenToggle").innerHTML = '<a class="nav-link" href="#" role="button" onclick="full_screen_mode(\'on\')"><i class="fas fa-expand fa-g"></i></a>';
    window.dispatchEvent(new Event('resize'));
  }
}

function enable_comments(model, object) {
  $.ajax({
    method: "GET",
    url: `${api_endpoint}/comments/?model=${model}&object=${object}&format=json`,
    xhrFields: { withCredentials: true },
    crossDomain: true,
    headers: {
      "Content-Type": "application/json",
      'X-CSRFToken': get_cookie("csrftoken")
    }
  }).done(function(data, textStatus, jqXHR) {
    if (data.results.length > 0) {
      $('#comments').prepend('<div id="comments-container"></div>');
      for (let i = 0; i < data.results.length; i++) {
          var comment = '<div class="d-flex mb-3"><div class="d-inline-block mr-3">'+data.results[i].avatar+'</div>';
          comment += '<div class="comment-card d-inline-block"><div class="comment-header">';
          comment += '<b>'+data.results[i].user+'</b> commented on '+data.results[i].creation_timestamp+'</div>';
          comment += '<div class="comment-body">'+data.results[i].body+'</div></div></div>';
          $('#comments-container').append(comment);
      }
    };
  });
}

function create_comment(model, object) {
  var body = $('#new_comment_text').val();
  $.ajax({
        method: "POST",
        url: `${api_endpoint}/comments/`,
        xhrFields: { withCredentials: true },
        crossDomain: true,
        headers: {
          "Content-Type": "application/json",
          'X-CSRFToken': get_cookie("csrftoken")
        },
        data: JSON.stringify({ 'model': model, 'object': object, 'body': body }),
  }).done(function(data, textStatus, jqXHR) {
        if (!$('#comments-container').length) {
          $('#comments').prepend('<div id="comments-container"></div>');
        };
        var comment = '<div class="d-flex mb-3"><div class="d-inline-block mr-3">'+data.avatar+'</div>';
        comment += '<div class="comment-card d-inline-block"><div class="comment-header">';
        comment += '<b>'+data.user+'</b> commented on '+data.creation_timestamp+'</div>';
        comment += '<div class="comment-body">'+data.body+'</div></div></div>';
        $('#comments-container').append(comment);
        $('#new_comment_text').val("");
        if ($('#comment_count').length) {
          if ($('#comment_count').hasClass('inline-badge')) {
            $('#comment_count').html(parseInt($('#comment_count').text(), 10) + 1)
          } else {
            $('#comment_count').html(1);
            $('#comment_count').addClass('inline-badge');
          }
        }
  }).fail(function(jqXHR, textStatus, errorThrown) {
        toastr.error('There was an error saving your comment: '+errorThrown);
  });
}

function ticket_set_state(id, action) {
  $.ajax({
    method: "PATCH",
    url: `${api_endpoint}/tickets/${id}/set_state/`,
    xhrFields: { withCredentials: true },
    crossDomain: true,
    headers: {
      "Content-Type": "application/json",
      'X-CSRFToken': get_cookie("csrftoken")
    },
    data: JSON.stringify({ "action": action })
  }).done(function(data, textStatus, jqXHR) {
        switch (action) {
          case 'Close':
            $('#ticket_status').removeClass('ticket-detail-open').addClass('ticket-detail-closed');
            $('#ticket_status').html('<i class="fa fa-exclamation-circle fa-fw"></i> Closed');
            let today = new Date();
            $('.ticket-detail-status').html(today.toLocaleDateString("en-GB", { year: 'numeric', month: 'short', day: 'numeric' })+' | '+data.username);
            $('#ticket_status_box').find('button').removeClass('btn-primary').addClass('btn-danger').text('Open');
            break;
          case 'Open':
            $('#ticket_status').removeClass('ticket-detail-closed').addClass('ticket-detail-open');
            $('#ticket_status').html('<i class="fa fa-exclamation-circle fa-fw"></i> Open');
            $('.ticket-detail-status').html('This ticket is still open');
            $('#ticket_status_box').find('button').removeClass('btn-danger').addClass('btn-primary').text('Close');
        }
  }).fail(function(jqXHR, textStatus, errorThrown) {
    if (errorThrown == "Forbidden") {
      toastr.error("You do not have the required permissions to change the status on that ticket.");
    } else {
      toastr.error('There was an error communicating with the server: '+errorThrown);
    }
  });
}

function fix_dt_search() {
  $('.dataTables_filter label').contents().filter(function () { return this.nodeType == 3; }).remove();
}
