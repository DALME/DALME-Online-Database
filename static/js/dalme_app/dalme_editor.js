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
      tag_reference = {};
      footer_content = '...';
      maxHeight = $(window).height() - 340;
      editor_mode = 'render';
      edit_mode = 'off';
      folio_array = folio_list;
      folio_idx = 0;
      hasBraces = false;
      hasColumns = false;
      hasLeaders = false;
      hasMarginalNotes = false;
      noteBarOn = false;
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
          $('#editor').html('<div class="mt-auto mb-auto ml-auto mr-auto">This folio/page has not been transcribed. \
          Click <b>Edit</b> to start...</div>');
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
                let tei_cont = $('<div id="tei-container"></div>');
                tei_cont.html(text);
                $('#editor').removeClass("justify-content-center").addClass("justify-content-left").append(tei_cont);
                $('#author').html('Transcribed by '+data.author);
                setupTeiRendering()
            });
            // $('[data-toggle="tooltip"]').tooltip({container: 'body', trigger: 'hover'});
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
    let new_h = remainingSpace - $('#editor-toolbar').outerHeight();
    $('#editor').height(new_h);
    resetPanelMetrics();
    if (editor_mode == 'xml') {
      $('#tag-menu').height(new_h);
      xmleditor.resize(); 
    } else {
      updateTeiRendering();
    };
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
      resetTeiRendering();
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
            let tei_cont = $('<div id="tei-container"></div>');
            tei_cont.html(text);
            $('#editor').removeClass("justify-content-center").addClass("justify-content-left").append(tei_cont);
            setupTeiRendering();
        });
      } else {
        $('#editor').html('<div class="mt-auto mb-auto ml-auto mr-auto">This folio/page has not been transcribed. Click <b>Edit</b> to start...</div>');
        $('#editor').html('No transcription available');
      };
      // $('[data-toggle="tooltip"]').tooltip({container: 'body', trigger: 'hover'});
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
            resetTeiRendering();
            let text_to_render = tr_text.replace(/\n/g, '<lb/>');
            tei.makeHTML5('<TEI xmlns="http://www.tei-c.org/ns/1.0"><text><body>'+text_to_render+'</body></text></TEI>', function(text) {
                let tei_cont = $('<div id="tei-container"></div>');
                tei_cont.html(text);
                $('#editor').append(tei_cont);
                setupTeiRendering();
            });
            // $('[data-toggle="tooltip"]').tooltip({container: 'body', trigger: 'hover'});
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
        scrollPastEnd: 0.1,
        useSoftTabs: false,
        navigateWithinSoftTabs: true,
    });
  }
}

function setEditorToolbar() {
  let editor_options = $('#hidden-content').html();
  $('#editor-right-toolbar')
    .prepend('<button class="editor-btn no-active button-border-left" id="btn_cancel" onclick="cancelEditor()"><i class="fa fa-times-circle fa-fw">\</i> Cancel</button>')
    .prepend('<button class="editor-btn no-active button-border-left" id="btn_save" onclick="saveButton()" disabled><i class="fa fa-save fa-fw"></i> Save</button>');
  $('#editor-left-toolbar')
    .prepend('<button class="editor-btn no-active button-border-right" id="btn_options" onclick="editorOptionsMenu()" title="Editor options" data-toggle="tooltip"><i class="fas fa-cog fa-fw" ></i></button>')
    .append('<button class="editor-btn no-active button-border-right" id="btn_redo" onclick="redoEditor()" title="Redo" data-toggle="tooltip" disabled><i class="fa fa-redo-alt fa-fw"></i></button>')
    .append('<button class="editor-btn no-active button-border-right" id="btn_undo" onclick="undoEditor()" title="Undo" data-toggle="tooltip" disabled><i class="fa fa-undo-alt fa-fw"></i></button>');
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
              tei_data = data[0];
              tag_menu_html = '<div class="tag-menu-container">';

              for (const section of tei_data) { // open 1
                tag_menu_html += `<div class="tag-menu-section-head collapsed" id="heading_${section.id}" \ 
                data-toggle="collapse" data-target="#${section.id}" aria-expanded="false" aria-controls="${section.id}">${section.section}</div> \
                <div id="${section.id}" class="collapse" aria-labelledby="heading_${section.id}" data-parent="#tag-menu">`;
                
                for (const item of section.items) {
                  const item_id = item.label.replaceAll(' ', '').replaceAll('/', '').toLowerCase();
                  const defaultCt = item.default_content || null;
                  tag_reference[item_id] = item;
                  
                  if ('attributes' in item) {
                    const att_array = [];
                    var isButton = false;
                    var isMenu = false;

                    if (item.attributes.length == 1 && item.attributes[0].type == 'menu') { // open 2
                      tag_menu_html += `<div class="list-group dropleft"><div class="tag-menu-button" data-toggle="dropdown" \
                      aria-haspopup="true" aria-expanded="false"><i class="fas fa-caret-left fa-fw mr-1">\
                      </i>${item.label}<i class="fas fa-info-circle fa-fw ml-auto pl-2 tag-tooltip" data-html="true" \
                      data-toggle="tooltip" data-placement="left" title="${item.help} <a href='${item.documentation}' target='_blank'>See documentation</a>">\
                      </i></div><div id="${item_id}_dd" class="dropdown-menu">`;
                      isMenu = true;

                    } else if (item.attributes.length == 1 && !item.attributes[0].editable) {
                      tag_menu_html += `<div class="tag-menu-button-safe" onclick="addTag('${item_id}')"><i class="fas \
                      fa-ellipsis-v fa-fw mr-1"></i>${item.label}<i class="fas fa-info-circle fa-fw ml-auto pl-2 \
                      tag-tooltip" data-html="true" data-toggle="tooltip" data-placement="left" title="${item.help} \
                      <a href='${item.documentation}' target='_blank'>See documentation</a>"></i></div>`;
                      isButton = true;

                    } else { // open 4
                      tag_menu_html += `<div class="list-group dropleft"><div class="tag-menu-button tag-keep-open" data-toggle="dropdown" \
                      aria-haspopup="true" aria-expanded="false"><i class="fas fa-caret-left fa-fw mr-1"> \
                      </i>${item.label}<i class="fas fa-info-circle fa-fw ml-auto pl-2 tag-tooltip" data-html="true" data-toggle="tooltip" \
                      data-placement="left" title="${item.help} <a href='${item.documentation}' target='_blank'>See documentation</a>"></i> \
                      </div><div id="${item_id}_dd" class="dropdown-menu tag-menu-dropdown p-2"><div class="tag-menu-form">\
                      <div class="input-container">`;
                    }

                    for (const attribute of item.attributes) {
                        if (attribute.editable) {
                          if (isMenu) {
                            for (const opt of attribute.options) {
                              tag_menu_html += `<a class="dropdown-item" href="#" onclick="addTag('${item_id}', '${opt.value}')">${opt.label}</a>`;
                            }
                            tag_menu_html += '</div></div>'; // close 2

                          } else {
                            if (attribute.type == 'special') {
                              if (item.label == 'Glyph') {
                                tag_menu_html += '</div><div class="glyph-container">';
                                for (const opt of attribute.options) {
                                  tag_menu_html += `<button class="glyph" data-toggle="tooltip" title="${opt.description}" \
                                  onclick="$(\'#${item_id+'_'+attribute.name}\').val(\'${opt.value}\')">&#x${opt.value};</button>`;
                                }
                                tag_menu_html += '</div><div class="input-container">'
                                tag_menu_html += `<div class="input-grp"><input class="form-control form-control-sm" type="text" \
                                id="${item_id+'_'+attribute.name}" placeholder="Unicode value" aria-describedby="${item_id+'_'+attribute.name+'_help'}">\
                                <small id="${item_id+'_'+attribute.name+'_help'}" class="form-text-flex text-muted"><span>\
                                You can find new glyphs by consulting <a href="https://symbl.cc/en/unicode/" target="_blank">character tables</a> \
                                or by <a href="https://shapecatcher.com" target="_blank">drawing the desired symbol</a>.</span></small></div>`; 
                              }
                            } else {
                              if (attribute.type == 'string') {
                                  let att_html = attribute.description ? '<div class="input-grp">' : '';
                                  att_html += `<input class="form-control form-control-sm" type="text" id="${item_id+'_'+attribute.name}" \
                                  placeholder="${attribute.label}"`;
  
                                  if (attribute.description) {
                                    att_html += ` aria-describedby="${item_id+'_'+attribute.name+'_help'}">\
                                    <small id="${item_id+'_'+attribute.name+'_help'}" class="form-text-flex text-muted"><span>${attribute.description}</span></small></div>`
                                  } else {
                                    att_html += '>';
                                  }
                                  
                                  tag_menu_html += att_html;
  
                              } else if (attribute.type == 'textarea') {
                                  let att_html = attribute.description ? '<div class="input-grp">' : '';
                                  att_html += `</div><textarea class="form-control form-control-sm" id="${item_id+'_'+attribute.name}" \
                                  placeholder="${attribute.label}"`;
                                  
                                  if (attribute.description) {
                                    att_html += ` aria-describedby="${item_id+'_'+attribute.name+'_help'}"></textarea>\
                                    <small id="${item_id+'_'+attribute.name+'_help'}" class="form-text-flex text-muted">${attribute.description}</small>\
                                    </div><div class="input-container">`
                                  } else {
                                    att_html += '></textarea><div class="input-container">';
                                  }
  
                                  tag_menu_html += att_html;
                              
                              } else if (attribute.type == 'choice') {
                                  tag_menu_html += `<select class="form-control form-control-sm" id="${item_id+'_'+attribute.name}">`
                                  tag_menu_html += `<option disabled selected>${attribute.label}</option>`;
                                  
                                  for (const opt of attribute.options) {
                                    tag_menu_html += `<option value="${opt.value}"`;
                                    if (opt.value == attribute.default) {
                                      tag_menu_html += ' selected';
                                    }
                                    tag_menu_html += `>${opt.label}</option>`;
                                  };
                                  
                                  tag_menu_html += `</select>`;

                              } else if (attribute.type == 'multichoice') {
                                  tag_menu_html += `</div><div class="multi-container" id="${item_id+'_'+attribute.name}">`;
                                  for (const opt of attribute.options) {
                                    tag_menu_html += `<div class="form-check"><input class="form-check-input" \
                                    type="checkbox" value="${opt.value}" id="${item_id+'_'+opt.value}"`
                                    if (opt.value == attribute.default) {
                                      tag_menu_html += ' checked="true"';
                                    }
                                    tag_menu_html += `><label class="form-check-label" for="${item_id+'_'+opt.value}">${opt.label}</label></div>`;
                                    if (opt.description) {
                                      tag_menu_html += `<div class="multi-help">${opt.description}</div>`;
                                    }
                                  };
                                  tag_menu_html += '</div><div class="input-container">';
                              }
                            }
                          }
                        }
                    }
                    
                    if (!isButton && !isMenu) {
                      tag_menu_html += `<button type="button" class="btn btn-primary dd-button" onclick="addTag('${item_id}')">Add</button>\
                      </div></div></div></div>`;
                    }
                  
                  } else {
                      tag_menu_html += `<div class="tag-menu-button-safe" onclick="addTag('${item_id}')"><i class="fas \
                      fa-ellipsis-v fa-fw mr-1"></i>${item.label}<i class="fas fa-info-circle fa-fw ml-auto pl-2 \
                      tag-tooltip" data-html="true" data-toggle="tooltip" data-placement="left" title="${item.help} \
                      <a href='${item.documentation}' target='_blank'>See documentation</a>"></i></div>`;
                  };
                }
                tag_menu_html += '</div>';
              }

              tag_menu_html += '</div>';
              $('#tag-menu').show();
              $('#tag-menu').html(tag_menu_html);
              $('#tag-menu').height($('#editor').outerHeight());
              $('.tag-tooltip').tooltip({container: 'body', delay: { "show": 100, "hide": 1000 }});
              $('.tag-menu-dropdown').on('click', function(e) { e.stopPropagation(); });
              $('.tag-keep-open').on('click', function(e) { $(this).next().toggle(); });
              $('.dd-button').on('click', function(e) { $(this).parent().parent().parent().toggle(); });
          
          }).fail(function(jqXHR, textStatus, errorThrown) {
              toastr.error('The following error occured while attempting to retrieve the data for the tags menu: '+errorThrown);
          });
      
      } else {
          $('#tag-menu').show();
          $('#tag-menu').html(tag_menu_html);
          $('#tag-menu').height($('#editor').outerHeight());
          $('.tag-tooltip').tooltip({container: 'body', delay: { "show": 100, "hide": 1000 }});
          $('.tag-menu-dropdown').on('click', function(e) { e.stopPropagation(); });
          $('.tag-menu-button').on('click', function(e) { $(this).next().toggle(); });
          $('.dd-button').on('click', function(e) { $(this).parent().parent().parent().toggle(); });
      }

  } else {
      $('#tag-menu').html('');
      $('#tag-menu').hide();
  }
}

function addTag(item_id, value=null) {
    const item_data = tag_reference[item_id];
    const attributes = {};
    let type = item_data.type;
    let tag_attributes = null;
    let tag_content = null;
    let prefix = null;
    let suffix = null;
    let tag_output = '<' + item_data.tag;
    let insert_range = xmleditor.selection.getRange();
    let insert_point = insert_range.end;
    let skip_tag = false;

    if (item_data.attributes) {
      item_data.attributes.forEach((attr) => {
        if (!attr.editable) {
          attributes[attr.name] = attr.default;
        } else if (attr.type == 'menu') {
          attributes[attr.name] = value;
        } else {
          let reset_val = attr.default ? attr.default : '';
          if (['string', 'textarea', 'special'].includes(attr.type)) {
            attributes[attr.name] = $(`#${item_id}_${attr.name}`).val();
            $(`#${item_id}_${attr.name}`).val(reset_val);
          
          } else if (attr.type == 'multichoice') {
            let att_list = [];
            $(`#${item_id}_${attr.name}`).find('input[type=checkbox]').each(function(index, el) {
              if (this.checked) {
                att_list.push($(this).val());
                if ($(this).val() != reset_val) {
                  $(this).prop("checked", false);
                }
              }
            });
            if (att_list.length) {
              attributes[attr.name] = att_list;
            }

          } else {
            let sel_val = $(`#${item_id}_${attr.name}`).find('option:selected').val();
            if (sel_val && sel_val != attr.label) {
              attributes[attr.name] = sel_val;
            }
            if (reset_val != '') {
              $(`#${item_id}_${attr.name}`).val(reset_val);
            } else {
              $(`#${item_id}_${attr.name}`)[0].selectedIndex = 0;
            }
          }
        }
      })
    }

    if (type == 'w') {
      let selection = xmleditor.getSelectedText();
      if (selection) {
        tag_content = selection;
      } else if (item_data.default_content) {
        tag_content = item_data.default_content;
      }
    }

    if (item_id == 'columns') {
      let col_count = attributes.columns;
      let content = '';
      for (let i = 0; i < col_count; i++) {
        content += `\n\t<ab type="column" n="${i+1}">`;
        if (i == 0 && tag_content) {
          let lines = tag_content.split('\n');
          lines.forEach((line) => {
            content += `\n\t\t${line}`;
          })
        } else {
          content += `\n\t\tCOLUMN ${i+1} CONTENT`;
        }
        content += '\n\t</ab>';
      }
      tag_content = `${content}\n`;
      prefix = '\n';
    }

    if (item_id == 'glyph') {
      let opt = item_data.attributes[0].options.filter((i) => i.value == attributes.ref)[0];
      if (opt.wrapper) {
        prefix = `<${opt.wrapper.tag}`;
        if (opt.wrapper.attributes) {
          for (const key in opt.wrapper.attributes) {
            prefix += ` ${key}="${opt.wrapper.attributes[key]}"`
          }
          prefix += '>'
        } else {
          prefix += '>'
        }
        suffix = `</${opt.wrapper.tag}>`;
      }
    }

    if (item_data.tag == 'note') {
      let { text, rend, gloss, lang, ...x_attributes } = attributes;
      tag_attributes = x_attributes;
      rend = Array.isArray(rend) ? rend.join(' ') : rend;
    
      if (['renvoi', 'brace', 'gloss'].includes(tag_attributes.type)) {
        const note_id = Math.ceil(Math.random()*10000);
        prefix = '\n';
        suffix = '\n';
        tag_attributes['xml:id'] = note_id;
        
        if (tag_attributes.type == 'renvoi') {
          xmleditor.session.replace(insert_range, `<ref target="${note_id}" rend="${rend}">${tag_content}</ref>`);
        } else if (tag_attributes.type == 'gloss') {
          xmleditor.session.replace(insert_range, `<term xml:id="${note_id}">${tag_content}</term>`);
          var gloss_tag = `\n<noteGrp>\n\t<gloss target="${note_id}" lang="${lang}">${gloss}</gloss>\n</noteGrp>\n`;
          if (!text || text == '') {
            skip_tag = true;
          }
        } else {
          let content = `<seg type="brace" target="${note_id}" rend="${rend}">`;
          let lines = tag_content.split('\n');
          lines.forEach((line) => {
            content += `\n\t${line}`;
          })
          content += '\n</seg>';
          xmleditor.session.replace(insert_range, content);
        }

        insert_point = { row: xmleditor.session.getLength(), column: 0 };
        tag_content = text;
        type = 'sc';

        if (typeof gloss_tag != 'undefined') {
          xmleditor.session.insert(insert_point, gloss_tag);
          insert_point = { row: insert_point.row + 1, column: 0 };
          prefix = '\t';
        }
  
      } else if (tag_attributes.type == 'marginal') {
        prefix = ' ';
        tag_content = text;
      }
    }

    if (item_data.tag == 'table') {
      let rend_attr = attributes.rend ? attributes.rend.filter((attr) => !['hor_header', 'vert_header'].includes(attr)) : null;
      let row_count = attributes.rows ? attributes.rows : 3;
      let col_count = attributes.cols ? attributes.cols : 3;
      let body = '';

      if (tag_content) {
        tag_content = tag_content.trim();
        let lines = tag_content.split('\n');
        let splitter = ',';
        row_count = lines.length;

        lines.forEach((line, i) => {
          if (i == 0) { splitter = line.includes('\t') ? '\t' : ','; }
          let row = i == 0 && attributes.rend.includes('hor_header') ? '\t<row role="label">\n' : '\t<row role="data">\n';
          let cols = line.split(splitter);
          if (i == 0) { col_count = cols.length; }

          cols.forEach((col, j) => {
            if (j == 0 && attributes.rend.includes('vert_header')) {
              row += `\t\t<cell role="label">${col.trim()}</cell>\n`;
            } else {
              row += `\t\t<cell>${col.trim()}</cell>\n`;
            }
          })

          row += '\t</row>\n';
          body += row;
        })
        
      } else {
        for (let i = 0; i < row_count; i++) {
          let row = i == 0 ? '\t<row role="label">\n' : '\t<row role="data">\n';
          let cell_str = i == 0 ? 'HEADER' : 'VALUE';
          for (let j = 0; j < col_count; j++) { 
            row += `\t\t<cell>${cell_str} ${j + 1}</cell>\n`;
          }
          row += '\t</row>\n';
          body += row;
        }
      }

      tag_content = `\n${body}`;
      tag_attributes = { rows: row_count, cols: col_count };
      prefix = '\n';

      if (rend_attr) {
        tag_attributes['rend'] = rend_attr.join(' ');
      }
    }

    if (tag_attributes == null && Object.keys(attributes).length) { 
      tag_attributes = attributes; 
    }

    if (tag_attributes && Object.keys(tag_attributes).length) {
      for (const prop in tag_attributes) {
        if (tag_attributes[prop] != '' && tag_attributes[prop] != 'Join') {
          let vals = Array.isArray(tag_attributes[prop]) ? tag_attributes[prop].join(' ') : tag_attributes[prop];
          tag_output += ` ${prop}="${vals}"`;
        }
        if (tag_attributes[prop] == 'hr') { prefix = '\n'; }
      }
    }

    tag_output = tag_content != null ? `${tag_output}>${tag_content}</${item_data.tag}>` : `${tag_output} />`;
    if (prefix) { tag_output = `${prefix}${tag_output}`; }
    if (suffix) { tag_output = `${tag_output}${suffix}`; }

    if (!skip_tag) {
      if (type == 'w') {
        xmleditor.session.replace(insert_range, tag_output);
      } else {
        xmleditor.session.insert(insert_point, tag_output);
      }
    }
}

function setupTeiRendering() {
  $('#editor').scrollTop(0);

  if ($('tei-seg[type=brace]').length) {
    hasBraces = true;
    formatBraces(); 
  }
  if ($('tei-ref').length) { 
    formatRenvois(); 
  }
  if ($('tei-gloss').length) { 
    formatGlosses(); 
  }
  if ($('tei-ab[type=column]').length) { 
    hasColumns = true;
    formatColumns(); 
  }
  if ($('tei-metamark[function=leader]').length) { 
    hasLeaders = true;
    formatLeaders();
  }
  if ($('tei-note[type=marginal]').length) {
    hasMarginalNotes = true;
    formatMarginalNotes();
  }

  // eliminate residual tei-lbs at end of document
  $('tei-lb').last().prevUntil(':not(tei-lb)', 'tei-lb').remove();
  
  $('[data-toggle="tooltip"]').tooltip();
  
  $(document).on('click', '.popover-header-closer', function(e) {
    e.preventDefault();
    e.stopPropagation();
    $(e.target).parent().parent().popover('hide');
  });
}

function updateTeiRendering() {
  if (noteBarOn) {
    $('#notebar').height($('#editor').outerHeight());
    $('#notebar').css({ top: `${Math.round($('#editor-toolbar').position().top + 30)}px`});
    $('.notes_container').height(Math.round($('#tei-container').outerHeight()));
    positionMarginalNotes();
  }
}

function resetTeiRendering() {
  $('[data-toggle="tooltip"]').tooltip('dispose');
  if (hasMarginalNotes) {
    toggleNotebar();
    hasMarginalNotes = false;
  }
  if (hasColumns) {
    hasColumns = false;
    $(document).off('click', '.ab-column-toggler');
  }
  hasBraces = false;
  hasLeaders = false;
  $('#editor').empty();
}

function toggleNotebar() {
  if (noteBarOn) {
    // turn off
    $('.notes_container').empty();
    $('#editor').off('scroll');
    $('#notebar').off('scroll wheel');
    $('#notebar').hide();
    noteBarOn = false;
  } else {
    // turn on
    $('#notebar').show();
    $('#notebar').height($('#editor').outerHeight());
    $('#notebar').css({ top: `${Math.round($('#editor-toolbar').position().top + 30)}px`});
    $('.notes_container').height(Math.round($('#tei-container').outerHeight()));
    positionMarginalNotes();
    $('#editor').on('scroll', function (e) {
      $('#notebar').scrollTop($(this).scrollTop());
    });
    $('#notebar').on('scroll wheel', function(e) {
      e.preventDefault();
      e.stopPropagation();
      return false;
    });
    noteBarOn = true;
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

function formatColumns() {
  $(document).on('click', '.ab-column-toggler', (e) => {
      const parent = e.target.closest('tei-ab');
      parent.classList.toggle('closed');
  });
}

function formatLeaders() {
  $('tei-metamark[function=leader]:not([rend=ellipsis])').each(function(index, el) {
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

    const wrapper = $('<div class="tei-leader-line"></div>');
    const post = $('<div></div>');
    const anchor = $(next_array[next_array.length - 1]).next();
    post.append(next_array);
    wrapper.append(prev_array);
    wrapper.append($(this));
    wrapper.append(post);
    wrapper.insertBefore(anchor);
  });
}

function positionMarginalNotes() {
  let sum_height = 0;
  const rest = $('#tei-container').offset().top;
  $('tei-note[type=marginal]').each(function(index, el) {
    let anchor_top = $(`#${$(el).attr("data-anchor")}`).offset().top;
    let note_height = $(el).height();
    $(el).css({ top: `${anchor_top - rest - sum_height}px`});
    sum_height += note_height;
  });
}

function formatMarginalNotes() {
  $('tei-note[type=marginal]').each(function(index, el) {
    const note_id = Math.ceil(Math.random()*10000);
    const anchor = $(`<div class="note-anchor" id="${note_id}"></div>`);
    const anchor_target = $(el).prev().length ? $(el).prev() : $(el);
    anchor.insertBefore(anchor_target);
    $(el).attr("data-anchor", note_id);
    $(el).attr("data-height", Math.round($(el).outerHeight(true)));
    $('.notes_container').append($(el).remove());
  });
  toggleNotebar();
}

function formatBraces() {
  $('tei-seg[type=brace]').each(function(index, el) {
    let target = $(this).attr('target');
    if (target) {
      if (target.length > 1 && target.startsWith('#')) target = target.substring(1);
      $(this).append($(`tei-note#${target}`).remove());
    }
  });
  $('tei-note[type=brace]').popover({
    container: 'body',
    trigger: 'click',
    html: true,
    sanitize: false,
  });
}

function formatRenvois() {
  $('tei-ref').each( function(index, el) {
    let note_id = $(this).attr('target');
    if (note_id.length > 1 && note_id.startsWith('#')) note_id = note_id.substring(1);
    let note_el = $(`tei-note[id='${note_id}']`);
    let note = note_el.html();
    note = note.replaceAll('tei-a', 'a');
    note = note.replaceAll('⚭', '<i class="fas fa-link"></i>');

    if (note.length) {
        $(this).attr({
          'title': 'Note',
          'data-content': note,
          'data-toggle': 'popover',
          'data-template': '<div class="popover" role="tooltip"><div class="arrow"></div><div class="popover-header-wrapper"><h3 class="popover-header"></h3><div class="popover-header-closer"></div></div><div class="popover-body"></div></div>',
          'tabindex': '0',
        });
        note_el.remove();
      }
    });
    $('tei-ref').popover({
      container: 'body',
      trigger: 'click',
      html: true,
      sanitize: false,
    });
}

function formatGlosses() {
  const termList = {};
  $('tei-gloss').each(function(index, el) {
    const term_id = $(this).attr('target');
    if (!(term_id in termList)) {
      termList[term_id] = { 
        glosses: [],
        noteGrp: $(this).parent(), 
      }; 
    }
    termList[term_id].glosses.push({
      lang: $(this).attr('lang'),
      gloss: $(this).html()
    });
  });

  for (const termId in termList) {
    let note_el = $(`tei-note[id='${termId}']`);
    let note = note_el.length ? note_el.html() : '';
    let body = '<div class="gloss-container">';
    for (const gloss of termList[termId].glosses) {
      body = body + `<div class="inline-gloss"><div class="gloss-lang">${gloss.lang}</div>\
      <div class="gloss-text">${gloss.gloss}</div></div>`;
    }

    if (note.length) {
      note = note.replaceAll('tei-a', 'a');
      note = note.replaceAll('⚭', '<i class="fas fa-link"></i>');
      body = body + `<div class="inline-gloss-note">${note}</div>`;
    }

    body = body + '</div>';

    $(`tei-term[id='${termId}']`).attr({
      'title': 'Gloss',
      'data-content': body,
      'data-toggle': 'popover',
      'data-template': '<div class="popover" role="tooltip"><div class="arrow"></div><div class="popover-header-wrapper"><h3 class="popover-header"></h3><div class="popover-header-closer"></div></div><div class="popover-body"></div></div>',
      'tabindex': '0',
    });
    termList[termId].noteGrp.remove();
  }
  $('tei-term').popover({
    container: 'body',
    trigger: 'click',
    html: true,
    sanitize: false,
  });
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
