import unittest
from unittest.mock import patch, MagicMock
from mqtt_service import Mqtt_Service

class TestMqttService(unittest.TestCase):

    @patch('mqtt_service.mqtt.Client')
    def test_establish_connection_success(self, mock_mqtt_client):
        service = Mqtt_Service()
        client = MagicMock()
        mock_mqtt_client.return_value = client
        self.assertEqual(service.establish_connection(), client)

    @patch('mqtt_service.mqtt.Client')
    def test_disconnect_connection(self, mock_mqtt_client):
        service = Mqtt_Service()
        client = MagicMock()
        mock_mqtt_client.return_value = client
        service.disconnect_connection(client)
        client.disconnect.assert_called_once()

    @patch('mqtt_service.mqtt.Client')
    def test_send_command(self, mock_mqtt_client):
        service = Mqtt_Service()
        client = MagicMock()
        mock_mqtt_client.return_value = client
        service.send_command("test_body")
        client.publish.assert_called_once_with("ur3/set/cmd", "test_body")

    @patch('mqtt_service.mqtt.Client')
    def test_get_value(self, mock_mqtt_client):
        service = Mqtt_Service()
        client = MagicMock()
        mock_mqtt_client.return_value = client
        service.wait_for_response = MagicMock(return_value="test_value")
        value = service.get_value("test_body")
        self.assertEqual(value, "test_value")
        client.subscribe.assert_called_once_with("ur3/get/val")
        client.publish.assert_called_once_with("ur3/get/val", "test_body")

    def test_move_to_pos(self):
        service = Mqtt_Service()
        service.send_command = MagicMock()
        service.move_to_pos("test_pos")
        service.send_command.assert_called_once_with("movePos:test_pos")

    def test_get_pose(self):
        service = Mqtt_Service()
        service.get_value = MagicMock(return_value="test_pose")
        pose = service.get_Pose()
        self.assertEqual(pose, "test_pose")
        service.get_value.assert_called_once_with("getPose")

    def test_get_joints(self):
        service = Mqtt_Service()
        service.get_value = MagicMock(return_value="test_joints")
        joints = service.get_Joints()
        self.assertEqual(joints, "test_joints")
        service.get_value.assert_called_once_with("getJoints")

    def test_set_individual_axes(self):
        service = Mqtt_Service()
        service.send_command = MagicMock()
        service.set_individual_axes("x", 1.0)
        service.send_command.assert_called_once_with("x:1.0")

    def test_move_to_tcp_pos(self):
        service = Mqtt_Service()
        service.set_individual_axes = MagicMock()
        service.send_command = MagicMock()
        service.move_to_tcp_pos(1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0)
        service.set_individual_axes.assert_any_call("x", 1.0)
        service.set_individual_axes.assert_any_call("y", 2.0)
        service.set_individual_axes.assert_any_call("z", 3.0)
        service.set_individual_axes.assert_any_call("ax", 4.0)
        service.set_individual_axes.assert_any_call("ay", 5.0)
        service.set_individual_axes.assert_any_call("az", 6.0)
        service.send_command.assert_called_once_with("moveJ")

    def test_wait_for_response(self):
        service = Mqtt_Service()
        service.response = "test_response"
        self.assertEqual(service.wait_for_response(1.0), "test_response")

if __name__ == '__main__':
    unittest.main()
