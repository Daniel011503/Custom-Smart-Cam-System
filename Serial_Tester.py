import time, serial

PORT = "COM3"   # change if needed
BAUD = 115200

def send_and_read(s, cmd, wait_lines=2):
    s.write((cmd + "\n").encode())
    lines = []
    t0 = time.time()
    while len(lines) < wait_lines and time.time() - t0 < 1.0:
        line = s.readline().decode(errors="ignore").strip()
        if line:
            lines.append(line)
    print(f"{cmd} -> {lines}")

with serial.Serial(PORT, BAUD, timeout=0.2) as s:
    time.sleep(2)
    # Always good to ask status first
    send_and_read(s, "<STATUS>")
    send_and_read(s, "<ARM:1>")
    send_and_read(s, "<STATUS>")
    send_and_read(s, "<ALARM:ON>")
    time.sleep(0.5)
    send_and_read(s, "<STATUS>")
    send_and_read(s, "<ALARM:OFF>")
    send_and_read(s, "<ARM:0>")
    send_and_read(s, "<STATUS>")
