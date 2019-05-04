class Transcriber {

    constructor() {
        this.transcriber_state = 'on';
        this.viewer_container = document.getElementById('diva_viewer');
        this.render_container = document.getElementById('text_render');
        this.xml_container = document.getElementById('xml_editor');
        this.editor_container = this.render_container;
        this.editor_buttons = document.getElementById('editor-button-bar');
        this.author_container = document.getElementById('transcriber');
        this.footer_menubar = document.getElementById('tab-footer-interface');
        this.top_panel = document.getElementsByClassName('panel-top');
        this.editor_mode = 'render';
        this.folio_array = folio_list;
        if (this.folio_array[0].dam_id == 'None') {
          this.viewer_container.innerHTML = '<div class="mt-auto mb-auto">There is no image associated with this folio/page.</div>';
        } else {
          this.viewer_container.innerHTML = "";
          let diva = new Diva('diva_viewer', {
             objectData: '/pages/'+this.folio_array[0].id+'/manifest',
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
        };
        if (this.folio_array[0].tr_id == 'None') {
          this.render_container.innerHTML = '<div class="mt-auto mb-auto">This folio/page has not been transcribed. Click on Edit to start...</div>';
        } else {
          //var req = $.get("/api/transcriptions/"+this.folio_array[0].tr_id+"?format=json", function (data) { return data }, 'json');

          let tei = new CETEI();
          // tei.addBehaviors({
          //   'tei': {
          //     'gap': function(e) { e.setAttribute("title", this.getTeiTitle(e, 'gap')); e.setAttribute("data-toggle", "tooltip"); }, //@reason, @unit, @quantity, @extent
          //     'space': function(e) { e.setAttribute("title", this.getTeiTitle(e, 'space')); e.setAttribute("data-toggle", "tooltip"); }, //@unit, @quantity, @extent
          //     'unclear': function(e) { e.setAttribute("title", this.getTeiTitle(e, 'unclear')); e.setAttribute("data-toggle", "tooltip"); }, //@reason
          //     'supplied': function(e) { e.setAttribute("title", this.getTeiTitle(e, 'supplied')); e.setAttribute("data-toggle", "tooltip"); }, //@reason
          //     'add': function(e) { e.setAttribute("title", this.getTeiTitle(e, 'addition')); e.setAttribute("data-toggle", "tooltip"); }, //@place
          //     'abbr': function(e) { e.setAttribute("title", this.getTeiTitle(e, 'abbreviation')); e.setAttribute("data-toggle", "tooltip"); }, //@type
          //     'w': function(e) { e.setAttribute("title", this.getTeiTitle(e, 'word')); e.setAttribute("data-toggle", "tooltip"); }, //@type, @lemma
          //     'quote': function(e) { e.setAttribute("title", this.getTeiTitle(e, 'quote')); e.setAttribute("data-toggle", "tooltip"); } //@resp
          //   }
          // });
          this.getTranscriptionText(this.folio_array[0].tr_id)
            .then(data => tei.makeHTML5('<TEI xmlns="http://www.tei-c.org/ns/1.0"><text><body>'+data.transcription+'</body></text></TEI>', function(text) {
                $('#text_render').html(text);
            }))
            .catch(reason => alert(reason.message) );
          $('[data-toggle="tooltip"]').tooltip({container: 'body'});
          this.footer_menubar.style.display = "block";
          this.author_container.innerHTML = 'Transcribed by '+data.author;
        };
        window.addEventListener('resize', function () { this._resizeEditor(); }, false);
        $(this.top_panel).resizable({
            handles: {s: '.splitter-horizontal'},
            resize: function(e, ui) {
                var parent = ui.element.parent();
                var remainingSpace = parent.height() - ui.element.outerHeight();
                var divTwo = ui.element.next();
                var divTwoHeight = (remainingSpace - (divTwo.outerHeight() - divTwo.height()));
                var divTwoPercent = divTwoHeight/parent.height()*100+"%";
                divTwo.height(divTwoPercent);
                this.transcriber_container.height(divTwoHeight - 34);
                },
            stop: function (e, ui) {
              var parent = ui.element.parent();
              ui.element.css({ height: ui.element.height()/parent.height()*100+"%", });
              window.dispatchEvent(new Event('resize'));
              }
        });
    }

    _resizeEditor() {
        if (editor_mode == 'render') {
            var craptastic = 'something';
        } else if (editor_mode == 'xml') {
            xmleditor.resize();
        };
    }

    async getTranscriptionText(target) {
      let data = await $.get("/api/transcriptions/"+target+"?format=json", function (data) {
        return data
      }, 'json');
      return data
    }

    /******* Utility functions ***********/

    getTeiTitle(e, tag) {
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
}

// function xml_editor(mode, target_idx) {
//   var target = folio_array[target_idx].tr_id
//   folio_idx = target_idx
//   if (mode != 'initial') {
//     //save session + remove event handlers + restore default state of ui
//     editorSave();
//     xmleditor.off()
//     xmleditor.destroy()
//     editor_container.innerHTML = '<div class="spinner-border mt-auto mb-auto"></div>';
//     transcriber_container.innerHTML = '';
//     footer_menubar.style.display = "none";
//   };
//
//   if (target != 'None') {
//     //check if we have the session stored, if not, get the text from the API
//     var url = "/api/transcriptions/"+target+"?format=json"
//     $.get(url, function ( data ) {
//           xmleditor = ace.edit("xml_editor");
//           setEditorOptions('default');
//           xmleditor.session.setValue(data.transcription);
//           footer_menubar.style.display = "block";
//           transcriber_container.innerHTML = 'Transcribed by '+data.author;
//           document.getElementById('text_render').innerHTML = data.transcription_html;
//           updateToolbar();
//           xmleditor.session.on("change", debounce(editorSave, 500));
//           $('#xml-editor_options').find('input').on('change', '', function (e) { setEditorOptions(e) });
//           $('#xml-editor_options').find('select').on('change', function (e) { setEditorOptions(e) });
//       }, 'json');
//   } else {
//     xmleditor = ace.edit("xml_editor");
//     setEditorOptions('default');
//     xmleditor.session.setValue('Start new transcription...');
//     footer_menubar.style.display = "block";
//     transcriber_container.innerHTML = 'New transcription';
//     xmleditor.on("input", updateToolbar);
//     xmleditor.session.on("change", debounce(editorSave, 500));
//     $('#xml-editor_options').find('input').on('change', '', function (e) { setEditorOptions(e) });
//     $('#xml-editor_options').find('select').on('change', function (e) { setEditorOptions(e) });
//   };
// }
//
// function testKeybindings() {
//   xmleditor.commands.addCommand({
//     name: 'supplied_tag',
//     bindKey: {win: 'Ctrl-P',  mac: 'Command-Option-S'},
//     exec: function(xmleditor) {
//         var txt = xmleditor.getSelectedText();
//         var range = xmleditor.session.getTextRange(xmleditor.getSelectionRange());
//         txt = '<supplied>'+txt+'</supplied>';
//         xmleditor.session.replace(range, txt);
//     },
//     readOnly: false // false if this command should not apply in readOnly mode
//   });
// }
//
//
//
// function folioSwitch (target) {
//   //use global folio dictionary to get required values
//   var total = folio_array.length;
//   var prev = prevFolio(getFolioIndex(target));
//   var next = nextFolio(getFolioIndex(target));
//   var goto_index = getFolioIndex(target)
//   var current_index = goto_index - 1
//   var count = goto_index + 1
//   var goto = folio_array[goto_index];
//   //switch viewer
//   viewer('switch', goto_index)
//   //switch editor
//   editor('switch', goto_index)
//   var folio_menu = ''
//   //change folio menu
//   if (prev != 0) {
//     folio_menu = '<button type="button" class="editor-btn button-border-left disabled" id="'+prev.name+'" onclick="folioSwitch(this.id)"><i class="fa fa-caret-left fa-fw"></i></button>';
//   } else {
//     folio_menu = '<div class="disabled-btn-left"><i class="fa fa-caret-left fa-fw"></i></div>';
//   };
//   folio_menu = folio_menu+'<button id="folios" type="button" class="editor-btn button-border-left" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Folio '+goto.name+' ('+count+'/'+total+')</button><div class="dropdown-menu" aria-labelledby="folios">';
//   for ( i=0; i<total; i++ ) {
//     if (i == goto_index) {
//       folio_menu = folio_menu+'<div class="current-folio-menu">Folio '+folio_array[i].name+'</div>';
//     } else {
//       folio_menu = folio_menu+'<a class="dropdown-item" href="#" id="'+folio_array[i].name+'" onclick="folioSwitch(this.id)">Folio '+folio_array[i].name+'</a>';
//     }
//   };
//   folio_menu = folio_menu+'</div>';
//   if (next != 0) {
//     folio_menu = folio_menu+'<button type="button" class="editor-btn button-border-left" id="'+next.name+'" onclick="folioSwitch(this.id)"><i class="fa fa-caret-right fa-fw"></i></button>';
//   } else {
//     folio_menu = folio_menu+'<div class="disabled-btn-left"><i class="fa fa-caret-right fa-fw"></i></div>';
//   };
//   document.getElementById('folio-menu').innerHTML = folio_menu;
// }
//
//
// function updateToolbar() {
//   if (xmleditor.session.getUndoManager().isClean()) {
//     $("#xmleditor_save").addClass("disabled");
//   };
//
//   if (!xmleditor.session.getUndoManager().hasUndo()) {
//     $("#xmleditor_undo").addClass("disabled");
//   };
//   if (!xmleditor.session.getUndoManager().hasRedo()) {
//     $("#xmleditor_redo").addClass("disabled");
//   };
// }
//
// //editor.session.setValue(localStorage.savedValue || "Welcome to ace Toolbar demo!")
//
// function editorButtonSave() {
//     editorSave();
//     xmleditor.setReadOnly(true);
//     editor_buttons.innerHTML = '<button class="editor-btn float-right button-border-left" id="xmleditor_edit" type="button" onclick="editorButtonEdit();"><i class="fa fa-edit fa-fw"></i> Edit</button>';
//     //xmleditor.session.getUndoManager().markClean();
// }
//
// function editorSave() {
//     var tr_folio = folio_idx;
//     var tr_text = xmleditor.getValue();
//     if (tr_text != '' && tr_text != 'Start new transcription...' &&  !xmleditor.getReadOnly()) {
//       var tr_id = folio_array[tr_folio].tr_id
//       var tr_ver = folio_array[tr_folio].tr_version + 1;
//       var tr_page = folio_array[tr_folio].id
//       var tr_source = source_id;
//       if (tr_id != 'None') {
//         var url = "/api/transcriptions/"+tr_id+"/";
//         $.ajax({
//           method: "PUT",
//           url: url,
//           headers: { 'X-CSRFToken': getCookie("csrftoken") },
//           data: { 'version': tr_ver, 'transcription': tr_text },
//         }).done(function(data, textStatus, jqXHR) {
//             if (data['version'] > folio_array[tr_folio]['tr_version']) { folio_array[tr_folio]['tr_version'] = data['version'] };
//         }).fail(function(jqXHR, textStatus, errorThrown) { alert('There was an error saving the transcription to the server: '+errorThrown); });
//       } else {
//         var url = "/api/transcriptions/";
//         $.ajax({
//           method: "POST",
//           url: url,
//           headers: { 'X-CSRFToken': getCookie("csrftoken") },
//           data: { 'version': tr_ver, 'transcription': tr_text, 'source': tr_source, 'page': tr_page },
//         }).done(function(data, textStatus, jqXHR) {
//             folio_array[tr_folio]['tr_id'] = data['id'];
//             folio_array[tr_folio]['tr_version'] = data['version'];
//             transcriber_container.innerHTML = 'Transcribed by '+data['author'];
//         }).fail(function(jqXHR, textStatus, errorThrown) { alert('There was an error saving the transcription to the server: '+errorThrown); });
//       };
//     }
// }
//
// function editorButtonCancel() {
//     do {
//       xmleditor.undo()
//     } while (xmleditor.session.getUndoManager().hasUndo());
//     editorSave();
//     xmleditor.setReadOnly(true);
//     if (xmleditor.getValue() == '') { xmleditor.session.setValue('Start new transcription...'); };
//     editor_buttons.innerHTML = '<button class="editor-btn float-right button-border-left" id="xmleditor_edit" type="button" onclick="editorButtonEdit();"><i class="fa fa-edit fa-fw"></i> Edit</button>';
// }
//
// function editorButtonEdit() {
//     xmleditor.setReadOnly(false);
//     if (xmleditor.getValue() == 'Start new transcription...') { xmleditor.session.setValue(''); };
//     editor_buttons.innerHTML = '<button class="editor-btn float-right button-border-left editor-save" id="xmleditor_save" type="button" onclick="editorButtonSave();"><i class="fa fa-save fa-fw"></i> Save</button>\
//     <button class="editor-btn float-right button-border-left editor-cancel" id="xmleditor_cancel" type="button" onclick="editorButtonCancel();"><i class="fa fa-times-circle fa-fw"></i> Cancel</button>\
//     <button class="editor-btn float-left button-border-right" id="xmleditor_undo" type="button" onclick="xmleditor.undo();"><i class="fa fa-undo-alt fa-fw"></i></button>\
//     <button class="editor-btn float-left button-border-right" id="xmleditor_redo" type="button" onclick="xmleditor.redo();"><i class="fa fa-redo-alt fa-fw"></i></button>';
//     xmleditor.on("input", updateToolbar);
// }
//
// function setEditorOptions(mode) {
//   if (mode == 'default') {
//     xmleditor.setOptions({
//         theme: "ace/theme/chrome",
//         readOnly: true,
//         highlightActiveLine: true,
//         highlightSelectedWord: true,
//         highlightGutterLine: true,
//         showInvisibles: false,
//         showPrintMargin: false,
//         showFoldWidgets: true,
//         showLineNumbers: true,
//         showGutter: true,
//         displayIndentGuides: true,
//         fontSize: 14,
//         wrap: true,
//         foldStyle: "markbegin",
//         mode: "ace/mode/xml",
//         indentedSoftWrap: true,
//         fixedWidthGutter: true,
//     });
//   } else {
//     if (typeof mode !== 'undefined')  {
//       var target = mode.target;
//       var option = target.id;
//       if ($(target).is('select')) {
//         var value = $(target).val()
//       } else {
//         var value = $(target).prop('checked')
//       }
//       xmleditor.setOption(option, value);
//     }
//   };
// }
//
// function renderer(st) {
//   var editor = $('#xml_editor');
//   var renderer = $('#text_render');
//   if (st == 'on') {
//     var e_height = editor_container.innerHeight();
//     var e_width = editor_container.innerWidth();
//     var text = xmleditor.getValue();
//     editor_container.css({"z-index": -1});
//     renderer_container.height(e_height-40);
//     renderer_container.width(e_width-40);
//     renderer_container.css({"margin-top": -e_height + 'px', "z-index": 100});
//     var xml = '<TEI xmlns="http://www.tei-c.org/ns/1.0"><text><body>'+text+'</body></text></TEI>';
//     var tei = new CETEI();
//     tei.addBehaviors({
//       'tei': {
//         'gap': function(e) { e.setAttribute("title", getTEITitle(e, 'gap')); e.setAttribute("data-toggle", "tooltip"); }, //@reason, @unit, @quantity, @extent
//         'space': function(e) { e.setAttribute("title", getTEITitle(e, 'space')); e.setAttribute("data-toggle", "tooltip"); }, //@unit, @quantity, @extent
//         'unclear': function(e) { e.setAttribute("title", getTEITitle(e, 'unclear')); e.setAttribute("data-toggle", "tooltip"); }, //@reason
//         'supplied': function(e) { e.setAttribute("title", getTEITitle(e, 'supplied')); e.setAttribute("data-toggle", "tooltip"); }, //@reason
//         'add': function(e) { e.setAttribute("title", getTEITitle(e, 'addition')); e.setAttribute("data-toggle", "tooltip"); }, //@place
//         'abbr': function(e) { e.setAttribute("title", getTEITitle(e, 'abbreviation')); e.setAttribute("data-toggle", "tooltip"); }, //@type
//         'w': function(e) { e.setAttribute("title", getTEITitle(e, 'word')); e.setAttribute("data-toggle", "tooltip"); }, //@type, @lemma
//         'quote': function(e) { e.setAttribute("title", getTEITitle(e, 'quote')); e.setAttribute("data-toggle", "tooltip"); } //@resp
//       }
//     });
//     tei.makeHTML5(xml, function(data) { renderer_container.html(data); });
//     $('[data-toggle="tooltip"]').tooltip({container: 'body'});
//   } else if (st == 'off') {
//     editor_container.css({"z-index": 100});
//     renderer_container.css({"margin-top": 0, "z-index": -1});
//   }
// }
//
//
//
// function getFolioIndex(folio) {
//   return folio_array.findIndex(x => x.name === folio);
// }
//
// function nextFolio(i) {
//     if (i+1 >= folio_array.length) {
//       return 0;
//     } else {
//       i = i + 1; // increase i by one
//       return folio_array[i]; // give us back the item of where we are now
//     }
// }
//
// function prevFolio(i) {
//     if (i == 0) {
//       return 0;
//     } else {
//       i = i - 1; // decrease by one
//       return folio_array[i]; // give us back the item of where we are now
//     }
// }
