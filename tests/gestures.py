"""
Python implementation of gesture detection functions for testing
This mirrors the JavaScript implementation
"""
import math


def calculate_distance(point1, point2):
    """
    Calculate distance between two points

    Args:
        point1: Dictionary with 'x' and 'y' coordinates
        point2: Dictionary with 'x' and 'y' coordinates

    Returns:
        Distance in pixels as float
    """
    delta_x = point2['x'] - point1['x']
    delta_y = point2['y'] - point1['y']
    return math.sqrt(delta_x ** 2 + delta_y ** 2)


def calculate_angle(start, end):
    """
    Calculate angle of swipe in degrees

    Args:
        start: Dictionary with 'x' and 'y' coordinates
        end: Dictionary with 'x' and 'y' coordinates

    Returns:
        Angle in degrees (0-360)
    """
    delta_x = end['x'] - start['x']
    delta_y = end['y'] - start['y']
    angle = math.atan2(delta_y, delta_x) * (180 / math.pi)

    # Normalize to 0-360
    if angle < 0:
        angle += 360

    return angle


def get_swipe_direction(angle, tolerance=30):
    """
    Determine swipe direction from angle

    Args:
        angle: Angle in degrees
        tolerance: Angle tolerance in degrees

    Returns:
        Direction string: 'left', 'right', 'up', 'down', or None
    """
    # Right: 0° ± tolerance
    if (angle >= 0 and angle <= tolerance) or (angle >= 360 - tolerance and angle <= 360):
        return 'right'

    # Down: 90° ± tolerance
    if angle >= 90 - tolerance and angle <= 90 + tolerance:
        return 'down'

    # Left: 180° ± tolerance
    if angle >= 180 - tolerance and angle <= 180 + tolerance:
        return 'left'

    # Up: 270° ± tolerance
    if angle >= 270 - tolerance and angle <= 270 + tolerance:
        return 'up'

    return None  # Not a clear directional swipe


def validate_swipe(touch_data, options=None):
    """
    Validate if touch event qualifies as a swipe

    Args:
        touch_data: Dictionary containing 'start', 'end', 'startTime', 'endTime'
        options: Dictionary with 'minSwipeDistance', 'maxSwipeTime', 'swipeAngleTolerance'

    Returns:
        Dictionary with validation result
    """
    if options is None:
        options = {
            'minSwipeDistance': 50,
            'maxSwipeTime': 500,
            'swipeAngleTolerance': 30
        }

    start = touch_data['start']
    end = touch_data['end']
    start_time = touch_data['startTime']
    end_time = touch_data['endTime']

    distance = calculate_distance(start, end)
    duration = end_time - start_time
    angle = calculate_angle(start, end)
    direction = get_swipe_direction(angle, options['swipeAngleTolerance'])

    is_valid = (
        distance >= options['minSwipeDistance'] and
        duration >= 0 and  # Reject negative durations
        duration <= options['maxSwipeTime'] and
        direction is not None
    )

    return {
        'isValid': is_valid,
        'direction': direction,
        'distance': distance,
        'duration': duration,
        'angle': angle
    }
