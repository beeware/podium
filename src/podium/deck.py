from pathlib import Path
import hashlib

import toga
from toga.style import Pack


class PrimarySlideWindow(toga.MainWindow):
    def __init__(self, deck, secondary):
        self.deck = deck
        self.secondary = secondary
        super().__init__(
            title=self.deck.title,
            position=(200, 200),
            size=(984 if self.deck.aspect == '16:9' else 738, 576)
        )
        self.create()

    def create(self):
        self.html_view = toga.WebView(
            style=Pack(
                flex=1,
                width=984 if self.deck.aspect == '16:9' else 738,
                height=576
            ),
        )
        self.content = self.html_view

    @property
    def template_path(self):
        return self.deck.resource_path / "slide-template.html"

    def html_content(self):
        with self.template_path.open('r', encoding="utf-8") as data:
            template = data.read()

        html = template.format(
            resource_path=self.deck.resource_path,
            theme=self.deck.theme,
            aspect_ratio_tag=self.deck.aspect.replace(':', '-'),
            aspect_ratio=self.deck.aspect,
            title=self.deck.title,
            slide_content=self.deck.content,
            slide_number=self.deck.current_slide,
        )

        return html.encode("utf-8")

    def redraw(self):
        self.html_view.url = f"{self.deck.base_url}/slides"

    def on_close(self):
        self.secondary.close()


class SecondarySlideWindow(toga.Window):
    def __init__(self, deck):
        self.deck = deck
        super().__init__(
            title=self.deck.title + ": Speaker notes",
            position=(100, 100),
            size=(984 if self.deck.aspect == '16:9' else 738, 576),
            closable=False
        )
        self.create()

    def create(self):
        self.html_view = toga.WebView(
            style=Pack(
                flex=1,
                width=984 if self.deck.aspect == '16:9' else 738,
                height=576
            ),
        )
        self.content = self.html_view

    @property
    def template_path(self):
        return self.deck.resource_path / "notes-template.html"

    def html_content(self):
        with self.template_path.open('r', encoding='utf-8') as data:
            template = data.read()

        html = template.format(
            resource_path=self.deck.resource_path,
            theme=self.deck.theme,
            aspect_ratio_tag=self.deck.aspect.replace(':', '-'),
            aspect_ratio=self.deck.aspect,
            title=self.deck.title,
            slide_content=self.deck.content,
            slide_number=self.deck.current_slide,
        )
        return html.encode("utf-8")

    def redraw(self):
        self.html_view.url = f"{self.deck.base_url}/notes"


class SlideDeck(toga.Document):
    def __init__(self, path, app):
        super().__init__(
            path=path,
            document_type='Podium Slide Deck',
            app=app,
        )

    def create(self):
        self.aspect = '16:9'
        self.window_2 = SecondarySlideWindow(self)
        self.window_1 = PrimarySlideWindow(self, self.window_2)

        self.reversed_displays = False
        self.paused = False
        self.current_slide = 1

    @property
    def file_sha(self):
        return hashlib.sha256(str(self.path).encode("utf-8")).hexdigest()[:20]

    @property
    def title(self):
        return self.path.stem

    @property
    def resource_path(self):
        return self.app.paths.app / 'resources'

    def read(self):
        # TODO: There's only 1 theme.
        self.theme = 'default'
        if self.path.is_dir():
            # Multi-file .podium files must contain slides.md;
            # may contain style.css
            contentFile = self.path / "slides.md"

            print(f"Loading content from {contentFile}")
            with open(contentFile, 'r', encoding='utf-8') as f:
                self.content = f.read()
        else:
            # Single file can just be a standalone markdown file
            print(f"Loading content from {self.path}")
            with self.path.open('r', encoding='utf-8') as f:
                self.content = f.read()

    def show(self):
        self.window_1.redraw()
        self.window_1.show()

        self.window_2.redraw()
        self.window_2.show()

    @property
    def base_url(self):
        return f'http://{self.app.server_host}:{self.app.server_port}/deck/{self.file_sha}'

    @property
    def print_template_path(self):
        return self.resource_path / "print-template.html"

    def html_content(self):
        with self.print_template_path.open('r', encoding='utf-8') as data:
            template = data.read()

        html = template.format(
            resource_path=self.resource_path,
            theme=self.theme,
            aspect_ratio_tag=self.aspect.replace(':', '-'),
            aspect_ratio=self.aspect,
            title=self.title,
            slide_content=self.content,
            slide_number=self.current_slide,
        )
        return html.encode("utf-8")

    def switch_screens(self):
        print("Switch screens")
        if self.app.is_full_screen:
            self.reversed_displays = not self.reversed_displays
            if self.reversed_displays:
                self.app.set_full_screen(self.window_2, self.window_1)
            else:
                self.app.set_full_screen(self.window_1, self.window_2)
        else:
            print('Not in full screen mode')

    def change_aspect_ratio(self):
        print("Switch aspect ratio")
        if self.aspect == '16:9':
            self.aspect = '4:3'
        else:
            self.aspect = '16:9'

        if self.app.is_full_screen:
            # If we're fullscreen, just reload to apply different
            # aspect-related styles.
            self.reload()
        else:
            # If we're not fullscreen, we need to re-create the
            # display windows with the correct aspect ratio.
            self.window_1.close()

            self.window_2 = SecondarySlideWindow(self)
            self.window_1 = PrimarySlideWindow(self, self.window_2)

            self.window_1.app = self.app
            self.window_2.app = self.app

            self.show()

    def toggle_full_screen(self):
        print("Toggle full screen")
        if self.app.is_full_screen:
            self.app.exit_full_screen()
            self.app.show_cursor()
        else:
            if self.reversed_displays:
                self.app.set_full_screen(self.window_2, self.window_1)
            else:
                self.app.set_full_screen(self.window_1, self.window_2)

            self.app.hide_cursor()

    async def reload(self):
        self.read()

        self.current_slide = await self.window_1.html_view.evaluate_javascript("slideshow.getCurrentSlideNo()")

        print("Current slide:", self.current_slide)

        self.redraw()

    def redraw(self):
        self.window_1.redraw()
        self.window_2.redraw()

    async def on_key_press(self, widget, key, modifiers):
        print("KEY =", key, "modifiers=", modifiers)
        if key == toga.Key.ESCAPE:
            if self.app.is_full_screen:
                self.toggle_full_screen()
            else:
                print('Not in full screen mode')

        elif key == toga.Key.F11:
            self.toggle_full_screen()

        elif key == toga.Key.P and (toga.Key.MOD_1 in modifiers):
            if self.app.is_full_screen:
                self.toggle_pause()
            else:
                self.toggle_full_screen()

        elif key == toga.Key.TAB and (toga.Key.MOD_1 in modifiers):
            if self.app.is_full_screen:
                self.switch_screens()
            else:
                print('Not in full screen mode')

        elif key == toga.Key.A and (toga.Key.MOD_1 in modifiers):
            self.change_aspect_ratio()

        elif key in (
            toga.Key.RIGHT,
            toga.Key.DOWN,
            toga.Key.SPACE,
            toga.Key.ENTER,
            toga.Key.PAGE_DOWN
        ):
            self.goto_next_slide()

        elif key in (toga.Key.LEFT, toga.Key.UP, toga.Key.PAGE_UP):
            self.goto_previous_slide()

        elif key == toga.Key.HOME:
            self.goto_first_slide()

        elif key == toga.Key.END:
            self.goto_last_slide()

        elif key == toga.Key.R and (toga.Key.MOD_1 in modifiers):
            await self.reload()

        elif key == toga.Key.T and (toga.Key.MOD_1 in modifiers):
            self.reset_timer()

    def reset_timer(self):
        print("Reset Timer")

        self.window_1.html_view.evaluate_javascript("slideshow.resetTimer()")
        self.window_2.html_view.evaluate_javascript("slideshow.resetTimer()")

    def toggle_pause(self):
        if self.app.is_full_screen:
            if self.paused:
                print("Resume presentation")
                self.window_1.html_view.evaluate_javascript("slideshow.resume()")
                self.window_2.html_view.evaluate_javascript("slideshow.resume()")
                self.paused = False
            else:
                print("Pause presentation")
                self.window_1.html_view.evaluate_javascript("slideshow.pause()")
                self.window_2.html_view.evaluate_javascript("slideshow.pause()")
                self.paused = True
        else:
            print("Presentation not in fullscreen mode; pause/play disabled")

    def goto_first_slide(self):
        print("Goto first slide")

        self.window_1.html_view.evaluate_javascript("slideshow.gotoFirstSlide()")
        self.window_2.html_view.evaluate_javascript("slideshow.gotoFirstSlide()")

    def goto_last_slide(self):
        print("Goto previous slide")

        self.window_1.html_view.evaluate_javascript("slideshow.gotoLastSlide()")
        self.window_2.html_view.evaluate_javascript("slideshow.gotoLastSlide()")

    def goto_next_slide(self):
        print("Goto next slide")

        self.window_1.html_view.evaluate_javascript("slideshow.gotoNextSlide()")
        self.window_2.html_view.evaluate_javascript("slideshow.gotoNextSlide()")

    def goto_previous_slide(self):
        print("Goto previous slide")

        self.window_1.html_view.evaluate_javascript("slideshow.gotoPreviousSlide()")
        self.window_2.html_view.evaluate_javascript("slideshow.gotoPreviousSlide()")
