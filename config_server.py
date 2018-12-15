#!/usr/bin/env python3

import http.server
import json
config_file = "nightview.json"

def server_start(handler):
    httpd = http.server.HTTPServer(("", 8000), handler)
    httpd.serve_forever()

class ConfigHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # self.send_header("Content-Type", "application/json")
        config = open(config_file, "r")
        self.wfile.write(bytes(config.read().encode("utf-8")))
        config.close()
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length).decode("utf-8")
        self.send_response(200)
        self.end_headers()
        config = json.loads(body)
        self.update_config(config)
        return
    def update_config(self, new_config):
        with open(config_file, "r") as f:
            config = json.load(f)

        for key in config:
            try:
                config[key] = new_config[key]
            except KeyError:
                pass
        with open(config_file, "w") as fp:
            json.dump(config, fp=fp)




if __name__ == "__main__":
    server_start(ConfigHandler)
