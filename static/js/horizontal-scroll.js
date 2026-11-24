/**
 * PTVTI Horizontal Scroll Controller
 * Provides smooth horizontal scrolling with custom scrollbar and navigation controls
 *
 * Usage:
 * <div class="horizontal-scroll-section">
 *   <h2>Section Title</h2>
 *   <div class="horizontal-scroll-container" id="myScroll">
 *     <div class="horizontal-scrollbar-track">
 *       <div class="horizontal-scrollbar-thumb"></div>
 *     </div>
 *     <div class="horizontal-scroll-controls">
 *       <button class="horizontal-scroll-button prev" aria-label="Scroll left">
 *         <i class="fas fa-chevron-left"></i>
 *       </button>
 *       <button class="horizontal-scroll-button next" aria-label="Scroll right">
 *         <i class="fas fa-chevron-right"></i>
 *       </button>
 *     </div>
 *     <div class="horizontal-scroll-content">
 *       <div class="horizontal-scroll-item">
 *         <!-- Scrollable content -->
 *       </div>
 *     </div>
 *   </div>
 * </div>
 */

(function () {
  'use strict';

  // Default configuration
  const defaultConfig = {
    scrollAmount: 300,
    thumbRatio: 0.3,
    showControlsThreshold: 0.1, // Show nav buttons when 10% overflow
    autoHideDelay: 3000 // Auto-hide controls after 3 seconds of inactivity
  };

  /**
   * HorizontalScrollController class
   * Manages horizontal scrolling behavior for containers
   */
  class HorizontalScrollController {
    constructor(container, options = {}) {
      this.container = container;
      this.config = { ...defaultConfig, ...options };

      // State
      this.scrollPosition = 0;
      this.maxScroll = 0;
      this thumbRatio = this.config.thumbRatio;
      this.inactiveTimer = null;
      this.isDragging = false;
      this.dragStartX = 0;
      this.scrollStartX = 0;

      this.init();
    }

    /**
     * Initialize the controller
     */
    init() {
      this.createElements();
      this.bindEvents();
      this.updateScrollInfo();
      this.manageControlVisibility();
    }

    /**
     * Create scrollbar and control elements
     */
    createElements() {
      // Find or create scrollbar track
      let track = this.container.querySelector('.horizontal-scrollbar-track');
      if (!track) {
        track = document.createElement('div');
        track.className = 'horizontal-scrollbar-track';
        this.container.appendChild(track);
      }

      // Find or create thumb
      let thumb = track.querySelector('.horizontal-scrollbar-thumb');
      if (!thumb) {
        thumb = document.createElement('div');
        thumb.className = 'horizontal-scrollbar-thumb';
        track.appendChild(thumb);
      }

      // Find or create controls container
      let controls = this.container.querySelector('.horizontal-scroll-controls');
      if (!controls) {
        controls = document.createElement('div');
        controls.className = 'horizontal-scroll-controls';
        this.container.parentNode.insertBefore(controls, this.container.nextSibling);

        const prevBtn = document.createElement('button');
        prevBtn.className = 'horizontal-scroll-button prev';
        prevBtn.setAttribute('aria-label', 'Scroll left');
        prevBtn.innerHTML = '<i class="fas fa-chevron-left"></i>';

        const nextBtn = document.createElement('button');
        nextBtn.className = 'horizontal-scroll-button next';
        nextBtn.setAttribute('aria-label', 'Scroll right');
        nextBtn.innerHTML = '<i class="fas fa-chevron-right"></i>';

        controls.appendChild(prevBtn);
        controls.appendChild(nextBtn);
      }

      // Store references
      this.track = track;
      this.thumb = thumb;
      this.controls = controls;
      this.prevButton = controls.querySelector('.prev');
      this.nextButton = controls.querySelector('.next');

      // Bind control events
      if (this.prevButton) {
        this.prevButton.addEventListener('click', () => this.scrollLeft());
      }
      if (this.nextButton) {
        this.nextButton.addEventListener('click', () => this.scrollRight());
      }

      // Apply initial styles
      this.updateThumbPosition();
      this.manageControlVisibility();
    }

    /**
     * Bind scroll and interaction events
     */
    bindEvents() {
      // Scroll events
      this.container.addEventListener('scroll', () => {
        this.updateScrollInfo();
        this.updateThumbPosition();
        this.manageControlVisibility();
        this.resetInactiveTimer();
      });

      // Wheel event for horizontal scroll
      this.container.addEventListener('wheel', (e) => {
        if (Math.abs(e.deltaX) > Math.abs(e.deltaY) && e.deltaX !== 0) {
          e.preventDefault();
          this.scrollBy(e.deltaX);
          this.resetInactiveTimer();
        }
      }, { passive: false });

      // Touch events
      this.container.addEventListener('touchstart', (e) => {
        this.isDragging = true;
        this.dragStartX = e.touches[0].clientX;
        this.scrollStartX = this.container.scrollLeft;
        this.resetInactiveTimer();
      }, { passive: false });

      this.container.addEventListener('touchmove', (e) => {
        if (!this.isDragging) return;
        const deltaX = e.touches[0].clientX - this.dragStartX;
        this.scrollBy(-deltaX);
        e.preventDefault();
      }, { passive: false });

      this.container.addEventListener('touchend', () => {
        this.isDragging = false;
      });

      // Focus events for keyboard accessibility
      this.container.addEventListener('focusin', () => {
        this.manageControlVisibility(true);
      });

      this.container.addEventListener('focusout', () => {
        // Delay hiding to allow for focus transfer
        setTimeout(() => {
          if (!this.container.matches(':focus-within')) {
            this.manageControlVisibility(false);
          }
        }, 100);
      });

      // Keyboard navigation
      this.container.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowLeft') {
          e.preventDefault();
          this.scrollLeft();
        } else if (e.key === 'ArrowRight') {
          e.preventDefault();
          this.scrollRight();
        }
      });

      // Resize observer for responsive updates
      this.resizeObserver = new ResizeObserver(() => {
        this.updateScrollInfo();
        this.updateThumbPosition();
      });
      this.resizeObserver.observe(this.container);

      // Thumb drag events
      if (this.thumb) {
        this.thumb.addEventListener('mousedown', (e) => {
          this.isDragging = true;
          const rect = this.track.getBoundingClientRect();
          this.dragStartX = e.clientX;
          this.scrollStartX = this.container.scrollLeft;
          this.container.style.cursor = 'grabbing';
        });

        document.addEventListener('mousemove', (e) => {
          if (!this.isDragging) return;
          const rect = this.track.getBoundingClientRect();
          const deltaX = e.clientX - this.dragStartX;
          const maxThumbPos = rect.width - this.thumb.offsetWidth;
          const thumbPos = Math.max(0, Math.min(maxThumbPos, deltaX));
          const scrollRatio = maxThumbPos > 0 ? thumbPos / maxThumbPos : 0;
          this.scrollTo(scrollRatio * this.maxScroll);
        });

        document.addEventListener('mouseup', () => {
          this.isDragging = false;
          this.container.style.cursor = '';
        });
      }
    }

    /**
     * Update scroll position and max scroll values
     */
    updateScrollInfo() {
      this.scrollPosition = this.container.scrollLeft;

      const containerScrollWidth = this.container.scrollWidth;
      const containerClientWidth = this.container.clientWidth;
      this.maxScroll = Math.max(0, containerScrollWidth - containerClientWidth);

      // Update CSS custom property for thumb width ratio
      if (containerClientWidth > 0) {
        this.thumbRatio = containerClientWidth / containerScrollWidth;
        this.container.style.setProperty('--scroll-thumb-ratio', this.thumbRatio.toString());
      }
    }

    /**
     * Update thumb position based on scroll
     */
    updateThumbPosition() {
      if (!this.track || !this.thumb) return;

      const trackWidth = this.track.offsetWidth;
      const thumbWidth = Math.max(10, trackWidth * this.thumbRatio);

      // Calculate thumb position
      const scrollRatio = this.maxScroll > 0 ? this.scrollPosition / this.maxScroll : 0;
      const thumbPos = (trackWidth - thumbWidth) * scrollRatio;

      this.thumb.style.width = `${thumbWidth}px`;
      this.thumb.style.transform = `translateX(${thumbPos}px)`;
    }

    /**
     * Manage visibility of navigation controls
     */
    manageControlVisibility(manuallyShow = false) {
      if (this.controls) {
        if (manuallyShow) {
          this.controls.style.visibility = 'visible';
        } else {
          const hasOverflow = this.maxScroll > 0;
          const showControls = hasOverflow && (
            this.scrollPosition > this.config.showControlsThreshold * this.maxScroll ||
            this.scrollPosition < (1 - this.config.showControlsThreshold) * this.maxScroll
          );

          this.controls.style.visibility = showControls ? 'visible' : 'hidden';
        }
      }
    }

    /**
     * Reset the inactive timer
     */
    resetInactiveTimer() {
      if (this.inactiveTimer) {
        clearTimeout(this.inactiveTimer);
      }
      this.inactiveTimer = setTimeout(() => {
        this.manageControlVisibility(false);
      }, this.config.autoHideDelay);
    }

    /**
     * Scroll left by configured amount
     */
    scrollLeft() {
      this.scrollBy(-this.config.scrollAmount);
    }

    /**
     * Scroll right by configured amount
     */
    scrollRight() {
      this.scrollBy(this.config.scrollAmount);
    }

    /**
     * Scroll by a specific amount
     */
    scrollBy(amount) {
      const newPosition = Math.max(0, Math.min(this.scrollPosition + amount, this.maxScroll));
      this.scrollTo(newPosition);
    }

    /**
     * Scroll to a specific position with smooth animation
     */
    scrollTo(position) {
      this.container.scrollTo({
        left: position,
        behavior: 'smooth'
      });
    }

    /**
     * Update button disabled states
     */
    updateButtonStates() {
      if (this.prevButton) {
        this.prevButton.classList.toggle('disabled', this.scrollPosition <= 0);
      }
      if (this.nextButton) {
        this.nextButton.classList.toggle('disabled', this.scrollPosition >= this.maxScroll);
      }
    }

    /**
     * Destroy the controller
     */
    destroy() {
      if (this.resizeObserver) {
        this.resizeObserver.disconnect();
      }
      if (this.inactiveTimer) {
        clearTimeout(this.inactiveTimer);
      }
      this.isDragging = false;
    }
  }

  // Initialize all horizontal scroll containers when DOM is ready
  function initHorizontalScroll() {
    const containers = document.querySelectorAll('.horizontal-scroll-container, .horizontal-scroll-content');

    containers.forEach((container, index) => {
      // Only initialize if not already initialized
      if (!container.dataset.horizontalScrollInitialized) {
        // Ensure container has proper class
        if (!container.classList.contains('horizontal-scroll-container')) {
          container.classList.add('horizontal-scroll-container');
        }

        container.dataset.horizontalScrollInitialized = 'true';
        container.dataset.scrollIndex = index;

        // Create controller instance
        new HorizontalScrollController(container);
      }
    });
  }

  // Initialize when document is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initHorizontalScroll);
  } else {
    initHorizontalScroll();
  }

  // Export for module usage (if applicable)
  if (typeof window !== 'undefined') {
    window.HorizontalScrollController = HorizontalScrollController;
    window.initHorizontalScroll = initHorizontalScroll;
  }

})();