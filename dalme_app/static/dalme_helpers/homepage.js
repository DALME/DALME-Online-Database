function init_tables() {
    table_tickets = $('#dataTables-tickets').DataTable({
          'ajax': {
            'url': "/api/tickets/?format=json",
            'data': function (data) { return { "data": JSON.stringify( data ) }; }
          },
          serverSide: true,
          responsive: true,
          dom: "<'sub-card-header pr-2 d-flex'<'card-header-title'><'dt-btn-group'>fr><'card-body't><'sub-card-footer'i>",
          select: { style: 'single' },
          scrollResize: true,
          scrollY: "30vh",
          scrollX: "100%",
          deferRender: true,
          scroller: true,
          language: { searchPlaceholder: "Search" },
          rowId: "id",
          columnDefs: [
                {
                    title: "Id",
                    targets: 0,
                    data: "id",
                    visible: 1,
                    width: "20px"
                },
                {
                    title: "Ticket",
                    targets: 1,
                    data: "ticket",
                    visible: 1,
                    searchable: 0,
                    orderData: [ 5, 4 ],
                },
                {
                    title: "Tags",
                    targets: 2,
                    data: "tags",
                    visible: 1,
                    orderable: 0,
                    searchable: 0
                },
                {
                    title: "Attachments",
                    targets: 3,
                    data: "attachments",
                    visible: 1,
                    orderable: 0,
                    searchable: 0,
                },
                {
                    title: "Subject",
                    targets: 4,
                    data: "subject",
                    visible: 0
                },
                {
                    title: "Status",
                    targets: 5,
                    data: "status",
                    visible: 0
                },
          ]
    });
    table_worksets = $('#dataTables-worksets').DataTable({
          'ajax': {
            'url': "/api/worksets/?format=json",
            'data': function (data) { return { "data": JSON.stringify( data ) }; }
          },
          serverSide: true,
          responsive: true,
          dom: "<'sub-card-header pr-2 d-flex'<'card-header-title'><'dt-btn-group'>fr><'card-body't><'sub-card-footer'i>",
          select: { style: 'single' },
          scrollResize: true,
          scrollY: "30vh",
          scrollX: "100%",
          deferRender: true,
          scroller: true,
          language: { searchPlaceholder: "Search" },
          rowId: "id",
          columnDefs: [
                 {
                     title: "Id",
                     targets: 0,
                     data: "id",
                     visible: 0
                 },
                 {
                     title: "Workset",
                     targets: 1,
                     data: "workset",
                     orderData: [ 5, 3 ],
                     searchable: 0
                 },
                 {
                     title: "Progress",
                     targets: 2,
                     data: "progress_circle",
                     orderData: [ 6, 3 ],
                     searchable: 0
                 },
                 {
                     title: "Name",
                     targets: 3,
                     data: "name",
                     visible: 0,
                 },
                 {
                     title: "Description",
                     targets: 4,
                     data: "description",
                     visible: 0,
                 },
                 {
                     title: "Endpoint",
                     targets: 5,
                     data: "endpoint",
                     visible: 0,
                 },
                 {
                     title: "Progress",
                     targets: 6,
                     data: "progress",
                     visible: 0,
                 }
          ]
    });
    table_tasks = $('#dataTables-tasks').DataTable({
          'ajax': {
            'url': "/api/tasks/?format=json",
            'data': function (data) { return { "data": JSON.stringify( data ) }; }
          },
          serverSide: true,
          responsive: true,
          dom: "<'sub-card-header pr-2 d-flex'<'card-header-title'><'dt-btn-group'>fr><'card-body't><'sub-card-footer'i>",
          select: { style: 'single' },
          scrollResize: true,
          scrollY: "40vh",
          scrollX: "100%",
          deferRender: true,
          scroller: true,
          language: { searchPlaceholder: "Search" },
          rowId: "id",
          columnDefs: [
                 {
                     title: "Task",
                     targets: 0,
                     data: "task",
                     visible: 1,
                     orderData: [ 6, 7 ],
                     searchable: 0
                 },
                 {
                     title: "Dates",
                     targets: 1,
                     data: "dates",
                     visible: 1,
                     orderData: [ 5, 7 ],
                     searchable: 0
                 },
                 {
                     title: "Assigned to",
                     targets: 2,
                     data: "assigned_to",
                     visible: 1,
                     searchable: 0
                 },
                 {
                     title: "Attachments",
                     targets: 3,
                     data: "attachments",
                     visible: 1,
                     orderable: 0,
                     searchable: 0,
                 },
                 {
                     title: "Done",
                     targets: 4,
                     data: "completed",
                     render: function ( data, type, row, meta ) { return data == true ? '<i class="far fa-check-square"></i>' : '<i class="far fa-square"></i>';},
                     className: "td-center",
                     width: "19px",
                     visible: 1,
                     searchable: 0
                 },
                 {
                     title: "Due date",
                     targets: 5,
                     data: "due_date",
                     visible: 0,
                 },
                 {
                     title: "Title",
                     targets: 6,
                     data: "title",
                     visible: 0,
                 },
                 {
                     title: "Created",
                     targets: 7,
                     data: "creation_timestamp",
                     visible: 0,
                 },
                 {
                     title: "Description",
                     targets: 8,
                     data: "description",
                     visible: 0,
                 },
                 {
                     title: "Id",
                     targets: 9,
                     data: "id",
                     visible: 0
                 },
          ]
    });
    $('#dataTables-tickets_wrapper').find('.card-header-title').html('<i class="fa fa-ticket-alt fa-fw"></i> Issue Tickets');
    $('#dataTables-worksets_wrapper').find('.card-header-title').html('<i class="fa fa-layer-group fa-fw"></i> My Worksets');
    $('#dataTables-tasks_wrapper').find('.card-header-title').html('<i class="fa fa-user-check fa-fw"></i> My Tasks');
    fix_dt_search();
    table_tasks.on('select', function ( e, dt, type, indexes ) {
      if (typeof dt != 'undefined') {
         show_task_detail(dt.id());
      }
    });
    table_tasks.on('deselect', function ( e, dt, type, indexes ) {
          restore_detail_pane();
    });
}

function restore_detail_pane() {
  $('#task_detail_container').html('');
}

function show_task_detail(id) {
  $.get("/api/tasks/"+id+"/?format=json", function ( data ) {
      var fields = ['title', 'description', 'dates_detail', 'attachments_detail'];
      $('#task_detail_container').html('');
      for (let i = 0; i < fields.length; i++) {
          $('#task_detail_container').append(
            '<div class="task-detail-'+fields[i]+'">'+data[fields[i]]+'</div>'
          );
      }
  }, 'json');
}
