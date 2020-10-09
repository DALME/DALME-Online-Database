/**
 * This plug-in allows managing pages.
*/

(function(factory) {
  if (typeof define === 'function' && define.amd) {
    define(['jquery', 'datatables', 'datatables-editor'], factory);
  } else if (typeof exports === 'object') {
    // Node / CommonJS
    module.exports = function ($, dt) {
      if (!$) { $ = require('jquery'); }
      factory( $, dt || $.fn.dataTable || require('datatables') );
    };
  } else if (jQuery) {
    // Browser standard
    factory(jQuery, jQuery.fn.dataTable);
  }
}(function($, DataTable) {
'use strict';

if (!DataTable.ext.editorFields) {
  DataTable.ext.editorFields = {};
}

var _fieldTypes = DataTable.Editor ? DataTable.Editor.fieldTypes : DataTable.ext.editorFields;

_fieldTypes.dalmePages = {

  _addPage: function(conf, val) {

      let inst_id = typeof val != 'undefined' ? val.order : conf._control.length + 1

      let wrapper = $('<div/>').attr($.extend({id: inst_id, class: 'single-page-wrapper', 'data-order': inst_id}, {}));
      wrapper.append('<i class="fas fa-sort page-grab-handle"></i><div id="' + inst_id + '_id" class="d-none"></div>');
      wrapper.append('<input id="' + inst_id + '_order" type="text" class="form-control page_order">')
      wrapper.append('<i class="fas fa-book-open page-input-label"></i><input id="' + inst_id + '_name" type="text" class="form-control page_name" placeholder="Folio">')
      wrapper.append('<i class="fas fa-image page-input-label"></i><input id="' + inst_id + '_dam_id" type="text" class="form-control page_dam_id" placeholder="DAM ID">')
      wrapper.append('<div class="dropleft"><i class="fas fa-search page-dam-search h-100" data-toggle="dropdown"></i></div>');
      wrapper.append('<i class="fas fa-times-circle entry-clear-button"></i>')

      conf._input.append(wrapper)

      conf._input.find('.entry-clear-button').popover({
        toggle: 'popover',
        placement: 'right',
        html: true,
        sanitize: false,
        title: '',
        content: '<a href="#" data-page-id="' + inst_id + '" class="btn btn-sm btn-danger clear-page mr-1">Remove</a><a href="#" class="btn btn-sm btn-primary">Cancel</a>',
      })

      if (typeof val != 'undefined') {
        conf._input.find('#' + inst_id + '_id').val(val.id);
        conf._input.find('#' + inst_id + '_order').val(val.order);
        conf._input.find('#' + inst_id + '_name').val(val.name);
        conf._input.find('#' + inst_id + '_dam_id').val(val.dam_id);
      } else {
        conf._input.find('#' + inst_id + '_order').val(inst_id);
      }

      conf._control.push(inst_id)
  },

  _syncSort: function(conf) {
      let order = conf._input.sortable('toArray');
      for (let i = 0, len = order.length; i < len; ++i) {
          conf._input.find('#' + order[i] + '_order').val(i + 1);
      }
  },

  create: function(conf) {

      conf._input = $('<div/>').attr($.extend({
        id: conf.id,
        class: 'formset-entry-container'
      }, {}));

      conf._input.sortable({
          dataIdAttr: "data-order",
          sort: true,
          handle: '.page-grab-handle',
          ghostClass: "target-page-slot",
          draggable: '.single-page-wrapper'
      }).on('sortupdate', function() {
          _fieldTypes.dalmePages._syncSort(conf);
      });

      $(document).on("click.dalme", ".popover .clear-page" , function() {
          let inst_id = $(this).data('page-id')
          $(this).parents(".popover").popover('dispose');
          _fieldTypes.dalmePages.removePage(conf, inst_id);
      });

      conf._input.on('click.dalme', '.page-dam-search', function() {
        $(this).after($('#dam-search-dropdown')).dropdown();
      });

      conf._input.on('show.bs.dropdown', '.dropleft', function() {
          $('#dam-searchbox').focus();

          conf._input.on('search.dalme', '#dam-searchbox', function() {
            _fieldTypes.dalmePages.searchDAM(conf, this);
          });

          conf._input.on('click.dalme', '.dam-search-result', function() {
            let inst_id = $(this).parents('.single-page-wrapper').attr('id')
            conf._input.find('#' + inst_id + '_dam_id').val($(this).attr('id'));
          });
      });

      conf._input.on('shown.bs.dropdown', '.dropleft', function() {
          $('#dam-searchbox').focus();
      });

      conf._input.on('hide.bs.dropdown', '.dropleft', function() {
          conf._input.off('click.dalme', '.dam-search-result');
          conf._input.off('change.dalme', '#dam-searchbox');
          $('#dam-searchbox').val('');
          $('#dam-search-results').html('');
          $('#hidden-search-container').append($('#dam-search-dropdown'))
          $(this).find('.page-dam-search').dropdown('dispose');
      });

      return conf._input[0];
  },

  get: function(conf) {
      let value = []
      for (let i = 0, len = conf._control.length; i < len; ++i) {
        value.push({
          id: conf._input.find('#' + conf._control[i] + '_id').val(),
          order: conf._input.find('#' + conf._control[i] + '_order').val(),
          name: conf._input.find('#' + conf._control[i] + '_name').val(),
          dam_id: conf._input.find('#' + conf._control[i] + '_dam_id').val()
        })
      }
      return value;
  },

  set: function(conf, val) {
      conf._control = []
      conf._input.html('');
      for (let i = 0, len = val.length; i < len; ++i) { _fieldTypes.dalmePages._addPage(conf, val[i]); }
  },

  removePage: function(conf, inst_id) {
      conf._input.find('#' + inst_id).remove()
      _.remove(conf._control, function(i) { return i == inst_id })
      _fieldTypes.dalmePages._syncSort(conf);
  },

  searchDAM: function(conf, el) {
      let id = $(el).parent().parent().parent().attr('id')
      let query = $(el).val()
      if (query !== '') {
        $.ajax({
          method: "GET",
          url: "/api/images/?search=" + query
        }).done(function(data, textStatus, jqXHR) {
          if (typeof data != 'string') {
              $('#dam-search-results').removeClass('d-none');
              $('#dam-search-results').html('');
              for (let i = 0, len = data.length; i < len; ++i) {
                let result = '<div class="media dam-search-result" id="' + data[i].ref + '">\
                  <img src="' + data[i].url_thm + '" class="mr-3">\
                  <div class="media-body">\
                    <h6 class="mt-0 mb-0">' + data[i].field8 + '</h6>\
                    <span class="mr-1"><strong><small>ID:</small></strong></span>' + data[i].ref + '<br/>\
                    <span class="mr-1"><strong><small>FOLIO:</small></strong></span>' + data[i].field79 + '<br/>\
                    <span class="mr-1"><strong><small>FILENAME:</small></strong></span>' + data[i].field51 + '<br/>\
                    <span class="mr-1"><strong><small>CREATED:</small></strong></span>' + data[i].creation_date + '<br/>\
                  </div>\
                </div>'
                $('#dam-search-results').append(result)
              }
            } else {
              $('#dam-search-results').removeClass('d-none');
              $('#dam-search-results').append('<div class="dam-search-message">' + data + '</div>')
            }
        }).fail(function(jqXHR, textStatus, errorThrown) {
          $('#dam-search-results').removeClass('d-none');
          $('#dam-search-results').append('<div class="dam-search-error">There was an error communicating with the server: ' + errorThrown + '</div>')
        });
      } else {
        $('#dam-search-results').addClass('d-none');
        $('#dam-search-results').html('');
      }
  },

  addNew: function(conf) {
      _fieldTypes.dalmePages._addPage(conf);
  },

  destroy: function(conf) {
      conf._input.off('click.dalme');
      conf._input.off('search.dalme');
      conf._input.sortable('destroy');
  },

  errorMessage: function(errorMessage) {
      console.log('error = ' + errorMessage)
  }

};
}));
