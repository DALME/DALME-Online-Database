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

    let editor_fields = ['subject', 'description', 'tags', 'url', 'file'];
    let required_fields = ['subject', 'description', 'tags'];
    $('#form-field-container').html('')

    for (let i = 0, len = editor_fields.length; i < len; ++i) {
      if (required_fields.includes(editor_fields[i])) {
        $('#form-field-container').append('<div class="flex-row-reverse" data-editor-template="' + editor_fields[i]
            + '"></div>');
      } else {
        $('#form-field-container').append('<div class="flex-row-reverse" data-editor-template="' + editor_fields[i]
            + '"><i class="fas fa-times-circle field_clear_button"></i></div>');}
    }

    ticketForm = new $.fn.dataTable.Editor( {
          template: "#form-template",
          formOptions: {
            main: {
              buttons: true,
              focus: null,
              message: true,
              onBackground: "none",
              onBlur: "none",
              onComplete: "close",
              onEsc: "none",
              onFieldError: "focus",
              onReturn: "none",
              submit: "all",
              drawType: false,
              scope: "row"
            }
          },
          ajax: {
            method: "POST",
            url: `${api_endpoint}/tickets/`,
            xhrFields: { withCredentials: true },
            crossDomain: true,
            headers: {
              "Content-Type": "application/json-dte; charset=UTF-8",
              "Accept": "application/json-dte, text/javascript, */*; q=0.01",
              "X-CSRFToken": get_cookie("csrftoken")
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


    ticketForm.on('open', function (e, mode, action) {
        $('#header-button').insertAfter('.close');
        $('#header-button').remove();
        $('.DTE_Header').children('.close').remove();
        $('.DTE_Header_Content').html('<div class="form_title_text">' + ticketForm.title() + '</div>')
        $('[data-dte-e="form_error"]').appendTo($('.DTE_Body'));
        $('.DTE_Footer_Content').append($('#form-button-container').html());
        $('#form-button-container').remove();
        $('.DTE_Form_Content').find('.col-lg-4').removeClass('col-lg-4').addClass('col-lg-12');
        $('.DTE_Form_Content').find('.col-lg-8').removeClass('col-lg-8').addClass('col-lg-12');

        $('.DTE_Field').each(function() {
          if (!$(this).find('[data-dte-e="msg-info"]').is(':empty') ) {
            let info = $(this).find('[data-dte-e="msg-info"]').html();
            $(this).find('[data-dte-e="msg-label"]').html(info);
            $(this).find('[data-dte-e="msg-info"]').html('');
          }
        });

        $('.field_clear_button').each( function(i, el) {
          let field = $(el).parent().data('editor-template')
          $(el).popover({
              toggle: 'popover',
              placement: 'right',
              html: true,
              title: '',
              content: '<a href="#" id="' + field + '" class="btn btn-sm btn-danger clear-field mr-1">\
                  Remove</a><a href="#" class="btn btn-sm btn-primary">Cancel</a>',
            })
        })

        $(document).on("click.dalme", ".popover .btn-primary" , function() {
            $(this).parents(".popover").popover('hide');
        });

        $(document).on("click.dalme", ".popover .clear-field" , function() {
            toggle_fields($(this).attr('id'), editor_fields, 'hide');
            $(this).parents(".popover").popover('hide');
        });

        toggle_fields(required_fields, editor_fields);

        $("textarea").each( function( i, el ) {
            $(el).width(500);
            $(el).height(100);
        });

    });

    ticketForm.on('close.dalme', function (e) {
      $('.DTE_Form_Buttons').appendTo($('.DTE_Footer'));
      $('.DTE_Form_Buttons').removeClass('remove-action-buttons');
      $('.modal-header').removeClass('d-none');
      $('.modal-footer').removeClass('d-none');
      $('.DTE_Form_Info').removeClass('remove-action-info');

      $('#add-attribute-button').off('click.dalme');
      $('.field_clear_button').popover('dispose');
      $(document).off("click.dalme", ".popover .btn-primary");
      $(document).off("click.dalme", ".popover .clear-field");

      $('#form-field-container').html('')
    });

    ticketForm.on('submitSuccess', function(e, json, data, action) {
      toastr.success('The ticket was created successfully.');
      if (typeof table_tickets != 'undefined') {
        table_tickets.ajax.reload().draw();
      }
    });

    ticketForm.buttons([{
        text: "Create",
        className: "btn btn-success",
        action: function () { this.submit(); }
      },
      {
        text: "Cancel",
        className: "btn btn-primary",
        action: function () { this.close(); }
      }]).title('New Ticket').create();
}

function toggle_fields(target, editor_fields, action) {
  if (Array.isArray(target) && target.length) {
    let add_menu_list = [];

    for (let i = 0, len = editor_fields.length; i < len; ++i) {
      if (target.includes(editor_fields[i])) {
        toggle_fields(editor_fields[i], editor_fields, 'show')
      } else {
        toggle_fields(editor_fields[i], editor_fields, 'hide')
        add_menu_list.push(editor_fields[i]);
      }
    }

    if (add_menu_list.length) {
      add_menu_list.sort();

      $('#add-attribute-menu-container').html('');

      for (let i = 0, len = add_menu_list.length; i < len; ++i) {
          $('#add-attribute-menu-container').append('<a class="dropdown-item" href="#" data-menu-field="'
            + add_menu_list[i] + '">'
            + add_menu_list[i].replace('_', ' ').replace(/^\w/, (c) => c.toUpperCase()) + '</a>');
      }
      $('#add-attribute-button').removeClass('d-none');
      $('#add-attribute-menu-container').on('click.dalme', '.dropdown-item', function () {
        toggle_fields($(this).data('menu-field'), editor_fields, 'show');
      });

    } else {
      $('#add-attribute-button').addClass('d-none');
    }

  } else if (typeof action != 'undefined') {

    switch (action) {

      case 'hide':
        ticketForm.field(target).val('');
        ticketForm.hide(target);

        if ($(ticketForm.field(target).node()).parent().find('.field_clear_button').length) {
          $(ticketForm.field(target).node()).parent().find('.field_clear_button').addClass('d-none');
        }

        if (!$('#add-attribute-menu-container').find('[data-menu-field="' + target + '"]').length) {
          $('#add-attribute-menu-container').append('<a class="dropdown-item" href="#" data-menu-field="' + target + '">'
              + target.replace('_', ' ').replace(/^\w/, (c) => c.toUpperCase()) + '</a>');

          $('#add-attribute-menu-container').find('dropdown_item').sort(function(a, b) {
              return $(a).text().toLowerCase().localeCompare($(b).text().toLowerCase());
            }).each(function() {
              $('#add-attribute-menu-container').append(this);
          });
        }

        if ($('#add-attribute-button').hasClass('d-none')) {
          $('#add-attribute-button').removeClass('d-none');
        }

        break;

      case 'show':
        ticketForm.show(target);

        if ($(ticketForm.field(target).node()).parent().find('.field_clear_button').length) {
          $(ticketForm.field(target).node()).parent().find('.field_clear_button').removeClass('d-none');
        }

        if ($('#add-attribute-menu-container').find('[data-menu-field="' + target + '"]').length > 0) {
          $('#add-attribute-menu-container').find('[data-menu-field="' + target + '"]').remove()

          if ($('#add-attribute-menu-container').children().length < 1) {
            $('#add-attribute-button').addClass('d-none');
          }
        }
    }
  }
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

function get_user_avatar(image_path) {
  if (image_path == "None" || image_path == null || !image_path.length ) {
    return '<i class="fa fa-user-alt-slash img_avatar mt-1 fa-2x"></i>'
  } else {
    return '<img src="'+image_path+'" class="img_avatar" alt="avatar">'
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
          var comment = '<div class="d-flex mb-3"><div class="d-inline-block mr-3">'+get_user_avatar(data.results[i].creation_user.avatar)+'</div>';
          comment += '<div class="comment-card d-inline-block"><div class="comment-header">';
          comment += '<b>'+data.results[i].creation_user.username+'</b> commented on '+moment(data.results[i].creation_timestamp).format("DD-MMM-YYYY@HH:MM")+'</div>';
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
        var comment = '<div class="d-flex mb-3"><div class="d-inline-block mr-3">'+get_user_avatar(data.creation_user.avatar)+'</div>';
        comment += '<div class="comment-card d-inline-block"><div class="comment-header">';
        comment += '<b>'+data.creation_user.username+'</b> commented on '+moment(data.creation_timestamp).format("DD-MMM-YYYY@HH:MM")+'</div>';
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
