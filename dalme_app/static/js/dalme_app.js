/* custom JavaScript functions used by dalme.app */
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
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
  $('.dataTables_filter label').each(function() { $(this).html( $(this).find('input') )});
}

function createTaskList() {
  $.get("/api/options/?form=createtasklist&format=json", function ( data ) {
      var groups = data.groups;
      taskListForm = new $.fn.dataTable.Editor( {
            ajax: {
              method: "POST",
              url: "../api/tasklists/",
              headers: { 'X-CSRFToken': getCookie("csrftoken") },
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

function createTask() {
  $.get("/api/options/?form=createtask&format=json", function ( data ) {
      var staff = data.staff;
      var worksets = data.worksets;
      var lists = data.lists;
      taskForm = new $.fn.dataTable.Editor( {
            ajax: {
              method: "POST",
              url: "../api/tasks/",
              headers: { 'X-CSRFToken': getCookie("csrftoken") },
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
        });
        taskForm.buttons({
          text: "Save",
          className: "btn btn-primary",
          action: function () { this.submit(); }
        }).title('Create new task').create();
  }, 'json');
}

function updateSession(data) {
    $.ajax({
      type : "POST",
      url : "/su/",
      headers : {'X-CSRFToken': getCookie('csrftoken') },
      dataType : "json",
      data : data
    });
}

function fullScreenMode(action) {
  if (action == 'on') {
    var elem = document.documentElement;
    if (elem.requestFullscreen) {
        elem.requestFullscreen();
      } else if (elem.mozRequestFullScreen) { /* Firefox */
        elem.mozRequestFullScreen();
      } else if (elem.webkitRequestFullscreen) { /* Chrome, Safari and Opera */
        elem.webkitRequestFullscreen();
      } else if (elem.msRequestFullscreen) { /* IE/Edge */
        elem.msRequestFullscreen();
      };
    document.getElementById('fullScreenToggle').innerHTML = '<a class="nav-link" href="#" role="button" onclick="fullScreenMode(\'off\')"><i class="fas fa-compress fa-g"></i></a>';
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
    document.getElementById("fullScreenToggle").innerHTML = '<a class="nav-link" href="#" role="button" onclick="fullScreenMode(\'on\')"><i class="fas fa-expand fa-g"></i></a>';
  }
}

function removeParam(key, sourceURL) {
    var rtn = sourceURL.split("?")[0],
        param,
        params_arr = [],
        queryString = (sourceURL.indexOf("?") !== -1) ? sourceURL.split("?")[1] : "";
    if (queryString !== "") {
        params_arr = queryString.split("&");
        for (var i = params_arr.length - 1; i >= 0; i -= 1) {
            param = params_arr[i].split("=")[0];
            if (param === key) {
                params_arr.splice(i, 1);
            }
        }
        rtn = rtn + "?" + params_arr.join("&");
    }
    return rtn;
}

function taskMarkDone(task) {
  var url = "/api/tasks/"+task.id+"/";
  $.ajax({
    method: "PUT",
    url: url,
    headers: { 'X-CSRFToken': getCookie("csrftoken") },
    data: { 'completed': 1 },
  }).done(function(data, textStatus, jqXHR) {
      alert('done');
  }).fail(function(jqXHR, textStatus, errorThrown) { alert('There was an error: '+errorThrown); });
}
