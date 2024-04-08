// $(document.body).on('click', 'a.TooltipEntity[data-draftail-trigger]', function(e) {
//   let id = $(this).attr('href').split('/').reverse()[1];
//   if (id[0] == '#') id = id.slice(1);
//   window.EditorLastEntityID = id;
// });

// $(document.body).on('hidden.bs.modal', function(e) {
//   window.EditorLastEntityID = null;
// });

window.CustomUtils = {
  getUUID: () => {
    return ([1e7] + -1e3 + -4e3 + -8e3 + -1e11).replace(/[018]/g, (c) =>
      (c ^ (crypto.getRandomValues(new Uint8Array(1))[0] & (15 >> (c / 4)))).toString(16)
    );
  },
  stripTags: (html, alt) => {
    if (!alt) alt = "";
    const el = document.createElement("div");
    el.innerHTML = html;
    return el.textContent || tmp.innerText || alt;
  },
  getCookie: (name) => {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) == (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  },
  updateSession: (data) => {
    $.ajax({
      method : "POST",
      url: "/api/session/alter/",
      xhrFields: { withCredentials: true },
      crossDomain: true,
      headers: {
        "Content-Type": "application/json",
        'X-CSRFToken': window.CustomUtils.getCookie("csrftoken")
      },
      data : JSON.stringify(data)
    });
  },
}
