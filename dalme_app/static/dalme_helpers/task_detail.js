function task_detail() {
}

function edit_task() {
  if (typeof edit_state == 'undefined' || edit_state == 'off') {
      edit_state = 'on';
      $('.dropdown-task-add').addClass('edit_button_on');
      $.get("/api/options/?lists=active_staff,user_worksets,user_task_lists&format=json", function ( data ) {
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
          $('[data-editor-field]').on( 'click.dalme', function (e) {
            editTaskForm.bubble(this);
          } );
      }, 'json');
  } else {
      edit_state = 'off';
      $('.dropdown-task-add').removeClass('edit_button_on');
      $('[data-editor-field]').off('click.dalme');
  }
}

function task_change_state(task, action) {
    $.ajax({
      method: "GET",
      url: "/api/tasks/"+task+"/set_state/?action="+action,
    }).done(function(data, textStatus, jqXHR) {
          switch (action) {
            case 'mark_undone':
              $('#task_'+task).html('<i class="far fa-square fa-lg"></i>');
              $('.task-d_status').html('Not completed.');
              break;
            case 'mark_done':
              $('#task_'+task).html('<i class="far fa-check-square fa-lg"></i>');
              let today = new Date();
              $('.task-d_status').html('Completed: '+ today.toLocaleDateString("en-GB", { year: 'numeric', month: 'short', day: 'numeric' }));
          }
    }).fail(function(jqXHR, textStatus, errorThrown) {
        show_message('danger', 'There was an error communicating with the server: '+errorThrown);
    });
}
