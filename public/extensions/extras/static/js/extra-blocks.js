window.CustomUtils.toggleShowMore = (el) => {
  if (el.classList.contains("show-less")) {
    el.parentElement.style.maxHeight = "126px";
    el.classList.toggle("show-less");
  } else {
    el.parentElement.style.maxHeight = "1000px";
    el.classList.toggle("show-less");
  }
};

window.CustomUtils.toggleSection = (el) => {
  const icon = el.querySelector("i");
  icon.classList.toggle("fa-caret-up");
  icon.classList.toggle("fa-caret-down");
  el.setAttribute(
    "data-collapsed",
    el.getAttribute("data-collapsed") === "true" ? "false" : "true",
  );
  el.nextElementSibling.classList.toggle("u-none");
};

document.querySelectorAll(".text-expandable-container").forEach((el) => {
  if (el.scrollHeight > el.offsetHeight) {
    el.querySelector(".show-button").classList.toggle("u-none");
  }
});
