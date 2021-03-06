#!/usr/bin/env python

import math
import rospy
from sensor_msgs.msg import Joy
from std_msgs.msg import Bool
from oars_arbiter.voter import Voter_full
from oars_arbiter import createVote


def bound(n, lower, upper):
    if n < lower:
        return lower
    if n > upper:
        return upper
    return n


TIMEOUT = rospy.Duration.from_sec(1.2)


class JoyController(object):
    def __init__(self):
        self.control = {'p/s': 3, 'f/a': 4, 'spin': 0}
        self.switch = {'estop': 1, 'unestop': 0, 'rc_override': 3, 'rc_release': 2}

        self.voter = Voter_full('joystick')
        self.direction = 0
        self.speed = 0
        self.rotation = 0

        self.enabled = True

        rospy.init_node('joy_control')
        rospy.Subscriber('/joy', Joy, self.joy_cb)
        self.estop_pub = rospy.Publisher('/estop', Bool, queue_size=0)

        self.last_watchdog = rospy.Time.now()
        rospy.Subscriber('/shore_watchdog', Bool, self.watchdog_cb)

    def watchdog_cb(self, msg):
        """
        :type msg: Bool
        """
        if msg.data:
            self.last_watchdog = rospy.Time.now()

    def joy_cb(self, msg):
        ps_cmd = msg.axes[self.control['p/s']]
        fa_cmd = msg.axes[self.control['f/a']]
        spin_cmd = msg.axes[self.control['spin']]
        start_cmd = msg.buttons[self.switch['unestop']]
        stop_cmd = msg.buttons[self.switch['estop']]
        enable_cmd = msg.buttons[self.switch['rc_override']]
        disable_cmd = msg.buttons[self.switch['rc_release']]
        speed_01, dir_rad = self.cartesian_to_polar(fa_cmd, ps_cmd)

        self.speed = bound(speed_01 * 100, 0, 100)
        self.direction = round(dir_rad * 50 / math.pi)
        self.rotation = round(spin_cmd * 25)
        self.toggle_estop(stop_cmd, start_cmd)

        if not self.enabled and enable_cmd:
            self.enable()

        if self.enabled and disable_cmd:
            self.disable()

    def toggle_estop(self, stop_cmd, start_cmd):
        command = Bool()
        command.data = bool(stop_cmd)
        if stop_cmd or start_cmd:
            self.estop_pub.publish(command)

    def enable(self):
        self.enabled = True

        print "Joystick control enabled"

    def disable(self):
        self.enabled = False
        self.voter.dir_vote = createVote.max_speed(0)
        self.voter.speed_vote = createVote.max_speed(100)
        self.voter.make_vote()

        print "Joystick control disabled"

    @staticmethod
    def cartesian_to_polar(x, y):
        r = math.sqrt(x ** 2. + y ** 2.)
        theta = math.atan2(y, x)
        return r, theta

    def run(self):
        r = rospy.Rate(10)
        while not rospy.is_shutdown():
            if rospy.Time.now() - self.last_watchdog > TIMEOUT:
                self.estop_pub.publish(Bool(data=True))

            if self.enabled:
                self.voter.dir_vote = createVote.directionVoteGauss(self.direction)
                self.voter.turn_vote = createVote.yawVoteGauss(self.rotation)
                self.voter.speed_vote = createVote.max_speed(self.speed)
                self.voter.make_vote()
            r.sleep()


if __name__ == '__main__':
    joy = JoyController()
    joy.run()
