import socket
import time

DRONE_IP = "192.168.1.1"
DRONE_PORT = 7099

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

roll = 128
yaw = 128
pitch = 128
throttle = 145
mode = 2

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

def send_packet(roll, yaw, throttle, pitch, command=0):
    pkt = create_packet(roll, yaw, throttle, pitch, command, mode)
    sock.sendto(pkt, (DRONE_IP, DRONE_PORT))


print("Taking off...")
for _ in range(25):
    send_packet(128, 150, throttle, 128, command=1)
    time.sleep(0.1)

packet_count = 0
start_time = time.time()

print("Stage 1: Forward")
for _ in range(15):
    send_packet(155, 220, throttle, 128)
    packet_count += 1
    time.sleep(0.1)


print("Stage 2: spin")
for _ in range(20):  # send burst
    send_packet(128, 128, throttle, 210)
    packet_count += 1
    time.sleep(0.1)




print("Stage 3: Backward")
for _ in range(20):
    send_packet(128, 230, throttle, 128)
    packet_count += 1
    time.sleep(0.1)



print("Stage 4: Descend")
for _ in range(20):
    send_packet(128, 128, 120, 128)
    packet_count += 1
    time.sleep(0.05)

print("Landing...")
for _ in range(20):
    send_packet(128, 128, 120, 128, command=1)
    time.sleep(0.05)

total_time = time.time() - start_time
print(f"Flight complete in {total_time:.2f} seconds")
print(f"Packets sent: {packet_count}")
print(f"Throughput: {packet_count / total_time:.2f} packets/sec")