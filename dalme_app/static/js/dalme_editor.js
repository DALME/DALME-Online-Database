function startEditor() {
  if (typeof transcriber_state == 'undefined') {
      transcriber_state = 'on';
      footer_content = '...';
      viewer_container = document.getElementById('diva_viewer');
      editor_container = document.getElementById('editor');
      editor_toolbar = document.getElementById('editor-toolbar');
      author_container = document.getElementById('author');
      top_panel = document.getElementsByClassName('panel-top');
      maxHeight = $(window).height() - 340;
      editor_mode = 'render';
      edit_mode = 'off';
      folio_array = folio_list;
      folio_idx = 0;
      if (folio_array[0].dam_id == 'None') {
          $(viewer_container).html('<div class="mt-auto mb-auto">There is no image associated with this folio/page.</div>');
      } else {
          $(viewer_container).empty();
          diva = new Diva('diva_viewer', {
             objectData: '/pages/'+folio_array[0].id+'/manifest',
             enableAutoTitle: false,
             enableFullscreen: false,
             //enableKeyScroll: true,
             //blockMobileMove: true,
             enableGotoPage: false,
             enableGridIcon: false,
             enableImageTitles: false,
             enableToolbar: false,
             tileHeight: 1000,
             tileWidth: 1000
          });
      };
      if (folio_array[0].tr_id == 'None') {
          $(editor_container).html('<div class="mt-auto mb-auto">This folio/page has not been transcribed. Click on Edit to start...</div>');
          $(author_container).html('No transcription available');
      } else {
          $.get("/api/transcriptions/"+folio_array[0].tr_id+"?format=json", function (data) {
              tr_text = data.transcription;
              tei = new CETEI();
              tei.addBehaviors({
                'tei': {
                  'gap': function(e) { e.setAttribute("title", getTitle(e, 'gap')); e.setAttribute("data-toggle", "tooltip"); }, //@reason, @unit, @quantity, @extent
                  'space': function(e) { e.setAttribute("title", getTitle(e, 'space')); e.setAttribute("data-toggle", "tooltip"); }, //@unit, @quantity, @extent
                  'unclear': function(e) { e.setAttribute("title", getTitle(e, 'unclear')); e.setAttribute("data-toggle", "tooltip"); }, //@reason
                  'supplied': function(e) { e.setAttribute("title", getTitle(e, 'supplied')); e.setAttribute("data-toggle", "tooltip"); }, //@reason
                  'add': function(e) { e.setAttribute("title", getTitle(e, 'addition')); e.setAttribute("data-toggle", "tooltip"); }, //@place
                  'abbr': function(e) { e.setAttribute("title", getTitle(e, 'abbreviation')); e.setAttribute("data-toggle", "tooltip"); }, //@type
                  'w': function(e) { e.setAttribute("title", getTitle(e, 'word')); e.setAttribute("data-toggle", "tooltip"); }, //@type, @lemma
                  'quote': function(e) { e.setAttribute("title", getTitle(e, 'quote')); e.setAttribute("data-toggle", "tooltip"); } //@resp
                  }
              });
              tei.makeHTML5('<TEI xmlns="http://www.tei-c.org/ns/1.0"><text><body>'+tr_text+'</body></text></TEI>', function(text) {
                  $(editor_container).removeClass("justify-content-center").addClass("justify-content-left").html(text);
              });
              $('[data-toggle="tooltip"]').tooltip({container: 'body'});
              $(author_container).html('Transcribed by '+data.author);
          }, 'json');
      };
      $(top_panel).resizable({
          handles: {s: '.splitter-horizontal'},
          maxHeight: maxHeight,
          minHeight: 200,
          resize: function(e, ui) {
              const parent = ui.element.parent();
              const remainingSpace = parent.height() - ui.element.outerHeight();
              const divTwo = ui.element.next();
              const divTwoHeight = (remainingSpace - (divTwo.outerHeight() - divTwo.height()));
              const divTwoPercent = (divTwoHeight-28)/parent.height()*100+"%";
              divTwo.height(divTwoPercent);
              $(editor_container).height(divTwoHeight - 56);
              },
          stop: function (e, ui) {
            const parent = ui.element.parent();
            ui.element.css({ height: ui.element.height()/parent.height()*100+"%", });
            window.dispatchEvent(new Event('resize'));
            }
      });
      window.addEventListener('resize', function () { resizeEditor(); }, false);
      Diva.Events.subscribe('ObjectDidLoad', function () { alert('success'); });
  } else {
    $(author_container).html(footer_content);
  }
}

function cleanFooter() {
  footer_content = $(author_container).html();
  $(author_container).html('');
}

function changeEditorMode() {
  if (editor_mode == 'render') {
      editor_mode = 'xml';
      $(editor_container).empty();
      $('#btn_edit').html('<i class="fa fa-eye fa-fw"></i> View');
      xmleditor = ace.edit("editor");
      setEditorOptions();
      xmleditor.session.setValue(tr_text);
      xmleditor.session.on("change.dalme", debounce(saveEditor, 1000));
      setEditorToolbar();
      $(editor_container).on("input.dalme", updateEditorToolbar);
  } else if (editor_mode == 'xml') {
      editor_mode = 'render';
      saveEditor();
      removeEditorToolbar();
      tr_text = xmleditor.getValue();
      xmleditor.off("change.dalme");
      xmleditor.destroy();
      $('#btn_edit').html('<i class="fa fa-edit fa-fw"></i> Edit');
      tei.makeHTML5('<TEI xmlns="http://www.tei-c.org/ns/1.0"><text><body>'+tr_text+'</body></text></TEI>', function(text) {
          $(editor_container).removeClass("justify-content-center").addClass("justify-content-left").html(text);
      });
      $(editor_container).off("input.dalme");
      $('[data-toggle="tooltip"]').tooltip({container: 'body'});
  }
}

function changeEditorFolio(target) {
  $(document.body).css('cursor', 'wait');
  if (target != '') {
    var target = parseInt(target, 10);
    var total = folio_array.length;
    var prev = target != 0 ? target - 1 : '';
    var next = target + 1 >= total ? '' : target + 1;
    $.get("/api/transcriptions/"+folio_array[target].tr_id+"?format=json", function (data) {
        tr_text = data.transcription;
        if (editor_mode == 'render') {
            tei.makeHTML5('<TEI xmlns="http://www.tei-c.org/ns/1.0"><text><body>'+tr_text+'</body></text></TEI>', function(text) {
                $(editor_container).html(text);
            });
            $('[data-toggle="tooltip"]').tooltip({container: 'body'});
        } else if (editor_mode == 'xml') {
            saveEditor();
            xmleditor.session.setValue(tr_text);
            xmleditor.session.getUndoManager().reset();
            updateEditorToolbar();
        }
        $(author_container).html('Transcribed by '+data.author);
        $('#btn_prevFolio').attr('value', prev);
        $('#btn_selectFolio').text("Folio "+folio_array[target].name+" ("+(target+1)+"/"+total+")");
        $('#folio-menu').find('.current-folio').removeClass('current-folio');
        $('#folio-menu').find('#'+target).addClass('current-folio');
        $('#btn_nextFolio').attr('value', next);
        updateFolioButtons();
        diva.changeObject('/pages/'+folio_array[target].id+'/manifest');
        folio_idx = target;
        $(document.body).css('cursor', 'default');
        window.dispatchEvent(new Event('resize'));
    });
  }
}

function updateFolioButtons() {
  $("#btn_prevFolio").attr("disabled", $('#btn_prevFolio').attr('value') == '');
  $("#btn_nextFolio").attr("disabled", $('#btn_nextFolio').attr('value') == '');
}

function setEditorOptions(dict) {
  if (typeof dict !== 'undefined') {
    var value = $(dict.target).is('select') ? $(dict.target).val() : $(dict.target).prop('checked');
    xmleditor.setOption(dict.target.id, value);
  } else {
    xmleditor.setOptions({
        theme: "ace/theme/chrome",
        readOnly: false,
        highlightActiveLine: true,
        highlightSelectedWord: true,
        highlightGutterLine: true,
        showInvisibles: false,
        showPrintMargin: false,
        showFoldWidgets: true,
        showLineNumbers: true,
        showGutter: true,
        displayIndentGuides: true,
        fontSize: 14,
        wrap: true,
        foldStyle: "markbegin",
        mode: "ace/mode/xml",
        indentedSoftWrap: true,
        fixedWidthGutter: true,
        scrollPastEnd: 0.1
    });
  }
}

function setEditorToolbar() {
  $('#editor-right-toolbar')
    .prepend('<button class="editor-btn button-border-left" id="btn_cancel" onclick="cancelEditor()"><i class="fa fa-times-circle fa-fw"></i> Cancel</button>')
    .prepend('<button class="editor-btn button-border-left" id="btn_save" onclick="saveButton()" disabled><i class="fa fa-save fa-fw"></i> Save</button>');
  $('#editor-left-toolbar')
    .prepend('<button class="editor-btn button-border-right" id="btn_options" onclick="editorOptionsMenu()" title="Editor options" data-toggle="tooltip"><i class="fas fa-cog fa-fw" ></i></button>')
    .append('<button class="editor-btn button-border-right" id="btn_redo" onclick="redoEditor()" title="Redo" data-toggle="tooltip" disabled><i class="fa fa-redo-alt fa-fw"></i></button>')
    .append('<button class="editor-btn button-border-right" id="btn_undo" onclick="undoEditor()" title="Undo" data-toggle="tooltip" disabled><i class="fa fa-undo-alt fa-fw"></i></button>');
  $('#xmleditor-options').load('/static/includes/xmleditor_options.html', function() {
    $('#xmleditor-options-form').find('input').on('change.dalme', function (e) { setEditorOptions(e) });
    $('#xmleditor-options-form').find('select').on('change.dalme', function (e) { setEditorOptions(e) });
    $('[data-toggle="tooltip"]').tooltip({container: 'body'});
  });
}

function removeEditorToolbar() {
  $('#btn_cancel').remove();
  $('#btn_save').remove();
  $('#xmleditor-options-form').find('input').off('change.dalme');
  $('#xmleditor-options-form').find('select').off('change.dalme');
  $('#xmleditor-options').empty();
  $('#btn_options').remove();
  $('#btn_undo').remove();
  $('#btn_redo').remove();
}

function updateEditorToolbar() {
  $("#btn_save").attr("disabled", xmleditor.session.getUndoManager().isClean());
  $("#btn_undo").attr("disabled", !xmleditor.session.getUndoManager().hasUndo());
  $("#btn_redo").attr("disabled", !xmleditor.session.getUndoManager().hasRedo());
}

function saveButton() {
  saveEditor();
  $("#btn_save").attr("disabled", true);
}

function saveEditor() {
  var folio = folio_idx;
  var text = xmleditor.getValue();
  if (text != '' && !xmleditor.session.getUndoManager().isClean()) {
    var id = folio_array[folio].tr_id
    var ver = folio_array[folio].tr_version + 1;
    var page = folio_array[folio].id
    var source = source_id;
    if (id != 'None') {
      var url = "/api/transcriptions/"+id+"/";
      $.ajax({
        method: "PUT",
        url: url,
        headers: { 'X-CSRFToken': get_cookie("csrftoken") },
        data: { 'version': ver, 'transcription': text },
      }).done(function(data, textStatus, jqXHR) {
          if (data['version'] > folio_array[folio]['tr_version']) { folio_array[folio]['tr_version'] = data['version'] };
      }).fail(function(jqXHR, textStatus, errorThrown) { alert('There was an error saving the transcription to the server: '+errorThrown); });
    } else {
      var url = "/api/transcriptions/";
      $.ajax({
        method: "POST",
        url: url,
        headers: { 'X-CSRFToken': get_cookie("csrftoken") },
        data: { 'version': ver, 'transcription': text, 'source': source, 'page': page },
      }).done(function(data, textStatus, jqXHR) {
          folio_array[folio]['tr_id'] = data['id'];
          folio_array[folio]['tr_version'] = data['version'];
          $(author_container).html('Transcribed by '+data['author']);
      }).fail(function(jqXHR, textStatus, errorThrown) { alert('There was an error saving the transcription to the server: '+errorThrown); });
    };
  }
}

function cancelEditor() {
  if (confirm("Cancel the editing session? All your changes will be lost.")) {
      do {
          xmleditor.undo()
      } while (xmleditor.session.getUndoManager().hasUndo());
      changeEditorMode();
  }
}

function editorOptionsMenu() {
  $('#xmleditor-options').toggle();
}

function undoEditor() {
  xmleditor.undo();
  updateEditorToolbar();
}

function redoEditor() {
  xmleditor.redo();
  updateEditorToolbar();
}

function resizeEditor() {
  maxHeight = $(window).height() - 340;
  if (editor_mode == 'xml') {
      xmleditor.resize();
  }
}

/***** Utility functions *********/

function getTitle(e, tag) {
  if (e.hasAttribute("unit") && e.hasAttribute("quantity")) {
    var extent = 'extent ' + e.getAttribute("quantity") + ' ' + e.getAttribute("unit");
  } else if (e.hasAttribute("extent")) {
    var extent = 'extent ' + e.getAttribute("extent");
  };
  if (e.hasAttribute("reason")) { var reason = e.getAttribute("reason") };
  if (e.hasAttribute("type")) { var type = e.getAttribute("type") };
  if (e.hasAttribute("lemma")) { var lemma = '"' + e.getAttribute("lemma") + '"' };
  if (e.hasAttribute("resp")) { var resp = ' by ' + e.getAttribute("resp") };
  if (tag == 'word' && type && lemma) {
    var title = type + ': ' + lemma;
  } else {
    var title = tag;
    if (extent) {
      title = title + ': ' + extent;
      if (reason) { title = title + ', ' + reason; };
    } else if (reason) {
      title = title + ': ' + reason;
    } else if (type) {
      title = title + ': ' + type;
    } else if (resp) {
      title = title + resp;
    }
  };
  return title
}

function testKeybindings() {
  xmleditor.commands.addCommand({
    name: 'supplied_tag',
    bindKey: {win: 'Ctrl-P',  mac: 'Command-Option-S'},
    exec: function(xmleditor) {
        let txt = xmleditor.getSelectedText();
        const range = xmleditor.session.getTextRange(xmleditor.getSelectionRange());
        txt = '<supplied>'+txt+'</supplied>';
        xmleditor.session.replace(range, txt);
    },
    readOnly: false // false if this command should not apply in readOnly mode
  });
}
