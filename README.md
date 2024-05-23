# ROS packages for Remote Control Car model Utilities
# Packages
## 1. Remote controller node:
   - Parsing keyboard input:
     ```
     Variables:      Meanings:                                                                Keys:
     speed:         "[increase/decrease] forward speed"                                       [W/S]
     angle:         "[increase/decrease] steer-angle (positive:right | negative:left) "       [A/D]
     pid:           "Toggle Enable/Disable PID Controller"                                    [P]
     pid KP:        "[increase/decrease] Kp"                                                  [Z/X]
     pid KI:        "[increase/decrease] Ki"                                                  [V/B]
     pid KD:        "[increase/decrease] Kd"                                                  [N/M]
     maxSpeed :     "[increase/decrease] max forward speed"                                   [T/G]
     maxSteerAngle: "[increase/decrease] max steering angle"                                  [Y/H]
     acceleration:  "[increase/decrease] forward speed step"                                  [U/J]
     steerStep:     "[increase/decrease] steering angle step"                                 [I/K]
     Reset Params:                                                                            [R]
     Exit                                                                                     [Esc]
     ```
   - Converting into motion commands
   - Publishing to '/automobile/command' topic
## 2. RC receiver node:
   - Subscribe to '/automobile/command' topic
   - Decoding motion commands
   - Converting into Embedded API command
   - Send command to serial port connected with STM32-NUCLEO
