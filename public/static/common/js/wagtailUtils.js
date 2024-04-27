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
  toggleHamburger: (el) => {
    const menu = el.closest("nav").querySelector("ul");
    menu.classList.toggle("u-flex");
    menu.classList.toggle("u-none");
  },
  toggleLightbox: (el) => {
    document.querySelector(".lightbox-image").src = el.querySelector("img").src;
    document.querySelector(".lightbox-caption").innerHTML = el.querySelector(".caption").innerHTML;
    document.getElementById("lightbox").modal("show");
  },
  toggleSection: (el) => {
    const icon = el.querySelector("i");
    icon.classList.toggle("fa-caret-up");
    icon.classList.toggle("fa-caret-down");
    el.setAttribute(
      "data-collapsed",
      el.getAttribute("data-collapsed") === "true" ? "false" : "true",
    );
    el.nextElementSibling.classList.toggle("u-none");
  },
}
