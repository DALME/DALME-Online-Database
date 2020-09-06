/**
 * This plug-in splits dates into separate inputs for day, month, and year, to allow for incomplete dates to be used.
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

_fieldTypes.dalmeDate = {
  _addOptions: function(conf, options) {
        var selectize = conf._selectize;
        selectize.clearOptions();
        selectize.addOption( options );
        selectize.refreshOptions(false);
    },

  create: function(conf) {
    var that = this;

    var container = $('<div/>')
        .attr($.extend({id: conf.id, class: 'formset-date-container'}, {}));
    conf._input_day = $('<input/>')
        .attr($.extend({id: conf.id + '_day', type: 'number'}, conf.attr[0] || {}))
        .appendTo(container);
    conf._input_month = $('<select/>')
        .attr($.extend({id: conf.id + '_month'}, {}))
        .appendTo(container);
    conf._input_year = $('<input/>')
        .attr($.extend({id: conf.id + '_year', type: 'number'}, conf.attr[1] || {}))
        .appendTo(container);

    conf._input_month.selectize($.extend({
          valueField: 'value',
          labelField: 'label',
          searchField: 'label',
          dropdownParent: 'body'
        }, conf.opts ) );

    conf._selectize = conf._input_month[0].selectize;

    if (conf.options || conf.ipOpts) {
      _fieldTypes.dalmeDate._addOptions(conf, conf.options || conf.ipOpts);
    }

    this.on('preSubmit', function() { conf._selectize.close(); });

    return container[0];
  },

  get: function(conf) {
    let values = {
      d: conf._input_day.val(),
      m: conf._selectize.getValue(),
      y: conf._input_year.val()
    };
    return values
  },

  set: function(conf, val) {
    conf._input_day.val(val.d);
    conf._selectize.setValue(val.m);
    conf._input_year.val(val.y);
  },

  enable: function(conf) {
    conf._selectize.enable();
    $(conf._input_month).removeClass('disabled');
  },

  disable: function(conf) {
    conf._selectize.disable();
    $(conf._input_month).addClass('disabled');
  },

  inst: function(conf) {
    return conf._selectize;
  },

  update: function(conf, options) {
    _fieldTypes.dalmeDate._addOptions(conf, options);
  }
};
}));
