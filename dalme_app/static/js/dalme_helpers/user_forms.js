function user_forms_load() {

}

function user_forms_init() {
  dt_editor.on('submitSuccess.dalme', function(e, json, data, action) { location.reload(); });
}

function change_form(e, mode, action) {
  if (e.type == 'open') {
    if (action == 'edit') {
      toggle_password_button(e);
    }
    if (action == 'create') {
      dt_editor.field('last_name').input().on('change.dalme', suggest_fullname);
      dt_editor.field('email').input().on('change.dalme', suggest_username);
    }
  } else if (e.type == 'close') {
        toggle_password_button(e);
        dt_editor.field('last_name').input().off('change.dalme');
        dt_editor.field('email').input().off('change.dalme');
  }
}

function reset_password() {
  var conf = confirm("Are you sure you wish to reset this user's password?");
  if (conf == true) {
    var user_id = dt_editor.ids()[0];
    dt_editor.close();
    $.ajax({
      method: "POST",
      url: "/api/users/"+user_id+"/reset_password/",
      headers: {
        "Content-Type": "application/json",
        'X-CSRFToken': get_cookie("csrftoken")
      },
    }).done(function(data, textStatus, jqXHR) {
      toastr.success('An email with instructions was sent to the user.');
    }).fail(function(jqXHR, textStatus, errorThrown) {
      toastr.error('There was an error communicating with the server: '+errorThrown);
    });
  }
}

function toggle_password_button(e) {
  var container = $(dt_editor.field('password').node());
  var label = $(container).find('label');
  var button = '<div><button class="btn btn-light ml-0" type="button" id="reset_password">Reset password</button></div>';
  if (e.type == 'open' && typeof divs == 'undefined') { divs = $(container).children('div') };
  if (e.type == 'open') {
    $(divs).remove();
    $(label).after(button);
    password_state = 'button';
    $('#reset_password').on('click.dalme', reset_password);
  } else if (e.type == 'close') {
    if ( password_state == 'button' ) {
      $('#reset_password').off('click.dalme');
      $(container).find('button').remove();
      $(label).after(divs);
    }
  }
}

function suggest_fullname() {
  var first_name = dt_editor.field('first_name').val()
  var last_name = dt_editor.field('last_name').val()
  if (first_name != '' && last_name != '') {
    var suggestion = first_name+' '+last_name;
    dt_editor.field('profile.full_name').val(suggestion)
  }
}

function suggest_username() {
  var email = dt_editor.field('email').val()
  if (email != '' && email.includes("@")) {
    var suggestion = email.split("@")[0];
    dt_editor.field('username').val(suggestion)
  }
}
