function corpus_filter_module_load() {

}

function corpus_filter_module_init() {
  var container = $('<div class="dt-extra-buttons btn-group mr-1" id="corpus_filter"></div>');
  $(container).append('<button class="btn buttons-collection active" data-cf-mode="own" title="Show own sources" data-toggle="tooltip">\
  <i class="fas fa-user fa-sm"></i></button>');
  $(container).append('<button class="btn buttons-collection" data-cf-mode="team" title="Show team sources" data-toggle="tooltip">\
  <i class="fas fa-user-friends fa-sm"></i></button>');
  $(container).append('<button class="btn buttons-collection" data-cf-mode="all" title="Show all non-private sources" data-toggle="tooltip">\
  <i class="fas fa-users fa-sm"></i></button>');
  container.insertBefore('#dataTables-list_filter');
  $(container).find('[data-toggle="tooltip"]').tooltip({container: 'body', trigger: 'hover'});
  $(container).on('click.dalme', 'button', function() {
      if ($(this).hasClass('active')) {
        filter_set({'mode': ''}, options=['clear']);
        $(this).removeClass('active');
      } else {
        $(container).find('.active').removeClass('active');
        filter_set({'mode': $(this).data('cf-mode')});
        $(this).addClass('active');
      }
  });
}
