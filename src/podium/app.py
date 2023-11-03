from http import HTTPStatus
from http.server import HTTPServer, SimpleHTTPRequestHandler
from threading import Event, Thread
import re
import webbrowser

import toga

from podium.deck import SlideDeck


class DeckHTTPHandler(SimpleHTTPRequestHandler):
    DECK_URL_RE = re.compile(r"^/deck/([a-z\d]+)/(slides|notes|print)$")

    def do_GET(self):
        # Look for the URLs for dynamic deck content:
        #     /deck/<id>/slides
        #     /deck/<id>/notes
        #     /deck/<id>/print
        # If you find one of those, defer to the deck to build the
        # content dynamically, and build the GET response. All other
        # content is served statically; however, the path to that
        # content will be different depending on whether it's
        # builtin content or deck content.
        match = self.DECK_URL_RE.match(self.path)
        if match:
            deck = self.server.app.deck_for_id(match[1])
            if match[2] == "slides":
                content = deck.window_1.html_content()
            elif match[2] == "notes":
                content = deck.window_2.html_content()
            elif match[2] == "print":
                content = deck.html_content()
            else:
                self.send_error(HTTPStatus.NOT_FOUND, f"Unknown deck content {match[2]!r}")
                return
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.send_header("Content-Length", len(content))
            self.end_headers()
            self.wfile.write(content)
        else:
            #
            super().do_GET()

    def translate_path(self, path):
        if path == "/favicon.ico":
            # Favicon is a special case
            return str(self.server.resources_path / "podium.png")
        elif path.startswith('/resources/'):
            # Any URL starting with /resources/ is static app-based content
            return str(self.server.resources_path / path[11:])
        elif path.startswith('/deck/'):
            # Any URL starting with /deck is deck-based content, except for
            # the slide/notes/print dynamic content, which is handled by do_GET
            try:
                parts = path.split('/', 3)
                deck = self.server.app.deck_for_id(parts[2])
                return f"{deck.path}/{parts[3]}"
            except KeyError:
                self.send_error(HTTPStatus.NOT_FOUND, "Deck not found")
                return None
        else:
            # Any other URL is unknown content.
            self.send_error(HTTPStatus.NOT_FOUND, "File not found")
            return None

    def end_headers(self):
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()


class PodiumHTTPServer(HTTPServer):
    def __init__(self, app):
        self.app = app
        # Use port 0 to let the server select an available port.
        super().__init__(("127.0.0.1", 0), DeckHTTPHandler)

    @property
    def resources_path(self):
        return self.app.paths.app / "resources"


class Podium(toga.DocumentApp):
    def __init__(self):
        super().__init__(
            document_types={'podium': SlideDeck},
        )

        self.server_exists = Event()
        self.server_thread = Thread(target=self.web_server)
        self.server_thread.start()

        self.on_exit = self.cleanup

        self.server_exists.wait()
        self.server_host, self.server_port = self._httpd.socket.getsockname()
        print(f"Serving on {self.server_host}:{self.server_port}")

    # Web server #####################################################

    def web_server(self):
        print("Starting server...")
        self._httpd = PodiumHTTPServer(self)
        # The server is now listening, but connections will block until
        # serve_forever is run.
        self.server_exists.set()
        self._httpd.serve_forever()

    def cleanup(self, app, **kwargs):
        print("Shutting down...")
        self._httpd.shutdown()
        return True

    def deck_for_id(self, deck_id):
        return {
            doc.file_sha: doc
            for doc in self.documents
        }[deck_id]

    # FILE commands ##################################################

    async def reload(self, widget, **kwargs):
        await self.current_window.deck.reload()

    def print(self, widget, **kwargs):
        webbrowser.open(f"{self.current_window.deck.base_url}/print")

    # PLAY commands ##################################################

    def play(self, widget, **kwargs):
        self.play_command.enabled = False
        self.stop_command.enabled = True
        self.current_window.deck.toggle_full_screen()

    def stop(self, widget, **kwargs):
        self.play_command.enabled = True
        self.stop_command.enabled = False
        self.current_window.deck.toggle_full_screen()

    def reset_timer(self, widget, **kwargs):
        self.current_window.deck.reset_timer()

    def next_slide(self, widget, **kwargs):
        self.current_window.deck.goto_next_slide()

    def previous_slide(self, widget, **kwargs):
        self.current_window.deck.goto_previous_slide()

    def first_slide(self, widget, **kwargs):
        self.current_window.deck.goto_first_slide()

    def last_slide(self, widget, **kwargs):
        self.current_window.deck.goto_last_slide()

    # VIEW commands ##################################################

    def switch_screens(self, widget, **kwargs):
        self.current_window.deck.switch_screens()

    def change_aspect_ratio(self, widget, **kwargs):
        self.current_window.deck.change_aspect_ratio()

    def startup(self):
        play_group = toga.Group('Play', order=31)
        view_group = toga.Group('View', order=32)

        self.commands.add(
            toga.Command(
                self.reload,
                text='Reload slide deck',
                shortcut=toga.Key.MOD_1 + 'r',
                group=toga.Group.FILE,
                section=1
            ),
            toga.Command(
                self.print,
                text='Print...',
                shortcut=toga.Key.MOD_1 + 'p',
                group=toga.Group.FILE,
                section=2
            ),
        )
        self.play_command = toga.Command(
                self.play,
                text='Play slideshow',
                shortcut=toga.Key.MOD_1 + 'P',
                group=play_group,
                section=0,
                order=0,
            )
        self.stop_command = toga.Command(
                self.stop,
                text='Stop slideshow',
                shortcut=toga.Key.ESCAPE,
                group=play_group,
                section=0,
                order=1,
                enabled=False,
            )
        self.commands.add(
            self.play_command,
            self.stop_command,
            toga.Command(
                self.reset_timer,
                text='Reset timer',
                shortcut=toga.Key.MOD_1 + 't',
                group=play_group,
                section=0,
                order=2,
            ),
            toga.Command(
                self.next_slide,
                text='Next slide',
                shortcut=toga.Key.RIGHT,
                group=play_group,
                section=1,
                order=0,
            ),
            toga.Command(
                self.previous_slide,
                text='Previous slide',
                shortcut=toga.Key.LEFT,
                group=play_group,
                section=1,
                order=1,
            ),
            toga.Command(
                self.first_slide,
                text='First slide',
                shortcut=toga.Key.HOME,
                group=play_group,
                section=1,
                order=2,
            ),
            toga.Command(
                self.last_slide,
                text='Last slide',
                shortcut=toga.Key.END,
                group=play_group,
                section=1,
                order=3,
            ),
        )
        self.commands.add(
            toga.Command(
                self.switch_screens,
                text='Switch screens',
                shortcut=toga.Key.MOD_1 + toga.Key.TAB,
                group=view_group,
            ),
            toga.Command(
                self.change_aspect_ratio,
                text='Change aspect ratio',
                shortcut=toga.Key.MOD_1 + 'a',
                group=view_group,
            ),
        )


def main():
    return Podium()
