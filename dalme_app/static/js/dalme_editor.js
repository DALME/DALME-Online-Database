
function setupTranscriber() {
    editor_container = document.getElementById('xml_editor');
    transcriber_container = document.getElementById('transcriber');
    footer_menubar = document.getElementById('tab-footer-interface');
    viewer_container = document.getElementById('diva_viewer');
    editor_buttons = document.getElementById('editor-button-bar');

    if (typeof xmleditor == 'undefined') {
      getViewer('initial', 0);
      getEditor('initial', folio_list[0].tr_id);

      window.addEventListener('resize', function () {
          xmleditor.resize();
        }, false);

      window.addEventListener('beforeunload', function (e) {
        return false
      });

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
    }
}

function leaveTranscriber() {
  footer_menubar.style.display = "none";
}

function getEditor(mode, target) {
  if (mode != 'initial') {
    //save session
    xmleditor.destroy()
    editor_container.innerHTML = '<div class="spinner-border mt-auto mb-auto"></div>';
    transcriber_container.innerHTML = '';
    footer_menubar.style.display = "none";
  };

  if (target != 'None') {
    //check if we have the session stored
    //if not, get the text from the API
    url = "/api/transcriptions/"+target+"?format=json"
    $.get(url, function ( data ) {
          xmleditor = ace.edit("xml_editor");
          setEditorOptions();
          xmleditor.session.setValue(data.transcription);
          footer_menubar.style.display = "block";
          transcriber_container.innerHTML = 'Transcribed by '+data.author;
          document.getElementById('xml_render').innerHTML = data.transcription_html;
      }, 'json');
  } else {
    xmleditor = ace.edit("xml_editor");
    setEditorOptions();
    xmleditor.session.setValue('Start new transcription...');
    footer_menubar.style.display = "block";
    transcriber_container.innerHTML = 'New transcription';
    var refs = {};
    xmleditor.on("input", updateToolbar);
  };

}

function getViewer(mode, target_idx) {
  target = folio_list[target_idx].id
  dam_id = folio_list[target_idx].dam_id
  if (dam_id == 'None') {
    viewer_container.innerHTML = '<div class="mt-auto mb-auto">There is no image associated with this folio/page.</div>';
  } else {
    manifest = '/pages/'+target+'/manifest';
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
  total = folio_list.length;
  prev = prevFolio(getFolioIndex(target));
  next = nextFolio(getFolioIndex(target));
  goto_index = getFolioIndex(target)
  current_index = goto_index - 1
  count = goto_index + 1
  goto = folio_list[goto_index];
  //switch viewer
  getViewer('switch', goto_index)
  //switch editor
  getEditor('switch', goto.tr_id)

  //change folio menu
  if (prev != 0) {
    folio_menu = '<button type="button" class="editor-btn button-border-left disabled" id="'+prev.name+'" onclick="folioSwitch(this.id)"><i class="fa fa-caret-left fa-fw"></i></button>';
  } else {
    folio_menu = '<div class="disabled-btn-left"><i class="fa fa-caret-left fa-fw"></i></div>';
  };
  folio_menu = folio_menu+'<button id="folios" type="button" class="editor-btn button-border-left" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Folio '+goto.name+' ('+count+'/'+total+')</button><div class="dropdown-menu" aria-labelledby="folios">';
  for ( i=0; i<total; i++ ) {
    if (i == goto_index) {
      folio_menu = folio_menu+'<div class="current-folio-menu">Folio '+folio_list[i].name+'</div>';
    } else {
      folio_menu = folio_menu+'<a class="dropdown-item" href="#" id="'+folio_list[i].name+'" onclick="folioSwitch(this.id)">Folio '+folio_list[i].name+'</a>';
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
    localStorage.savedValue = xmleditor.getValue();
    xmleditor.session.getUndoManager().markClean();
    updateToolbar();
}

function editorButtonCancel() {
    do {
      xmleditor.undo()
    } while (xmleditor.session.getUndoManager().hasUndo());
    xmleditor.setReadOnly(true);
    editor_buttons.innerHTML = '<button class="editor-btn float-right button-border-left" id="xmleditor_edit" type="button" onclick="editorButtonEdit();"><i class="fa fa-edit fa-fw"></i> Edit</button>';
}

function editorButtonEdit() {
    xmleditor.setReadOnly(false);
    editor_buttons.innerHTML = '<button class="editor-btn float-right button-border-left editor-save" id="xmleditor_save" type="button" onclick="editorButtonSave();"><i class="fa fa-save fa-fw"></i> Save</button>\
    <button class="editor-btn float-right button-border-left editor-cancel" id="xmleditor_cancel" type="button" onclick="editorButtonCancel();"><i class="fa fa-times-circle fa-fw"></i> Cancel</button>\
    <button class="editor-btn float-left button-border-right" id="xmleditor_undo" type="button" onclick="xmleditor.undo();"><i class="fa fa-undo-alt fa-fw"></i></button>\
    <button class="editor-btn float-left button-border-right" id="xmleditor_redo" type="button" onclick="xmleditor.redo();"><i class="fa fa-redo-alt fa-fw"></i></button>';
    xmleditor.on("input", updateToolbar);
}

function setEditorOptions() {
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
      //following options require ext-language_tools.js
      //enableBasicAutocompletion: true,
      //enableLiveAutocompletion: true,
  });
}

function getFolioIndex(folio) {
  return folio_list.findIndex(x => x.name === folio);
}

function nextFolio(i) {
    if (i+1 >= folio_list.length) {
      return 0;
    } else {
      i = i + 1; // increase i by one
      return folio_list[i]; // give us back the item of where we are now
    }
}

function prevFolio(i) {
    if (i == 0) {
      return 0;
    } else {
      i = i - 1; // decrease by one
      return folio_list[i]; // give us back the item of where we are now
    }
}
