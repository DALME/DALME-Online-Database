function ownership_filter_module_load() {

}

function ownership_filter_module_init() {
  mode = user_prefs.list_scope;
  let buttons = [
    ["own", "Show own records", "fa-user"],
    ["team", "Show team records", "fa-user-friends"],
    ["all", "Show all non-private records", "fa-users"]
  ]
  var container = $('<div class="dt-extra-buttons btn-group mr-1" id="ownership_filter"></div>');
  for (let i = 0, len = buttons.length; i < len; ++i) {
    let active = buttons[i][0] == mode ? 'active' : '';
    $(container).append(`<button class="btn buttons-collection ${active}" data-of-mode="${buttons[i][0]}"\
    title="${buttons[i][1]}" data-toggle="tooltip"><i class="fas ${buttons[i][2]} fa-sm"></i></button>`);
  };
  container.insertBefore('#dataTables-list_filter');
  $(container).find('[data-toggle="tooltip"]').tooltip({container: 'body', trigger: 'hover'});
  $(container).on('click.dalme', 'button', function() {
      if (!$(this).hasClass('active')) {
        $(container).find('.active').removeClass('active');
        mode = $(this).data('of-mode');
        update_session({ 'list_scope': mode });
        dt_table.ajax.reload();
        $(this).addClass('active');
      }
  });
}
