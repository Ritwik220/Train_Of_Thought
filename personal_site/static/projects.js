function jumpSite() {
  const projects = document.querySelectorAll(".card");

  projects.forEach(project => {
    const url = project.querySelector(".name .text").getAttribute("site").toString();

    project.addEventListener("click", () => {
      if (url) {
        location = location.toString().replace("Projects", url);
      }
    });
  });
  const names = document.querySelectorAll("nav label");
  names.forEach(name => {
    name.addEventListener("click", () => {
      if (name.innerHTML){
        location = location.toString().replace("Projects", name.innerHTML)
      }
    })
  })
}

document.addEventListener("DOMContentLoaded", jumpSite);