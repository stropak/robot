Open interactive robotics platform for home use 

Description

The robot is a university thesis project focusing on the design and implementation of a functional mobile robot. The robot can be controlled through an interactive web application and is capable of transmitting video and two-way audio, making it suitable for remote monitoring purposes. The project is designed as an open-source platform, emphasizing low cost and easy expansion of additional functionalities.

The project utilizes Raspberry Pi as the main hardware platform and Python for the application development. The robot's movement and status information are transmitted using a bidirectional WebSocket channel provided by the Tornado library. Video and audio streaming are enabled through the UV4L framework, which leverages WebRTC technology for real-time communication.

Key Features

    Remote control of the mobile robot via a web application.
    Video streaming functionality for real-time monitoring.
    Two-way audio communication for remote interaction.
    Modular design for easy expansion and addition of new features.
    Open-source project, allowing for community contributions and improvements.
    Cost-effective implementation using Raspberry Pi and readily available components.
    
    
Application architecture

The main part of the application is the webapplication.py file, where the WebSocketConnection class is located to ensure web communication, as well as the main application code.
The other files represent individual modules for working with specific hardware components and contain classes of the same name.

Gamepad control

The gamepad.py file contains the code to control the robot using the ps4 gamepad via blootooth and is not related to the main application in any way.

Licence

The whole project is open source
