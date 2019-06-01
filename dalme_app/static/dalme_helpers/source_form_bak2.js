function source_form() {
  if (dt_table.ajax.url().split("/")[2] == 'sources') {
      source_editor = dt_editor;
      source_editor.on('open.dalme', function( e, mode, action ) { change_form(e, action) });
      source_editor.on('close.dalme', function( e ) { change_form(e) });
  } else if (dt_table.ajax.url().split("/")[2] == 'images') {
      $.get("/api/options/?lists=content_types_1,parent_sources_13&format=json", function ( option_data ) {
            const type_options = option_data.content_types;
            const parent_options = option_data.parent_sources;
            source_editor = new $.fn.dataTable.Editor( {
                ajax: {
                  create: {
                      type: 'POST',
                      url: '/api/sources/',
                      headers: {'X-CSRFToken': get_cookie("csrftoken") },
                      data: function (data) { return { "data": JSON.stringify( data ) }; }
                    },
                  edit: {
                      type: 'PATCH',
                      url: '/api/sources/_id_/',
                      headers: {'X-CSRFToken': get_cookie("csrftoken") },
                      data: function (data) { return { "data": JSON.stringify( data ) }; }
                    },
                  remove: {
                      type: 'DELETE',
                      url: '/api/sources/_id_/',
                      headers: {'X-CSRFToken': get_cookie("csrftoken") },
                      data: function (data) { data.data = null; return data; }
                    }
                  },
                  idSrc: "id",
                  template: "#inventoryForm",
                  fields: [
                      {
                            name: "name.name",
                            label: "Name",
                            type: "text",
                      },
                      {
                            name: "short_name",
                            label: "Short name",
                            type: "text",
                      },
                      {
                            name: "parent.id",
                            label: "Parent",
                            type: "chosen",
                            opts: {allow_single_deselect: "true"},
                            options: parent_options,
                      },
                      {
                            name: "type.id",
                            label: "Type",
                            type: "chosen",
                            options: type_options,
                      },
                      {
                            name: "is_inventory",
                            label: "Inventory",
                            type: "checkbox",
                            options: [{label: "", value: "1"}],
                      },
                  ]
              });
              source_editor.on('open.dalme', function( e, mode, action ) { change_form(e, action) });
              source_editor.on('close.dalme', function( e ) { change_form(e) });
          }, 'json');
      }
}

function change_form(e, action) {
  if (e.type == 'open') {
      att_set = 0;
      page_set = 0;
      attribute_formset = 'off';
      page_formset = 'off';
      $('.DTE_Form_Content').find('.col-lg-4').removeClass('col-lg-4').addClass('col-lg-2');
      $('.DTE_Form_Content').find('.col-lg-8').removeClass('col-lg-8').addClass('col-lg-10');
      if (action == 'edit') { init_editor() };
      source_editor.field('type.id').input().on('change', change_on_type);
      source_editor.field('is_inventory').input().on('change', change_on_inv);
  } else if (e.type == 'close') {
      clear_entries('attributes');
      $('#attribute-formset').collapse('hide');
      clear_entries('pages');
      $('#page-formset').collapse('hide');
  }
}

function change_on_type(callback) {
    $.get("/api/options/?lists=attribute_types_"+source_editor.get('type.id')+"&extra=1&format=json", function (option_data) {
          atype_choices = option_data.attribute_types.options;
          atype_ref = option_data.attribute_types.ref;
          if ($('#attribute-formset').hasClass('show')) {
              clear_entries('attributes');
          } else {
              attribute_control = {};
              attribute_formset = 'on';
              $('#attribute-formset').collapse('show');
          };
          if (typeof callback !== 'undefined') {
              Function('"use strict";return (' + callback +'())')();
          }
    }, 'json');
}

function change_on_inv() {
    if ($('#DTE_Field_is_inventory_0').is(':checked')) {
        page_control = {};
        page_formset = 'on';
        $('#page-formset').collapse('show');
    } else {
        clear_entries('pages');
        page_formset = 'off';
        $('#page-formset').collapse('hide');
    };
}

function clear_entries(e_type) {
  switch (e_type) {
    case 'attributes':
        $('#attribute-formset').find('select').off('dalme');
        if (!jQuery.isEmptyObject(attribute_control)) {
          for (const prop in attribute_control) {
              if (attribute_control.hasOwnProperty(prop)) {
                  source_editor.clear(attribute_control[prop]);
              }
          };
        };
        attribute_control = {};
        $('#attribute-formset').find('.formset-item').remove();
        $('#attribute-formset').find('.formset-body').append('<div class="formset-none">No attributes assigned.</div>');
        break;
    case 'pages':
        if (!jQuery.isEmptyObject(page_control)) {
          for (const prop in page_control) {
              if (page_control.hasOwnProperty(prop)) {
                  source_editor.clear(page_control[prop]);
              }
          };
        };
        page_control = {};
        $('#page-formset').find('.formset-table').remove();
        $('#page-formset').find('.formset-body').append('<div class="formset-none">No folios selected.</div>');
  }
}

function init_editor() {
    if (attribute_formset == 'on') {
        $.get("/api/attributes/?filter=object_id,"+source_editor.ids()+"&format=json", function (attribute_data) {
              var att_data = attribute_data.data;
              for (let i = 0, len = att_data.length; i < len; ++i) {
                  var prop_dict = {};
                  for (const prop in att_data[i]) {
                      if (att_data[i].hasOwnProperty(prop)) {
                         prop_dict[prop] = att_data[i][prop];
                      }
                  };
                  add_attribute_set(prop_dict);
              };
              $.get("/api/pages/?filter=sources__source,"+source_editor.ids()+"&format=json", function (page_data) {
                  var p_data = page_data.data;
                  change_on_inv();
                  for (let i = 0, len = p_data.length; i < len; ++i) {
                      var prop_dict = {};
                      for (const prop in p_data[i]) {
                          if (p_data[i].hasOwnProperty(prop)) {
                             prop_dict[prop] = p_data[i][prop];
                          }
                      };
                      add_page_set(prop_dict);
                  }
              }, 'json');
          }, 'json');
    } else {
        change_on_type(init_editor);
    }
}

function add_attribute_set(attribute) {
    if (att_set == 0) {
      $('#attribute-formset').find('.formset-none').remove();
    };
    att_set = att_set + 1
    var set_id = 'attributeset_'+att_set;
    var set_list = [];
    var new_set = '<div class="formset-item formset-row" id="'+set_id+'">'
    new_set += '<div class="formset-field-container mr-auto" data-editor-template="attributes.'+att_set+'.attribute_type">\
                </div><a class="remove_icon remove_attribute_set" onclick="remove_set(this)"><i class="fa fa-minus-circle"></i></a></div>'
    $('#attribute-formset').find('.formset-body').append(new_set);
    source_editor.add({
            name: "attributes."+att_set+".id",
            type: "hidden"
          });
    set_list.push("attributes."+att_set+".id");
    source_editor.add({
            label: "Attribute type",
            name: "attributes."+att_set+".attribute_type",
            type: "chosen",
            options: atype_choices
          });
    set_list.push("attributes."+att_set+".attribute_type");
    attribute_control[set_id] = set_list;
    var container = $("div[data-editor-template='attributes."+att_set+".attribute_type']");
    if (typeof attribute !== 'undefined') {
      source_editor.field("attributes."+att_set+".id").val(attribute['id']);
      source_editor.set("attributes."+att_set+".attribute_type", attribute['attribute_type']);
      container.find('select').chosen({width: "200px"});
      add_attribute_values(att_set, attribute);
    } else {
      container.find('select').chosen({width: "200px"}).change( function() {
          add_attribute_values($(this).attr('id').match(/\d+/)[0]);
      });
    }
    container.find('label').remove();
    container.find('.col-lg-8').removeClass('col-lg-8');
    $('#'+set_id).find('.form-group').removeClass('form-group').removeClass('row');
}

function add_page_set(page) {
    if (page_set == 0) {
      $('#page-formset').find('.formset-none').remove();
      $('#page-formset').find('.formset-body').append('<table class="formset-table">\
                            <thead><tr><th>Order</th><th>Folio</th><th>DAM Id</th></tr></thead>\
                            <tbody></tbody></table>');
    };
    page_set = page_set + 1
    var set_id = 'pageset_'+page_set;
    var set_list = [];
    var new_set = '<tr class="formset-row" id="'+set_id+'">';
    new_set += '<td class="formset-td" data-editor-template="pages.'+page_set+'.order"></td>\
                <td class="formset-td" data-editor-template="pages.'+page_set+'.name"></td>\
                <td class="formset-td" data-editor-template="pages.'+page_set+'.dam_id"></td>';
    $('#page-formset').find('tbody').append(new_set);
    source_editor.add({
            name: "pages."+page_set+".id",
            type: "hidden"
          });
    set_list.push("pages."+page_set+".id");
    source_editor.add({
            label: "Folio order",
            name: "pages."+page_set+".order",
            type: "text"
          });
    set_list.push("pages."+page_set+".order");
    source_editor.add({
            label: "Folio name",
            name: "pages."+page_set+".name",
            type: "text"
          });
    set_list.push("pages."+page_set+".name");
    source_editor.add({
            label: "Folio dam_id",
            name: "pages."+page_set+".dam_id",
            type: "text"
          });
    set_list.push("pages."+page_set+".dam_id");
    page_control[set_id] = set_list;
    if (typeof page !== 'undefined') {
      source_editor.field("pages."+page_set+".id").val(page['id']);
      source_editor.set("pages."+page_set+".order", page['order']);
      source_editor.set("pages."+page_set+".name", page['name']);
      source_editor.set("pages."+page_set+".dam_id", page['dam_id']);
    };
    $('[data-editor-template="pages.'+page_set+'.dam_id"]').find('.DTE_Field').append('<a class="remove_icon" onclick="alert(\'info\')"><i class="fa fa-info-circle"></i></a>\
      <a class="remove_icon remove_page_set" onclick="remove_set(this)"><i class="fa fa-minus-circle"></i></a>');
    var fields = $('#pageset_'+page_set).find('.formset-td');
    fields.find('label').remove();
    fields.find('.col-lg-8').removeClass('col-lg-8');
    fields.find('.DTE_Field').removeClass('form-group row');
}

function remove_set(el) {
  var container = $(el).parents('.formset-row');
  var set_id = $(container).attr('id');
  if ($(this).hasClass('remove_attribute_set')) {
      source_editor.clear(attribute_control[set_id]);
      delete attribute_control[set_id];
  } else if ($(this).hasClass('remove_page_set')) {
      source_editor.clear(page_control[set_id]);
      delete page_control[set_id];
  };
  $(container).remove();
}

function add_attribute_values(att_set=undefined, attribute=undefined) {
    if (typeof attribute !== 'undefined') {
        var id = att_set;
        var selected = attribute['attribute_type'];
        var type = attribute['data_type'];
        var opt = attribute['options_list'] || false;
        var type_container = $("div[data-editor-template='attributes."+id+".attribute_type']");
    } else {
        var id = att_set;
        var type_container = $("div[data-editor-template='attributes."+id+".attribute_type']");
        var selected = $(type_container).find('select').val();
        var type = atype_ref[selected][0];
        var opt = atype_ref[selected][1] || false;
    };
    var set_id = 'attributeset_'+id;
    if (opt) {
        $.get("/api/options/?lists=attribute_optexp_"+selected+"&format=json", function ( data ) {
            var choices = data.attribute_optexp;
            type_container.after('<div class="formset-field-container flex-fill" data-editor-template="attributes.'+id+'.value_'+type+'"></div>');
            source_editor.add({
                    label: "Attribute value",
                    name: "attributes."+id+".value_STR",
                    type: "chosen",
                    options: choices
                  });
            if (typeof attribute !== 'undefined') {
                source_editor.set("attributes."+id+".value_STR", attribute['value_STR']);
            };
            attribute_control[set_id].push("attributes."+id+".value_STR");
            $("div[data-editor-template='attributes."+id+".value_"+type+"']").find('label').remove();
            $("div[data-editor-template='attributes."+id+".value_"+type+"']").find('select').chosen();
        }, 'json');
    } else {
        switch (type) {
          case 'TXT':
              type_container.after('<div class="formset-field-container flex-fill" data-editor-template="attributes.'+id+'.value_TXT"></div>');
              source_editor.add({
                      label: "Attribute value",
                      name: "attributes."+id+".value_TXT",
                      type: 'textarea'
                    });
              if (typeof attribute !== 'undefined') {
                  source_editor.set("attributes."+id+".value_TXT", attribute['value_TXT']);
              };
              attribute_control[set_id].push("attributes."+id+".value_TXT");
              $("div[data-editor-template='attributes."+id+".value_TXT']").find('label').remove();
              break;
            case 'STR':
                type_container.after('<div class="formset-field-container flex-fill" data-editor-template="attributes.'+id+'.value_STR"></div>');
                source_editor.add({
                        label: "Attribute value",
                        name: "attributes."+id+".value_STR",
                        type: 'text'
                      });
                if (typeof attribute !== 'undefined') {
                    source_editor.set("attributes."+id+".value_STR", attribute['value_STR']);
                };
                attribute_control[set_id].push("attributes."+id+".value_STR");
                $("div[data-editor-template='attributes."+id+".value_STR']").find('label').remove();
                break;
            case 'INT':
                type_container.after('<div class="formset-field-container flex-fill" data-editor-template="attributes.'+id+'.value_INT"></div>');
                source_editor.add({
                        label: "Attribute value",
                        name: "attributes."+id+".value_INT",
                        type: 'text'
                      });
                if (typeof attribute !== 'undefined') {
                    source_editor.set("attributes."+id+".value_INT", attribute['value_STR']);
                };
                attribute_control[set_id].push("attributes."+id+".value_INT");
                $("div[data-editor-template='attributes."+id+".value_INT']").find('label').remove();
                break;
            case 'DATE':
                type_container.after('<div class="formset-field-container w-15"><div data-editor-template="attributes.'+id+'.value_DATE_d"></div></div>\
                    <div class="formset-field-container flex-fill"><div data-editor-template="attributes.'+id+'.value_DATE_m"></div></div>\
                    <div class="formset-field-container w-20"><div data-editor-template="attributes.'+id+'.value_DATE_y"></div></div>');
                source_editor.add({
                        label: "Day",
                        name: "attributes."+id+".value_DATE_d",
                        attr: { maxlength: 2, placeholder: 'day'},
                        type: "text"
                      });
                if (typeof attribute !== 'undefined') {
                    source_editor.set("attributes."+id+".value_DATE_d", attribute['value_DATE_d']);
                };
                attribute_control[set_id].push("attributes."+id+".value_DATE_d");
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
                if (typeof attribute !== 'undefined') {
                    source_editor.set("attributes."+id+".value_DATE_m", attribute['value_DATE_m']);
                };
                attribute_control[set_id].push("attributes."+id+".value_DATE_m");
                source_editor.add({
                        label: "Year",
                        name: "attributes."+id+".value_DATE_y",
                        attr: { maxlength: 4, placeholder: 'year'},
                        type: "text"
                      });
                if (typeof attribute !== 'undefined') {
                    source_editor.set("attributes."+id+".value_DATE_y", attribute['value_DATE_y']);
                };
                attribute_control[set_id].push("attributes."+id+".value_DATE_y");
                $("div[data-editor-template='attributes."+id+".value_DATE_d']").find('label').remove();
                $("div[data-editor-template='attributes."+id+".value_DATE_m']").find('label').remove();
                $("div[data-editor-template='attributes."+id+".value_DATE_y']").find('label').remove();
          }
    };
    $('#'+set_id).find('.form-group').removeClass('form-group').removeClass('row');
    $('#'+set_id).find('.col-lg-8').removeClass('col-lg-8');
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
                    headers: {'X-CSRFToken': get_cookie("csrftoken") },
                    data: function (data) { return { "data": JSON.stringify( data ) }; }
                  },
                edit: {
                    type: 'PATCH',
                    url: '/api/sources/_id_/',
                    headers: {'X-CSRFToken': get_cookie("csrftoken") },
                    data: function (data) { return { "data": JSON.stringify( data ) }; }
                  },
                remove: {
                    type: 'DELETE',
                    url: '/api/sources/_id_/',
                    headers: {'X-CSRFToken': get_cookie("csrftoken") },
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
            change_on_type();
            change_on_inv();
    }, 'json');
}
