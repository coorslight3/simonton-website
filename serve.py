"""Static file server for previewing site/ that disables browser caching."""
import functools, http.server, sys

class NoCache(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, max-age=0')
        super().end_headers()

port = int(sys.argv[1]) if len(sys.argv) > 1 else 8123
handler = functools.partial(NoCache, directory='site')
http.server.ThreadingHTTPServer(('', port), handler).serve_forever()
