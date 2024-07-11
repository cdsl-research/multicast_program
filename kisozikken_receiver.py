import network
import usocket as socket
import uasyncio as asyncio
import json
import machine
import utime
import select
import gc

# Global variables
sta_if = network.WLAN(network.STA_IF)
rssi_status = 0
received_sequence_number = ""
received_data = ""
first_packet_received = False
received_data_list = []
current_cycle = -1



# TCP server settings
tcp_server_port = "適宜設定する"

def inet_aton(ip):
    parts = [int(part) for part in ip.split('.')]
    return bytes(parts)

def connect_wifi(ssid, password):
    global sta_if
    if not sta_if.isconnected():
        print('Connecting to WiFi...')
        sta_if.active(True)
        sta_if.connect(ssid, password)
        while not sta_if.isconnected():
            pass
        machine.Pin(2, machine.Pin.OUT).value(1)  # Assuming the blue LED is connected to GPIO pin 2

    print('Network configuration:', sta_if.ifconfig())
    return sta_if

async def receive_multicast(mcast_sock):
    global sta_if, rssi_status, current_cycle, received_data_list

    while True:
        try:
            data, addr = mcast_sock.recvfrom(2048)
            if data:
                rssi_status = sta_if.status("rssi")
                current_time = utime.ticks_ms()
                received_message = json.loads(data.decode('utf-8'))
                
                cycle = received_message["cycle"]
                sequence_number = received_message["sequence_number"]

                if cycle > current_cycle or (cycle == 0 and current_cycle == 119):
                    if received_data_list:
                        write_to_csv(f"7_02_E7/received_data_{current_cycle + 1}.csv", received_data_list)
                        received_data_list = []
                    current_cycle = cycle
                    print(f"Starting new cycle: {current_cycle}")

                received_data_list.append({
                    "cycle": cycle,
                    "sequence_number": sequence_number,
                    "rssi": rssi_status,
                    "time": current_time
                })

                if sequence_number % 100 == 0:
                    print(f"Received packet {sequence_number} of cycle {cycle}")

                if sequence_number == 749:
                    print(f"Completed cycle {cycle}")

        except Exception as e:
            print(f"Error receiving multicast message: {type(e).__name__}, {str(e)}")

async def main():
    ssid = "ssid"
    password = "password"
    MULTICAST_IP = "適宜設定する"
    MULTI_PORT = "適宜設定する"
    sta_if = connect_wifi(ssid, password)

    if sta_if.isconnected():
        mcast_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        mcast_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        mreq = inet_aton(MULTICAST_IP) + inet_aton('0.0.0.0')
        mcast_sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        mcast_sock.bind(('0.0.0.0', MULTI_PORT))

        print("Starting multicast reception...")
        await receive_multicast(mcast_sock)
    else:
        print("Failed to connect to Wi-Fi")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Error running main: {e}")
    machine.Pin(2, machine.Pin.OUT).value(0)
        



