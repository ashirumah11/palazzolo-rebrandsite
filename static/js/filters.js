/**
 * PTVTI COURSE & CONTENT FILTERS
 * Instant client-side filtering for cards with data-department or data-search
 */

document.addEventListener('DOMContentLoaded', () => {
  const filterPills = document.querySelectorAll('.filter-pill[data-filter]');
  const cards = document.querySelectorAll('[data-filterable-card]');
  const searchInput = document.querySelector('[data-filter-search]');
  const emptyState = document.getElementById('filterEmptyState');

  let activeDepartment = 'all';
  let searchQuery = '';

  const applyFilters = () => {
    let visibleCount = 0;

    cards.forEach((card) => {
      const cardDept = (card.getAttribute('data-department') || '').toLowerCase();
      const cardText = (card.getAttribute('data-search-text') || card.textContent || '').toLowerCase();

      const matchesDept = (activeDepartment === 'all') || (cardDept === activeDepartment.toLowerCase());
      const matchesSearch = !searchQuery || cardText.includes(searchQuery.toLowerCase());

      if (matchesDept && matchesSearch) {
        card.style.display = '';
        visibleCount++;
      } else {
        card.style.display = 'none';
      }
    });

    if (emptyState) {
      emptyState.style.display = (visibleCount === 0) ? 'block' : 'none';
    }
  };

  if (filterPills.length) {
    filterPills.forEach((pill) => {
      pill.addEventListener('click', (e) => {
        e.preventDefault();
        filterPills.forEach((p) => p.classList.remove('active'));
        pill.classList.add('active');
        activeDepartment = pill.getAttribute('data-filter') || 'all';
        applyFilters();
      });
    });
  }

  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      searchQuery = e.target.value.trim();
      applyFilters();
    });
  }
});
