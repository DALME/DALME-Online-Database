$(document.body).on('click', 'a.TooltipEntity[data-draftail-trigger]', function(e) {
  let id = $(this).attr('href').split('/').reverse()[1];
  if (id[0] == '#') id = id.slice(1);
  window.dalmeLastEntityID = id;
});

$(document.body).on('hidden.bs.modal', function(e) {
  window.dalmeLastEntityID = null;
});
