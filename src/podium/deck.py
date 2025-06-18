import hashlib

import toga

def size_for_aspect(aspect):
    return (984 if aspect == '16:9' else 738, 576)


def gtk_key_press_event(widget, event):
    # GTK WebViews eat keyboard press events.
    from toga_gtk.libs import Gdk
    if event.keyval == Gdk.KEY_Right:
        widget.interface.app.next_slide(None)
    elif event.keyval == Gdk.KEY_Left:
        widget.interface.app.previous_slide(None)
    elif event.keyval == Gdk.KEY_Home:
        widget.interface.app.first_slide(None)
    elif event.keyval == Gdk.KEY_End:
        widget.interface.app.last_slide(None)
    elif event.keyval == Gdk.KEY_Escape:
        widget.interface.app.stop(None)

    return False


class PrimarySlideWindow(toga.DocumentWindow):
    def __init__(self, doc, secondary):
        self.secondary = secondary
        super().__init__(
            doc=doc,
            size=size_for_aspect(doc.aspect),
        )
        self.create()

    def create(self):
        self.html_view = toga.WebView(flex=1)

        # GTK WebViews eat key press events; propegate them to a handler
        if toga.platform.current_platform == "linux":
            self.html_view._impl.native.connect("key_press_event", gtk_key_press_event)

        self.content = self.html_view

    @property
    def template_path(self):
        return self.doc.resource_path / "slide-template.html"

    def html_content(self):
        with self.template_path.open('r', encoding="utf-8") as data:
            template = data.read()

        html = template.format(
            resource_path=self.doc.resource_path,
            theme=self.doc.theme,
            aspect_ratio_tag=self.doc.aspect.replace(':', '-'),
            aspect_ratio=self.doc.aspect,
            title=self.doc.title,
            slide_content=self.doc.content,
            slide_number=self.doc.current_slide,
        )

        return html.encode("utf-8")

    def redraw(self):
        self.html_view.url = f"{self.doc.base_url}/slides"

    def close(self):
        self.secondary.close()
        super().close()


class SecondarySlideWindow(toga.Window):
    def __init__(self, doc):
        self.doc = doc
        super().__init__(
            size=size_for_aspect(doc.aspect),
            closable=False
        )
        self.create()

    @property
    def _default_title(self) -> str:
        return self.doc.title + " - Speaker notes"

    def create(self):
        self.html_view = toga.WebView(flex=1)

        # GTK WebViews eat key press events; propegate them to a handler
        if toga.platform.current_platform == "linux":
            self.html_view._impl.native.connect("key_press_event", gtk_key_press_event)

        self.content = self.html_view

    @property
    def template_path(self):
        return self.doc.resource_path / "notes-template.html"

    def html_content(self):
        with self.template_path.open('r', encoding='utf-8') as data:
            template = data.read()

        html = template.format(
            resource_path=self.doc.resource_path,
            theme=self.doc.theme,
            aspect_ratio_tag=self.doc.aspect.replace(':', '-'),
            aspect_ratio=self.doc.aspect,
            title=self.doc.title,
            slide_content=self.doc.content,
            slide_number=self.doc.current_slide,
        )
        return html.encode("utf-8")

    def redraw(self):
        self.html_view.url = f"{self.doc.base_url}/notes"


class SlideDeck(toga.Document):
    description = "Slide Deck"
    extensions = ["podium", "md"]

    def create(self):
        # TODO: There's only 1 theme.
        self.theme = 'default'
        self.aspect = '16:9'
        self.reversed_displays = False
        self.paused = False
        self.current_slide = 1
        self.content = ""

        self.secondary_window = SecondarySlideWindow(self)
        self.main_window = PrimarySlideWindow(self, self.secondary_window)

    @property
    def file_sha(self):
        return hashlib.sha256(str(self.path).encode("utf-8")).hexdigest()[:20]

    @property
    def resource_path(self):
        return self.app.paths.app / 'resources'

    def read(self):
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

        # main window title will be automatically updated;
        # manually update secondary window title
        self.secondary_window.title = self.secondary_window._default_title

    def show(self):
        self.redraw()

        self.main_window.show()
        self.secondary_window.show()

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
        if self.app.in_presentation_mode:
            self.reversed_displays = not self.reversed_displays
            if self.reversed_displays:
                self.app.enter_presentation_mode([self.secondary_window, self.main_window])
            else:
                self.app.enter_presentation_mode([self.main_window, self.secondary_window])
        else:
            print('Not in full screen mode')

    def change_aspect_ratio(self):
        print("Switch aspect ratio")
        if self.aspect == '16:9':
            self.aspect = '4:3'
        else:
            self.aspect = '16:9'

        if self.app.in_presentation_mode:
            # If we're fullscreen, just reload to apply different
            # aspect-related styles.
            self.reload()
        else:
            new_aspect_size = size_for_aspect(self.aspect)
            self.secondary_window.size = new_aspect_size
            self.main_window.size = new_aspect_size

    def toggle_full_screen(self):
        print("Toggle full screen")
        if self.app.in_presentation_mode:
            self.app.exit_presentation_mode()
            self.app.show_cursor()
        else:
            if self.reversed_displays:
                self.app.enter_presentation_mode([self.secondary_window, self.main_window])
            else:
                self.app.enter_presentation_mode([self.main_window, self.secondary_window])

            self.app.hide_cursor()

    async def reload(self):
        self.read()

        self.current_slide = await self.main_window.html_view.evaluate_javascript("slideshow.getCurrentSlideNo()")

        print("Current slide:", self.current_slide)

        self.redraw()

    def redraw(self):
        self.main_window.redraw()
        self.secondary_window.redraw()

    async def on_key_press(self, widget, key, modifiers):
        print("KEY =", key, "modifiers=", modifiers)
        if key == toga.Key.ESCAPE:
            if self.app.in_presentation_mode:
                self.toggle_full_screen()
            else:
                print('Not in full screen mode')

        elif key == toga.Key.F11:
            self.toggle_full_screen()

        elif key == toga.Key.P and (toga.Key.MOD_1 in modifiers):
            if self.app.in_presentation_mode:
                self.toggle_pause()
            else:
                self.toggle_full_screen()

        elif key == toga.Key.TAB and (toga.Key.MOD_1 in modifiers):
            if self.app.in_presentation_mode:
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

        self.main_window.html_view.evaluate_javascript("slideshow.resetTimer()")
        self.secondary_window.html_view.evaluate_javascript("slideshow.resetTimer()")

    def toggle_pause(self):
        if self.app.in_presentation_mode:
            if self.paused:
                print("Resume presentation")
                self.main_window.html_view.evaluate_javascript("slideshow.resume()")
                self.secondary_window.html_view.evaluate_javascript("slideshow.resume()")
                self.paused = False
            else:
                print("Pause presentation")
                self.main_window.html_view.evaluate_javascript("slideshow.pause()")
                self.secondary_window.html_view.evaluate_javascript("slideshow.pause()")
                self.paused = True
        else:
            print("Presentation not in fullscreen mode; pause/play disabled")

    def goto_first_slide(self):
        print("Goto first slide")

        self.main_window.html_view.evaluate_javascript("slideshow.gotoFirstSlide()")
        self.secondary_window.html_view.evaluate_javascript("slideshow.gotoFirstSlide()")

    def goto_last_slide(self):
        print("Goto previous slide")

        self.main_window.html_view.evaluate_javascript("slideshow.gotoLastSlide()")
        self.secondary_window.html_view.evaluate_javascript("slideshow.gotoLastSlide()")

    def goto_next_slide(self):
        print("Goto next slide")

        self.main_window.html_view.evaluate_javascript("slideshow.gotoNextSlide()")
        self.secondary_window.html_view.evaluate_javascript("slideshow.gotoNextSlide()")

    def goto_previous_slide(self):
        print("Goto previous slide")

        self.main_window.html_view.evaluate_javascript("slideshow.gotoPreviousSlide()")
        self.secondary_window.html_view.evaluate_javascript("slideshow.gotoPreviousSlide()")
