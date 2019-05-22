function image_preview() {
}


function set_preview(action) {
  if (action == 'on') {
      $('.panel-right').html('<div class="card-columns" id="thumb-container"></div>');
      let i_selected = dt_table.rows( { selected: true, page: 'current' } ).data();
      add_thumbnails(i_selected);
      $('#dataTables-list').on('select.dt.dalme', function ( e, dt, type, indexes ) { add_thumbnails(dt_table.rows(indexes).data()); });
      $('#dataTables-list').on('deselect.dt.dalme', function ( e, dt, type, indexes ) { remove_thumbnails(dt_table.rows(indexes).data()); });
  } else if (action == 'off') {
      $('#dataTables-list').off('select.dt.dalme deselect.dt.dalme');
  }
}

function add_thumbnails(selected) {
  for (let i = 0, len = selected.length; i < len; ++i) {
    $.ajax({
      method: "GET",
      url: "/api/images/"+selected[i]['ref']['ref']+"/get_preview_url/?format=json"
    }).done(function(data, textStatus, jqXHR) {
        $('#thumb-container').append('<div class="card card-thumbnail" id="thumb_'+selected[i]['ref']['ref']+'">\
          <img src="'+data['preview_url']+'" class="card-img-top" alt="dam_image">\
          <div class="card-body"><p class="card-text">DAM Id: '+selected[i]['ref']['ref']+'</p></div></div>');
        $('#thumb_'+selected[i]['ref']['ref']).attr('order', selected[i]['ref']['ref']);
    }).fail(function(jqXHR, textStatus, errorThrown) {
        $('#thumb-container').append('<div class="card card-thumbnail" id="thumb_'+selected[i]['ref']['ref']+'">\
          <div class="img-placeholder d-flex justify-content-center align-items-center"><i class="d-block fa fa-eye-slash fa-2x mt-3 mb-3"></i></div>\
          <div class="card-body"><p class="card-text">DAM Id: '+selected[i]['ref']['ref']+'</p></div></div>');
        $('#thumb_'+selected[i]['ref']['ref']).attr('order', selected[i]['ref']['ref']);
    });
  };
}

function remove_thumbnails(selected) {
  for (let i = 0, len = selected.length; i < len; ++i) {
    $('#thumb_'+selected[i]['ref']['ref']).remove();
  }
}

function create_source_from_selected() {
    let selected = dt_table.rows( { selected: true, page: 'current' } ).data();
    var sel_ids = []
    for (let i = 0, len = selected.length; i < len; ++i) {
      sel_ids.push(selected[i]['ref']['ref']);
    };
    $.ajax({
      method: "GET",
      url: "/api/images/get_info_for_source/?data="+sel_ids+"&format=json"
    }).done(function(data, textStatus, jqXHR) {
          init_source_editor(data);
    }).fail(function(jqXHR, textStatus, errorThrown) {
          alert('There was an error communicating with the server: '+errorThrown);
    });
}
