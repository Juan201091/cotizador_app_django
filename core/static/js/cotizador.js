document.addEventListener("DOMContentLoaded", function () {
  const loader = document.getElementById("loader");

  document.body.addEventListener("htmx:beforeRequest", () => {
    loader.style.display = "flex";
  });

  document.body.addEventListener("htmx:afterSwap", () => {
    loader.style.display = "none";
  });

  document.body.addEventListener("htmx:responseError", () => {
    loader.style.display = "none";
    alert("Ocurrió un error al procesar la solicitud.");
  });
});