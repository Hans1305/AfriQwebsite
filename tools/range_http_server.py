from __future__ import annotations

import argparse
import http.server
import mimetypes
import os
import re
import socketserver
import urllib.parse


class RangeRequestHandler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path: str) -> str:
        parsed = urllib.parse.urlsplit(path)
        return super().translate_path(parsed.path)

    def _send_file(self, file_path: str) -> None:
        try:
            file_stat = os.stat(file_path)
        except OSError:
            self.send_error(404, "File not found")
            return

        ctype = self.guess_type(file_path)
        if not ctype:
            ctype = "application/octet-stream"

        range_header = self.headers.get("Range")
        if range_header:
            m = re.match(r"bytes=(\d*)-(\d*)\s*$", range_header)
            if m:
                start_s, end_s = m.group(1), m.group(2)
                size = file_stat.st_size
                if start_s == "" and end_s == "":
                    range_header = None
                else:
                    if start_s == "":
                        suffix = int(end_s)
                        start = max(size - suffix, 0)
                        end = size - 1
                    else:
                        start = int(start_s)
                        end = int(end_s) if end_s != "" else size - 1
                        end = min(end, size - 1)

                    if start >= size or end < start:
                        self.send_response(416)
                        self.send_header("Content-Range", f"bytes */{size}")
                        self.end_headers()
                        return

                    self.send_response(206)
                    self.send_header("Content-Type", ctype)
                    self.send_header("Accept-Ranges", "bytes")
                    self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
                    self.send_header("Content-Length", str(end - start + 1))
                    self.send_header("Last-Modified", self.date_time_string(file_stat.st_mtime))
                    self.end_headers()

                    if self.command == "HEAD":
                        return

                    with open(file_path, "rb") as f:
                        f.seek(start)
                        remaining = end - start + 1
                        chunk_size = 64 * 1024
                        while remaining > 0:
                            chunk = f.read(min(chunk_size, remaining))
                            if not chunk:
                                break
                            self.wfile.write(chunk)
                            remaining -= len(chunk)
                    return

        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Content-Length", str(file_stat.st_size))
        self.send_header("Last-Modified", self.date_time_string(file_stat.st_mtime))
        self.end_headers()

        if self.command == "HEAD":
            return

        with open(file_path, "rb") as f:
            self.copyfile(f, self.wfile)

    def do_HEAD(self) -> None:
        file_path = self.translate_path(self.path)
        if os.path.isdir(file_path):
            return super().do_HEAD()
        return self._send_file(file_path)

    def do_GET(self) -> None:
        file_path = self.translate_path(self.path)
        if os.path.isdir(file_path):
            return super().do_GET()
        return self._send_file(file_path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5500)
    args = parser.parse_args()

    mimetypes.add_type("video/mp4", ".mp4")
    handler = RangeRequestHandler
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.ThreadingTCPServer((args.host, args.port), handler) as httpd:
        httpd.serve_forever()


if __name__ == "__main__":
    main()
