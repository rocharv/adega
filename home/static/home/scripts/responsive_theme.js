if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
  setTheme("dark");
}
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', event => {
  const newTheme = event.matches ? "dark" : "light";
  setTheme(newTheme);
});

// const systemTheme = window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
// document.documentElement.setAttribute("data-bs-theme", systemTheme);
// // Adjust Bootstrap .shadow-sm if theme is dark to
// // --bs-box-shadow: 0 0.125rem 0.25rem rgba(255, 255, 255, 0.075);
// if (systemTheme === "dark") {
//   const shadowSm = document.querySelectorAll(".shadow");
//   shadowSm.forEach((el) => {
//     el.style.setProperty("--bs-box-shadow", "0 0.5em 1rem rgba(255, 255, 255, 0.075)");
//   });
// }


// // Additional code to listen for changes in the theme preference
// window.matchMedia("(prefers-color-scheme: dark)").addEventListener('change', event => {

// });

function setTheme(theme) {
  if (theme === "dark") {
    document.documentElement.setAttribute("data-bs-theme", "dark");
    const shadowSm = document.querySelectorAll(".shadow");
    shadowSm.forEach((el) => {
      el.style.setProperty("--bs-box-shadow", "0 0.5em 1rem rgba(255, 255, 255, 0.15)");
    });
  } else {
    document.documentElement.setAttribute("data-bs-theme", "light");
    const shadowSm = document.querySelectorAll(".shadow");
    shadowSm.forEach((el) => {
      el.style.setProperty("--bs-box-shadow", "0 0.5rem 1rem rgba(40, 0, 0, 0.15)");
    });
  }
}
