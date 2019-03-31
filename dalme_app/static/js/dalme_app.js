/* custom JavaScript functions used by dalme.app */
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function updateSession(data) {
    $.ajax({
      type : "POST",
      url : "/su/",
      headers : {'X-CSRFToken': getCookie('csrftoken') },
      dataType : "json",
      data : data
    });
}

function fullScreenMode(action) {
  if (action == 'on') {
    var elem = document.documentElement;
    if (elem.requestFullscreen) {
        elem.requestFullscreen();
      } else if (elem.mozRequestFullScreen) { /* Firefox */
        elem.mozRequestFullScreen();
      } else if (elem.webkitRequestFullscreen) { /* Chrome, Safari and Opera */
        elem.webkitRequestFullscreen();
      } else if (elem.msRequestFullscreen) { /* IE/Edge */
        elem.msRequestFullscreen();
      };
    document.getElementById('fullScreenToggle').innerHTML = '<a class="nav-link" href="#" role="button" onclick="fullScreenMode(\'off\')"><i class="fas fa-compress fa-g"></i></a>';
  } else {
    if (document.exitFullscreen) {
      document.exitFullscreen();
    } else if (document.mozCancelFullScreen) { /* Firefox */
      document.mozCancelFullScreen();
    } else if (document.webkitExitFullscreen) { /* Chrome, Safari and Opera */
      document.webkitExitFullscreen();
    } else if (document.msExitFullscreen) { /* IE/Edge */
      document.msExitFullscreen();
    };
    document.getElementById("fullScreenToggle").innerHTML = '<a class="nav-link" href="#" role="button" onclick="fullScreenMode(\'on\')"><i class="fas fa-expand fa-g"></i></a>';
  }
}
