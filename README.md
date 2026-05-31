# 🔍 Port Scanner + Banner Grabber

A fast, multi-threaded port scanner with service banner grabbing — built in Python using OOP and concurrent threading.

> ⚠️ **For educational and authorized use only.** Only scan systems you have explicit permission to test.

---

## ✨ Features

- ⚡ Multi-threaded scanning (default: 100 threads)
- 🏷️ Service banner grabbing (HTTP, SSH, FTP, etc.)
- 🎯 Preset port lists: `top20`, `top100`, `full`
- 📊 Clean summary output
- 💾 JSON export for reports
- 🧱 OOP design — easy to extend

---

## 🚀 Usage

```bash
# Scan top 20 common ports (default)
python main.py scanme.nmap.org

# Scan specific ports
python main.py 192.168.1.1 -p 22,80,443

# Scan a port range
python main.py 192.168.1.1 -p 1-1024

# Full scan with 200 threads
python main.py 192.168.1.1 -p full -t 200

# Save results to JSON
python main.py scanme.nmap.org -o results.json

# Verbose mode (show all ports)
python main.py scanme.nmap.org -v
```

---

## 📦 Installation

```bash
git clone https://github.com/yourusername/port-scanner.git
cd port-scanner
python main.py --help
```

No external dependencies — uses Python standard library only.

---

## 📁 Project Structure

```
port-scanner/
├── scanner/
│   ├── __init__.py
│   ├── port_scanner.py   ← Core scanner with threading
│   └── banner_grabber.py ← Banner grabbing logic
├── main.py               ← CLI entry point
└── README.md
```

---

## 🖥️ Example Output

```
============================================================
       🔍 PORT SCANNER + BANNER GRABBER
       ⚠️  For authorized targets only!
============================================================

🔍 Scanning scanme.nmap.org (45.33.32.156) — 20 ports | Threads: 100

------------------------------------------------------------
  [OPEN  ] 22     SSH             SSH-2.0-OpenSSH_6.6.1p1
  [OPEN  ] 80     HTTP            HTTP/1.1 200 OK

============================================================
✅ Scan complete in 3.12s
🟢 Open ports: 2 / 20
```

---

## 📄 License

MIT License — free to use and modify.
