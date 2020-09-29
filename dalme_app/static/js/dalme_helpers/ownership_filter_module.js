function ownership_filter_module_load() {

}

function ownership_filter_module_init() {
  var container = $('<div class="dt-extra-buttons btn-group mr-1" id="ownership_filter"></div>');
  $(container).append('<button class="btn buttons-collection active" data-of-mode="own" title="Show own records" data-toggle="tooltip">\
  <i class="fas fa-user fa-sm"></i></button>');
  $(container).append('<button class="btn buttons-collection" data-of-mode="team" title="Show team records" data-toggle="tooltip">\
  <i class="fas fa-user-friends fa-sm"></i></button>');
  $(container).append('<button class="btn buttons-collection" data-of-mode="all" title="Show all non-private records" data-toggle="tooltip">\
  <i class="fas fa-users fa-sm"></i></button>');
  container.insertBefore('#dataTables-list_filter');
  $(container).find('[data-toggle="tooltip"]').tooltip({container: 'body', trigger: 'hover'});
  $(container).on('click.dalme', 'button', function() {
      if (!$(this).hasClass('active')) {
        $(container).find('.active').removeClass('active');
        filter_set({'mode': $(this).data('of-mode')});
        $(this).addClass('active');
      }
  });
}
