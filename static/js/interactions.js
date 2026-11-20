/**
 * PTVTI UI INTERACTIONS (Copy to clipboard, modal triggers)
 */

document.addEventListener('DOMContentLoaded', () => {
  // Copy to clipboard (e.g. for Application tracking reference)
  const copyButtons = document.querySelectorAll('[data-copy-target]');
  copyButtons.forEach((btn) => {
    btn.addEventListener('click', async () => {
      const targetId = btn.getAttribute('data-copy-target');
      const targetEl = document.getElementById(targetId);
      if (targetEl) {
        const text = targetEl.value || targetEl.textContent || '';
        try {
          await navigator.clipboard.writeText(text.trim());
          const originalText = btn.innerHTML;
          btn.innerHTML = '<i class="fas fa-check text-success me-1"></i> Copied!';
          setTimeout(() => {
            btn.innerHTML = originalText;
          }, 2500);
        } catch (err) {
          console.error('Clipboard copy failed:', err);
        }
      }
    });
  });
});
