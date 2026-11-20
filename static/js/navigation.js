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
});
