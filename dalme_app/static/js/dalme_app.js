/* custom JavaScript functions used by dalme.app */
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function updateSession(data) {
    $.ajax({
      type : "POST",
      url : "/su/",
      headers : {'X-CSRFToken': getCookie('csrftoken') },
      dataType : "json",
      data : data
    });
}

function fullScreenMode(action) {
  if (action == 'on') {
    var elem = document.documentElement;
    if (elem.requestFullscreen) {
        elem.requestFullscreen();
      } else if (elem.mozRequestFullScreen) { /* Firefox */
        elem.mozRequestFullScreen();
      } else if (elem.webkitRequestFullscreen) { /* Chrome, Safari and Opera */
        elem.webkitRequestFullscreen();
      } else if (elem.msRequestFullscreen) { /* IE/Edge */
        elem.msRequestFullscreen();
      };
    document.getElementById('fullScreenToggle').innerHTML = '<a class="nav-link" href="#" role="button" onclick="fullScreenMode(\'off\')"><i class="fas fa-compress fa-g"></i></a>';
  } else {
    if (document.exitFullscreen) {
      document.exitFullscreen();
    } else if (document.mozCancelFullScreen) { /* Firefox */
      document.mozCancelFullScreen();
    } else if (document.webkitExitFullscreen) { /* Chrome, Safari and Opera */
      document.webkitExitFullscreen();
    } else if (document.msExitFullscreen) { /* IE/Edge */
      document.msExitFullscreen();
    };
    document.getElementById("fullScreenToggle").innerHTML = '<a class="nav-link" href="#" role="button" onclick="fullScreenMode(\'on\')"><i class="fas fa-expand fa-g"></i></a>';
  }
}

function setupTranscriber() {
    initial_folio = '/pages/'+folio_list[0].id+'/manifest';
    diva = new Diva('diva_viewer', {
        objectData: initial_folio,
        //objectData: '{{ request.build_absolute_uri }}manifest',
        enableAutoTitle: false,
        enableFullscreen: false,
        //enableKeyScroll: false,
        //blockMobileMove: false,
        enableGotoPage: false,
        enableGridIcon: false,
        enableImageTitles: false,
        //plugins: [Diva.DalmePlugin],
    });

    xmleditor = ace.edit("xml_editor");
    xmleditor.setOptions({
        theme: "ace/theme/chrome",
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
        indentedSoftWrap: true
        //following options require ext-language_tools.js
        //enableBasicAutocompletion: true,
        //enableLiveAutocompletion: true,
    });
    xmleditor.session.setValue(getTranscription(folio_list[0].tr_id));

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

      window.addEventListener('resize', function ()
        {
          xmleditor.resize();
        }, false);
}

function getTranscription(pk) {
  if (pk != 'None') {
    url = "/api/transcriptions/"+pk
    return $.get(url);
  } else {
    return ''
  }
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

function folioSwitch (target) {
  //use global folio dictionary to get required values
  total = folio_list.length;
  prev = prevFolio(getFolioIndex(target));
  next = nextFolio(getFolioIndex(target));
  goto_index = getFolioIndex(target)
  current_index = goto_index - 1
  count = goto_index + 1
  goto = folio_list[goto_index];
  //save state of ACE IF IN EDIT MODE
  //current_tr = xmleditor.getValue(); // or session.getValue
  //folio_list[current_index].tr = current_tr;
  //send message to diva.js to reload with new object data
  manifest = '/pages/'+goto.id+'/manifest';
  diva.changeObject(manifest);
  $(window).trigger('resize');
  //send message to ACE to switch to new transcription data
  //xmleditor.session.setValue(getTranscription(goto.tr_id)); // set value and reset undo history

  //change interface elements
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
