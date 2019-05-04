function initializeHelper(editor) {
  editor.on('open', function( e, mode, action ) { changeForm(e, action) });
  editor.on('close', function( e ) { changeForm(e) });
  password_state = 'divs';
}

function changeForm(e, action) {
  if (e.type == 'open') {
    if (action == 'edit') {
      togglePasswordButton(e);
    } else if (action == 'create') {
      //add listeners
      $(dt_editor.field('user.last_name').node()).find('input').on('change', function() { suggestFullname() });
      $(dt_editor.field('user.email').node()).find('input').on('change', function() { suggestUsername() });
    }
  } else if (e.type == 'close') {
    togglePasswordButton(e);
  }
}

function togglePasswordButton(e) {
  var container = $(dt_editor.field('user.password').node());
  var label = $(container).find('label');
  var button = '<div class="col-lg-8"><button class="btn btn-light" type="button" id="reset_password">Reset password</button></div>';
  if (e.type == 'open' && typeof divs == 'undefined') { divs = $(container).children('div') };
  if (e.type == 'open') {
    $(divs).remove();
    $(label).after(button);
    password_state = 'button';
  } else if (e.type == 'close') {
    if ( password_state == 'button' ) {
      $(container).find('button').remove();
      $(label).after(divs);
    }
  }
}

function suggestFullname() {
  var first_name = $(dt_editor.field('user.first_name').node()).find('input').val();
  var last_name = $(dt_editor.field('user.last_name').node()).find('input').val();
  if (first_name != '' && last_name != '') {
    var suggestion = first_name+' '+last_name;
    $(dt_editor.field('full_name').node()).find('input').val(suggestion);
  }
}

function suggestUsername() {
  var email = $(dt_editor.field('user.email').node()).find('input').val();
  if (email != '' && email.includes("@")) {
    var suggestion = email.split("@")[0];
    $(dt_editor.field('user.username').node()).find('input').val(suggestion);
  }
}
