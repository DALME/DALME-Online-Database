function initializePreviewHelper() {
  $('#dataTables-list').on('select.dt', function ( e, dt, type, indexes ) {
      $('.panel-right').empty();
      $.ajax({
        method: "GET",
        url: "/api/images/"+dt.id()+"/get_preview_url/?format=json"
      }).done(function(data, textStatus, jqXHR) {
          $('.panel-right').prepend('<div id="image_preview_container"><img src="'+data['preview_url']+'" class="card-img-top" alt="dam_image" id="image_preview"></div>');
      }).fail(function(jqXHR, textStatus, errorThrown) {
          alert('There was an error retrieving the preview image from the server: '+errorThrown);
      });
      $('.panel-right').append('<div id="image_details"></div>');
      var data = dt_table.rows(indexes).data();
      var attributes = Object.entries(data[0]);
      delete attributes['ref'];
      var columns = dt_options['columnDefs']
      for (var [name, value] of attributes) {
        var label = columns.filter(function(r) { return r['data'] == name })[0]['title'];
        $('#image_details').append('<div class="form-row">\
              <div class="col-sm-3 text-right">\
                <span class="attribute_list_label">'+ label +'</span>\
              </div>\
              <div class="col-sm-9">\
                <span class="attribute_list_value">'+ value +'</span>\
              </div>\
          </div>');
      }
  });
}
