#!/usr/bin/env python3
"""Verify that render_pdf.py blocks remote HTTP/S resources by default."""
import asyncio
import sys
import threading
import http.server
import pathlib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.resolve()))
from render_pdf import html_to_pdf

hits = []

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        hits.append(self.path)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'OK')
    def log_message(self, *a): pass

def main():
    server = http.server.HTTPServer(('127.0.0.1', 0), Handler)
    port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    temp = Path('/tmp/test_remote_block')
    temp.mkdir(parents=True, exist_ok=True)
    html = f'<!DOCTYPE html><html><body><img src="http://127.0.0.1:{port}/pixel.png"></body></html>'
    html_path = temp / 'remote.html'
    html_path.write_text(html)

    async def run():
        hits.clear()
        pdf_block = await html_to_pdf(str(html_path), str(temp / 'blocked.pdf'), block_remote=True)
        blocked = len(hits)

        hits.clear()
        pdf_allow = await html_to_pdf(str(html_path), str(temp / 'allowed.pdf'), block_remote=False)
        allowed = len(hits)

        print(f'Blocked hits: {blocked}')
        print(f'Allowed hits: {allowed}')

        assert blocked == 0, f'Expected 0 hits when blocked, got {blocked}'
        assert allowed >= 1, f'Expected >=1 hits when allowed, got {allowed}'
        print('PASS')

    asyncio.run(run())
    server.shutdown()
    return 0

if __name__ == '__main__':
    sys.exit(main())
