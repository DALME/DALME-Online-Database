/* custom JavaScript functions used by dalme.app */
function get_cookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function fix_dt_search() {
  $('.dataTables_filter label').contents().filter(function () { return this.nodeType == 3; }).remove();
}

function create_task_list() {
  $.get("/api/options/?lists=user_groups&format=json", function ( data ) {
      const groups = data.user_groups;
      taskListForm = new $.fn.dataTable.Editor( {
            ajax: {
              method: "POST",
              url: "/api/tasklists/",
              headers: { 'X-CSRFToken': get_cookie("csrftoken") },
              data: function (data) { return { "data": JSON.stringify( data ) }; }
            },
            fields: [
              {
                label: "List name",
                name: "name",
                message: "Name of the list to be created"
              },
              {
                label: "Group",
                name:  "group",
                message: "Group of users that will utilize the list",
                type: "selectize",
                opts: {'placeholder': "Select user group"},
                options: groups
              },
            ]
        });
        taskListForm.on('submitSuccess', function(e, json, data, action) {
          show_message('success', 'The task list was created successfully.');
          if (typeof table_lists != 'undefined') {
            table_lists.ajax.reload();
          }
        });
        taskListForm.buttons({
          text: "Create",
          className: "btn btn-primary",
          action: function () { this.submit(); }
        }).title('Create New Task List').create();
  }, 'json');
}

function create_task() {
  $.get("/api/options/?lists=active_staff,user_worksets,user_task_lists&format=json", function ( data ) {
      const staff = data.active_staff;
      const worksets = data.user_worksets;
      const lists = data.user_task_lists;
      taskForm = new $.fn.dataTable.Editor( {
            ajax: {
              method: "POST",
              url: "/api/tasks/",
              headers: { 'X-CSRFToken': get_cookie("csrftoken") },
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
                  message: "Task list to which the task should be added",
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
                  message: "Workset to be used for the task, if applicable",
                  type: "selectize",
                  opts: {'placeholder': "Select workset"},
                  options: worksets
                },
                {
                  label: "URL",
                  name:  "url",
                  message: "URL related to the task, if applicable",
                  type: "text"
                },
                {
                  label: "Attachment",
                  name:  "file",
                  message: "A file to be attached to the task ",
                  type: "upload",
                  ajax: {
                    method: "POST",
                    url: "/api/attachments/",
                    headers: { 'X-CSRFToken': get_cookie("csrftoken")},
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
        show_message('success', 'The task was created successfully.');
        if (typeof table_tasks != 'undefined') {
          table_tasks.ajax.reload().draw();
        }
      });
      taskForm.buttons({
          text: "Create",
          className: "btn btn-primary",
          action: function () { this.submit(); }
        }).title('Create New Task').create();
  }, 'json');
}

function task_set_state(task, state) {
    if (state == 'True' || state == true || state == 'true' || state == 1 || state == '1') {
      var action = 'mark_undone';
    } else {
      var action = 'mark_done';
    };
    $.ajax({
      method: "GET",
      url: "/api/tasks/"+task+"/set_state/?action="+action,
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
        show_message('danger', 'There was an error communicating with the server: '+errorThrown);
    });
}

function create_ticket() {
    ticketForm = new $.fn.dataTable.Editor( {
          ajax: {
            method: "POST",
            url: "/api/tickets/",
            headers: { 'X-CSRFToken': get_cookie("csrftoken") },
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
                message: "A URL related to the ticket, if applicable",
                type: "text"
              },
              {
                label: "Attachment",
                name:  "file",
                message: "A file to be attached to the ticket, <i>e.g. a screenshot</i>",
                type: "upload",
                ajax: {
                  method: "POST",
                  url: "/api/attachments/",
                  headers: { 'X-CSRFToken': get_cookie("csrftoken")},
                },
                dragDrop: 'true',
                dragDropText: "Drag file here",
                uploadText: "Choose file..."
              }
          ]
    });
    ticketForm.on('submitSuccess', function(e, json, data, action) {
      show_message('success', 'The ticket was created successfully.');
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

function update_session(data) {
    $.ajax({
      type : "POST",
      url : "/su/",
      headers : {'X-CSRFToken': get_cookie('csrftoken') },
      dataType : "json",
      data : data
    });
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
  }
}

function remove_param(key, sourceURL) {
    var rtn = sourceURL.split("?")[0],
        param,
        params_arr = [],
        queryString = (sourceURL.indexOf("?") !== -1) ? sourceURL.split("?")[1] : "";
    if (queryString !== "") {
        params_arr = queryString.split("&");
        for (let i = params_arr.length - 1; i >= 0; i -= 1) {
            param = params_arr[i].split("=")[0];
            if (param === key) {
                params_arr.splice(i, 1);
            }
        }
        rtn = rtn + "?" + params_arr.join("&");
    }
    return rtn;
}

function get_params(sourceURL) {
    var params = {};
    var parts = sourceURL.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {
        params[key] = value;
    });
    return params;
}

function show_message(type, text) {
  var message = '<div class="alert alert-'+type+' alert-dismissable" role="alert">';
  message += '<button type="button" class="close" data-dismiss="alert" aria-hidden="true">×</button>';
  message += text+'</div>';
  $('.topbar-dalme').after(message);
}

function enable_comments(model, object) {
  $.get("/api/comments/?model="+model+"&object="+object+"&format=json", function ( data ) {
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
  }, 'json');
}

function create_comment(model, object) {
  var body = $('#new_comment_text').val();
  $.ajax({
        method: "POST",
        url: "/api/comments/",
        headers: { 'X-CSRFToken': get_cookie("csrftoken") },
        data: { 'model': model, 'object': object, 'body': body },
  }).done(function(data, textStatus, jqXHR) {
        if (!$('#comments-container').length) {
          $('#comments').prepend('<div id="comments-container"></div>');
        };
        var comment = '<div class="d-flex mb-3"><div class="d-inline-block mr-3">'+data.avatar+'</div>';
        comment += '<div class="comment-card d-inline-block"><div class="comment-header">';
        comment += '<b>'+data.user+'</b> commented on '+data.creation_timestamp+'</div>';
        comment += '<div class="comment-body">'+data.body+'</div></div></div>';
        $('#comments-container').append(comment);
  }).fail(function(jqXHR, textStatus, errorThrown) {
        show_message('danger', 'There was an error saving your comment: '+errorThrown);
  });
}

function ticket_set_state(id, action) {
  $.ajax({
    method: "GET",
    url: "/api/tickets/"+id+"/set_state/?action="+action,
  }).done(function(data, textStatus, jqXHR) {
        switch (action) {
          case 'Close':
            $('#ticket_status').removeClass('ticket-detail-open').addClass('ticket-detail-closed');
            $('#ticket_status').html('<i class="fa fa-exclamation-circle fa-fw"></i> Closed');
            let today = new Date();
            $('#ticket_status_box').prepend('<div class="ticket-detail-date">'+today.toLocaleDateString("en-GB", { year: 'numeric', month: 'short', day: 'numeric' })+' | '+data.username+'</div>');
            $('#ticket_status_box').find('button').removeClass('btn-primary').addClass('btn-danger').text('Open');
            break;
          case 'Open':
            $('#ticket_status').removeClass('ticket-detail-closed').addClass('ticket-detail-open');
            $('#ticket_status').html('<i class="fa fa-exclamation-circle fa-fw"></i> Open');
            $('.ticket-detail-date').remove();
            $('#ticket_status_box').find('button').removeClass('btn-danger').addClass('btn-primary').text('Close');
        }
  }).fail(function(jqXHR, textStatus, errorThrown) {
      show_message('danger', 'There was an error communicating with the server: '+errorThrown);
  });
}
