
function setupTranscriber() {
    editor_container = document.getElementById('xml_editor');
    transcriber_container = document.getElementById('transcriber');
    footer_menubar = document.getElementById('tab-footer-interface');
    viewer_container = document.getElementById('diva_viewer');
    editor_buttons = document.getElementById('editor-button-bar');
    folio_array = folio_list;

    if (typeof xmleditor == 'undefined') {
      getViewer('initial', 0);
      getEditor('initial', 0);

      window.addEventListener('resize', function () { xmleditor.resize(); }, false);
      //listerner for editor options
      $('#xml-editor_options').find('input').on('change', '', function (e) { setEditorOptions(e) });
      $('#xml-editor_options').find('select').on('change', function (e) { setEditorOptions(e) });
      $('.panel-top').resizable(
        {
          handles: {s: '.splitter-horizontal'},
          resize: function(e, ui) {
              var parent = ui.element.parent();
              var remainingSpace = parent.height() - ui.element.outerHeight();
              var divTwo = ui.element.next();
              var divTwoHeight = (remainingSpace - (divTwo.outerHeight() - divTwo.height()));
              var divTwoPercent = divTwoHeight/parent.height()*100+"%";
              divTwo.height(divTwoPercent);
              $('#xml_editor').height(divTwoHeight - 34);
              },
          stop: function (e, ui) {
            var parent = ui.element.parent();
            ui.element.css({ height: ui.element.height()/parent.height()*100+"%", });
            window.dispatchEvent(new Event('resize'));
            }
        });
    } else {
      footer_menubar.style.display = "block";
    };
}

function leaveTranscriber() {
  footer_menubar.style.display = "none";
}

function getEditor(mode, target_idx) {
  var target = folio_array[target_idx].tr_id
  folio_idx = target_idx
  if (mode != 'initial') {
    //save session + remove event handlers + restore default state of ui
    editorSave();
    xmleditor.off()
    xmleditor.destroy()
    editor_container.innerHTML = '<div class="spinner-border mt-auto mb-auto"></div>';
    transcriber_container.innerHTML = '';
    footer_menubar.style.display = "none";
  };

  if (target != 'None') {
    //check if we have the session stored, if not, get the text from the API
    var url = "/api/transcriptions/"+target+"?format=json"
    $.get(url, function ( data ) {
          xmleditor = ace.edit("xml_editor");
          setEditorOptions('default');
          xmleditor.session.setValue(data.transcription);
          footer_menubar.style.display = "block";
          transcriber_container.innerHTML = 'Transcribed by '+data.author;
          document.getElementById('text_render').innerHTML = data.transcription_html;
          updateToolbar();
          xmleditor.session.on("change", debounce(editorSave, 500));
      }, 'json');
  } else {
    xmleditor = ace.edit("xml_editor");
    setEditorOptions('default');
    xmleditor.session.setValue('Start new transcription...');
    footer_menubar.style.display = "block";
    transcriber_container.innerHTML = 'New transcription';
    xmleditor.on("input", updateToolbar);
    xmleditor.session.on("change", debounce(editorSave, 500));
  };

}

function testKeybindings() {
  xmleditor.commands.addCommand({
    name: 'supplied_tag',
    bindKey: {win: 'Ctrl-P',  mac: 'Command-Option-S'},
    exec: function(xmleditor) {
        var txt = xmleditor.getSelectedText();
        var range = xmleditor.session.getTextRange(xmleditor.getSelectionRange());
        txt = '<supplied>'+txt+'</supplied>';
        xmleditor.session.replace(range, txt);
    },
    readOnly: false // false if this command should not apply in readOnly mode
  });
}

function getViewer(mode, target_idx) {
  var target = folio_array[target_idx].id
  var dam_id = folio_array[target_idx].dam_id
  if (dam_id == 'None') {
    viewer_container.innerHTML = '<div class="mt-auto mb-auto">There is no image associated with this folio/page.</div>';
  } else {
    var manifest = '/pages/'+target+'/manifest';
    if (mode == 'initial') {
      viewer_container.innerHTML = "";
      diva = new Diva('diva_viewer', {
          objectData: manifest,
          enableAutoTitle: false,
          enableFullscreen: false,
          enableKeyScroll: true,
          blockMobileMove: true,
          enableGotoPage: false,
          enableGridIcon: false,
          enableImageTitles: false,
          enableToolbar: false,
          tileHeight: 1000,
          tileWidth: 1000,
      });
      } else {
        diva.changeObject(manifest);
      };
    };
    //window.dispatchEvent(new Event('resize'));
}

function folioSwitch (target) {
  //use global folio dictionary to get required values
  var total = folio_array.length;
  var prev = prevFolio(getFolioIndex(target));
  var next = nextFolio(getFolioIndex(target));
  var goto_index = getFolioIndex(target)
  var current_index = goto_index - 1
  var count = goto_index + 1
  var goto = folio_array[goto_index];
  //switch viewer
  getViewer('switch', goto_index)
  //switch editor
  getEditor('switch', goto_index)
  var folio_menu = ''
  //change folio menu
  if (prev != 0) {
    folio_menu = '<button type="button" class="editor-btn button-border-left disabled" id="'+prev.name+'" onclick="folioSwitch(this.id)"><i class="fa fa-caret-left fa-fw"></i></button>';
  } else {
    folio_menu = '<div class="disabled-btn-left"><i class="fa fa-caret-left fa-fw"></i></div>';
  };
  folio_menu = folio_menu+'<button id="folios" type="button" class="editor-btn button-border-left" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Folio '+goto.name+' ('+count+'/'+total+')</button><div class="dropdown-menu" aria-labelledby="folios">';
  for ( i=0; i<total; i++ ) {
    if (i == goto_index) {
      folio_menu = folio_menu+'<div class="current-folio-menu">Folio '+folio_array[i].name+'</div>';
    } else {
      folio_menu = folio_menu+'<a class="dropdown-item" href="#" id="'+folio_array[i].name+'" onclick="folioSwitch(this.id)">Folio '+folio_array[i].name+'</a>';
    }
  };
  folio_menu = folio_menu+'</div>';
  if (next != 0) {
    folio_menu = folio_menu+'<button type="button" class="editor-btn button-border-left" id="'+next.name+'" onclick="folioSwitch(this.id)"><i class="fa fa-caret-right fa-fw"></i></button>';
  } else {
    folio_menu = folio_menu+'<div class="disabled-btn-left"><i class="fa fa-caret-right fa-fw"></i></div>';
  };
  document.getElementById('folio-menu').innerHTML = folio_menu;
}


function updateToolbar() {
  if (xmleditor.session.getUndoManager().isClean()) {
    $("#xmleditor_save").addClass("disabled");
  };

  if (!xmleditor.session.getUndoManager().hasUndo()) {
    $("#xmleditor_undo").addClass("disabled");
  };
  if (!xmleditor.session.getUndoManager().hasRedo()) {
    $("#xmleditor_redo").addClass("disabled");
  };
}

//editor.session.setValue(localStorage.savedValue || "Welcome to ace Toolbar demo!")

function editorButtonSave() {
    editorSave();
    xmleditor.setReadOnly(true);
    editor_buttons.innerHTML = '<button class="editor-btn float-right button-border-left" id="xmleditor_edit" type="button" onclick="editorButtonEdit();"><i class="fa fa-edit fa-fw"></i> Edit</button>';
    //xmleditor.session.getUndoManager().markClean();
}

function editorSave() {
    var tr_folio = folio_idx;
    var tr_text = xmleditor.getValue();
    if (tr_text != '' && tr_text != 'Start new transcription...') {
      var tr_id = folio_array[tr_folio].tr_id
      var tr_ver = folio_array[tr_folio].tr_version + 1;
      var tr_page = folio_array[tr_folio].id
      var tr_source = source_id;
      if (tr_id != 'None') {
        var url = "/api/transcriptions/"+tr_id+"/";
        $.ajax({
          method: "PUT",
          url: url,
          headers: { 'X-CSRFToken': getCookie("csrftoken") },
          data: { 'version': tr_ver, 'transcription': tr_text },
        }).done(function(data, textStatus, jqXHR) {
            if (data['version'] > folio_array[tr_folio]['tr_version']) { folio_array[tr_folio]['tr_version'] = data['version'] };
        }).fail(function(jqXHR, textStatus, errorThrown) { alert('There was an error saving the transcription to the server: '+errorThrown); });
      } else {
        var url = "/api/transcriptions/";
        $.ajax({
          method: "POST",
          url: url,
          headers: { 'X-CSRFToken': getCookie("csrftoken") },
          data: { 'version': tr_ver, 'transcription': tr_text, 'source': tr_source, 'page': tr_page },
        }).done(function(data, textStatus, jqXHR) {
            folio_array[tr_folio]['tr_id'] = data['id'];
            folio_array[tr_folio]['tr_version'] = data['version'];
            transcriber_container.innerHTML = 'Transcribed by '+data['author'];
        }).fail(function(jqXHR, textStatus, errorThrown) { alert('There was an error saving the transcription to the server: '+errorThrown); });
      };
    }
}

function editorButtonCancel() {
    do {
      xmleditor.undo()
    } while (xmleditor.session.getUndoManager().hasUndo());
    editorSave();
    xmleditor.setReadOnly(true);
    if (xmleditor.getValue() == '') { xmleditor.session.setValue('Start new transcription...'); };
    editor_buttons.innerHTML = '<button class="editor-btn float-right button-border-left" id="xmleditor_edit" type="button" onclick="editorButtonEdit();"><i class="fa fa-edit fa-fw"></i> Edit</button>';
}

function editorButtonEdit() {
    xmleditor.setReadOnly(false);
    if (xmleditor.getValue() == 'Start new transcription...') { xmleditor.session.setValue(''); };
    editor_buttons.innerHTML = '<button class="editor-btn float-right button-border-left editor-save" id="xmleditor_save" type="button" onclick="editorButtonSave();"><i class="fa fa-save fa-fw"></i> Save</button>\
    <button class="editor-btn float-right button-border-left editor-cancel" id="xmleditor_cancel" type="button" onclick="editorButtonCancel();"><i class="fa fa-times-circle fa-fw"></i> Cancel</button>\
    <button class="editor-btn float-left button-border-right" id="xmleditor_undo" type="button" onclick="xmleditor.undo();"><i class="fa fa-undo-alt fa-fw"></i></button>\
    <button class="editor-btn float-left button-border-right" id="xmleditor_redo" type="button" onclick="xmleditor.redo();"><i class="fa fa-redo-alt fa-fw"></i></button>';
    xmleditor.on("input", updateToolbar);
}

function setEditorOptions(mode) {
  if (mode == 'default') {
    xmleditor.setOptions({
        theme: "ace/theme/chrome",
        readOnly: true,
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
    });
  } else {
    if (typeof mode !== 'undefined')  {
      var target = mode.target;
      var option = target.id;
      if ($(target).is('select')) {
        var value = $(target).val()
      } else {
        var value = $(target).prop('checked')
      }
      xmleditor.setOption(option, value);
    }
  };
}

function getFolioIndex(folio) {
  return folio_array.findIndex(x => x.name === folio);
}

function nextFolio(i) {
    if (i+1 >= folio_array.length) {
      return 0;
    } else {
      i = i + 1; // increase i by one
      return folio_array[i]; // give us back the item of where we are now
    }
}

function prevFolio(i) {
    if (i == 0) {
      return 0;
    } else {
      i = i - 1; // decrease by one
      return folio_array[i]; // give us back the item of where we are now
    }
}
