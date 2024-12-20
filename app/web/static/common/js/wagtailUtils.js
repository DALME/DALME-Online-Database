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
  goToLogin: async () => {
    const screenshot = document.documentElement.cloneNode(true);
    const reader = new FileReader();
    screenshot.style.pointerEvents = "none";
    screenshot.style.overflow = "hidden";
    screenshot.style.webkitUserSelect = "none";
    screenshot.style.mozUserSelect = "none";
    screenshot.style.msUserSelect = "none";
    screenshot.style.oUserSelect = "none";
    screenshot.style.userSelect = "none";
    screenshot.dataset.scrollX = window.scrollX;
    screenshot.dataset.scrollY = window.scrollY;
    screenshot.querySelector("[data-domain]").remove();
    screenshot.querySelectorAll("link").forEach((el) => el.href = el.href);
    screenshot.querySelectorAll("script").forEach((el) => el.src = el.src);
    screenshot.querySelectorAll("img").forEach((el) => el.src = el.src);
    screenshot.querySelectorAll("[style]").forEach((el) => {
      el.setAttribute("style", el.getAttribute("style").replace(/url\((.+)\)/gi, `url(${window.location.href}$1)`));
    });
    console.log(screenshot);
    const blob = new Blob([screenshot.outerHTML], { type: "text/html" });
    reader.readAsDataURL(blob);
    reader.onloadend = () => {
      window.localStorage.setItem("origin_background", reader.result);
      window.location.assign("/db/?next=/cms/");
    }
  },
}
