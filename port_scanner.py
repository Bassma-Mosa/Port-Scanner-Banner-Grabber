import socket
import threading
from dataclasses import dataclass, field
from typing import List
from concurrent.futures import ThreadPoolExecutor, as_completed

from .banner_grabber import BannerGrabber


# Common ports and their service names
COMMON_SERVICES = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
    53: "DNS", 80: "HTTP", 110: "POP3", 143: "IMAP",
    443: "HTTPS", 445: "SMB", 3306: "MySQL", 3389: "RDP",
    5432: "PostgreSQL", 6379: "Redis", 8080: "HTTP-Alt",
    8443: "HTTPS-Alt", 27017: "MongoDB",
}


@dataclass
class ScanResult:
    port: int
    state: str          # open / closed
    service: str
    banner: str = ""

    def __str__(self):
        banner_info = f" | Banner: {self.banner}" if self.banner and self.banner != "N/A" else ""
        return f"  [{self.state.upper():6}] {self.port:<6} {self.service:<15}{banner_info}"


@dataclass
class ScanReport:
    host: str
    ip: str
    results: List[ScanResult] = field(default_factory=list)

    @property
    def open_ports(self):
        return [r for r in self.results if r.state == "open"]


class PortScanner:
    def __init__(self, timeout: float = 1.0, threads: int = 100, grab_banners: bool = True):
        self.timeout = timeout
        self.threads = threads
        self.grab_banners = grab_banners
        self.banner_grabber = BannerGrabber(timeout=timeout)
        self._lock = threading.Lock()

    def resolve(self, host: str) -> str:
        """Resolve hostname to IP."""
        try:
            return socket.gethostbyname(host)
        except socket.gaierror:
            raise ValueError(f"Cannot resolve host: {host}")

    def _scan_port(self, host: str, port: int) -> ScanResult:
        """Scan a single port."""
        service = COMMON_SERVICES.get(port, "Unknown")
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(self.timeout)
                result = s.connect_ex((host, port))
                if result == 0:
                    banner = self.banner_grabber.grab(host, port) if self.grab_banners else ""
                    return ScanResult(port=port, state="open", service=service, banner=banner)
                else:
                    return ScanResult(port=port, state="closed", service=service)
        except Exception:
            return ScanResult(port=port, state="closed", service=service)

    def scan(self, host: str, ports: List[int], verbose: bool = False) -> ScanReport:
        """Scan multiple ports using threads."""
        ip = self.resolve(host)
        report = ScanReport(host=host, ip=ip)

        print(f"\n🔍 Scanning {host} ({ip}) — {len(ports)} ports | Threads: {self.threads}\n")
        print("-" * 60)

        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = {executor.submit(self._scan_port, host, port): port for port in ports}
            for future in as_completed(futures):
                result = future.result()
                with self._lock:
                    report.results.append(result)
                    if verbose or result.state == "open":
                        print(result)

        # Sort by port number
        report.results.sort(key=lambda r: r.port)
        return report
