/**
 * PTVTI NAVIGATION UTILITIES
 */

document.addEventListener('DOMContentLoaded', () => {
  // Highlight active menu item based on current location pathname
  const currentPath = window.location.pathname;
  const navLinks = document.querySelectorAll('.navbar-nav .nav-link');

  navLinks.forEach((link) => {
    const href = link.getAttribute('href');
    if (href && href !== '/' && currentPath.startsWith(href)) {
      link.classList.add('active');
    } else if (href === '/' && currentPath === '/') {
      link.classList.add('active');
    }
  });

  // Close mobile navbar collapse when clicking outside or pressing Escape
  const navCollapse = document.getElementById('ptvtiNavCollapse');
  if (navCollapse) {
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && navCollapse.classList.contains('show')) {
        const bsCollapse = bootstrap.Collapse.getInstance(navCollapse);
        if (bsCollapse) bsCollapse.hide();
      }
    });
  }

  // More Dropdown: Hover on desktop, click on mobile
  const moreDropdownToggle = document.getElementById('moreDropdown');
  if (moreDropdownToggle) {
    const moreDropdownMenu = moreDropdownToggle.nextElementSibling;

    // Desktop: open on hover
    const dropdownParent = moreDropdownToggle.parentElement;
    if (window.innerWidth >= 1200) {
      dropdownParent.addEventListener('mouseenter', () => {
        const bsDropdown = new bootstrap.Dropdown(moreDropdownToggle);
        bsDropdown.show();
      });
      dropdownParent.addEventListener('mouseleave', () => {
        const bsDropdown = bootstrap.Dropdown.getInstance(moreDropdownToggle);
        if (bsDropdown) bsDropdown.hide();
      });
    }

    // Mobile: toggle on click, close when clicking outside
    document.addEventListener('click', (e) => {
      if (!dropdownParent.contains(e.target) && !e.target.closest('.dropdown-menu')) {
        const bsDropdown = bootstrap.Dropdown.getInstance(moreDropdownToggle);
        if (bsDropdown) bsDropdown.hide();
      }
    });

    // Close dropdown on Escape key
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        const bsDropdown = bootstrap.Dropdown.getInstance(moreDropdownToggle);
        if (bsDropdown) bsDropdown.hide();
      }
    });
  }
});
