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
      maxHeight = $(window).height() - 340;
      editor_mode = 'render';
      edit_mode = 'off';
      folio_array = folio_list;
      folio_idx = 0;
      resetPanelMetrics();
      tei = new CETEI();
      tei.addBehaviors(dalmeTeiBehaviours);
      if (folio_array[0].dam_id == 'None') {
          $('#diva_viewer').html('<div class="mt-auto mb-auto">There is no image associated with this folio/page.</div>');
      } else {
          $('#diva_viewer').empty();
          diva = new Diva('diva_viewer', {
             objectData: '/pages/'+folio_array[0].id+'/manifest',
             enableAutoTitle: false,
             enableFullscreen: false,
             enableKeyScroll: false,
             blockMobileMove: false,
             enableSpaceScroll: false,
             enableGotoPage: false,
             enableGridIcon: false,
             enableImageTitles: false,
             enableToolbar: true,
             tileHeight: 1000,
             tileWidth: 1000
          });
      };
      if (folio_array[0].tr_id == 'None') {
          $('#editor').html('<div class="mt-auto mb-auto ml-auto mr-auto">This folio/page has not been transcribed. Click <b>Edit</b> to start...</div>');
          $('#author').html('No transcription available');
          tr_text = '';
      } else {
          $.ajax({
            method: "GET",
            url: `${api_endpoint}/transcriptions/${folio_array[0].tr_id}/?format=json`,
            xhrFields: { withCredentials: true },
            crossDomain: true,
            headers: {
              "Content-Type": "application/json",
              'X-CSRFToken': get_cookie("csrftoken")
            }
          }).done(function(data, textStatus, jqXHR) {
            tr_text = data.transcription;
            let text_to_render = tr_text.replace(/\n/g, '<lb/>');
            tei.makeHTML5('<TEI xmlns="http://www.tei-c.org/ns/1.0"><text><body>'+text_to_render+'</body></text></TEI>', function(text) {
                $('#editor').removeClass("justify-content-center").addClass("justify-content-left").html(text);
            });
            $('[data-toggle="tooltip"]').tooltip({container: 'body', trigger: 'hover'});
            $('#author').html('Transcribed by '+data.author);
            setupTeiRendering()
          });
      };
      $('.panel-top').resizable({
          handles: {s: '.splitter-horizontal'},
          maxHeight: maxHeight,
          minHeight: 200,
          resize: function(e, ui) { resizeEditor(ui.element.outerHeight()); }
      });
      window.addEventListener('resize', function () {
          if (window_height != $(window).height() || window_width != $(window).width()) {
              maxHeight = $(window).height() - 340;
              const c_height = $('#tr_editor').height() - $('#viewer-toolbar').outerHeight();
              const new_top_height = c_height * ( top_height / container_height * 100 ) / 100;
              $('.panel-top').height(new_top_height);
              resizeEditor(new_top_height);
              if (top_width & 1) {
                $('#diva_viewer').width(top_width + 1);
                Diva.Events.publish("PanelSizeDidChange");
              };
              if (editor_mode == 'xml') { xmleditor.resize() };
          }
      }, false);
      Diva.Events.subscribe('DocumentDidLoad', function () { window.dispatchEvent(new Event('resize')); });
  } else {
    $('#author').html(footer_content);
  }
}

function resizeEditor(top_height) {
    var diva_height = Math.round(top_height - $('.splitter-horizontal').height() + 3);
    if (diva_height & 1) { diva_height += 1 };
    const remainingSpace = $('#tr_editor').height() - top_height - $('#viewer-toolbar').outerHeight();
    $('.panel-bottom').height(remainingSpace);
    $('#diva_viewer').height(diva_height);
    $('#editor').height(remainingSpace - $('#editor-toolbar').outerHeight());
    $('#tag-menu').height(remainingSpace - $('#editor-toolbar').outerHeight());
    if (editor_mode == 'xml') { xmleditor.resize() };
    resetPanelMetrics();
}

function resetPanelMetrics() {
  window_height = $(window).height();
  window_width = $(window).width();
  container_height = $('#tr_editor').height() - $('#viewer-toolbar').outerHeight();
  top_height = $('.panel-top').outerHeight();
  bottom_height = $('.panel-bottom').outerHeight();
  top_width = $('.panel-top').width();
}

function cleanFooter() {
  footer_content = $('#author').html();
  $('#author').html('');
}

function changeEditorMode() {
  if (editor_mode == 'render') {
      editor_mode = 'xml';
      $('#editor').empty();
      $('#btn_edit').html('<i class="fa fa-eye fa-fw"></i> View');
      xmleditor = ace.edit("editor");
      setEditorOptions();
      xmleditor.session.setValue(tr_text);
      xmleditor.session.on("change", _.debounce(saveEditor, 1000));
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
      xmleditor.renderer.freeze();
      xmleditor.destroy();
      $('#btn_edit').html('<i class="fa fa-edit fa-fw"></i> Edit');
      if (tr_text != '') {
        let text_to_render = tr_text.replace(/\n/g, '<lb/>');
        tei.makeHTML5('<TEI xmlns="http://www.tei-c.org/ns/1.0"><text><body>'+text_to_render+'</body></text></TEI>', function(text) {
            $('#editor').removeClass("justify-content-center").addClass("justify-content-left").html(text);
        });
        setupTeiRendering()
      } else {
        $('#editor').html('<div class="mt-auto mb-auto ml-auto mr-auto">This folio/page has not been transcribed. Click <b>Edit</b> to start...</div>');
        $('#editor').html('No transcription available');
      };
      $('[data-toggle="tooltip"]').tooltip({container: 'body', trigger: 'hover'});
  }
}

function changeEditorImage(target) {
  if (folio_array[target].dam_id == 'None') {
      $('#diva_viewer').html('<div class="mt-auto mb-auto">There is no image associated with this folio/page.</div>');
  } else {
      diva.changeObject('/pages/'+folio_array[target].id+'/manifest');
      diva.setZoomLevel(2);
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
        $('#editor').html('<div class="mt-auto mb-auto ml-auto mr-auto">This folio/page has not been transcribed. Click <b>Edit</b> to start...</div>');
        $('#author').html('No transcription available');
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
      $.ajax({
        method: "GET",
        url: `${api_endpoint}/transcriptions/${folio_array[target].tr_id}/?format=json`,
        xhrFields: { withCredentials: true },
        crossDomain: true,
        headers: {
          "Content-Type": "application/json",
          'X-CSRFToken': get_cookie("csrftoken")
        }
      }).done(function(data, textStatus, jqXHR) {
        tr_text = data.transcription;
        if (editor_mode == 'render') {
            let text_to_render = tr_text.replace(/\n/g, '<lb/>');
            tei.makeHTML5('<TEI xmlns="http://www.tei-c.org/ns/1.0"><text><body>'+text_to_render+'</body></text></TEI>', function(text) {
                $('#editor').html(text);
            });
            $('[data-toggle="tooltip"]').tooltip({container: 'body', trigger: 'hover'});
            setupTeiRendering()
        } else if (editor_mode == 'xml') {
            saveEditor();
            xmleditor.session.setValue(tr_text);
            xmleditor.session.getUndoManager().reset();
            updateEditorToolbar();
        }
        $('#author').html('Transcribed by '+data.author);
        $('#btn_prevFolio').attr('value', prev);
        $('#btn_selectFolio').text("Folio "+folio_array[target].name+" ("+(target+1)+"/"+total+")");
        $('#folio-menu').find('.current-folio').removeClass('current-folio');
        $('#folio-menu').find('#'+target).addClass('current-folio');
        $('#btn_nextFolio').attr('value', next);
        updateFolioButtons();
        changeEditorImage(target);
        folio_idx = target;
        $(document.body).css('cursor', 'default');
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
  let editor_options = $('#hidden-content').html();
  $('#editor-right-toolbar')
    .prepend('<button class="editor-btn button-border-left" id="btn_cancel" onclick="cancelEditor()"><i class="fa fa-times-circle fa-fw"></i> Cancel</button>')
    .prepend('<button class="editor-btn button-border-left" id="btn_save" onclick="saveButton()" disabled><i class="fa fa-save fa-fw"></i> Save</button>');
  $('#editor-left-toolbar')
    .prepend('<button class="editor-btn button-border-right" id="btn_options" onclick="editorOptionsMenu()" title="Editor options" data-toggle="tooltip"><i class="fas fa-cog fa-fw" ></i></button>')
    .append('<button class="editor-btn button-border-right" id="btn_redo" onclick="redoEditor()" title="Redo" data-toggle="tooltip" disabled><i class="fa fa-redo-alt fa-fw"></i></button>')
    .append('<button class="editor-btn button-border-right" id="btn_undo" onclick="undoEditor()" title="Undo" data-toggle="tooltip" disabled><i class="fa fa-undo-alt fa-fw"></i></button>');
  $('#xmleditor-options').html(editor_options);
  $('#xmleditor-options-form').find('input').on('change.dalme', function (e) { setEditorOptions(e) });
  $('#xmleditor-options-form').find('select').on('change.dalme', function (e) { setEditorOptions(e) });
  $('[data-toggle="tooltip"]').tooltip({container: 'body', trigger: 'hover'});
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
      var url = `${api_endpoint}/transcriptions/${id}/`;
      $.ajax({
        method: "PUT",
        url: url,
        xhrFields: { withCredentials: true },
        crossDomain: true,
        headers: {
          "Content-Type": "application/json",
          'X-CSRFToken': get_cookie("csrftoken")
        },
        data: JSON.stringify({ 'version': ver, 'transcription': text, 'source': source }),
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
      var url = `${api_endpoint}/transcriptions/`;
      $.ajax({
        method: "POST",
        url: url,
        xhrFields: { withCredentials: true },
        crossDomain: true,
        headers: {
          "Content-Type": "application/json",
          'X-CSRFToken': get_cookie("csrftoken")
        },
        data: JSON.stringify({ 'version': ver, 'transcription': text, 'source': source, 'page': page }),
      }).done(function(data, textStatus, jqXHR) {
          folio_array[folio]['tr_id'] = data['id'];
          folio_array[folio]['tr_version'] = data['version'];
          $('#author').html('Transcribed by '+data['author']);
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

function setTagMenu(action) {
  if (action == 'on') {
      if (typeof tag_menu_html == 'undefined') {
          $.ajax({
            method: "POST",
            url: `${api_endpoint}/configs/get/`,
            xhrFields: { withCredentials: true },
            crossDomain: true,
            headers: {
              "Content-Type": "application/json",
              'X-CSRFToken': get_cookie("csrftoken")
            },
            data: JSON.stringify({
              'target': 'editor_tei_tags'
            })
          }).done(function(data, textStatus, jqXHR) {
              tei_tags = data[0];
              tag_menu_html = '';
              for (let i = 0, len = tei_tags.length; i < len; ++i) {
                  let item = tei_tags[i];
                  let att_array = [];
                  if ('section' in item) {
                      if (item.section == 'close') {
                        tag_menu_html += '</div></div>';
                      } else {
                        tag_menu_html += `<div class="tag-menu-container"><div class="tag-menu-section-head collapsed" id="heading_${item.id}" data-toggle="collapse" \
                        data-target="#${item.id}" aria-expanded="false" aria-controls="${item.id}">${item.section}</div>\
                        <div id="${item.id}" class="collapse" aria-labelledby="heading_${item.id}" data-parent="#tag-menu">`;
                      }
                  } else {
                      if ('attribute_name' in item) {
                        att_array.push(item.attribute_name+'|'+item.attribute_value);
                      };
                      if ('attributes' in item) {
                          tag_menu_html += `<div class="list-group dropleft"><div class="tag-menu-button tag-keep-open" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false"><i class="fas fa-caret-left fa-fw mr-1">\
                          </i>${item.name}<i class="far fa-info-circle fa-fw ml-auto pl-2 tag-tooltip" data-html="true" data-toggle="tooltip" data-placement="left" title="${item.help} \
                          <a href='https://wiki.dalme.org/DALME_TEI_Schema${item.link}' target='_blank'>See DALME Wiki</a>"></i>\
                          </div><div id="${item.tag_name}_dd" class="dropdown-menu tag-menu-dropdown p-2"><div class="tag-menu-form">`;
                          let message = '';
                          for (let j = 0, lenj = item.attributes.length; j < lenj; ++j) {
                            let att = item.attributes[j];
                            message += att.message;
                            att_array.push(att.name+'|'+att.type+'|'+item.tag_name+'_'+att.name);
                            if (att.type == 'text') {
                                tag_menu_html += `<input class="form-control form-control-sm" type="text" id="${item.tag_name+'_'+att.name}" placeholder="${att.label}">`;
                                if ('options' in att) {
                                  message += ' (<i>e.g.:</i> ';
                                  let opt_list = [];
                                  for (let k = 0, lenk = att.options.length; k < lenk; ++k) {
                                    opt_list.push(`<a href="#" onclick="$(\'#${item.tag_name+'_'+att.name}\').val(\'${att.options[k]}\')">${att.options[k]}</a>`);
                                  };
                                  message += opt_list.join(', ')
                                  message += ')';
                                };
                            } else if (att.type == 'choice') {
                                tag_menu_html += `<select class="form-control form-control-sm" id="${item.tag_name+'_'+att.name}">`
                                tag_menu_html += `<option disabled selected>${att.label}</option>`;
                                for (let k = 0, lenk = att.options.length; k < lenk; ++k) { tag_menu_html += `<option>${att.options[k]}</option>`; };
                                tag_menu_html += `</select>`;
                            };
                          };
                          message += '.';
                          tag_menu_html += `<button type="button" class="btn btn-primary dd-button" onclick="addTag('${item.type}', '${item.tag_name}', '${att_array.join('-')}')">Add</button>`;
                          tag_menu_html += `</div><small class="form-text text-muted">${message}</small></div></div>`;
                      } else if ('menu' in item) {
                          tag_menu_html += `<div class="list-group dropleft"><div class="tag-menu-button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false"><i class="fas fa-caret-left fa-fw mr-1">\
                          </i>${item.name}<i class="far fa-info-circle fa-fw ml-auto pl-2 tag-tooltip" data-html="true" data-toggle="tooltip" data-placement="left" title="${item.help} \
                          <a href='https://wiki.dalme.org/DALME_TEI_Schema${item.link}' target='_blank'>See DALME Wiki</a>"></i>\
                          </div><div id="${item.tag_name}_dd" class="dropdown-menu">`;
                          for (let j = 0, lenj = item.menu.length; j < lenj; ++j) {
                            tag_menu_html += `<a class="dropdown-item" href="#" onclick="addTag('${item.type}', '${item.tag_name}', '${item.attribute}|${item.menu[j]}')">${item.menu[j]}</a>`;
                          };
                          tag_menu_html += '</div>';
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
              $('.tag-keep-open').on('click', function(e) { $(this).next().toggle(); });
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
    if (tag == 'note' || tag == 'seg') { var special_att = {} };
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
              if (tag == 'note' || tag == 'seg') {
                special_att[att[0]] = att_value;
              } else {
                tag_attributes.push([att[0], att_value]);
              }
          }
      }
    };
    if (tag == 'seg') {
      tag_attributes.push(['target', special_att['target']]);
      tag_attributes.push(['rend', special_att['rend']]);
    };
    if (tag == 'note') {
      if (special_att['type'] == 'renvoi') {
        const note_ref = `<ref target="${special_att['target']}"/>`;
        const note_output = `\n\n<note xml:id="${special_att['target']}">${special_att['text']}</note>`;
        xmleditor.session.insert(xmleditor.getCursorPosition(), note_ref);
        xmleditor.session.insert({row: xmleditor.session.getLength(), column: 0}, note_output)
      } else {
        const tag_output = `<note type="${special_att['type']}">${special_att['text']}</note>`;
        xmleditor.session.insert(xmleditor.getCursorPosition(), tag_output)
      }
    } else {
      var tag_output = '<' + tag;
      if (tag_attributes.length != 0) {
        for (let i = 0, len = tag_attributes.length; i < len; ++i) {
          if (tag_attributes[i][1] != '' && tag_attributes[i][1] != 'Join') {
            tag_output += ' ' + tag_attributes[i][0] + '="' + tag_attributes[i][1] + '"';
          }
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
      if (tag == 'seg') {
        const note_output = `\n\n<note type="brace" xml:id="${special_att['target']}">${special_att['text']}</note>`;
        xmleditor.session.insert({row: xmleditor.session.getLength(), column: 0}, note_output)
      };
    }
}

function setupTeiRendering() {
  if ($('tei-seg[type=brace]').length) { formatBraces(); }
  if ($('tei-note[type=marginal]').length) { formatMarginalNotes(); }
  if ($('tei-ref[target]').length) { formatRenvois(); }
  if ($('tei-ab[type=column]').length) { formatColumns(); }
  if ($('tei-metamark[function=leader]').length) { formatLeaders(); }
  $('[data-toggle="tooltip"]').tooltip();
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

function editDescription() {
  if ($('#descriptionEditor').length) {
    initial_description_text = $('#descriptionEditor').text();
    $('#descriptionEditor').attr('contenteditable', true);
  } else {
    $('#description-container').html('<div id="descriptionEditor" contenteditable="true"></div>')
    initial_description_text = '';
  }
  $('#descriptionEditorToolbar').html('<button class="sub-card-button" role="button" onclick="saveDescription()">Save</button>\
  <button class="sub-card-button" role="button" onclick="cancelDescription()">Cancel</button>');
}

function cancelDescription() {
  if (confirm("Cancel the editing session? All your changes will be lost.")) {
    endDescriptionEditing(initial_description_text)
  }
}

function endDescriptionEditing(description_text) {
  if (description_text == '') {
      $('#description-container').html('<div class="placeholder d-flex justify-content-center align-items-center">\
          <div class="d-block fa-stack mt-5 mb-5"><i class="d-block fas fa-align-left fa-stack-2x"></i><i class="d-block fas fa-slash fa-stack-2x"></i>\
          </div></div>')
  } else {
    $('#descriptionEditor').text(description_text);
    $('#descriptionEditor').attr('contenteditable', false);
  }
  $('#descriptionEditorToolbar').html('<button class="sub-card-button" role="button" onclick="editDescription()">Edit</button>');
}

function saveDescription() {
  var description_text = $('#descriptionEditor').text();
  if (description_text !== initial_description_text) {
    if (confirm("Save changes and exit? This action cannot be undone.")) {
      $.ajax({
        method: "PATCH",
        url: `${api_endpoint}/sources/${source_id}/change_description/`,
        xhrFields: { withCredentials: true },
        crossDomain: true,
        headers: {
          "Content-Type": "application/json",
          'X-CSRFToken': get_cookie("csrftoken")
        },
        data: JSON.stringify({ "description": description_text })
      }).done(function(data, textStatus, jqXHR) {
          toastr.success("The description was updated.");
          endDescriptionEditing(description_text)
      }).fail(function(jqXHR, textStatus, errorThrown) {
        if (errorThrown == "Forbidden") {
          toastr.error("You do not have the required permissions to modify this description.");
        } else {
          toastr.error('There was an error saving the description to the server: '+errorThrown);
        }
        endDescriptionEditing(initial_description_text)
      });
    }
  }
}

function formatBraces() {
  $('tei-seg[type=brace]').each(function(index, el) {
    let target = $(this).attr('target');
    if (target) {
      if (target.length > 1 && target.startsWith('#')) target = target.substring(1);
      $(this).append($(`tei-note#${target}`).remove());
    }
  });
}

function formatMarginalNotes() {
  $('tei-note[type=marginal]').each(function(index, el) {
    let margin_top = Math.round($(this).position().top);
    let note = $(this).remove();
    $(note).css({ top: `${margin_top}px`});
    $('.notes_container').append(note);
  });
  $('.notes_container').height($('tei-text').height());
  $('#transcription').on('scroll', function (e) {
    $('#notebar').scrollTop($(this).scrollTop());
  });
  $('#notebar').on('scroll wheel', function(e) {
    e.preventDefault();
    e.stopPropagation();
    return false;
  });
}

function formatColumns() {
  $(document).on('click', '.ab-column-toggler', (e) => {
      const parent = e.target.closest('tei-ab');
      parent.classList.toggle('closed');
  });
}

function formatLeaders() {
  let container_width = Math.round(Math.max($('tei-text').innerWidth(), $('tei-body').innerWidth()));
  $('tei-metamark[function=leader]').each(function(index, el) {
    let sum = 0;
    let prev_array = [];
    let next_array = [];
    let prevSibs = $(this).prevUntil('tei-lb');
    let prevChild = $(this).prevUntil('*:has(tei-lb)');
    let nextSibs = $(this).nextUntil('tei-lb');
    let nextChild = $(this).nextUntil('*:has(tei-lb)');
    if (prevChild.length < prevSibs.length) {
      let prev_el = prevChild.length ? prevChild : this;
      prev_array = $.merge(prevChild, $(prev_el).prev().children().nextUntil('tei-lb'));
    } else {
      prev_array = prevSibs;
    }
    if (nextChild.length < nextSibs.length) {
      let next_el = nextChild.length ? nextChild : this;
      next_array = $.merge(nextChild, $(next_el).next().children().nextUntil('tei-lb'));
    } else {
      next_array = nextSibs;
    }
    const line_el = $.merge(prev_array, next_array)
    line_el.each(function(i, elt) { sum += $(this).innerWidth(); });
    const container_column = $(this).parents('.ab-content');
    if (container_column.length) {
      let column_width = container_column.attr('width');
      if (typeof column_width === typeof undefined || column_width === false) {
        container_column.attr('width', container_column.innerWidth());
      }
      container_width = container_column.attr('width');
    }
    let target_width = container_width - sum - 15;
    target_width = target_width > 10 ? target_width : 10;
    $(this).width(target_width);
  });
}

function formatRenvois() {
  $('tei-ref[target]').each( function(index, el) {
    let note_id = $(this).attr('target');
    if (note_id.length > 1 && note_id.startsWith('#')) note_id = note_id.substring(1);
    note = $(`tei-note[id='${note_id}']`)
    if (note.length) {
      $(this).attr({
        title: note.html(),
        'data-toggle': 'tooltip',
        'data-html': true,
        'data-template': '<div class="tooltip note" role="tooltip"><div class="arrow"></div><div class="tooltip-inner"></div></div>',
      })
    }
  })
}

// function create_named_entity() {
//     namedEntityForm = new $.fn.dataTable.Editor( {
//           ajax: {
//             method: "POST",
//             url: `${api_endpoint}/tasklists/`,
//             headers: { 'X-CSRFToken': get_cookie("csrftoken") },
//             data: function (data) { return { "data": JSON.stringify( data ) }; }
//           },
//           fields: [
//             {
//               label: "List name",
//               name: "name",
//               fieldInfo: "Name of the list to be created"
//             },
//             {
//               label: "Group",
//               name:  "group",
//               fieldInfo: "Group of users that will utilize the list",
//               type: "selectize",
//               opts: {'placeholder': "Select user group"},
//               options: groups
//             },
//           ]
//       });
//       namedEntityForm.on('submitSuccess', function(e, json, data, action) {
//         toastr.success('The task list was created successfully.');
//         if (typeof table_lists != 'undefined') {
//           table_lists.ajax.reload();
//         }
//       });
//       namedEntityForm.buttons({
//         text: "Create",
//         className: "btn btn-primary",
//         action: function () { this.submit(); }
//       }).title('Create New Task List').create();
// }
