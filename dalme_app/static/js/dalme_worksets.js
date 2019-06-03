function init_worksets() {
    let gap_start = workset['progress']-2;
    let gap_end = workset['progress']+2;
    let prop = 'linear-gradient(to right, #e3f0f5, #e3f0f5 '+gap_start+'%, #ffffff '+gap_end+'%, #ffffff'
    $('.workset-controller-status').css({ background: prop });
    if (workset['prev_id'] == 'none') {
        $('.workset-controller-prev').addClass('disabled');
    };
    if (workset['next_id'] == 'none') {
        $('.workset-controller-next').addClass('disabled');
    }
}

function ws_next() {
  if (workset['next_id'] != 'none') {
    $.ajax({
      method: "GET",
      url: "/api/worksets/"+workset['workset_id']+"/set_state/?action=mark_done&seq="+workset['current'],
    }).done(function(data, textStatus, jqXHR) {
        let next_seq = parseInt(workset['current'])+1;
        let url = '/'+workset['endpoint']+'/'+workset['next_id']+'/?workset='+workset['workset_id']+'&seq='+next_seq;
        window.location.href = url;
    }).fail(function(jqXHR, textStatus, errorThrown) {
        show_message('danger', 'There was an error communicating with the server: '+errorThrown);
    });
  }
}

// function ws_next() {
//   if (workset['next_id'] != 'none') {
//       ws_mark('mark_done');
//       let next_seq = parseInt(workset['current'])+1;
//       let url = '/'+workset['endpoint']+'/'+workset['next_id']+'/?workset='+workset['workset_id']+'&seq='+next_seq;
//       window.location.href = url;
//   }
// }

function ws_prev() {
  if (workset['prev_id'] != 'none') {
      let prev_seq = parseInt(workset['current'])-1;
      let url = '/'+workset['endpoint']+'/'+workset['prev_id']+'/?workset='+workset['workset_id']+'&seq='+prev_seq;
      window.location.href = url;
  }
}

function ws_mark(action) {
  $.ajax({
    method: "GET",
    url: "/api/worksets/"+workset['workset_id']+"/set_state/?action="+action+"&seq="+workset['current'],
  }).fail(function(jqXHR, textStatus, errorThrown) {
    show_message('danger', 'There was an error communicating with the server: '+errorThrown);
  });
}

function ws_show_list() {

}
