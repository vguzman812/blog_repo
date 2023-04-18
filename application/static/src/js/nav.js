// Check if user has previously chosen a theme
let theme = localStorage.getItem('theme');
let links = document.querySelectorAll('.light-theme-toggler, .dark-theme-toggler');
let btns = document.querySelectorAll('.btn-outline-light, .btn-outline-dark');
let navs = document.querySelectorAll('.navbar-dark, .navbar-light');
let dropdowns = document.querySelectorAll('.dropdown-menu-dark, .dropdown-menu-light');




if(theme === null) {
  // Default theme is light
  theme = 'light';
  localStorage.setItem('theme', theme);
}

// Set initial theme
document.documentElement.setAttribute('data-theme', theme);

// Toggle theme function
function toggleTheme() {
  if(theme === 'light') {
    theme = 'dark';
  } else {
    theme = 'light';
  }
  localStorage.setItem('theme', theme);
  document.documentElement.setAttribute('data-theme', theme);

  // Disable the link with the current theme
  links.forEach(link => {
    if (link.innerText.toLowerCase() === theme) {
      link.classList.add("disabled", "text-decoration-line-through");
    } else {
      link.classList.remove("disabled", "text-decoration-line-through");
    }
  });
  //  Toggle btn themes
  btns.forEach(btn => {
    if (btn.classList.contains("btn-outline-light")) {
      btn.classList.add("btn-outline-dark");
      btn.classList.remove("btn-outline-light")
    } else {
      btn.classList.add("btn-outline-light");
      btn.classList.remove("btn-outline-dark")    }
  });
  navs.forEach(nav => {
    if (nav.classList.contains("navbar-dark")) {
      nav.classList.add("navbar-light");
      nav.classList.remove("navbar-dark")
    } else {
      nav.classList.add("navbar-dark");
      nav.classList.remove("navbar-light")    }
  });

  dropdowns.forEach(dropdown => {
    if (dropdown.classList.contains("dropdown-menu-dark")) {
      dropdown.classList.add("dropdown-menu-light");
      dropdown.classList.remove("dropdown-menu-dark")
    } else {
      dropdown.classList.add("dropdown-menu-dark");
      dropdown.classList.remove("dropdown-menu-light")    }
  });
}

// Add event listeners to theme toggler links
document.querySelectorAll('.light-theme-toggler, .dark-theme-toggler').forEach(link => {
  link.addEventListener('click', toggleTheme);
});

// Disable the link with the current theme on page load
document.querySelectorAll('.light-theme-toggler, .dark-theme-toggler').forEach(link => {
  if (link.innerText.toLowerCase() === theme) {
    link.classList.add("disabled");
  }
});