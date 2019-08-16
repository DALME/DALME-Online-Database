function switch_tab(tab) {
  switch (tab) {
    case 'info-tab':
      cleanFooter();
      localStorage.setItem('sourceTab','info-tab');
      break;
    case 'comments-tab':
      cleanFooter();
      localStorage.setItem('sourceTab','comments-tab');
      break;
    case 'editor-tab':
      startEditor();
      localStorage.setItem('sourceTab','editor-tab');
  }
}

function startEditor() {
  if (typeof transcriber_state == 'undefined') {
      transcriber_state = 'on';
      footer_content = '...';
      viewer_container = document.getElementById('diva_viewer');
      editor_container = document.getElementById('editor');
      tag_menu = document.getElementById('tag-menu');
      editor_toolbar = document.getElementById('editor-toolbar');
      author_container = document.getElementById('author');
      top_panel = document.getElementsByClassName('panel-top');
      maxHeight = $(window).height() - 340;
      editor_mode = 'render';
      edit_mode = 'off';
      folio_array = folio_list;
      folio_idx = 0;
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
      if (folio_array[0].dam_id == 'None') {
          $(viewer_container).html('<div class="mt-auto mb-auto">There is no image associated with this folio/page.</div>');
      } else {
          $(viewer_container).empty();
          diva = new Diva('diva_viewer', {
             objectData: '/pages/'+folio_array[0].id+'/manifest',
             enableAutoTitle: false,
             enableFullscreen: false,
             enableKeyScroll: true,
             blockMobileMove: true,
             enableGotoPage: false,
             enableGridIcon: false,
             enableImageTitles: false,
             enableToolbar: false,
             tileHeight: 1000,
             tileWidth: 1000
          });
      };
      if (folio_array[0].tr_id == 'None') {
          $(editor_container).html('<div class="mt-auto mb-auto ml-auto mr-auto">This folio/page has not been transcribed. Click <b>Edit</b> to start...</div>');
          $(author_container).html('No transcription available');
          tr_text = '';
      } else {
          $.get("/api/transcriptions/"+folio_array[0].tr_id+"?format=json", function (data) {
              tr_text = data.transcription;
              tei.makeHTML5('<TEI xmlns="http://www.tei-c.org/ns/1.0"><text><body>'+tr_text+'</body></text></TEI>', function(text) {
                  $(editor_container).removeClass("justify-content-center").addClass("justify-content-left").html(text);
              });
              $('[data-toggle="tooltip"]').tooltip({container: 'body', trigger: 'hover'});
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
              $(tag_menu).height(divTwoHeight - 56);
              },
          stop: function (e, ui) {
            const parent = ui.element.parent();
            ui.element.css({ height: ui.element.height()/parent.height()*100+"%", });
            //window.dispatchEvent(new Event('resize'));
            }
      });
      window.addEventListener('resize', function () { resizeEditor(); }, false);
      Diva.Events.subscribe('DocumentDidLoad', function () { window.dispatchEvent(new Event('resize')); });
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
      xmleditor.session.on("change", debounce(saveEditor, 1000));
      xmleditor.session.on("change", updateEditorToolbar);
      setEditorToolbar();
      setTagMenu('on');
  } else if (editor_mode == 'xml') {
      editor_mode = 'render';
      saveEditor();
      removeEditorToolbar();
      setTagMenu('off');
      tr_text = xmleditor.getValue();
      xmleditor.off("change");
      xmleditor.destroy();
      $('#btn_edit').html('<i class="fa fa-edit fa-fw"></i> Edit');
      if (tr_text != '') {
        tei.makeHTML5('<TEI xmlns="http://www.tei-c.org/ns/1.0"><text><body>'+tr_text+'</body></text></TEI>', function(text) {
            $(editor_container).removeClass("justify-content-center").addClass("justify-content-left").html(text);
        });
      } else {
        $(editor_container).html('<div class="mt-auto mb-auto ml-auto mr-auto">This folio/page has not been transcribed. Click <b>Edit</b> to start...</div>');
        $(author_container).html('No transcription available');
      };
      $('[data-toggle="tooltip"]').tooltip({container: 'body', trigger: 'hover'});
  }
}

function changeEditorImage(target) {
  if (folio_array[target].dam_id == 'None') {
      $(viewer_container).html('<div class="mt-auto mb-auto">There is no image associated with this folio/page.</div>');
  } else {
      diva.changeObject('/pages/'+folio_array[target].id+'/manifest');
  }
}

function changeEditorFolio(target) {
  $(document.body).css('cursor', 'wait');
  if (target != '') {
    var target = parseInt(target, 10);
    var total = folio_array.length;
    var prev = target != 0 ? target - 1 : '';
    var next = target + 1 >= total ? '' : target + 1;
    if (folio_array[target].tr_id == 'None') {
        if (editor_mode == 'xml') { changeEditorMode() };
        $(editor_container).html('<div class="mt-auto mb-auto ml-auto mr-auto">This folio/page has not been transcribed. Click <b>Edit</b> to start...</div>');
        $(author_container).html('No transcription available');
        tr_text = '';
        $('#btn_prevFolio').attr('value', prev);
        $('#btn_selectFolio').text("Folio "+folio_array[target].name+" ("+(target+1)+"/"+total+")");
        $('#folio-menu').find('.current-folio').removeClass('current-folio');
        $('#folio-menu').find('#'+target).addClass('current-folio');
        $('#btn_nextFolio').attr('value', next);
        updateFolioButtons();
        changeEditorImage(target);
        folio_idx = target;
        $(document.body).css('cursor', 'default');
    } else {
        $.get("/api/transcriptions/"+folio_array[target].tr_id+"?format=json", function (data) {
            tr_text = data.transcription;
            if (editor_mode == 'render') {
                tei.makeHTML5('<TEI xmlns="http://www.tei-c.org/ns/1.0"><text><body>'+tr_text+'</body></text></TEI>', function(text) {
                    $(editor_container).html(text);
                });
                $('[data-toggle="tooltip"]').tooltip({container: 'body', trigger: 'hover'});
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
            changeEditorImage(target);
            folio_idx = target;
            $(document.body).css('cursor', 'default');
            //window.dispatchEvent(new Event('resize'));
        });
    }
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
    $('[data-toggle="tooltip"]').tooltip({container: 'body', trigger: 'hover'});
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
        data: { 'version': ver, 'transcription': text, 'source': source },
      }).done(function(data, textStatus, jqXHR) {
          if (data['version'] > folio_array[folio]['tr_version']) { folio_array[folio]['tr_version'] = data['version'] };
      }).fail(function(jqXHR, textStatus, errorThrown) {
        if (errorThrown == "Forbidden") {
          toastr.error("You do not have the required permissions to edit this transcription.");
        } else {
          toastr.error('There was an error saving the transcription to the server: '+errorThrown);
        }
      });
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
      }).fail(function(jqXHR, textStatus, errorThrown) {
        if (errorThrown == "Forbidden") {
          toastr.error("You do not have the required permissions to save this transcription.");
        } else {
          toastr.error('There was an error saving the transcription to the server: '+errorThrown);
        }
      });
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

function setTagMenu(action) {
  if (action == 'on') {
      if (typeof tag_menu_html == 'undefined') {
          $.ajax({
              method: "GET",
              url: "/api/options/?target=json_file&name=editor_tei_tags&format=json",
          }).done(function(data, textStatus, jqXHR) {
              tei_tags = data.json_file;
              tag_menu_html = '';
              for (let i = 0, len = tei_tags.length; i < len; ++i) {
                  let item = tei_tags[i];
                  let att_array = [];
                  if ('section' in item) {
                      if (item.section == 'pre-close') {
                        tag_menu_html += '</div></div>';
                      };
                      tag_menu_html += `<div class="tag-menu-container"><div class="tag-menu-section-head`;
                      if (item.expanded == 'false') { tag_menu_html += ' collapsed' };
                      tag_menu_html += `" id="heading_${item.id}" data-toggle="collapse" \
                      data-target="#${item.id}" aria-expanded="${item.expanded}" aria-controls="${item.id}">${item.title}</div>\
                      <div id="${item.id}" class="collapse`;
                      if (item.expanded == 'true') { tag_menu_html += ' show' };
                      tag_menu_html += `" aria-labelledby="heading_${item.id}" data-parent="#tag-menu">`;
                  } else {
                      if ('attribute_name' in item) {
                        att_array.push(item.attribute_name+'|'+item.attribute_value);
                      };
                      if ('attributes' in item) {
                          let message = item.message;
                          tag_menu_html += `<div class="list-group dropleft"><div class="tag-menu-button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false"><i class="fas fa-caret-left fa-fw mr-1">\
                          </i>${item.name}<i class="far fa-info-circle fa-fw ml-auto pl-2 tag-tooltip" data-html="true" data-toggle="tooltip" data-placement="left" title="${item.help} <a href='https://wiki.dalme.org/DALME_TEI_Schema${item.link}' target='_blank'>See DALME Wiki</a>"></i>\
                          </div><div id="${item.tag_name}_dd" class="dropdown-menu tag-menu-dropdown p-2"><div class="tag-menu-form">`;
                          for (let j = 0, lenj = item.attributes.length; j < lenj; ++j) {
                            let att = item.attributes[j];
                            att_array.push(att.name+'|'+att.type+'|'+item.tag_name+'_'+att.name);
                            if (att.type == 'text') {
                                tag_menu_html += `<input class="form-control form-control-sm" type="text" id="${item.tag_name+'_'+att.name}" placeholder="${att.label}">`;
                                if ('options' in att) {
                                  message += 'Common choices: ';
                                  for (let k = 0, lenk = att.options.length; k < lenk; ++k) {
                                    message += `<a href="#" onclick="$(\'#${item.tag_name+'_'+att.name}\').val(\'${att.options[k]}\')">${att.options[k]}</a> `;
                                  };
                                };
                            } else if (att.type == 'choice') {
                                tag_menu_html += `<select class="form-control form-control-sm" id="${item.tag_name+'_'+att.name}">`
                                tag_menu_html += `<option disabled selected>${att.label}</option>`;
                                for (let k = 0, lenk = att.options.length; k < lenk; ++k) { tag_menu_html += `<option>${att.options[k]}</option>`; };
                                tag_menu_html += `</select>`;
                            };
                          };
                          tag_menu_html += `<button type="button" class="btn btn-primary dd-button" onclick="addTag('${item.type}', '${item.tag_name}', '${att_array.join('-')}')">Add</button>`;
                          tag_menu_html += `</div><small class="form-text text-muted">${message}</small></div></div>`;
                      } else {
                          tag_menu_html += `<div class="tag-menu-button" onclick="addTag('${item.type}', '${item.tag_name}', '${att_array.join('-')}')"><i class="fas fa-caret-left fa-fw mr-1">\
                          </i>${item.name}<i class="far fa-info-circle fa-fw ml-auto pl-2 tag-tooltip" data-html="true" data-toggle="tooltip" data-placement="left" title="${item.help}"></i></div>`;
                      };
                  }
              };
              tag_menu_html += '</div></div>';
              $('#tag-menu').show();
              $('#tag-menu').html(tag_menu_html);
              $('.tag-tooltip').tooltip({container: 'body', delay: { "show": 100, "hide": 1000 }});
              $('.tag-menu-dropdown').on('click', function(e) { e.stopPropagation(); });
              $('.tag-menu-button').on('click', function(e) { $(this).next().toggle(); });
              $('.dd-button').on('click', function(e) { $(this).parent().parent().toggle(); });
          }).fail(function(jqXHR, textStatus, errorThrown) {
              toastr.error('The following error occured while attempting to retrieve the data for the tags menu: '+errorThrown);
          });
      } else {
          $('#tag-menu').show();
          $('#tag-menu').html(tag_menu_html);
          $('.tag-tooltip').tooltip({container: 'body', delay: { "show": 100, "hide": 1000 }});
          $('.tag-menu-dropdown').on('click', function(e) { e.stopPropagation(); });
          $('.tag-menu-button').on('click', function(e) { $(this).next().toggle(); });
          $('.dd-button').on('click', function(e) { $(this).parent().parent().toggle(); });
      }
  } else {
      $('#tag-menu').html('');
      $('#tag-menu').hide();
  }
}

function addTag(type, tag, att_array) {
    let tag_attributes = [];
    if (tag == 'note') { var note_att = {} };
    if (att_array) {
      if (att_array.includes('-')) {
        att_array = att_array.split('-');
      } else {
        att_array = [att_array];
      };
      for (let i = 0, len = att_array.length; i < len; ++i) {
          let att = att_array[i].split('|');
          if (att.length == 2) {
              tag_attributes.push([att[0], att[1]]);
          } else {
              let att_value = '';
              switch (att[1]) {
                case 'text':
                    att_value = $('#'+att[2]).val();
                    $('#'+att[2]).val('');
                    break;
                case 'choice':
                    att_value = $('#'+att[2]).find('option:selected').text();
                    $('#'+att[2])[0].selectedIndex = 0;
              };
              if (tag == 'note') {
                note_att[att[0]] = att_value;
              } else {
                tag_attributes.push([att[0], att_value]);
              }
          }
      }
    };
    if (tag == 'note') {
      if (note_att['type'] == 'renvoi') {
        note_ref = `<ref target="#note_${note_att['ref']}"/>`;
        note_output = `\n\n<note xml:id="note_${note_att['ref']}">${note_att['text']}</note>`;
        xmleditor.session.insert(xmleditor.getCursorPosition(), note_ref);
        xmleditor.session.insert({row: xmleditor.session.getLength(), column: 0}, note_output)
      } else {
        tag_output = `<note type="${note_att['type']}">${note_att['text']}</note>`;
        xmleditor.session.insert(xmleditor.getCursorPosition(), tag_output)
      }
    } else {
      tag_output = '<' + tag;
      if (tag_attributes.length != 0) {
        for (let i = 0, len = tag_attributes.length; i < len; ++i) {
          tag_output += ' ' + tag_attributes[i][0] + '="' + tag_attributes[i][1] + '"';
        }
      };
      if (type == 'w') {
        const range = xmleditor.selection.getRange();
        tag_output += '>' + xmleditor.getSelectedText() + '</' + tag + '>';
        xmleditor.session.replace(range, tag_output);
      } else {
        tag_output += '/>';
        xmleditor.session.insert(xmleditor.getCursorPosition(), tag_output)
      };
    }
}


/***** Utility functions *********/
function setKeybindings() {
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
