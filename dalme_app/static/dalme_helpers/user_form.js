function user_form() {
  dt_editor.on('open.dalme', function( e, mode, action ) { change_form(e, action) });
  dt_editor.on('close.dalme', function( e ) { change_form(e) });
  password_state = 'divs';
}

function change_form(e, action) {
  if (e.type == 'open') {
    if (action == 'edit') {
      toggle_password_button(e);
      dt_editor.on('submitSuccess', function(e, json, data, action) { toastr.success('The user was updated succesfully.') });
    } else if (action == 'create') {
      dt_editor.on('submitSuccess', function(e, json, data, action) { toastr.success('The user was created succesfully.') });
      $(dt_editor.field('user.last_name').node()).find('input').on('change.dalme', function() { suggest_fullname() });
      $(dt_editor.field('user.email').node()).find('input').on('change.dalme', function() { suggest_username() });
    }
  } else if (e.type == 'close') {
        toggle_password_button(e);
        $(dt_editor.field('user.last_name').node()).find('input').off('change.dalme');
        $(dt_editor.field('user.email').node()).find('input').off('change.dalme');
  }
}

function toggle_password_button(e) {
  var container = $(dt_editor.field('user.password').node());
  var label = $(container).find('label');
  var button = '<div class="col-lg-8"><button class="btn btn-light ml-0" type="button" id="reset_password">Reset password</button></div>';
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

function suggest_fullname() {
  var first_name = $(dt_editor.field('user.first_name').node()).find('input').val();
  var last_name = $(dt_editor.field('user.last_name').node()).find('input').val();
  if (first_name != '' && last_name != '') {
    var suggestion = first_name+' '+last_name;
    $(dt_editor.field('full_name').node()).find('input').val(suggestion);
  }
}

function suggest_username() {
  var email = $(dt_editor.field('user.email').node()).find('input').val();
  if (email != '' && email.includes("@")) {
    var suggestion = email.split("@")[0];
    $(dt_editor.field('user.username').node()).find('input').val(suggestion);
  }
}
