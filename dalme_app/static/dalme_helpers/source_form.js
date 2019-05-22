function source_form() {

}

function source_form_on() {
    $('#DTE_Field_type').on('change.dalme', changeOnType);
    $('#DTE_Field_is_inventory_0').on('click.dalme', changeOnInv);
    att_set = 0;
    page_set = 0;
}

function source_form_off() {

}

function init_source_editor(para_data) {
    img_data = para_data.data.image_data
    var suggested_fields = para_data.data.suggested_fields
    $.get("/api/options/?lists=content_types_1,parent_sources_13&format=json", function ( option_data ) {
          const type_options = option_data.content_types;
          const parent_options = option_data.parent_sources;
          source_editor = new $.fn.dataTable.Editor( {
              ajax: {
                create: {
                    type: 'POST',
                    url: '/api/sources/',
                    headers: {'X-CSRFToken': getCookie("csrftoken") },
                    data: function (data) { return { "data": JSON.stringify( data ) }; }
                  },
                edit: {
                    type: 'PATCH',
                    url: '/api/sources/_id_/',
                    headers: {'X-CSRFToken': getCookie("csrftoken") },
                    data: function (data) { return { "data": JSON.stringify( data ) }; }
                  },
                remove: {
                    type: 'DELETE',
                    url: '/api/sources/_id_/',
                    headers: {'X-CSRFToken': getCookie("csrftoken") },
                    data: function (data) { data.data = null; return data; }
                  }
                },
                idSrc: "id",
                template: "#inventoryForm",
                fields: [
                    {
                          name: "name",
                          label: "Name",
                          type: "text",
                    },
                    {
                          name: "short_name",
                          label: "Short name",
                          type: "text",
                    },
                    {
                          name: "type",
                          label: "Type",
                          type: "chosen",
                          options: type_options,
                    },
                    {
                          name: "parent",
                          label: "Parent",
                          type: "chosen",
                          opts: {allow_single_deselect: "true"},
                          options: parent_options,
                    },
                    {
                          name: "is_inventory",
                          label: "Inventory",
                          type: "checkbox",
                          options: [{label: "", value: "1"}],
                    },
                ]
            });
            source_editor.create(false);
            source_editor.set('type', 13);
            source_editor.set('is_inventory', 1);
            if ('name' in suggested_fields) { source_editor.set('name', suggested_fields.name); };
            if ('short_name' in suggested_fields) { source_editor.set('short_name', suggested_fields.short_name); };
            source_editor.buttons({
                text: "Create",
                className: "btn btn-primary",
                action: function () { this.submit(); }
              }).title('Create New Source').open();
            changeOnType();
            changeOnInv();
    }, 'json');
}

function changeOnType() {
    att_set = 0;
    var c_type = $('#DTE_Field_type').val();
    $.get("/api/options/?lists=attribute_types_"+c_type+"&extra=1&format=json", function ( option_data ) {
          atype_choices = option_data.attribute_types.options;
          atype_ref = option_data.attribute_types.ref;
          if ($('#attribute-formset').hasClass('show')) {
              $('#attribute-formset').find('.formset-item').remove();
          } else {
              $('#attribute-formset').collapse('show');
          };
          addAttributeSet();
    }, 'json');
}

function changeOnInv() {
    page_set = 0;
    if ($('#DTE_Field_is_inventory_0').is(':checked')) {
        $('#page-formset').collapse('show');
    } else {
        $('#page-formset').find('.formset-item').remove();
        $('#page-formset').collapse('hide');
    };
    addPageSet();
}

function addAttributeSet() {
    att_set = att_set + 1
    var new_set = '<div class="formset-item" id="attributeset_'+att_set+'">'
    new_set += '<div class="formset-field-container" data-editor-template="attributes.'+att_set+'.type">\
                </div><a class="remove_icon" onclick="removeSet(this)"><i class="fa fa-minus-circle fa-lg"></i></a></div>'
    $('#attribute-formset').find('.formset-body').append(new_set);
    source_editor.add({
            label: "Attribute type",
            name: "attributes."+att_set+".type",
            type: "chosen",
            options: atype_choices
          });
    var container = $("div[data-editor-template='attributes."+att_set+".type']");
    container.find('label').remove();
    container.find('select').chosen().change(showAttributeField);
    container.find('.col-lg-8').removeClass('col-lg-8');
    container.find('.DTE_Field_Type_chosen').removeClass('row form-group');
}

function addPageSet() {
    if (typeof img_data !== 'undefined') {
        let order = 0;
        var pages = []
        for (const prop in img_data) {
          if (img_data.hasOwnProperty(prop)) {
              pages.push([order+1, img_data[prop]['folio'], prop]);
              order = order + 1;
          }
        }
    } else {
      pages = [[1,"",""]]
    };
    for (let i = 0, len = pages.length; i < len; ++i) {
        page_set = page_set + 1
        var new_set = '<div class="formset-item" id="pageset_'+page_set+'">'
        new_set += '<div class="formset-field-container" data-editor-template="pages.'+page_set+'.order"></div>\
                    <div class="formset-field-container" data-editor-template="pages.'+page_set+'.name"></div>\
                    <div class="formset-field-container" data-editor-template="pages.'+page_set+'.dam_id"></div>\
                    <a class="remove_icon" onclick="alert(\'info\')"><i class="fa fa-info-circle fa-lg"></i></a>\
                    <a class="remove_icon" onclick="removeSet(this)"><i class="fa fa-minus-circle fa-lg"></i></a></div>'
        $('#page-formset').find('.formset-body').append(new_set);
        source_editor.add({
                label: "Folio order",
                name: "pages."+page_set+".order",
                type: "text"
              });
        source_editor.add({
                label: "Folio name",
                name: "pages."+page_set+".name",
                type: "text"
              });
        source_editor.add({
                label: "Folio dam_id",
                name: "pages."+page_set+".dam_id",
                type: "text"
              });
        source_editor.set("pages."+page_set+".order", pages[i][0]);
        source_editor.set("pages."+page_set+".name", pages[i][1]);
        source_editor.set("pages."+page_set+".dam_id", pages[i][2]);
        var fields = $('#pageset_'+page_set).find('.formset-field-container');
        fields.find('label').remove();
        fields.find('.col-lg-8').removeClass('col-lg-8');
    };
}

function removeSet(el) {
  $(el).parent().remove();
}

function showAttributeField() {
    var id = $(this).attr('id').match(/\d+/)[0];
    var selected = $(this).val();
    var type = atype_ref[selected][0];
    var opt = atype_ref[selected][1] || false;
    var type_container = $("div[data-editor-template='attributes."+id+".type']");
    if (opt) {
        $.get("/api/options/?lists=attribute_optexp_"+selected+"&format=json", function ( data ) {
            var choices = data.attribute_optexp;
            type_container.after('<div class="formset-field-container" data-editor-template="attributes.'+id+'.value_'+type+'"></div>');
            source_editor.add({
                    label: "Attribute value",
                    name: "attributes."+id+".value_STR",
                    type: "chosen",
                    options: choices
                  });
            $("div[data-editor-template='attributes."+id+".value_"+type+"']").find('label').remove();
            $("div[data-editor-template='attributes."+id+".value_"+type+"']").find('select').chosen();
        }, 'json');
    } else {
        if (type != 'DATE') {
          type_container.after('<div class="formset-field-container" data-editor-template="attributes.'+id+'.value_'+type+'"></div>');
          if (type == 'TXT') { var dte_type = 'textarea' } else { var dte_type = 'text' };
          source_editor.add({
                  label: "Attribute value",
                  name: "attributes."+id+".value_"+type,
                  type: dte_type
                });
          $("div[data-editor-template='attributes."+id+".value_"+type+"']").find('label').remove();
        } else {
          type_container.after('<div class="formset-field-container">\
              <div data-editor-template="attributes.'+id+'.value_DATE_d"></div>\
              <div data-editor-template="attributes.'+id+'.value_DATE_m"></div>\
              <div data-editor-template="attributes.'+id+'.value_DATE_y"></div></div>');
          source_editor.add({
                  label: "Day",
                  name: "attributes."+id+".value_DATE_d",
                  attr: { maxlength: 2, placeholder: 'day'},
                  type: "text"
                });
          source_editor.add({
                  label: "Month",
                  name: "attributes."+id+".value_DATE_m",
                  type: "chosen",
                  opts: {"disable_search": true},
                  options: {
                    "":"",
                    "January":1,
                    "February":2,
                    "March":3,
                    "April":4,
                    "May":5,
                    "June":6,
                    "July":7,
                    "August":8,
                    "September":9,
                    "October":10,
                    "November":11,
                    "December":12
                  }
                });
          source_editor.add({
                  label: "Year",
                  name: "attributes."+id+".value_DATE_y",
                  attr: { maxlength: 4, placeholder: 'year'},
                  type: "text"
                });
          $("div[data-editor-template='attributes."+id+".value_DATE_d']").find('label').remove();
          $("div[data-editor-template='attributes."+id+".value_DATE_m']").find('label').remove();
          $("div[data-editor-template='attributes."+id+".value_DATE_y']").find('label').remove();
        }
    }
}
