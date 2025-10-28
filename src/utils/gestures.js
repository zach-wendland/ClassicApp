/**
 * Touch gesture detection utility for mobile interactions
 * Detects swipe gestures (left, right, up, down) with configurable thresholds
 */

const DEFAULT_OPTIONS = {
  minSwipeDistance: 50,    // Minimum distance in pixels to register as swipe
  maxSwipeTime: 500,       // Maximum time in ms for a swipe gesture
  swipeAngleTolerance: 30  // Degrees of tolerance for direction detection
};

/**
 * Calculate distance between two points
 * @param {Object} point1 - First point with x, y coordinates
 * @param {Object} point2 - Second point with x, y coordinates
 * @returns {number} Distance in pixels
 */
export function calculateDistance(point1, point2) {
  const deltaX = point2.x - point1.x;
  const deltaY = point2.y - point1.y;
  return Math.sqrt(deltaX * deltaX + deltaY * deltaY);
}

/**
 * Calculate angle of swipe in degrees
 * @param {Object} start - Start point with x, y coordinates
 * @param {Object} end - End point with x, y coordinates
 * @returns {number} Angle in degrees (0-360)
 */
export function calculateAngle(start, end) {
  const deltaX = end.x - start.x;
  const deltaY = end.y - start.y;
  let angle = Math.atan2(deltaY, deltaX) * (180 / Math.PI);

  // Normalize to 0-360
  if (angle < 0) {
    angle += 360;
  }

  return angle;
}

/**
 * Determine swipe direction from angle
 * @param {number} angle - Angle in degrees
 * @param {number} tolerance - Angle tolerance in degrees
 * @returns {string|null} Direction: 'left', 'right', 'up', 'down', or null
 */
export function getSwipeDirection(angle, tolerance = 30) {
  // Right: 0° ± tolerance
  if ((angle >= 0 && angle <= tolerance) || (angle >= 360 - tolerance && angle <= 360)) {
    return 'right';
  }

  // Down: 90° ± tolerance
  if (angle >= 90 - tolerance && angle <= 90 + tolerance) {
    return 'down';
  }

  // Left: 180° ± tolerance
  if (angle >= 180 - tolerance && angle <= 180 + tolerance) {
    return 'left';
  }

  // Up: 270° ± tolerance
  if (angle >= 270 - tolerance && angle <= 270 + tolerance) {
    return 'up';
  }

  return null; // Not a clear directional swipe
}

/**
 * Validate if touch event qualifies as a swipe
 * @param {Object} touchData - Object containing start, end, time data
 * @param {Object} options - Configuration options
 * @returns {Object} Validation result with isValid, direction, distance, duration
 */
export function validateSwipe(touchData, options = DEFAULT_OPTIONS) {
  const { start, end, startTime, endTime } = touchData;

  const distance = calculateDistance(start, end);
  const duration = endTime - startTime;
  const angle = calculateAngle(start, end);
  const direction = getSwipeDirection(angle, options.swipeAngleTolerance);

  const isValid =
    distance >= options.minSwipeDistance &&
    duration <= options.maxSwipeTime &&
    direction !== null;

  return {
    isValid,
    direction,
    distance,
    duration,
    angle
  };
}

/**
 * Touch gesture detector class
 * Handles touch events and emits gesture callbacks
 */
export class GestureDetector {
  constructor(element, callbacks = {}, options = {}) {
    this.element = element;
    this.callbacks = callbacks;
    this.options = { ...DEFAULT_OPTIONS, ...options };

    this.touchData = {
      start: null,
      end: null,
      startTime: null,
      endTime: null
    };

    this.isTouching = false;

    // Bind event handlers
    this.handleTouchStart = this.handleTouchStart.bind(this);
    this.handleTouchMove = this.handleTouchMove.bind(this);
    this.handleTouchEnd = this.handleTouchEnd.bind(this);

    this.attach();
  }

  /**
   * Attach event listeners to element
   */
  attach() {
    if (!this.element) return;

    this.element.addEventListener('touchstart', this.handleTouchStart, { passive: true });
    this.element.addEventListener('touchmove', this.handleTouchMove, { passive: true });
    this.element.addEventListener('touchend', this.handleTouchEnd, { passive: true });
    this.element.addEventListener('touchcancel', this.handleTouchEnd, { passive: true });
  }

  /**
   * Detach event listeners from element
   */
  detach() {
    if (!this.element) return;

    this.element.removeEventListener('touchstart', this.handleTouchStart);
    this.element.removeEventListener('touchmove', this.handleTouchMove);
    this.element.removeEventListener('touchend', this.handleTouchEnd);
    this.element.removeEventListener('touchcancel', this.handleTouchEnd);
  }

  /**
   * Handle touch start event
   * @param {TouchEvent} event
   */
  handleTouchStart(event) {
    const touch = event.touches[0];

    this.touchData.start = {
      x: touch.clientX,
      y: touch.clientY
    };
    this.touchData.startTime = Date.now();
    this.isTouching = true;

    if (this.callbacks.onTouchStart) {
      this.callbacks.onTouchStart(this.touchData);
    }
  }

  /**
   * Handle touch move event
   * @param {TouchEvent} event
   */
  handleTouchMove(event) {
    if (!this.isTouching) return;

    const touch = event.touches[0];

    this.touchData.end = {
      x: touch.clientX,
      y: touch.clientY
    };

    if (this.callbacks.onTouchMove) {
      this.callbacks.onTouchMove(this.touchData);
    }
  }

  /**
   * Handle touch end event
   * @param {TouchEvent} event
   */
  handleTouchEnd(event) {
    if (!this.isTouching) return;

    // Use last known position if no touches remain
    if (event.changedTouches && event.changedTouches.length > 0) {
      const touch = event.changedTouches[0];
      this.touchData.end = {
        x: touch.clientX,
        y: touch.clientY
      };
    }

    this.touchData.endTime = Date.now();
    this.isTouching = false;

    // Validate and process swipe
    const swipeResult = validateSwipe(this.touchData, this.options);

    if (swipeResult.isValid) {
      this.handleSwipe(swipeResult);
    }

    if (this.callbacks.onTouchEnd) {
      this.callbacks.onTouchEnd(this.touchData, swipeResult);
    }

    // Reset touch data
    this.resetTouchData();
  }

  /**
   * Handle validated swipe gesture
   * @param {Object} swipeResult - Swipe validation result
   */
  handleSwipe(swipeResult) {
    const { direction } = swipeResult;

    // Call general swipe callback
    if (this.callbacks.onSwipe) {
      this.callbacks.onSwipe(direction, swipeResult);
    }

    // Call direction-specific callbacks
    const directionCallback = this.callbacks[`onSwipe${this.capitalize(direction)}`];
    if (directionCallback) {
      directionCallback(swipeResult);
    }
  }

  /**
   * Reset touch data
   */
  resetTouchData() {
    this.touchData = {
      start: null,
      end: null,
      startTime: null,
      endTime: null
    };
  }

  /**
   * Capitalize first letter of string
   * @param {string} str
   * @returns {string}
   */
  capitalize(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
  }

  /**
   * Destroy the gesture detector
   */
  destroy() {
    this.detach();
    this.element = null;
    this.callbacks = null;
    this.touchData = null;
  }
}

/**
 * Composable function for Vue components
 * Returns gesture detector setup function
 */
export function useGestures() {
  let detector = null;

  const setupGestures = (element, callbacks, options) => {
    // Clean up existing detector
    if (detector) {
      detector.destroy();
    }

    // Create new detector
    detector = new GestureDetector(element, callbacks, options);

    return detector;
  };

  const cleanupGestures = () => {
    if (detector) {
      detector.destroy();
      detector = null;
    }
  };

  return {
    setupGestures,
    cleanupGestures
  };
}
