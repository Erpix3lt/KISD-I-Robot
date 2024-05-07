import unittest
from unittest.mock import MagicMock, patch
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from interface.robot_service import Robot_Service

class TestRobotService(unittest.TestCase):
    """
    This is a mockup test suite for the interface package. It will not 
    publish any MQTT messages.
    """
    def setUp(self):
        self.robot_service = Robot_Service()

    def test_move_pos(self):
        with patch.object(self.robot_service, 'set_cmd') as mock_set_cmd:
            self.robot_service.move_pos("test_pos")
            mock_set_cmd.assert_called_once_with("movePos:test_pos")

    def test_get_pose(self):
        with patch.object(self.robot_service, 'set_cmd') as mock_set_cmd:
            with patch.object(self.robot_service, 'get_val') as mock_get_val:
                self.robot_service.get_pose()
                mock_set_cmd.assert_called_once_with("getPose")
                mock_get_val.assert_called_once()

    def test_get_joints(self):
        with patch.object(self.robot_service, 'set_cmd') as mock_set_cmd:
            with patch.object(self.robot_service, 'get_val') as mock_get_val:
                self.robot_service.get_joints()
                mock_set_cmd.assert_called_once_with("getJoints")
                mock_get_val.assert_called_once()

    def test_set_axis_invalid_axes(self):
        with patch.object(self.robot_service, 'set_cmd') as mock_set_cmd:
            self.robot_service.set_axis("invalid", 1.0)
            mock_set_cmd.assert_not_called()

    def test_move_to_tcp_pos(self):
        with patch.object(self.robot_service, 'set_cmd') as mock_set_cmd:
            self.robot_service.move_to_tcp_pos(1.0, 2.0, 3.0, ax=4.0, blend=5.0, time=6.0)
            expected_calls = [
                unittest.mock.call('x:1.0'),
                unittest.mock.call('y:2.0'),
                unittest.mock.call('z:3.0'),
                unittest.mock.call('ax:4.0'),
                unittest.mock.call('blend:6.0'),
                unittest.mock.call('time:6.0'),
                unittest.mock.call('movejPose')
            ]
            mock_set_cmd.assert_has_calls(expected_calls, any_order=True)

    def test_assert_has_reached_tcp_pos(self):
        with patch.object(self.robot_service, 'get_pose', return_value="pose:p[1.0, 2.0, 3.0, 4.0, 5.0, 6.0]") as mock_get_pose:
            self.assertTrue(self.robot_service.assert_has_reached_tcp_pos(1.0, 2.0, 3.0, 4.0, 5.0, 6.0))
            self.assertFalse(self.robot_service.assert_has_reached_tcp_pos(1.0, 2.0, 3.0, 4.0, 5.0, 7.0))

if __name__ == '__main__':
    unittest.main()
