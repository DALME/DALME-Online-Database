function task_detail() {
}

function edit_task(id) {
      $.get("/api/options/?target=active_staff,user_worksets,user_task_lists&format=json", function ( data ) {
          const staff = data.active_staff;
          const worksets = data.user_worksets;
          const lists = data.user_task_lists;
          editTaskForm = new $.fn.dataTable.Editor( {
                ajax: {
                  method: "PATCH",
                  url: "/api/tasks/_id_/",
                  headers: { 'X-CSRFToken': get_cookie("csrftoken") },
                  data: function (data) { return { "data": JSON.stringify( data ) }; }
                },
                fields: [
                    {
                      label: "Id",
                      name:  "id",
                      type: "hidden"
                    },
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
                        url: "/api/attachments/",
                        headers: { 'X-CSRFToken': get_cookie("csrftoken")},
                      },
                      display: function (id) {
                        return editTaskForm.file('Attachment', id).filename;
                      },
                      clearText: "Remove File",
                      dragDrop: 'true',
                      dragDropText: "Drag file here",
                      uploadText: "Choose file..."
                    }
                ]
          });
          editTaskForm.on('submitSuccess', function(e, json, data, action) {
            toastr.success('The task was updated successfully.');
            location.reload();
          });
          editTaskForm.buttons({
            text: "Update",
            className: "btn btn-primary",
            action: function () { this.submit(); }
          }).title('Edit Task').edit(id, false);
          let file_obj = {}
          file_obj[task['file']] = { id: task['file'], filename: $('.attachment-file-label').text() };
          $.fn.dataTable.Editor.files['Attachment'] = file_obj;
          for (const prop in task) {
              if (task.hasOwnProperty(prop)) {
                  editTaskForm.set(prop, task[prop]);
              }
          };
          editTaskForm.open();
      }, 'json');
}

function delete_task(id) {
  var conf = confirm("Are you sure you wish to delete this task?");
  if (conf == true) {
    $.ajax({
      method: "DELETE",
      url: "/api/tasks/"+id,
      headers: { 'X-CSRFToken': get_cookie("csrftoken") },
    }).done(function(data, textStatus, jqXHR) {
      window.location.href = "/tasks";
    }).fail(function(jqXHR, textStatus, errorThrown) {
      toastr.error('There was an error communicating with the server: '+errorThrown);
    });
  }
}

function task_change_state(task, action) {
    $.ajax({
      method: "PATCH",
      url: "/api/tasks/"+task+"/set_state/",
      headers: { 'X-CSRFToken': get_cookie("csrftoken") },
      data: { "action": action }
    }).done(function(data, textStatus, jqXHR) {
          switch (action) {
            case 'mark_undone':
              $('#task_'+task).html('<i class="far fa-square fa-lg"></i>');
              $('.task-detail-status').html('Not completed.');
              break;
            case 'mark_done':
              $('#task_'+task).html('<i class="far fa-check-square fa-lg"></i>');
              let today = new Date();
              $('.task-detail-status').html('Completed: '+ today.toLocaleDateString("en-GB", { year: 'numeric', month: 'short', day: 'numeric' }));
          }
    }).fail(function(jqXHR, textStatus, errorThrown) {
      if (errorThrown == "Forbidden") {
        toastr.error("You do not have the required permissions to change the status on this task.");
      } else {
        toastr.error('There was an error communicating with the server: '+errorThrown);
      }
    });
}
