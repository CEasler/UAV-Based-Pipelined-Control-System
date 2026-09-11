For this project, we used wireshark to capture packets sent betweeen a kit drone and the remote it came with.
We were then able to replicate these packets to have a python script control the drone through command signal bytes. 
We used this to create a demonstration of how pipelined vs nonpipelined data is sent through a real world output. 
Pipelining does not necessarily reduce the time of a single instruction, but it increases overall throughput by eliminating idle time between stages. 
Our nonpipelined script sends around 5 packets per second while the pipelined senda around 20. This improves responsiveness and decreases idle time.

For the demonstration, we have the drone fly in a straight line, turn around 180 degrees and fly back to its starting point.

