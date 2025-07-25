document.addEventListener("DOMContentLoaded", () => {
  var texts = document.querySelectorAll("label.text, button.text");
  texts.forEach((text, i) => {
    text.addEventListener("click", () => {
      location= `${location.toString().replace("/Home", `/${text.innerHTML}`)}`;
    });
  });
})
