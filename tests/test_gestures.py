"""
Unit tests for gesture detection functions
Tests touch gesture recognition, swipe validation, and direction detection
"""

import unittest
import math
from gestures import (
    calculate_distance,
    calculate_angle,
    get_swipe_direction,
    validate_swipe
)


class TestCalculateDistance(unittest.TestCase):
    """Test cases for calculate_distance function"""

    def test_horizontal_distance(self):
        """Test horizontal distance calculation"""
        point1 = {'x': 0, 'y': 0}
        point2 = {'x': 100, 'y': 0}
        distance = calculate_distance(point1, point2)
        self.assertEqual(distance, 100.0)

    def test_vertical_distance(self):
        """Test vertical distance calculation"""
        point1 = {'x': 0, 'y': 0}
        point2 = {'x': 0, 'y': 50}
        distance = calculate_distance(point1, point2)
        self.assertEqual(distance, 50.0)

    def test_diagonal_distance(self):
        """Test diagonal distance calculation (Pythagorean theorem)"""
        point1 = {'x': 0, 'y': 0}
        point2 = {'x': 3, 'y': 4}
        distance = calculate_distance(point1, point2)
        self.assertEqual(distance, 5.0)  # 3-4-5 triangle

    def test_negative_coordinates(self):
        """Test distance with negative coordinates"""
        point1 = {'x': -10, 'y': -10}
        point2 = {'x': 10, 'y': 10}
        distance = calculate_distance(point1, point2)
        expected = math.sqrt(20**2 + 20**2)
        self.assertAlmostEqual(distance, expected, places=2)

    def test_zero_distance(self):
        """Test zero distance (same point)"""
        point1 = {'x': 50, 'y': 50}
        point2 = {'x': 50, 'y': 50}
        distance = calculate_distance(point1, point2)
        self.assertEqual(distance, 0.0)


class TestCalculateAngle(unittest.TestCase):
    """Test cases for calculate_angle function"""

    def test_angle_right(self):
        """Test angle for rightward swipe (0 degrees)"""
        start = {'x': 0, 'y': 0}
        end = {'x': 100, 'y': 0}
        angle = calculate_angle(start, end)
        self.assertAlmostEqual(angle, 0, places=1)

    def test_angle_down(self):
        """Test angle for downward swipe (90 degrees)"""
        start = {'x': 0, 'y': 0}
        end = {'x': 0, 'y': 100}
        angle = calculate_angle(start, end)
        self.assertAlmostEqual(angle, 90, places=1)

    def test_angle_left(self):
        """Test angle for leftward swipe (180 degrees)"""
        start = {'x': 100, 'y': 0}
        end = {'x': 0, 'y': 0}
        angle = calculate_angle(start, end)
        self.assertAlmostEqual(angle, 180, places=1)

    def test_angle_up(self):
        """Test angle for upward swipe (270 degrees)"""
        start = {'x': 0, 'y': 100}
        end = {'x': 0, 'y': 0}
        angle = calculate_angle(start, end)
        self.assertAlmostEqual(angle, 270, places=1)

    def test_angle_diagonal(self):
        """Test angle for diagonal swipe (45 degrees)"""
        start = {'x': 0, 'y': 0}
        end = {'x': 100, 'y': 100}
        angle = calculate_angle(start, end)
        self.assertAlmostEqual(angle, 45, places=1)

    def test_angle_normalization(self):
        """Test that angles are normalized to 0-360"""
        start = {'x': 100, 'y': 100}
        end = {'x': 50, 'y': 50}
        angle = calculate_angle(start, end)
        self.assertGreaterEqual(angle, 0)
        self.assertLess(angle, 360)


class TestGetSwipeDirection(unittest.TestCase):
    """Test cases for get_swipe_direction function"""

    def test_direction_right(self):
        """Test right direction detection"""
        angle = 0
        direction = get_swipe_direction(angle)
        self.assertEqual(direction, 'right')

    def test_direction_right_with_tolerance(self):
        """Test right direction with angle tolerance"""
        angle = 20  # Within default 30° tolerance
        direction = get_swipe_direction(angle)
        self.assertEqual(direction, 'right')

    def test_direction_right_near_360(self):
        """Test right direction near 360 degrees"""
        angle = 350  # Within tolerance of 0°
        direction = get_swipe_direction(angle)
        self.assertEqual(direction, 'right')

    def test_direction_down(self):
        """Test down direction detection"""
        angle = 90
        direction = get_swipe_direction(angle)
        self.assertEqual(direction, 'down')

    def test_direction_left(self):
        """Test left direction detection"""
        angle = 180
        direction = get_swipe_direction(angle)
        self.assertEqual(direction, 'left')

    def test_direction_up(self):
        """Test up direction detection"""
        angle = 270
        direction = get_swipe_direction(angle)
        self.assertEqual(direction, 'up')

    def test_direction_none_outside_tolerance(self):
        """Test that angles outside tolerance return None"""
        angle = 45  # Not within tolerance of any cardinal direction
        direction = get_swipe_direction(angle)
        self.assertIsNone(direction)

    def test_custom_tolerance(self):
        """Test with custom tolerance value"""
        angle = 45
        direction = get_swipe_direction(angle, tolerance=50)
        self.assertEqual(direction, 'right')  # Within 50° of 0°


class TestValidateSwipe(unittest.TestCase):
    """Test cases for validate_swipe function"""

    def test_valid_right_swipe(self):
        """Test validation of a valid right swipe"""
        touch_data = {
            'start': {'x': 0, 'y': 100},
            'end': {'x': 100, 'y': 100},
            'startTime': 0,
            'endTime': 200
        }
        result = validate_swipe(touch_data)

        self.assertTrue(result['isValid'])
        self.assertEqual(result['direction'], 'right')
        self.assertEqual(result['distance'], 100.0)
        self.assertEqual(result['duration'], 200)

    def test_valid_left_swipe(self):
        """Test validation of a valid left swipe"""
        touch_data = {
            'start': {'x': 200, 'y': 100},
            'end': {'x': 50, 'y': 100},
            'startTime': 0,
            'endTime': 250
        }
        result = validate_swipe(touch_data)

        self.assertTrue(result['isValid'])
        self.assertEqual(result['direction'], 'left')
        self.assertAlmostEqual(result['distance'], 150.0, places=1)

    def test_valid_down_swipe(self):
        """Test validation of a valid down swipe"""
        touch_data = {
            'start': {'x': 100, 'y': 0},
            'end': {'x': 100, 'y': 80},
            'startTime': 0,
            'endTime': 300
        }
        result = validate_swipe(touch_data)

        self.assertTrue(result['isValid'])
        self.assertEqual(result['direction'], 'down')
        self.assertEqual(result['distance'], 80.0)

    def test_valid_up_swipe(self):
        """Test validation of a valid up swipe"""
        touch_data = {
            'start': {'x': 100, 'y': 200},
            'end': {'x': 100, 'y': 100},
            'startTime': 0,
            'endTime': 200
        }
        result = validate_swipe(touch_data)

        self.assertTrue(result['isValid'])
        self.assertEqual(result['direction'], 'up')
        self.assertEqual(result['distance'], 100.0)

    def test_invalid_too_short(self):
        """Test that swipe too short is invalid"""
        touch_data = {
            'start': {'x': 0, 'y': 0},
            'end': {'x': 30, 'y': 0},  # Only 30px, minimum is 50px
            'startTime': 0,
            'endTime': 200
        }
        result = validate_swipe(touch_data)

        self.assertFalse(result['isValid'])

    def test_invalid_too_slow(self):
        """Test that swipe too slow is invalid"""
        touch_data = {
            'start': {'x': 0, 'y': 0},
            'end': {'x': 100, 'y': 0},
            'startTime': 0,
            'endTime': 600  # 600ms, maximum is 500ms
        }
        result = validate_swipe(touch_data)

        self.assertFalse(result['isValid'])

    def test_invalid_diagonal(self):
        """Test that diagonal swipe (not cardinal direction) is invalid"""
        touch_data = {
            'start': {'x': 0, 'y': 0},
            'end': {'x': 100, 'y': 100},  # 45 degree angle
            'startTime': 0,
            'endTime': 200
        }
        result = validate_swipe(touch_data)

        self.assertFalse(result['isValid'])
        self.assertIsNone(result['direction'])

    def test_custom_options_min_distance(self):
        """Test validation with custom minimum distance"""
        touch_data = {
            'start': {'x': 0, 'y': 0},
            'end': {'x': 40, 'y': 0},
            'startTime': 0,
            'endTime': 200
        }
        options = {
            'minSwipeDistance': 30,  # Lower than default 50
            'maxSwipeTime': 500,
            'swipeAngleTolerance': 30
        }
        result = validate_swipe(touch_data, options)

        self.assertTrue(result['isValid'])
        self.assertEqual(result['direction'], 'right')

    def test_custom_options_max_time(self):
        """Test validation with custom maximum time"""
        touch_data = {
            'start': {'x': 0, 'y': 0},
            'end': {'x': 100, 'y': 0},
            'startTime': 0,
            'endTime': 800
        }
        options = {
            'minSwipeDistance': 50,
            'maxSwipeTime': 1000,  # Higher than default 500
            'swipeAngleTolerance': 30
        }
        result = validate_swipe(touch_data, options)

        self.assertTrue(result['isValid'])
        self.assertEqual(result['direction'], 'right')

    def test_custom_options_angle_tolerance(self):
        """Test validation with custom angle tolerance"""
        touch_data = {
            'start': {'x': 0, 'y': 0},
            'end': {'x': 100, 'y': 50},  # About 26.5 degrees
            'startTime': 0,
            'endTime': 200
        }
        options = {
            'minSwipeDistance': 50,
            'maxSwipeTime': 500,
            'swipeAngleTolerance': 15  # Tighter tolerance
        }
        result = validate_swipe(touch_data, options)

        self.assertFalse(result['isValid'])  # Should fail with tight tolerance

    def test_fast_swipe(self):
        """Test very fast swipe"""
        touch_data = {
            'start': {'x': 0, 'y': 0},
            'end': {'x': 200, 'y': 0},
            'startTime': 0,
            'endTime': 100  # Very fast
        }
        result = validate_swipe(touch_data)

        self.assertTrue(result['isValid'])
        self.assertEqual(result['duration'], 100)

    def test_long_swipe(self):
        """Test very long swipe"""
        touch_data = {
            'start': {'x': 0, 'y': 0},
            'end': {'x': 500, 'y': 0},
            'startTime': 0,
            'endTime': 400
        }
        result = validate_swipe(touch_data)

        self.assertTrue(result['isValid'])
        self.assertEqual(result['distance'], 500.0)


if __name__ == '__main__':
    unittest.main()
