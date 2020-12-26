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
      method: "PATCH",
      url: `${api_endpoint}/sets/${workset['workset_id']}/workset_state/`,
      xhrFields: { withCredentials: true },
      crossDomain: true,
      headers: {
        "Content-Type": "application/json",
        'X-CSRFToken': get_cookie("csrftoken")
      },
      data: JSON.stringify({ "action": "mark_done", "target": workset['current_id']})
    }).done(function(data, textStatus, jqXHR) {
        let url = `${api_endpoint}/${workset['endpoint']}/${workset['next_id']}/?set=${workset['workset_id']}`
        window.location.href = url;
    }).fail(function(jqXHR, textStatus, errorThrown) {
      if (errorThrown == "Forbidden") {
        toastr.error("You do not have the required permissions to change the state of this workset.");
      } else {
        toastr.error('There was an error communicating with the server: '+errorThrown);
      }
    });
  }
}

function ws_prev() {
  if (workset['prev_id'] != 'none') {
      let url = `${api_endpoint}/${workset['endpoint']}/${workset['prev_id']}/?set=${workset['workset_id']}`;
      window.location.href = url;
  }
}

function ws_mark(action) {
  $.ajax({
    method: "PATCH",
    url: `${api_endpoint}/sets/${workset['workset_id']}/workset_state/`,
    xhrFields: { withCredentials: true },
    crossDomain: true,
    headers: {
      "Content-Type": "application/json",
      'X-CSRFToken': get_cookie("csrftoken")
    },
    data: JSON.stringify({ "action": action, "target": workset['current_id']})
  }).fail(function(jqXHR, textStatus, errorThrown) {
    if (errorThrown == "Forbidden") {
      toastr.error("You do not have the required permissions to change the state of this workset.");
    } else {
      toastr.error('There was an error communicating with the server: '+errorThrown);
    }
  });
}

function ws_show_list() {
  let url = `${api_endpoint}/${workset['endpoint']}/?set=${workset['workset_id']}`;
  window.location.href = url;
}
