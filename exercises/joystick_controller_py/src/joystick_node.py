#!_______
import rospy
from autominy_msgs.msg import NormalizedSpeedCommand, NormalizedSteeringCommand

import pygame
from pygame.locals import *

class Node:
    
    def __init__(self):
        self.vel_pub = rospy._______("_______",_______,queue_size=1)
        self.giro_pub = rospy._______("_______",_______,queue_size=1)
        self.rate = rospy.Rate(___)

        pygame.init()
        pygame.joystick.init()
        self.joystick = self.update_joystick_list(True)
        self.gas = 0.0
        self.stearing = 0.0
    
    def update_joystick_list(self, verbose=False):
        joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
        if verbose==True:
            for joystick in joysticks:
                print(joystick.get_name())
        return joysticks

    def publish(self,velocidad,giro):
        vel_msg = _______
        giro_msg = _______
        vel_msg.value = velocidad
        giro_msg.value = giro

        self.vel_pub._______(_______)
        self.giro_pub._______(_______)
    
    def talk(self):
        while not rospy.is_shutdown():
            for event in pygame.event.get():
                # Joystick controller
                if event.type == JOYDEVICEADDED:
                    self.joysticks = self.update_joystick_list(True)
                if event.type == JOYDEVICEREMOVED:
                    self.joysticks = self.update_joystick_list()
                    
                if event.type == JOYBUTTONDOWN and event.button == 2:
                    self.gas = 0.2
                if event.type == JOYBUTTONUP and event.button == 2:
                    self.gas = 0.0
                if event.type == JOYAXISMOTION and event.axis == 0:
                    self.stearing = event.value/2

                # Pygame
                if event.type == QUIT:
                    pygame.quit()
            self.publish(self.gas, self.stearing)
            self.rate.sleep()

def main():
    _______.init_node("_______",anonymous=True)
    node = Node()
    node.talk()

if __name__=='__main__':
    main()		

