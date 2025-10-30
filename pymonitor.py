import requests
import time
import socket
import sys
from datetime import datetime
from options.header import *

prev_data = {"ip": None, "server": None, "size": None, "time": []}

def get_ip(domain):
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror:
        return "Tidak bisa resolve IP"

def spinner_animation(target, duration=3):
    spinner = ["|", "/", "-", "\\"]
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        sys.stdout.write(f"\r[{spinner[i % len(spinner)]}] Monitoring {target}...")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    sys.stdout.write("\r" + " " * 50 + "\r")  # hapus spinner

def monitor(url):
    try:
        start = time.time()
        response = requests.get(url, timeout=5)
        elapsed = time.time() - start
        size = len(response.content)
        server = response.headers.get("Server", "Unknown")
        content_type = response.headers.get("Content-Type", "Unknown")
        ip = get_ip(url.replace("https://", "").replace("http://", "").split("/")[0])

        print(f"{g}[{datetime.now().strftime('%H:%M:%S')}]{rs} Monitoring   : {url}")
        print(f"{g}[{datetime.now().strftime('%H:%M:%S')}]{rs} Status       : {response.status_code} ({'OK' if response.status_code == 200 else 'WARN'})")
        print(f"{g}[{datetime.now().strftime('%H:%M:%S')}]{rs} Waktu respon : {elapsed:.2f} detik")
        print(f"{g}[{datetime.now().strftime('%H:%M:%S')}]{rs} Ukuran data  : {size} bytes")
        print(f"{g}[{datetime.now().strftime('%H:%M:%S')}]{rs} Server       : {server}")
        print(f"{g}[{datetime.now().strftime('%H:%M:%S')}]{rs} Tipe konten  : {content_type}")
        print(f"{g}[{datetime.now().strftime('%H:%M:%S')}]{rs} Alamat IP    : {ip}")

        anomalies = []
        if prev_data["ip"] and ip != prev_data["ip"]:
            anomalies.append("IP address berubah!")
        if prev_data["server"] and server != prev_data["server"]:
            anomalies.append("Server header berubah!")
        if prev_data["size"] and abs(size - prev_data["size"]) > prev_data["size"] * 0.3:
            anomalies.append("Ukuran halaman berubah signifikan!")
        if prev_data["time"]:
            avg_time = sum(prev_data["time"]) / len(prev_data["time"])
            if elapsed > avg_time * 2:
                anomalies.append("Waktu respon 2x lebih lambat dari rata-rata!")

        if anomalies:
            print("\nANOMALI TERDETEKSI:")
            for a in anomalies:
                print(f"   {a}")
            print("="*60)

        prev_data["ip"] = ip
        prev_data["server"] = server
        prev_data["size"] = size
        prev_data["time"].append(elapsed)
        if len(prev_data["time"]) > 10:
            prev_data["time"].pop(0)

        with open("webpulse_log.txt", "a") as f:
            f.write(f"[{datetime.now()}] {url} | Status: {response.status_code} | "
                    f"Time: {elapsed:.2f}s | Size: {size} | IP: {ip}\n")
            if anomalies:
                f.write(f"  >> ANOMALY: {', '.join(anomalies)}\n")

    except requests.exceptions.RequestException as e:
        print("="*60)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {url} DOWN!")
        print(f"Error: {e}")
        print("="*60)
        with open("webpulse_log.txt", "a") as f:
            f.write(f"[{datetime.now()}] {url} | DOWN | Error: {e}\n")

def main():
    while True:
        try:
            clean_screen()
            header()
            target = input("[?] Masukkan URL website: ").strip()
            if not target:
                print("URL tidak boleh kosong!")
                continue

            print("\n[+] Memulai monitoring...\n")
            spinner_animation(target, duration=3)
            monitor(target)

            tanya = input("\n[?] Ulangi monitoring? (y/n) ").lower()
            if tanya == "y":
                continue
            elif tanya == "n":
                print("[!] Keluar dari tools...")
                time.sleep(0.5)
                break
        except KeyboardInterrupt:
            print("\n[!] Alat monitoring dihentikan")
            break

if __name__ == "__main__":
    main()
