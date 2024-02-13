function source_forms_load() {
}

function source_forms_init() {
  one_time_setup = false;
}

function source_form_setup(e, mode, action) {
    if (!one_time_setup) {
      $('[for="DTE_Field_pages[]"]').remove()
      $('[for="DTE_Field_sets[]-id"]').remove()
      $('[for="DTE_Field_credits[]"]').remove()

      $('#add_page_button').on('click.dalme', function() {
        dt_editor.field('pages[]').addNew();
      })

      $('#add_credit_button').on('click.dalme', function() {
        dt_editor.field('credits[]').addNew();
      })

      one_time_setup = true;
    }

    if (source_type == 'records') {
      $('#form-side-container').removeClass('d-none');
    }

    if (source_type == 'bibliography') {
      let selectize = dt_editor.field('attributes.zotero_key').inst()
      // console.log(selectize)
      selectize.on('change', populate_biblio_fields);
    }

    if (action == 'create') {
      toggle_fields(required_list);
    } else if (action == 'edit') {
      var row_data = dt_table.row(dt_editor.modifier()).data();
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
    }
}

function source_form_restore(e) {
  if (source_type == 'records') {
    $('#form-side-container').addClass('d-none');
  }
}

function populate_biblio_fields() {
  let selectize = dt_editor.field('attributes.zotero_key').inst()
  let opt = selectize.options[selectize.getValue()]
  let types = {
    'book': 1,
    'bookSection': 4,
    'encyclopediaArticle': 9,
    'journalArticle': 3,
    'magazineArticle': 6,
    'manuscript': 7,
    'newspaperArticle': 6,
    'thesis': 11,
    'webpage': 2
  }
  dt_editor.field('name').set(opt.title)
  dt_editor.field('short_name').set(opt.shortTitle)
  dt_editor.field('type.id').set(types[opt.itemType])
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
//             "value_str": "",
//             "attribute_name": "Record type (record_type)",
//             "data_type": "STR",
//             "options_list": "list(set(list(Attribute.objects.filter(attribute_type=28).values_list('value_str', flat=True))))"
//           },
//           {
//             "attribute_type": 29,
//             "value_str": "",
//             "attribute_name": "Record type phrase (record_type_phrase)",
//             "data_type": "STR",
//             "options_list": ""
//           }
//         ];
//         const person_text = 'person' in source_fields ? source_fields.person : '';
//         default_attributes.push(
//           {
//             "attribute_type": 37,
//             "value_str": person_text,
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
//                 "value_date_d": d_array.day,
//                 "value_date_m": d_array.month,
//                 "value_date_y": d_array.year,
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
//                   "value_date_d": d_array.day,
//                   "value_date_m": d_array.month,
//                   "value_date_y": d_array.year,
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
//               "value_str": source_fields.city,
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
