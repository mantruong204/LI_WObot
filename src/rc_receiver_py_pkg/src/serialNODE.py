#!/usr/bin/env python3

import serial
from filehandler      import FileHandler
from messageconverter import MessageConverter
import json

import rospy

from std_msgs.msg      import String
# from utils.srv        import subscribing, subscribingResponse

class serialNODE():
    def __init__(self):
        """It forwards the control messages received from socket to the serial handling node. 
        """
        devFile = '/dev/ttyACM0'
        logFile = 'historyFile.txt'
        
        # comm init       
        self.serialCom = serial.Serial(devFile,19200,timeout=0.1)
        self.serialCom.flushInput()
        self.serialCom.flushOutput()

        # log file init
        self.historyFile = FileHandler(logFile)
        
        # message converted init
        self.messageConverter = MessageConverter()
        
        self.buff=""
        self.isResponse=False
        self.__subscribers={}
        
        rospy.init_node('serialNODE', anonymous=False)
        
        self.command_subscriber = rospy.Subscriber("/automobile/command", String, self._write)
        
        # self.subscribe = rospy.Service("command_feedback_en", subscribing, self._subscribe)        
    
     # ===================================== RUN ==========================================
    def run(self):
        """Apply the initializing methods and start the threads
        """
        rospy.loginfo("starting serialNODE")
        self._read()    
        
    # ===================================== READ ==========================================
    def _read(self):
        """ It's represent the reading activity on the the serial.
        """
        while not rospy.is_shutdown():
            read_chr=self.serialCom.read()
            try:
                read_chr=(read_chr.decode("ascii"))
                if read_chr=='@':
                    self.isResponse=True
                    if len(self.buff)!=0:
                        self.__checkSubscriber(self.buff)
                    self.buff=""
                elif read_chr=='\r':   
                    self.isResponse=False
                    if len(self.buff)!=0:
                        self.__checkSubscriber(self.buff)
                    self.buff=""
                if self.isResponse:
                    self.buff+=read_chr
                self.historyFile.write(read_chr)
                 
            except UnicodeDecodeError:
                pass
    
    def __checkSubscriber(self,f_response):
        """ Checking the list of the waiting object to redirectionate the message to them. 
        """
        l_key=f_response[1:5]
        if l_key in self.__subscribers:
            subscribers = self.__subscribers[l_key]
            for sub in subscribers:
                sub.publish(f_response)
    
    # def _subscribe(self, msg):
    #     """Enable the feedback from from a type of command to ensure receiving from embedded.
    #     To avoid topic names collision, specify the node name and code in the topic itself. 
    #     """
    #     if msg.subscribing:
    #         if msg.code in self.__subscribers:
    #             for sub in self.__subscribers[msg.code]:
    #                 if (msg.topic == sub.name):
    #                     subscribingResponse(False)
    #             else:
    #                 command_publisher = rospy.Publisher(msg.topic, String, queue_size=1)
    #                 self.__subscribers[msg.code].append(command_publisher)
    #                 subscribingResponse(True)
    #         else:
    #             command_publisher = rospy.Publisher(msg.topic, String, queue_size=1)
    #             self.__subscribers[msg.code] = [command_publisher]
    #             subscribingResponse(True)
    #     else:
    #         if msg.code in self.__subscribers:     
    #             for sub in self.__subscribers[msg.code]:
    #                 if (msg.topic == sub.name):
    #                     sub.unregister()
    #                     self.__subscribers[msg.code].remove(sub)
    #                     subscribingResponse(True)
    #             else:
    #                 return subscribingResponse(False)
    #         else:
    #             raise subscribingResponse(False)
        
        
    # ===================================== WRITE ==========================================
    def _write(self, msg):
        """ Represents the writing activity on the the serial.
        """
        command = json.loads(msg.data)
        # Unpacking the dictionary into action and values
        command_msg = self.messageConverter.get_command(**command)
        self.serialCom.write(command_msg.encode('ascii'))
        self.historyFile.write(command_msg)
        rospy.loginfo("Sent to serial port: {}".format(command_msg))
            
            
if __name__ == "__main__":
    serNod = serialNODE()
    serNod.run()
