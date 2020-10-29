/**
 * This plug-in allows managing credits.
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

_fieldTypes.dalmeCredits = {

  _addCredit: function(conf, val) {

      let inst_id = conf._control.length

      let wrapper = $('<div/>').attr($.extend({id: inst_id, class: 'single-credit-wrapper'}, {}));
      let agent_select = $('<select/>').attr($.extend({id: inst_id + '_agent', class: 'form-control'}, {})).appendTo(wrapper);
      let type_select = $('<select/>').attr($.extend({id: inst_id + '_type', class: 'form-control'}, {})).appendTo(wrapper);
      wrapper.append('<div class="dropleft"><i class="fas fa-sticky-note page-credit-note h-100" data-toggle="dropdown" id="' +
          inst_id + '_note_button" aria-haspopup="true" aria-expanded="false"></i>\
          <div class="dropdown-menu formset-dropdown" aria-labelledby=id="' + inst_id + '_note_button">\
          <button type="button" class="modal_close_button" aria-label="Close"><span aria-hidden="true">&times;</span></button>\
          <label class="col-form-label">NOTES</label><textarea id="' + inst_id + '_note" class="form-control page_credit_note"></textarea>\
          </div></div>');
      wrapper.append('<i class="fas fa-times-circle entry-clear-button"></i>')

      agent_select.selectize({
        placeholder: conf.opts.agents['placeholder'],
        preload: conf.opts.agents['preload'],
        dropdownParent: null,
        valueField: conf.opts.agents['valueField'],
        labelField: conf.opts.agents['labelField'],
        searchField: conf.opts.agents['searchField'],
        load: eval(`(function(query, callback) {$.ajax({url: "${api_endpoint}/${conf.opts.agents['url']}" + encodeURIComponent(query),\
        type: 'GET',xhrFields: { withCredentials: true },crossDomain: true,headers: {"X-CSRFToken": get_cookie("csrftoken")},\
        error: function() {callback();},success: function(res) {callback(res);}});})`),
      });

      type_select.selectize({
        placeholder: conf.opts.types['placeholder'],
        preload: conf.opts.types['preload'],
        dropdownParent: null,
        valueField: conf.opts.types['valueField'],
        labelField: conf.opts.types['labelField'],
        searchField: conf.opts.types['searchField'],
        load: eval(`(function(query, callback) {$.ajax({url: "${api_endpoint}/${conf.opts.types['url']}" + encodeURIComponent(query),\
        type: 'GET',xhrFields: { withCredentials: true },crossDomain: true,headers: {"X-CSRFToken": get_cookie("csrftoken")},\
        error: function() {callback();},success: function(res) {callback(res);}});})`),
      });

      conf['_selectize_agent_' + inst_id] = agent_select[0].selectize;
      conf['_selectize_type_' + inst_id] = type_select[0].selectize;

      conf._input.append(wrapper)

      conf._input.find('.entry-clear-button').popover({
        toggle: 'popover',
        placement: 'right',
        html: true,
        sanitize: false,
        title: '',
        content: '<a href="#" data-credit-id="' + inst_id + '" class="btn btn-sm btn-danger clear-credit mr-1">Remove</a><a href="#" class="btn btn-sm btn-primary">Cancel</a>',
      })

      if (typeof val != 'undefined') {
        conf['_selectize_agent_' + inst_id].addOption({
          id: val.id,
          standard_name: val.standard_name
        });

        conf['_selectize_type_' + inst_id].addOption({
          id: val.type.id,
          name: val.type.name
        });

        conf['_selectize_agent_' + inst_id].setValue(val.id)
        conf['_selectize_type_' + inst_id].setValue(val.type.id)
        conf._input.find('#' + inst_id + '_note').val(val.note);
      }

      conf._control.push(inst_id)
  },

  create: function(conf) {

      conf._input = $('<div/>').attr($.extend({
        id: conf.id,
        class: 'formset-entry-container'
      }, {}));

      $(document).on("click.dalme", ".popover .clear-credit" , function() {
          let inst_id = $(this).data('credit-id')
          $(this).parents(".popover").popover('dispose');
          _fieldTypes.dalmeCredits.removeCredit(conf, inst_id);
      });

      return conf._input[0];
  },

  get: function(conf) {
      let value = []
      for (let i = 0, len = conf._control.length; i < len; ++i) {
        value.push({
          id: conf['_selectize_agent_' + conf._control[i]].getValue(),
          type: conf['_selectize_type_' + conf._control[i]].getValue(),
          note: conf._input.find('#' + conf._control[i] + '_note').val()
        })
      }
      return value;
  },

  set: function(conf, val) {
      conf._control = []
      conf._input.html('');
      for (let i = 0, len = val.length; i < len; ++i) { _fieldTypes.dalmeCredits._addCredit(conf, val[i]); }
  },

  removeCredit: function(conf, inst_id) {
      conf._input.find('#' + inst_id).remove()
      _.remove(conf._control, function(i) { return i == inst_id })
  },

  addNew: function(conf) {
      _fieldTypes.dalmeCredits._addCredit(conf);
  },

  destroy: function(conf) {
      conf._input.off('click.dalme');
  },

  errorMessage: function(errorMessage) {
      console.log('error = ' + errorMessage)
  }

};
}));
