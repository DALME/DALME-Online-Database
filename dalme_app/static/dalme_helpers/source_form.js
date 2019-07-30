function source_form() {
  if (dt_table.ajax.url().split("/")[2] == 'sources') {
    $.get("/api/options/?lists=content_types_opt&format=json", function (option_data) {
          ct_opt = option_data.content_types_opt;
          source_editor = dt_editor;
          source_editor.hide(['parent.value', 'has_inventory']);
          source_editor.on('open.dalme', function(e, mode, action) { change_form(e, action) });
          source_editor.on('close.dalme', function(e) { change_form(e) });
    }, 'json');
  } else if (dt_table.ajax.url().split("/")[2] == 'images') {
      $.get("/api/options/?lists=content_types_opt,content_types_0,parent_sources_13&format=json", function (option_data) {
            ct_opt = option_data.content_types_opt;
            const type_options = option_data.content_types;
            parent_options = option_data.parent_sources;
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
                            name: "name.value",
                            label: "Name",
                            type: "text",
                            message: "Name of the source, <i>eg: Inventory of Poncius Gassini (ADBR 3B 57)</i>",
                      },
                      {
                            name: "short_name",
                            label: "Short name",
                            type: "text",
                            message: "A short name for the source to use in lists, <i>eg: ADBR 3B 57 (Gassini)</i>"
                      },
                      {
                            name: "type.value",
                            label: "Type",
                            type: "selectize",
                            options: type_options,
                      },
                      {
                            name: "parent.value",
                            label: "Parent",
                            type: "selectize",
                            options: parent_options,
                            message: "Parent record,if applicable, <i>eg: a book for a book chapter, a register for an act, etc.</i>"
                      },
                      {
                            name: "has_inventory",
                            label: "Inventory",
                            type: "checkbox",
                            options: [{label: "Indicates whether this source contains an inventory.", value: "1"}],
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
      attribute_control = {};
      page_control = {};
      $('.DTE_Form_Content').find('.col-lg-4').removeClass('col-lg-4').addClass('col-lg-2');
      $('.DTE_Form_Content').find('.col-lg-8').removeClass('col-lg-8').addClass('col-lg-10');
      if (action == 'edit') {
          source_editor.on('submitSuccess', function(e, json, data, action) { toastr.success('The source was updated succesfully.') });
          init_editor()
      } else if (action == 'create') {
          source_editor.on('submitSuccess', function(e, json, data, action) { toastr.success('The source was created succesfully.') });
      };
      source_editor.field('type.value').input().on('change.dalme', change_on_type);
  } else if (e.type == 'close') {
      source_editor.field('type.value').input().off('change.dalme');
      source_editor.hide(['parent.value', 'has_inventory']);
      clear_entries('attributes');
      $('#attribute-formset').collapse('hide');
      clear_entries('pages');
      $('#page-formset').collapse('hide');
  }
}

function change_on_type(callback='undefined') {
    var ctype = source_editor.get('type.value');
    $.get("/api/options/?lists=parent_sources_"+ctype+",attribute_types_"+ctype+"&extra=1&format=json", function (option_data) {
          atype_choices = option_data.attribute_types.options;
          atype_ref = option_data.attribute_types.ref;
          parent_options = option_data.parent_sources;
          if ($('#attribute-formset').hasClass('show')) {
              clear_entries('attributes');
          } else {
              attribute_control = {};
              attribute_formset = 'on';
              $('#attribute-formset').collapse('show');
          };
          if (ct_opt[ctype]['pages'] == 1) {
              if (!$('#page-formset').hasClass('show')) {
                  page_control = {};
                  page_formset = 'on';
                  $('#page-formset').collapse('show');
              }
          } else {
              if ($('#page-formset').hasClass('show')) {
                  clear_entries('pages');
                  page_formset = 'off';
                  $('#page-formset').collapse('hide');
              }
          };
          if (ct_opt[ctype]['inv'] == 1) {
              if (!source_editor.field('has_inventory').displayed()) {
                source_editor.show('has_inventory');
              }
          } else {
              if (source_editor.field('has_inventory').displayed()) {
                source_editor.hide('has_inventory');
              }
          };
          if (parent_options != 'n/a') {
            source_editor.field('parent.value').update(parent_options);
            if (!source_editor.field('parent.value').displayed()) {
              source_editor.show('parent.value');
            }
          } else {
            if (source_editor.field('parent.value').displayed()) {
              source_editor.hide('parent.value');
            }
          };
          if (typeof callback !== 'undefined') {
              Function('"use strict";return (' + callback +'())')();
          }
    }, 'json');
}

function clear_entries(e_type) {
  switch (e_type) {
    case 'attributes':
        $('#attribute-formset').find('select').off('change.dalme');
        if (!jQuery.isEmptyObject(attribute_control)) {
          for (const prop in attribute_control) {
              if (attribute_control.hasOwnProperty(prop)) {
                  source_editor.clear(attribute_control[prop]);
              }
          };
        };
        attribute_control = {};
        $('#attribute-formset').find('.formset-item').remove();
        if (!$('#attribute-formset').find('.formset-none').length) {
            $('#attribute-formset').find('.formset-body').append('<div class="formset-none">No attributes assigned.</div>');
        }
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
        $('#page-formset').find('.formset-item').remove();
        if (!$('#page-formset').find('.formset-none').length) {
            $('#page-formset').find('.formset-body').append('<div class="formset-none">No folios selected.</div>');
        }
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
                  page_control = {};
                  page_formset = 'on';
                  $('#page-formset').collapse('show');
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
                </div><a class="remove_icon remove_attribute_set" onclick="remove_set(this)"\
                data-toggle="tooltip" data-placement="top" title="Remove attribute"><i class="fa fa-minus-circle"></i></a></div>'
    $('#attribute-formset').find('.formset-body').append(new_set);
    if (typeof attribute !== 'undefined') {
      source_editor.add({
              name: "attributes."+att_set+".id",
              type: "hidden"
            });
      set_list.push("attributes."+att_set+".id");
    };
    source_editor.add({
            label: "Attribute type",
            name: "attributes."+att_set+".attribute_type",
            type: "selectize",
            className: "attribute_selectize",
            options: atype_choices
          });
    set_list.push("attributes."+att_set+".attribute_type");
    attribute_control[set_id] = set_list;
    var container = $("div[data-editor-template='attributes."+att_set+".attribute_type']");
    if (typeof attribute !== 'undefined') {
      source_editor.field("attributes."+att_set+".id").val(attribute['id']);
      source_editor.set("attributes."+att_set+".attribute_type", attribute['attribute_type']);
      add_attribute_values(att_set, attribute);
    } else {
      container.find('select').change( function() {
           add_attribute_values($(this).attr('id').match(/\d+/)[0]);
      });
    }
    container.find('label').remove();
    container.find('.col-lg-8').removeClass('col-lg-8');
    $('#'+set_id).find('.form-group').removeClass('form-group').removeClass('row');
    $('[data-toggle="tooltip"]').tooltip({container: 'body', trigger: 'hover'});
}

function add_page_set(page) {
    if (page_set == 0) {
      $('#page-formset').find('.formset-none').remove();
    };
    page_set = page_set + 1
    var set_id = 'pageset_'+page_set;
    var set_list = [];
    var new_set = '<fieldset class="formset-item formset-row" id="'+set_id+'">'
    new_set += '<div class="formset-field-container w-15" data-editor-template="pages.'+page_set+'.order"></div>\
                <div class="formset-field-container w-15" data-editor-template="pages.'+page_set+'.name"></div>\
                <div class="formset-field-container flex-fill" data-editor-template="pages.'+page_set+'.dam_id"></div>\
                <div class="util-icon-set"><a class="info_icon" data-toggle="popover" title="DAM Metadata"\
                data-content="Metadata from the DAM can only be shown if an image id is included in the page record."><i class="fa fa-info-circle"></i></a>\
                <a class="remove_icon remove_page_set" onclick="remove_set(this)" data-toggle="tooltip" data-placement="top"\
                title="Remove folio"><i class="fa fa-minus-circle"></i></a></div></fieldset>'
    $('#page-formset').find('.formset-body').append(new_set);
    source_editor.add({
            name: "pages."+page_set+".id",
            type: "hidden"
          });
    set_list.push("pages."+page_set+".id");
    source_editor.add({
            label: "Order",
            name: "pages."+page_set+".order",
            type: "text",
            className: "d-flex"
          });
    set_list.push("pages."+page_set+".order");
    source_editor.add({
            label: "Folio",
            name: "pages."+page_set+".name",
            type: "text",
            className: "d-flex"
          });
    set_list.push("pages."+page_set+".name");
    source_editor.add({
            label: "DAM Id",
            name: "pages."+page_set+".dam_id",
            type: "text",
            className: "d-flex"
          });
    set_list.push("pages."+page_set+".dam_id");
    page_control[set_id] = set_list;
    if (typeof page !== 'undefined') {
      source_editor.field("pages."+page_set+".id").val(page['id']);
      source_editor.set("pages."+page_set+".order", page['order']);
      source_editor.set("pages."+page_set+".name", page['name']);
      source_editor.set("pages."+page_set+".dam_id", page['dam_id']);
    };
    $('#'+set_id).find('.col-lg-8').removeClass('col-lg-8').addClass('flex-grow-1');
    $('#'+set_id).find('.col-lg-4').removeClass('col-lg-4');
    $('#'+set_id).find('.form-group').removeClass('form-group').removeClass('row');
    $('[data-toggle="tooltip"]').tooltip({container: 'body', trigger: 'hover'});
    $('[data-toggle="popover"]').popover({container: 'body'});
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
        var set_id = 'attributeset_'+id;
        if (Object.keys(attribute_control[set_id]).length > 2) {
            for (let i = 2, len = Object.keys(attribute_control[set_id]).length; i < len; ++i) {
              source_editor.clear(attribute_control[set_id][i]);
              $("div[data-editor-template='"+attribute_control[set_id][i]+"']").remove();
              delete attribute_control[set_id][i];
            }
        }
    } else {
        var id = att_set;
        var type_container = $("div[data-editor-template='attributes."+id+".attribute_type']");
        var selected = $(type_container).find('select').val();
        var type = atype_ref[selected][0];
        var opt = atype_ref[selected][1] || false;
        var set_id = 'attributeset_'+id;
        if (Object.keys(attribute_control[set_id]).length > 1) {
          for (let i = 1, len = Object.keys(attribute_control[set_id]).length; i < len; ++i) {
            source_editor.clear(attribute_control[set_id][i]);
            $("div[data-editor-template='"+attribute_control[set_id][i]+"']").remove();
            delete attribute_control[set_id][i];
          }
        }
    };
    if (opt) {
        $.get("/api/options/?lists=attribute_optexp_"+selected+"&format=json", function ( data ) {
            var choices = data.attribute_optexp;
            type_container.after('<div class="formset-field-container flex-fill" data-editor-template="attributes.'+id+'.value_'+type+'"></div>');
            source_editor.add({
                    label: "Attribute value",
                    name: "attributes."+id+".value_STR",
                    type: "selectize",
                    options: choices
                  });
            if (typeof attribute !== 'undefined') {
                source_editor.set("attributes."+id+".value_STR", attribute['value_STR']);
            };
            attribute_control[set_id].push("attributes."+id+".value_STR");
            $("div[data-editor-template='attributes."+id+".value_"+type+"']").find('label').remove();
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
                source_editor.add({
                        label: "Month",
                        name: "attributes."+id+".value_DATE_m",
                        type: "selectize",
                        opts: { placeholder: "month" },
                        options: [
                          {'label': "January", 'value': 1},
                          {'label': "February", 'value': 2},
                          {'label': "March", 'value': 3},
                          {'label': "April", 'value': 4},
                          {'label': "May", 'value': 5},
                          {'label': "June", 'value': 6},
                          {'label': "July", 'value': 7},
                          {'label': "August", 'value': 8},
                          {'label': "September", 'value': 9},
                          {'label': "October", 'value': 10},
                          {'label': "November", 'value': 11},
                          {'label': "December", 'value': 12}
                        ]
                      });
                source_editor.add({
                        label: "Year",
                        name: "attributes."+id+".value_DATE_y",
                        attr: { maxlength: 4, placeholder: 'year'},
                        type: "text"
                      });
                attribute_control[set_id].push("attributes."+id+".value_DATE_d");
                attribute_control[set_id].push("attributes."+id+".value_DATE_m");
                attribute_control[set_id].push("attributes."+id+".value_DATE_y");
                if (typeof attribute !== 'undefined') {
                    source_editor.set("attributes."+id+".value_DATE_d", attribute['value_DATE_d']);
                    source_editor.set("attributes."+id+".value_DATE_m", attribute['value_DATE_m']);
                    source_editor.set("attributes."+id+".value_DATE_y", attribute['value_DATE_y']);
                };
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
    source_editor.create(false);
    source_editor.set('type.value', 13);
    source_editor.set('has_inventory', 1);
    if ('name' in suggested_fields) {
        source_editor.set('name.value', suggested_fields.name);
    } else {
        source_editor.field('name.value').input().attr("placeholder", "No suggestion, please enter name manually");
    }
    if ('short_name' in suggested_fields) {
        source_editor.set('short_name', suggested_fields.short_name);
    } else {
        source_editor.field('short_name').input().attr("placeholder", "No suggestion, please enter short name manually");
    }
    source_editor.buttons({
        text: "Create",
        className: "btn btn-primary",
        action: function () { this.submit(); }
    }).title('Create New Source').open();
    create_from_images();
}

function create_from_images() {
    if (attribute_formset == 'on') {
        page_control = {};
        page_formset = 'on';
        $('#page-formset').collapse('show');
        let order = 0;
        var pages = []
        for (const prop in img_data) {
          if (img_data.hasOwnProperty(prop)) {
              add_page_set({
                'id': 'null',
                'order': order+1,
                'name': img_data[prop]['folio'],
                'dam_id': prop
              });
              order = order + 1;
          }
        }
    } else {
        change_on_type(create_from_images);
    }
}
