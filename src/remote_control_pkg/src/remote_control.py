#!/usr/bin/env python3

import json
from pynput import keyboard

from RcBrainThread import RcBrainThread
from std_msgs.msg import String

import rospy

class RemoteControlTransmitterProcess():
    # ===================================== INIT==========================================
    def __init__(self):
        """Run on the PC. It forwards the commans from the user via KeboardListenerThread to the RcBrainThread. 
        The RcBrainThread converts them into actual commands and sends them to the remote via a socket connection.
        
        """
        self.dirKeys   = ['w', 'a', 's', 'd']
        self.paramKeys = ['t','g','y','h','u','j','i','k', 'r', 'p']
        self.pidKeys = ['z','x','v','b','n','m']

        self.allKeys = self.dirKeys + self.paramKeys + self.pidKeys
        
        self.rcBrain   =  RcBrainThread()   
        
        rospy.init_node('CONTROLLERnode', anonymous=False)     
        self.publisher = rospy.Publisher('/automobile/command', String, queue_size=1)

    # ===================================== RUN ==========================================
    def run(self):
        """Apply initializing methods and start the threads. 
        """
        with keyboard.Listener(on_press = self.keyPress, on_release = self.keyRelease) as listener: 
            listener.join()
	
    # ===================================== KEY PRESS ====================================
    def keyPress(self,key):
        """Processing the key pressing 
        
        Parameters
        ----------
        key : pynput.keyboard.Key
            The key pressed
        """                                     
        try:                                                
            if key.char in self.allKeys:
                keyMsg = 'p.' + str(key.char)

                self._send_command(keyMsg)
    
        except: pass
        
    # ===================================== KEY RELEASE ==================================
    def keyRelease(self, key):
        """Processing the key realeasing.
        
        Parameters
        ----------
        key : pynput.keyboard.Key
            The key realeased. 
        
        """ 
        if key == keyboard.Key.esc:                        #exit key      
            self.publisher.publish('{"action":"3","steerAngle":0.0}')   
            return False
        try:                                               
            if key.char in self.allKeys:
                keyMsg = 'r.'+str(key.char)

                self._send_command(keyMsg)
    
        except: pass                                                              
                 
    # ===================================== SEND COMMAND =================================
    def _send_command(self, key):
        """Transmite the command to the remotecontrol receiver. 
        
        Parameters
        ----------
        inP : Pipe
            Input pipe. 
        """
        command = self.rcBrain.getMessage(key)
        if command is not None:
	
            command = json.dumps(command)
            self.publisher.publish(command)  
            
if __name__ == '__main__':
    try:
        nod = RemoteControlTransmitterProcess()
        nod.run()
    except rospy.ROSInterruptException:
        pass