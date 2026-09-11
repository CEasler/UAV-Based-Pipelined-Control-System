UAV-Based Pipelined Control System
Overview:
    This project demonstrates the effects of pipelined vs. non-pipelined data transmission using a real-world UAV as the output system.
    We used Wireshark to capture the communication packets exchanged between a kit drone and its original remote controller. By analyzing and replicating these packets, we were able to identify the command signal bytes used to control the drone and recreate those commands through Python.

    This allowed us to apply computer architecture concepts to a physical system and demonstrate how increased throughput can improve the responsiveness of a real-world output.

How It Works:

    The project follows three primary steps:

    1. Packet Capture
        Wireshark was used to capture packets transmitted between the drone and its original remote controller.
    2. Packet Replication
        The captured packets were analyzed to identify the command signal bytes associated with different drone controls. These commands were then replicated using Python.
    3. Throughput Demonstration
        Two Python scripts were developed to demonstrate the difference between non-pipelined and pipelined transmission. Both scripts send the same sequence of commands to the drone, allowing the effect of different transmission rates to be observed through the drone’s physical movement.

Pipelined vs. Non-Pipelined Transmission:

    Pipelining does not necessarily reduce the execution time of a single instruction. Instead, it increases overall throughput by reducing idle time between stages of execution.

    We demonstrated this concept by varying the rate at which command packets were sent to the UAV:
        Transmission Method	Approx. Packets/Second
        Non-Pipelined	~5 packets/sec
        Pipelined	~20 packets/sec

    The pipelined implementation achieves approximately 4× the packet throughput, resulting in more frequent command updates, reduced idle time, and improved responsiveness.

Flight Demonstration:

    To ensure a consistent comparison, both implementations execute the same flight sequence:

        1. Fly forward in a straight line
        2. Turn 180°
        3. Fly back toward the starting position

    Because the command sequence remains consistent between implementations, the primary variable being demonstrated is the rate at which control packets are transmitted.

Technologies Used:

    * Python — UAV control and packet transmission
    * Wireshark — Network packet capture and analysis
    * Wi-Fi — Communication between the control system and UAV
    * UAV / Kit Drone — Physical output system
    * Computer Architecture Concepts — Pipelining, throughput, and instruction execution

Project Presentation:  

    Watch the full project demonstration for our collected quantitative and qualitative data:
    
        https://youtu.be/iejolHPOw9g

    Key Takeaway:

        This project demonstrates how computer architecture concepts such as pipelining and throughput can extend beyond theoretical instruction execution and be applied to a real-world embedded system. By controlling a physical UAV through replicated network commands, we were able to visualize how increased throughput can reduce idle time and improve the responsiveness of a system.