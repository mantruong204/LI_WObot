#!/usr/bin/env python3

import socket

import rospy

from std_msgs.msg import String

class serialDealerNODE():
    def __init__(self):
        """It forwards the control messages received from socket to the serial handling node. 
        """
        
        rospy.init_node('serialDealerNODE', anonymous=False)
        
        # Command publisher object
        self.command_publisher = rospy.Publisher("/automobile/command", String, queue_size=1)
        
    
     # ===================================== RUN ==========================================
    def run(self):
        """Apply the initializing methods and start the threads
        """
        rospy.loginfo("starting serialDealerNODE")
        self._init_socket()
        self._read_stream()

    # ===================================== INIT SOCKET ==================================
    def _init_socket(self):
        """Initialize the communication socket server.
        """
        self.port       =   12244
        self.serverIp   =   '0.0.0.0'
        
        self.server_socket = socket.socket(
                                    family  = socket.AF_INET, 
                                    type    = socket.SOCK_DGRAM
                                )
        self.server_socket.bind((self.serverIp, self.port))
        self.server_socket.settimeout(1)
        
    def _read_stream(self):
        """Receive the message and forwards them to the Serial Handler Node. 
        """
        
        while not rospy.is_shutdown():
            try:
                bts, addr = self.server_socket.recvfrom(1024)

                command   =  bts.decode()
                self.command_publisher.publish(command)
            except:
                pass
        else:
            self.server_socket.close()
            
            
if __name__ == "__main__":
    serDealerNod = serialDealerNODE()
    serDealerNod.run()
