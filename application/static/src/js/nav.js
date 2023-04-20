// Check if user has previously chosen a theme
let theme = localStorage.getItem('theme');
let themeTogglers = document.querySelectorAll('.light-theme-toggler, .dark-theme-toggler');
let navs = document.querySelectorAll('.navbar');
let dropdowns = document.querySelectorAll('.dropdown-menu');




if(theme === null) {
  // Default theme is light
  theme = 'light';
  localStorage.setItem('theme', theme);
}

// Set the theme on page load
document.documentElement.setAttribute('data-theme', theme);

// Set initial theme
document.documentElement.setAttribute('data-theme', theme);
if(theme ==='light') {
    // Add navbar settings
    navs.forEach(nav => {
        nav.classList.add("navbar-light");
    });
    dropdowns.forEach(dropdown => {
      dropdown.classList.add("dropdown-menu-light");
      dropdown.classList.remove("dropdown-menu-dark")
    });
}
if(theme ==='dark') {
    // Add navbar settings
    navs.forEach(nav => {
        nav.classList.add("navbar-dark");
    });
    dropdowns.forEach(dropdown => {
      dropdown.classList.add("dropdown-menu-dark");
      dropdown.classList.remove("dropdown-menu-light")
    });
}

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
  themeTogglers.forEach(link => {
    if (link.innerText.toLowerCase() === theme) {
      link.classList.add("disabled", "text-decoration-line-through");
    } else {
      link.classList.remove("disabled", "text-decoration-line-through");
    }
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

// Add event listeners to theme toggler themeTogglers
document.querySelectorAll('.light-theme-toggler, .dark-theme-toggler').forEach(link => {
  link.addEventListener('click', toggleTheme);
});

// Disable the link with the current theme on page load
document.querySelectorAll('.light-theme-toggler, .dark-theme-toggler').forEach(link => {
  if (link.innerText.toLowerCase() === theme) {
    link.classList.add("disabled", "text-decoration-line-through");
  }
});

