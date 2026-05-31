#!/usr/bin/env python3
"""
Port Scanner + Banner Grabber
Author: Your Name
GitHub: https://github.com/yourusername/port-scanner
"""

import argparse
import json
import sys
from datetime import datetime

from scanner import PortScanner


# Preset port ranges
PRESETS = {
    "top20": [21,22,23,25,53,80,110,143,443,445,
              3306,3389,5432,6379,8080,8443,27017,8000,9200,5900],
    "top100": list(range(1, 1025)),
    "full": list(range(1, 65536)),
}


def parse_ports(port_arg: str):
    """Parse port argument: '80', '80,443', '1-1024', or preset name."""
    if port_arg in PRESETS:
        return PRESETS[port_arg]

    ports = set()
    for part in port_arg.split(","):
        part = part.strip()
        if "-" in part:
            start, end = part.split("-")
            ports.update(range(int(start), int(end) + 1))
        else:
            ports.add(int(part))
    return sorted(ports)


def export_json(report, filename: str):
    data = {
        "host": report.host,
        "ip": report.ip,
        "scan_time": datetime.now().isoformat(),
        "open_ports": [
            {"port": r.port, "service": r.service, "banner": r.banner}
            for r in report.open_ports
        ],
    }
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
    print(f"\n💾 Results saved to {filename}")


def main():
    parser = argparse.ArgumentParser(
        description="🔍 Port Scanner + Banner Grabber",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("host", help="Target host or IP (e.g. scanme.nmap.org)")
    parser.add_argument(
        "-p", "--ports",
        default="top20",
        help="Ports to scan:\n  top20       - 20 common ports (default)\n  top100      - ports 1-1024\n  full        - all 65535 ports\n  80,443      - specific ports\n  1-1000      - port range",
    )
    parser.add_argument("-t", "--threads", type=int, default=100, help="Number of threads (default: 100)")
    parser.add_argument("--timeout", type=float, default=1.0, help="Socket timeout in seconds (default: 1.0)")
    parser.add_argument("--no-banner", action="store_true", help="Skip banner grabbing")
    parser.add_argument("-o", "--output", help="Save results to JSON file")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show all ports (including closed)")

    args = parser.parse_args()

    print("=" * 60)
    print("       🔍 PORT SCANNER + BANNER GRABBER")
    print("       ⚠️  For authorized targets only!")
    print("=" * 60)

    try:
        ports = parse_ports(args.ports)
        scanner = PortScanner(
            timeout=args.timeout,
            threads=args.threads,
            grab_banners=not args.no_banner,
        )

        start = datetime.now()
        report = scanner.scan(args.host, ports, verbose=args.verbose)
        duration = (datetime.now() - start).total_seconds()

        # Summary
        print("\n" + "=" * 60)
        print(f"✅ Scan complete in {duration:.2f}s")
        print(f"🟢 Open ports: {len(report.open_ports)} / {len(ports)}")

        if report.open_ports:
            print("\n📋 Open Ports Summary:")
            print(f"  {'PORT':<8} {'SERVICE':<15} {'BANNER'}")
            print("  " + "-" * 50)
            for r in report.open_ports:
                banner = r.banner[:50] if r.banner and r.banner != "N/A" else "-"
                print(f"  {r.port:<8} {r.service:<15} {banner}")

        if args.output:
            export_json(report, args.output)

    except ValueError as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⛔ Scan interrupted by user.")
        sys.exit(0)


if __name__ == "__main__":
    main()
