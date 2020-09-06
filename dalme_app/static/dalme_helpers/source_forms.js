function source_forms_load() {
}

function source_forms_init() {
  sets_list = [];
  pages_list = [];
  one_time_setup = false;
  attribute_concordance_rev = {}
  for (key in attribute_concordance)
    attribute_concordance_rev[attribute_concordance[key]] = key;
  dt_editor.on('initEdit.dalme', function(e, node, data, items, type) {
      return new Promise(function (resolve, reject) {
          $.ajax({
              method: "POST",
              url: "/api/sources/" + data.id + "/has_permission/",
              headers: { 'X-CSRFToken': get_cookie("csrftoken") },
          }).done(function(response, textStatus, jqXHR) {
              resolve();
          }).fail(function(jqXHR, textStatus, errorThrown) {
              dt_editor.on('preOpen.dalme', function(e, mode, action) { return false });
              toastr.error(jqXHR.responseJSON.detail);
              resolve();
          });
      });
  });
}

function source_form_setup(e, mode, action) {
    if (!one_time_setup) {
      $('.sets-body').on('click.dalme', '.formset_flatentry_delete', function() {
        let conf = confirm("Are you sure you wish to remove this set?");
        if (conf == true) {
          remove_formset(this, 'sets');
        }
      });
      $('#pages-table').on('click.dalme', '.page_delete', function() {
        remove_formset(this, 'pages');
      });
      one_time_setup = true;
    }
    if (source_type == 'records') {
      $('#add-pages-button').removeClass('d-none');
    }
    if (action == 'create') {
      toggle_fields(required_list);
    }
    if (action == 'edit') {
      let row_data = dt_table.row(dt_editor.modifier()).data();
      let current_attributes = []
      Object.keys(row_data).forEach((x) => { current_attributes.push(attribute_concordance[x])});
      if (Object.keys(row_data).includes('attributes')) {
        Object.keys(row_data['attributes']).forEach((x) => { current_attributes.push(attribute_concordance[x])});
      }
      if (Object.keys(row_data).includes('workflow')) {
        Object.keys(row_data['workflow']).forEach((x) => { current_attributes.push(attribute_concordance[x])});
      }
      required_list.forEach((x) => {
        if (!current_attributes.includes(x)) {
          current_attributes.push(x)
        }
      })
      toggle_fields(current_attributes.filter(Boolean));
      if (row_data['pages'].length) {
        pages_list = row_data['pages'];
        populate_formset('pages');
      }
      if (row_data['sets'].length) {
        sets_list = row_data['sets'];
        populate_formset('sets');
      }
    }
}

function source_form_restore(e) {
  $('#add-pages-button').addClass('d-none');
  if (sets_list.length) {
    for (let i = 0, len = sets_list.length; i < len; ++i) {
      let set = 'sets.' + i + '.set_id';
      if (dt_editor.order().includes(set)) { dt_editor.clear(set); }
    }
  }
  sets_list.splice(0, sets_list.length);
  $('.sets-body').html('');
  $('#sets-formset').removeClass('show');
  if (pages_list.length) {
    for (let i = 0, len = pages_list.length; i < len; ++i) {
      dt_editor.clear('pages.' + i + '.id');
      dt_editor.clear('pages.' + i + '.order');
      dt_editor.clear('pages.' + i + '.name');
      dt_editor.clear('pages.' + i + '.dam_id');
    }
  }
  pages_list.splice(0, pages_list.length);
  $('.pages-table-body').html('');
  $('#pages-formset').removeClass('show');
}

function toggle_fields(field_list) {
  let editor_fields = Object.values(attribute_concordance);
  let add_menu_list = [];
  for (let i = 0, len = editor_fields.length; i < len; ++i) {
    if (field_list.includes(editor_fields[i])) {
      dt_editor.show(editor_fields[i]);
      if (typeof multi_attributes !== 'undefined') {
        if (multi_attributes.includes(editor_fields[i])) {
          add_menu_list.push(editor_fields[i]);
        }
      }
    } else {
      dt_editor.hide(editor_fields[i]);
      add_menu_list.push(editor_fields[i]);
    }
  }
  populate_add_menu(add_menu_list);
}

function populate_add_menu(menu_list) {
  if (menu_list) {
    let clean_menu_list = []
    menu_list.forEach((x) => { clean_menu_list.push(attribute_concordance_rev[x])});
    clean_menu_list.sort();
    $('#add-attribute-menu-container').html('');
    for (let i = 0, len = clean_menu_list.length; i < len; ++i) {
        $('#add-attribute-menu-container').append('<a class="dropdown-item" href="#" onclick="dt_editor.show(\'' + attribute_concordance[clean_menu_list[i]] + '\')">' + clean_menu_list[i].replace('_', ' ').replace(/^\w/, (c) => c.toUpperCase()) + '</a>');
    }
    $('#add-attribute-button').removeClass('d-none');
  } else {
    $('#add-attribute-button').addClass('d-none');
  }
}

function toggle_formset(type) {
  let alternate = type == 'sets' ? 'pages' : 'sets'
  if ($('#' + type +'-formset').hasClass('show')) {
    $('#' + type + '-formset').removeClass('show');
    $('#add-' + type + '-button').find('.fa-caret-right').removeClass('fa-caret-right').addClass('fa-caret-left');
    $('#add-' + type + '-button').removeClass('active');
  } else {
    if ($('#' + alternate +'-formset').hasClass('show')) {
      $('#' + alternate + '-formset').removeClass('show');
      $('#add-' + alternate + '-button').find('.fa-caret-right').removeClass('fa-caret-right').addClass('fa-caret-left');
      $('#add-' + alternate + '-button').removeClass('active');
    }
    $('#' + type + '-formset').addClass('show');
    $('#add-' + type + '-button').find('.fa-caret-left').removeClass('fa-caret-left').addClass('fa-caret-right');
    $('#add-' + type + '-button').addClass('active');
  }
}

function populate_formset(type) {
  var count = 0;
  switch (type) {
    case 'sets':
      for (let i = 0, len = sets_list.length; i < len; ++i) {
          $('.sets-body').append('<div class="formset_flatentry" id="sets.' + i + '">\
          <div class="d-flex flex-column flex-grow-1 ml-2 mr-2 pb-2 pt-2">\
          <span class="formset_flatentry_title">' + sets_list[i]['name'] + '</span>\
          <span class="formset_flatentry_detail">' + sets_list[i]['detail_string'] + '</span>\
          </div><div class="formset_flatentry_delete button-pointer" title="Delete set" data-list-id="' + i + '"><i class="fas fa-trash-alt fa-fw"></i></div></div>');
          dt_editor.add({ name: 'sets.' + i + '.set_id', type: 'hidden' });
      }
      count = sets_list.length;
      break;
    case 'pages':
      for (let i = 0, len = pages_list.length; i < len; ++i) {
        add_page(pages_list[i], i);
      }
      count = pages_list.length;
  }
  $('#' + type + '-count').html(count);
}

function add_set() {
  var index = sets_list.length;
  $('.sets-body').append('<div class="formset_flatentry"><div class="w-100" data-editor-template="sets.' + index + '.set_id"></div><div class="formset_flatentry_delete button-pointer" title="Delete set" data-list-id="' + index + '"><i class="fas fa-trash-alt fa-fw"></i></div></div>');
  dt_editor.add({
        name: 'sets.' + index + '.set_id',
        type: "selectize",
        opts: {
            placeholder: "Select set",
            preload: true,
            load: function(query, callback) {
                      var self = this;
                      $.ajax({
                          method: "GET",
                          url: "/api/sets/?format=select&q=" + encodeURIComponent(query),
                      }).done(function(response, textStatus, jqXHR) {
                          callback(response);
                          console.log(self)
                      }).fail(function(jqXHR, textStatus, errorThrown) {
                          callback();
                      });
                  },
            render: {
              option: function(item, escape) {
                return '<div class="pt-2 pb-2 pl-2 pr-2">' +
                '<div class="formset_flatentry_title">' + escape(item.label) + '</div>' +
                '<div class="formset_flatentry_detail">' + escape(item.detail) + '</div>' +
                '</div>';
              }
            }
        }
    });
  sets_list.push({'set_id': 'sets.' + index});
  $('#sets-formset').find('label').remove();
  $('#sets-formset').find('.col-lg-8').removeClass('col-lg-8');
}

function add_page(page, index) {
  if ($('#pages-table').hasClass('d-none')) {
    $('#pages-table').removeClass('d-none');
  }
  if (typeof page == 'undefined') {
    var index = pages_list.length;
  }
  $('.pages-table-body').append('<div class="d-table-row" id="pages.' + index + '">\
    <div class="d-none" data-editor-template="pages.' + index + '.id"></div>\
    <div class="formset-td" data-editor-template="pages.' + index + '.order"></div>\
    <div class="formset-td" data-editor-template="pages.' + index + '.name"></div>\
    <div class="formset-td" data-editor-template="pages.' + index + '.dam_id"></div>\
    <div class="formset-td page_delete" data-list-id="' + index + '"><i class="fas fa-trash-alt fa-fw"></i></div></div>');
  dt_editor.add({ name: 'pages.' + index + '.id', type: "hidden" });
  dt_editor.add({ name: 'pages.' + index + '.order', type: "text" });
  dt_editor.add({ name: 'pages.' + index + '.name', type: "text" });
  dt_editor.add({ name: 'pages.' + index + '.dam_id', type: "text" });
  $('#pages-table').find('label').remove();
  $('#pages-table').find('.col-lg-8').removeClass('col-lg-8');
  if (typeof page == 'undefined') {
    pages_list.push({'id': 'pages.' + index});
  } else {
    dt_editor.set('pages.' + index + '.id', page['id']);
    dt_editor.set('pages.' + index + '.order', page['order']);
    dt_editor.set('pages.' + index + '.name', page['name']);
    dt_editor.set('pages.' + index + '.dam_id', page['dam_id']);
  }
}

function remove_formset(element, type) {
  let index = $(element).data('list-id');
  if (type == 'pages') {
    dt_editor.clear('pages.' + index + '.id');
    dt_editor.clear('pages.' + index + '.order');
    dt_editor.clear('pages.' + index + '.name');
    dt_editor.clear('pages.' + index + '.dam_id');
    pages_list.splice(index, 1);
    $(element).parent().remove();
  } else {
    let field = 'sets.' + index + '.set_id';
    if (dt_editor.order().includes(field)) { dt_editor.clear(field);}
    sets_list.splice(index, 1);
    $(element).parent().remove();
  }
}

// function init_dt_editor(para_data) {
//     folio_data = para_data.data.folios
//     source_fields = para_data.data.source_fields
//     dt_editor.create(false);
//     dt_editor.set('type.value', 13);
//     dt_editor.set('has_inventory', 1);
//     if (source_fields.name != '') {
//         dt_editor.set('name.value', source_fields.name);
//     } else {
//         dt_editor.field('name.value').input().attr("placeholder", "No suggestion, please enter name manually");
//     };
//     if (source_fields.short_name != '') {
//         dt_editor.set('short_name', source_fields.short_name);
//     } else {
//         dt_editor.field('short_name').input().attr("placeholder", "No suggestion, please enter short name manually");
//     };
//     dt_editor.buttons({
//         text: "Create",
//         className: "btn btn-primary",
//         action: function () { this.submit(); }
//     }).title('Create New Source').open();
//     create_from_images();
// }
//
// function create_from_images() {
//     if (attribute_formset == 'on') {
//         var default_attributes = [
//           {
//             "attribute_type": 28,
//             "value_STR": "",
//             "attribute_name": "Record type (record_type)",
//             "data_type": "STR",
//             "options_list": "list(set(list(Attribute.objects.filter(attribute_type=28).values_list('value_STR', flat=True))))"
//           },
//           {
//             "attribute_type": 29,
//             "value_STR": "",
//             "attribute_name": "Record type phrase (record_type_phrase)",
//             "data_type": "STR",
//             "options_list": ""
//           }
//         ];
//         const person_text = 'person' in source_fields ? source_fields.person : '';
//         default_attributes.push(
//           {
//             "attribute_type": 37,
//             "value_STR": person_text,
//             "attribute_name": "Named persons",
//             "data_type": "STR",
//             "options_list": ""
//           }
//         );
//         if ('SourceStartDate' in source_fields || 'ressourcedate' in source_fields) {
//           const d_array = 'SourceStartDate' in source_fields ? get_rsdate_array(source_fields.SourceStartDate) : get_rsdate_array(source_fields.ressourcedate);
//           if (d_array && d_array.year < 1999) {
//             default_attributes.push(
//               {
//                 "attribute_type": 26,
//                 "attribute_name": "Start date",
//                 "value_DATE_d": d_array.day,
//                 "value_DATE_m": d_array.month,
//                 "value_DATE_y": d_array.year,
//                 "data_type": "DATE",
//                 "options_list": ""
//               },
//             );
//           };
//         };
//         if ('SourceEndDate' in source_fields) {
//           const d_array = get_rsdate_array(source_fields.SourceEndDate);
//           if (d_array) {
//               default_attributes.push(
//                 {
//                   "attribute_type": 25,
//                   "attribute_name": "End date",
//                   "value_DATE_d": d_array.day,
//                   "value_DATE_m": d_array.month,
//                   "value_DATE_y": d_array.year,
//                   "data_type": "DATE",
//                   "options_list": ""
//                 },
//               );
//           };
//         };
//         if ('city' in source_fields) {
//           default_attributes.push(
//             {
//               "attribute_type": 36,
//               "value_STR": source_fields.city,
//               "attribute_name": "City",
//               "data_type": "STR",
//               "options_list": "[{'label': i.name, 'value': i.name} for i in City.objects.all()]"
//             }
//           );
//         };
//         for (let i = 0, len = default_attributes.length; i < len; ++i) { add_attribute_set(default_attributes[i], 'create'); };
//         page_control = {};
//         page_formset = 'on';
//         $('#page-formset').collapse('show');
//         let order = 0;
//         var pages = []
//         for (const prop in folio_data) {
//           if (folio_data.hasOwnProperty(prop)) {
//               add_page_set({
//                 'id': 'null',
//                 'order': order+1,
//                 'name': folio_data[prop],
//                 'dam_id': prop
//               });
//               order = order + 1;
//           }
//         }
//     } else {
//         change_on_type(create_from_images);
//     }
// }
//
// function get_rsdate_array(d_string) {
//     var date_array = {};
//     var dashes = (d_string.match(/-/g) || []).length;
//     switch (dashes) {
//       case 2:
//         var date_match = d_string.match(/(\d{4})-(\d{2})-(\d{2})/) || 0;
//         break;
//       case 1:
//         var date_match = d_string.match(/(\d{4})-(\d{2})/) || 0;
//         break;
//       case 0:
//         var date_match = d_string.match(/(\d{4})/) || 0;
//     };
//     if (typeof date_match != 0) {
//       date_array['day'] = typeof date_match[3] === 'undefined' ? '' : date_match[3];
//       date_array['month'] = typeof date_match[2] === 'undefined' ? '' : date_match[2];
//       date_array['year'] = date_match[1];
//     };
//     return date_array;
// }
