"""
An example ROS 2 node written in Python.

See the real node here:
https://github.com/Sooner-Rover-Team/auto_ros2/tree/main/src/navigator/navigator_node
"""

from dataclasses import dataclass
import time
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSPresetProfiles
from rclpy.subscription import Subscription
from sensor_msgs.msg import NavSatFix
from typing_extensions import override


@dataclass(kw_only=True)
class NavigatorNode(Node):
    """
    An example ROS 2 node.

    Notice how there's the `@dataclass` annotation thingy up there? That lets
    us say _what_ data will be stored in the class. It cleans things up a lot!

    After this comment ends, you'll see the class "data fields"...
    """

    _gps_subscription: Subscription
    """
    Here's our first field!

    This `_gps_subscription` variable is accessible throughout the class, in
    all of its methods.
    """

    def __init__(self):
        """
        "Initializes" the node.

        This function makes the node known to ROS 2 when it's created in
        Python code. It also sets up a bunch of variables, like our
        `_gps_subscription` field.
        """

        # first, we have to initialize the `Node` class that this one extends.
        #
        # inside that `__init__` function, we're giving our node a name. ROS 2
        # will refer to it as `navigator_node` from now on, unless you rename
        # it in a launch file.
        #
        # IMPORTANT: you are REQUIRED to call this function to correctly create
        # a ROS 2 node.
        super().__init__("navigator_node")

        # next, we can initialize the `_gps_subscription` variable.
        #
        # you can see that we have another method at the bottom of this class
        # called `_gps_callback`. that's a function we want to run if another
        # node sends us a `NavSatFix` (GPS message).
        #
        # so, let's set that up accordingly:
        self._gps_subscription = self.create_subscription(
            msg_type=NavSatFix,
            topic="/sensors/gps",
            callback=self._gps_callback,
            qos_profile=QoSPresetProfiles.SENSOR_DATA.value,
        )

        # great! we've now set up a ROS 2 node correctly!
        #
        # the function now returns...

    # required boilerplate -- please ignore!
    @override
    def __hash__(self) -> int:
        return super().__hash__()

    def _gps_callback(self, msg: NavSatFix):
        """This function runs when we receive a GPS message!"""

        # extract data from message
        lat: float = msg.latitude
        lon: float = msg.longitude
        alt: float = msg.altitude

        # print out the data
        print(f"Got a GPS message! lat: {lat}, lon: {lon}, alt: {alt}")


def main(args: list[str] | None = None):
    """
    Starts the Navigator node.
    """
    rclpy.init(args=args)
    navigator_node: NavigatorNode = NavigatorNode()

    # tell the user that the node's running, and let them know how to stop it!
    #
    # note that the weird \033 escapes down there show color in the terminal,
    # which makes it a little easier to read, in my view. ~bray
    print(
        "The Navigator node is now running! You can press Ctrl + C at any time to stop it."
    )
    print()
    print("Please paste the following code into another ROS 2 terminal:")
    print(
        '\033[0;34mros2 \033[0;35mtopic pub \033[0;32m/sensors/gps sensor_msgs/NavSatFix \033[0;31m"{ latitude: 1.0, longitude: 2.0, altitude: 3.0 }"\033[0m'
    )
    print()

    # spin the node until ROS 2 stops it (or you spam Ctrl^C)
    while rclpy.ok():
        rclpy.spin_once(navigator_node, timeout_sec=0)
        time.sleep(1e-4)

    # destroy the Node explicitly
    #
    # this is optional - otherwise, the garbage collector does it automatically
    # when it runs.
    navigator_node.destroy_node()
    rclpy.shutdown()
