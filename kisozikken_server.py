import time
import socket
import json
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta

# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# IP settings
hostname = socket.gethostname()
hostname, alias_list, ipaddr_list = socket.gethostbyname_ex(hostname)
logging.info(f"Host IP addresses: {ipaddr_list}")

LOCALHOST = socket.gethostbyname(socket.gethostname())
MULTICAST_IP = "適宜設定する"
MULTI_PORT = "適宜設定する"

# Transmission settings
logging.info("-----------Transmission Settings-------------")
PACKET_SIZE = 1000
PACKETS_PER_CYCLE = 750
TOTAL_CYCLES = 120

# UDP socket creation
udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_sock.bind(('0.0.0.0', MULTI_PORT))  # Bind for multicast communication

# Dictionary to store cycle start times
cycle_start_times = {}

def send_packets(chunks, cycle):
    for i, chunk in enumerate(chunks):
        chunk = chunk.ljust(PACKET_SIZE, '\0')
        msg = {
            "cycle": cycle,
            "sequence_number": i,
            "datas": chunk
        }
        send_json_message = json.dumps(msg)
        try:
            udp_sock.sendto(send_json_message.encode(), (MULTICAST_IP, MULTI_PORT))
            if i % 100 == 0:
                logging.info(f"Sent packet {i} of cycle {cycle}")
        except Exception as e:
            logging.error(f"Send error: {e}")
        time.sleep(0.05)

def get_japan_time():
    # UTC時間を取得し、日本時間（UTC+9）に変換
    utc_time = datetime.utcnow()
    japan_time = utc_time + timedelta(hours=9)
    return japan_time

def main():
    chunks = []
    FILE_NAME = 'sendingFile_750KB.txt'
    with open(FILE_NAME, 'r') as f:
        for line in f:
            line = line.strip()
            chunks.append(line[:PACKET_SIZE])

    for cycle in range(TOTAL_CYCLES):
        japan_time = get_japan_time()
        cycle_start_times[cycle] = f"{japan_time.hour:02d}-{japan_time.minute:02d}"

        logging.info(f"Starting cycle {cycle + 1} at {cycle_start_times[cycle]}")
        send_packets(chunks, cycle)
        time.sleep(1)

    # Print all cycle start times
    logging.info("Cycle start times:")
    for cycle, start_time in cycle_start_times.items():
        logging.info(f"Cycle {cycle}: {start_time}")

if __name__ == "__main__":
    main()
