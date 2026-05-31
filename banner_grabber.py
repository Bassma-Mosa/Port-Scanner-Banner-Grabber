import socket


class BannerGrabber:
    def __init__(self, timeout: float = 2.0):
        self.timeout = timeout

    def grab(self, host: str, port: int) -> str:
        """Try to grab the service banner from an open port."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(self.timeout)
                s.connect((host, port))

                # Send a generic HTTP request for web ports
                if port in (80, 8080, 8000):
                    s.send(b"HEAD / HTTP/1.0\r\n\r\n")
                elif port == 443:
                    return "HTTPS (SSL/TLS)"
                else:
                    s.send(b"\r\n")

                banner = s.recv(1024).decode(errors="ignore").strip()
                return banner[:200] if banner else "No banner"

        except Exception:
            return "N/A"
