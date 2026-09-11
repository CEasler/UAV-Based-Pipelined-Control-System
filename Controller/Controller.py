import socket
import time
import curses

DRONE_IP = "192.168.1.1"
DRONE_PORT = 7099

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

roll = 128
yaw = 128
pitch = 128
throttle = 140   # IMPORTANT: baseline hover (adjust 140–155)
mode = 2
command = 0

def create_packet(roll, yaw, throttle, pitch, command, mode):
    packet = [0] * 21

    packet[0] = 0x03
    packet[1] = 0x66
    packet[2] = 0x14

    packet[3] = int(roll)
    packet[4] = int(yaw)
    packet[5] = int(throttle)
    packet[6] = int(pitch)

    packet[7] = int(command)
    packet[8] = int(mode)

    checksum = packet[3] ^ packet[4] ^ packet[5] ^ packet[6] ^ packet[7] ^ packet[8]
    packet[19] = checksum
    packet[20] = 0x99

    return bytes(packet)

def send_packet():
    pkt = create_packet(roll, yaw, throttle, pitch, command, mode)
    sock.sendto(pkt, (DRONE_IP, DRONE_PORT))

def main(stdscr):
    global roll, yaw, pitch, throttle, command

    curses.cbreak()
    stdscr.nodelay(True)
    stdscr.clear()

    stdscr.addstr(0, 0, "Drone Controller (X to quit)")
    stdscr.addstr(1, 0, "T = takeoff | Arrow keys = throttle")

    # 🚀 TAKEOFF BURST
    stdscr.addstr(3, 0, "Taking off...")
    stdscr.refresh()
    for _ in range(20):
        pkt = create_packet(roll, yaw, throttle, pitch, 1, mode)
        sock.sendto(pkt, (DRONE_IP, DRONE_PORT))
        time.sleep(0.05)

    command = 0

    while True:
        key = stdscr.getch()


        # Forward / Back
        if key == ord('w'):
            pitch = min(255, pitch + 50)
        elif key == ord('s'):
            pitch = max(0, pitch - 50)

        # Left / Right
        elif key == ord('a'):
            roll = max(0, roll - 15)
        elif key == ord('d'):
            roll = min(255, roll + 15)

        # Yaw
        elif key == ord('q'):
            yaw = max(0, yaw - 15)
        elif key == ord('e'):
            yaw = min(255, yaw + 15)

        # Throttle
        elif key == curses.KEY_UP:
            throttle = min(255, throttle + 5)
        elif key == curses.KEY_DOWN:
            throttle = max(0, throttle - 5)

        # Land (send command pulse)
        elif key == ord('l'):
            for _ in range(10):
                pkt = create_packet(roll, yaw, throttle, pitch, 1, mode)
                sock.sendto(pkt, (DRONE_IP, DRONE_PORT))
                time.sleep(0.05)

        # Exit
        elif key == ord('x'):
            break

        roll += (128 - roll) * 0.2
        pitch += (128 - pitch) * 0.2
        yaw += (128 - yaw) * 0.2

        # Send packet continuously
        send_packet()

        # Display
        stdscr.addstr(5, 0, f"Throttle: {int(throttle)}     ")
        stdscr.addstr(6, 0, f"Roll: {int(roll)} Pitch: {int(pitch)} Yaw: {int(yaw)}     ")
        stdscr.refresh()

        time.sleep(0.05)

curses.wrapper(main)