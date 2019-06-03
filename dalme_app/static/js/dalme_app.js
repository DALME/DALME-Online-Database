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
      const groups = data.user_group_list;
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
                type: "chosen",
                options: groups
              },
            ]
        });
        taskListForm.buttons({
          text: "Save",
          className: "btn btn-primary",
          action: function () { this.submit(); }
        }).title('Create new list').create();
  }, 'json');
}

function create_task(type) {
  $.get("/api/options/?lists=active_staff,user_worksets,user_task_lists&format=json", function ( data ) {
      const staff = data.staff_list;
      const worksets = data.workset_list;
      const lists = data.user_task_lists;
      if (type != 'ticket') {
        var fields = [
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
            label: "Workset",
            name:  "workset",
            type: "chosen",
            options: worksets
          },
          {
            label: "Due date",
            name:  "due_date",
            type: "datetime",
            format: "YYYY-MM-DD"
          },
          {
            label: "Assigned to",
            name:  "assigned_to",
            type: "chosen",
            options: staff
          },
          {
            label: "List",
            name:  "task_list",
            type: "chosen",
            options: lists
          }
            ]
      } else {
        var fields = [
            {
              label: "Issue",
              name:  "title"
            },
            {
              label: "Description",
              name:  "description",
              type: "textarea"
            }
          ]
      }
      taskForm = new $.fn.dataTable.Editor( {
            ajax: {
              method: "POST",
              url: "/api/tasks/",
              headers: { 'X-CSRFToken': get_cookie("csrftoken") },
              data: function (data) { return { "data": JSON.stringify( data ) }; }
            },
            fields: fields
        });
      if (type != 'ticket') {
        taskForm.buttons({
          text: "Create",
          className: "btn btn-primary",
          action: function () { this.submit(); }
        }).title('Create New Task').create();
      } else {
        taskForm.buttons({
          text: "Report",
          className: "btn btn-primary",
          action: function () { this.submit(); }
        }).title('Report Issue').create();
      }
  }, 'json');
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

function mark_task_done(task) {
  const url = "/api/tasks/"+task.id+"/";
  $.ajax({
    method: "PUT",
    url: url,
    headers: { 'X-CSRFToken': get_cookie("csrftoken") },
    data: { 'completed': 1 },
  }).done(function(data, textStatus, jqXHR) {
    show_message('success', 'Task marked as completed.');
  }).fail(function(jqXHR, textStatus, errorThrown) {
    show_message('danger', 'There was an error communicating with the server: '+errorThrown);
  });
}
