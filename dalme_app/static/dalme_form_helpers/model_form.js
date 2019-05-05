function initializeFormHelper() {
  $('#parent_class_select').on('change', updateClass );
  $('#dataTables-table').on('click', 'tbody td:not(:first-child)', function (e) {
        dt_editor.inline(this);
    });
}

function updateClass() {
  const value = $('#parent_class_select').children("option:selected").val();
  if (value !=0) {
      dt_table.ajax.url("/api/fields/?format=json&list=" +value).draw();
      $.ajax({
        method: "GET",
        url: "/api/lists/"+value+"/?format=json"
      }).done(function(data, textStatus, jqXHR) {
        var attributes = Object.entries(data);
        $('#parent_class_info').empty();
        for (var [label, value] of attributes) {
          if (value != '') {
              let html = '<div class="model-attribute-container"><div class="model-attribute-label">'+ label +'</div><div class="model-attribute-value">'+ value +'</div></div>';
              $('#parent_class_info').append(html);
          }
        };
      }).fail(function(jqXHR, textStatus, errorThrown) {
          alert('There was an error retrieving the data for this list from the server: '+errorThrown);
      });
      window.dispatchEvent(new Event('resize'));
  } else {
      dt_table.ajax.url("/api/fields/?format=json").draw();
      $('#parent_class_info').empty();
      window.dispatchEvent(new Event('resize'));
  }
}

function addClassEntry() {
  $.get("/api/options/?form=modelslist&format=json", function ( data ) {
      const content_types = data.content_types;
      const model_class_name = 'list';
      modelClassForm = new $.fn.dataTable.Editor( {
            ajax: {
              method: "POST",
              url: "/api/lists/",
              headers: { 'X-CSRFToken': getCookie("csrftoken") },
              data: function (data) { return { "data": JSON.stringify( data ) }; }
            },
            fields: [
              {
                label: "Name",
                name:  "name"
              },
              {
                label: "Short name",
                name:  "short_name"
              },
              {
                label: "Description",
                name:  "description",
                type: "textarea"
              },
              {
                label: "API URL",
                name:  "api_url",
              },
              {
                label: "Form helper",
                name:  "form_helper",
              },
              {
                label: "Preview helper",
                name:  "preview_helper",
              },
              {
                label: "Content types",
                name:  "content_types",
                type: "chosen",
                attr: { multiple: true },
                options: content_types
              }
                ]
        });
        modelClassForm.buttons({
          text: "Save",
          className: "btn btn-primary",
          action: function () { this.submit(); }
        }).title('Create new '+model_class_name).create();
  }, 'json');
}

function editClassEntry() {

}
