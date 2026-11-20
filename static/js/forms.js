/**
 * PTVTI FORM VALIDATION & ENHANCEMENTS
 */

document.addEventListener('DOMContentLoaded', () => {
  // Validate file upload size (< 5MB)
  const fileInputs = document.querySelectorAll('input[type="file"][data-max-size-mb]');
  fileInputs.forEach((input) => {
    input.addEventListener('change', () => {
      const maxMb = parseFloat(input.getAttribute('data-max-size-mb')) || 5;
      const maxBytes = maxMb * 1024 * 1024;
      if (input.files && input.files[0]) {
        if (input.files[0].size > maxBytes) {
          alert(`Selected file exceeds the maximum allowed size of ${maxMb}MB.`);
          input.value = '';
        }
      }
    });
  });

  // Visual disable on submit to prevent duplicate submissions
  const forms = document.querySelectorAll('form[data-prevent-duplicate]');
  forms.forEach((form) => {
    form.addEventListener('submit', () => {
      const submitBtn = form.querySelector('button[type="submit"]');
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>Processing...';
      }
    });
  });
});
