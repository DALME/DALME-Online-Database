function get_cookie(name) {
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
}

function update_session(data) {
    $.ajax({
      method : "POST",
      url: `${api_endpoint}/session/alter/`,
      xhrFields: { withCredentials: true },
      crossDomain: true,
      headers: {
        "Content-Type": "application/json",
        'X-CSRFToken': get_cookie("csrftoken")
      },
      data : JSON.stringify(data)
    });
}

function remove_param(key, sourceURL) {
    if (!Array.isArray(key)) {
      key = [key]
    }
    var rtn = sourceURL.split("?")[0],
        param,
        params_arr = [],
        queryString = (sourceURL.indexOf("?") !== -1) ? sourceURL.split("?")[1] : "";
    if (queryString !== "") {
        params_arr = queryString.split("&");
        for (let i = 0, len = key.length; i < len; ++i) {
          for (let j = params_arr.length - 1; j >= 0; j -= 1) {
              param = params_arr[j].split("=")[0];
              if (param === key[i]) {
                  params_arr.splice(j, 1);
              }
          }
        }
        rtn = rtn + "?" + params_arr.join("&");
    }
    return rtn;
}

function get_params(sourceURL) {
    var params = {};
    var parts = sourceURL.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {
        params[key] = value;
    });
    return params;
}
