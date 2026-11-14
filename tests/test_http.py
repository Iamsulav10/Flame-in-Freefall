"""Start and probe the server inside one process/network test environment."""

import json
import socket
import subprocess
import sys
import time
import unittest
from http.cookies import SimpleCookie
from pathlib import Path
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]


class HttpSmokeTest(unittest.TestCase):
    def test_server_starts_and_serves_without_application_error(self):
        with socket.socket() as probe:
            probe.bind(("127.0.0.1", 0))
            port = probe.getsockname()[1]
        process = subprocess.Popen(
            [sys.executable, "-m", "streamlit", "run", "app.py",
             "--server.address", "127.0.0.1", "--server.port", str(port),
             "--server.headless", "true"], cwd=ROOT,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        )
        try:
            deadline = time.monotonic() + 15
            ready = False
            while time.monotonic() < deadline:
                try:
                    with urlopen(f"http://127.0.0.1:{port}/_stcore/health", timeout=1) as response:
                        ready = response.status == 200 and response.read() == b"ok"
                    if ready:
                        break
                except OSError:
                    if process.poll() is not None:
                        break
                    time.sleep(0.2)
            self.assertTrue(ready, "Local health endpoint did not become ready")
            with urlopen(f"http://127.0.0.1:{port}/", timeout=3) as response:
                self.assertEqual(response.status, 200)
                body = response.read().decode()
                self.assertIn("text/html", response.headers["Content-Type"])
                self.assertIn("<html", body)
                cookies = SimpleCookie()
                for header in response.headers.get_all("Set-Cookie", []):
                    cookies.load(header)
                # Record names/attributes, never random cookie values.
                observation = {
                    "health_status": 200, "root_status": 200,
                    "cookie_attributes": {
                        name: {key: value for key, value in item.items() if value}
                        for name, item in cookies.items()
                    },
                    "scope": "Initial local HTTP requests only; no browser session or public host tested",
                }
                (ROOT / "reports" / "http-check.json").write_text(json.dumps(observation, indent=2) + "\n")
        finally:
            process.terminate()
            try:
                process.communicate(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.communicate()


if __name__ == "__main__":
    unittest.main()
