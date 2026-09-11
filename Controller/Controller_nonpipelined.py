import socket
import time
import curses

DRONE_IP = "192.168.1.1"
DRONE_PORT = 7099

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

mode = 2

roll = 128
yaw = 128
pitch = 128
throttle = 155   

def create_packet(roll, yaw, throttle, pitch, command, mode):
    packet = [0]*21
    packet[0]=0x03; packet[1]=0x66; packet[2]=0x14

    packet[3]=int(roll)
    packet[4]=int(yaw)
    packet[5]=int(throttle)
    packet[6]=int(pitch)

    packet[7]=int(command)
    packet[8]=int(mode)

    packet[19]=packet[3]^packet[4]^packet[5]^packet[6]^packet[7]^packet[8]
    packet[20]=0x99

    return bytes(packet)

def send(command=0):
    sock.sendto(create_packet(roll,yaw,throttle,pitch,command,mode),
                (DRONE_IP,DRONE_PORT))

def main(stdscr):
    global roll, yaw, pitch, throttle

    curses.cbreak()
    stdscr.nodelay(True)

    stdscr.addstr(0,0,"Drone Controller (X to quit)")
    stdscr.addstr(1,0,"W/S=Forward/Back | A/D=Left/Right")
    stdscr.addstr(2,0,"Q/E=Rotate | ↑/↓=Throttle")

    # 🚀 TAKEOFF
    for _ in range(25):
        send(command=1)
        time.sleep(0.1)

    while True:
        key = stdscr.getch()

        # 🎮 Movement (STRONGER VALUES)
        if key == ord('w'):
            pitch = min(255, pitch + 25)
        elif key == ord('s'):
            pitch = max(0, pitch - 25)

        elif key == ord('a'):
            roll = max(0, roll - 25)
        elif key == ord('d'):
            roll = min(255, roll + 25)

        elif key == ord('q'):
            yaw = max(0, yaw - 25)
        elif key == ord('e'):
            yaw = min(255, yaw + 25)

        elif key == curses.KEY_UP:
            throttle = min(255, throttle + 5)
        elif key == curses.KEY_DOWN:
            throttle = max(0, throttle - 5)

        elif key == ord('l'):  # land
            for _ in range(20):
                send(command=1)
                time.sleep(0.04)

        elif key == ord('x'):
            break

        # 🧠 Smooth return to neutral (VERY IMPORTANT)
        roll += (128 - roll) * 0.15
        pitch += (128 - pitch) * 0.15
        yaw += (128 - yaw) * 0.15

        send()

        stdscr.addstr(4,0,f"Throttle: {int(throttle)}   ")
        stdscr.addstr(5,0,f"Roll:{int(roll)} Pitch:{int(pitch)} Yaw:{int(yaw)}   ")
        stdscr.refresh()

        time.sleep(0.03)  # FAST loop (pipelined)

curses.wrapper(main)