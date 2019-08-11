import os
from urllib.parse import quote

import toga
from toga.style import Pack

import podium


class SlideWindow(toga.Window):
    def __init__(self, deck, master):
        self.deck = deck
        self.master = master
        title = os.path.splitext(os.path.basename(deck.filename))[0]

        if not master:
            title += ": Speaker notes"
        super().__init__(
            title=title,
            position=(200, 200) if master else (100, 100),
            size=(984 if self.deck.aspect == '16:9' else 738, 576),
            # FIXME: This should be False; but doing so
            # enforces a constraint on the full screen window.
            # When a formal "full screen" API is introduced,
            # this can be restored.
            # resizeable=False,
            closeable=True if master else None
        )
        self.create()

    def create(self):
        self.html_view = toga.WebView(
            style=Pack(
                flex=1,
                width=984 if self.deck.aspect == '16:9' else 738,
                height=576
            ),
            on_key_down=self.deck.on_key_press
        )
        self.content = self.html_view

    @property
    def template_name(self):
        if self.master:
            return "slide-template.html"
        else:
            return "notes-template.html"

    def redraw(self, slide='1'):
        with open(os.path.join(self.deck.resource_path, self.template_name), 'r') as data:
            template = data.read()

        content = template.format(
            resource_path=os.path.join(self.deck.resource_path),
            theme=self.deck.theme,
            style_overrides=self.deck.style_overrides,
            aspect_ratio_tag=self.deck.aspect.replace(':', '-'),
            aspect_ratio=self.deck.aspect,
            slide_content=self.deck.content,
            slide_number=slide,
        )

        self.html_view.set_content(self.deck.fileURL, content)

    def on_close(self):
        if self.master:
            self.deck.window_2._impl.close()


class SlideDeck(toga.Document):
    def __init__(self, filename, app):
        super().__init__(
            filename=filename,
            document_type='Podium Slide Deck',
            app=app,
        )

        self.aspect = '16:9'
        self.window_2 = SlideWindow(self, master=False)
        self.window_2.app = self.app
        self.window_1 = SlideWindow(self, master=True)
        self.window_1.app = self.app

        self.reversed_displays = False
        self.paused = False

    @property
    def resource_path(self):
        return os.path.join(
            os.path.dirname(os.path.abspath(podium.__file__)),
            'resources',
        )

    def read(self):
        # TODO: There's only 1 theme.
        self.theme = 'default'
        if os.path.isdir(self.filename):
            # Multi-file .podium files must contain slides.md;
            # may contain style.css
            styleFile = os.path.join(self.filename, "style.css")
            contentFile = os.path.join(self.filename, "slides.md")

            with open(contentFile, 'r', encoding='utf-8') as f:
                self.content = f.read()

            if os.path.exists(styleFile):
                with open(styleFile, 'r', encoding='utf-8') as f:
                    self.style_overrides = f.read()
            else:
                self.style_overrides = ''
        else:
            # Single file can just be a standalone markdown file
            with open(self.filename, 'r', encoding='utf-8') as f:
                self.content = f.read()
            self.style_overrides = ''

    def show(self):
        self.window_1.redraw()
        self.window_1.show()

        self.window_2.redraw()
        self.window_2.show()

    @property
    def fileURL(self):
        return 'file://{}/'.format(quote(self.filename))

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
            self.window_1._impl.close()

            self.window_2 = SlideWindow(self, master=False)
            self.window_1 = SlideWindow(self, master=True)

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

    def reload(self):
        self.read()

        slide = self.window_1.html_view.evaluate("slideshow.getCurrentSlideNo()")
        print("Current slide:", slide)

        self.redraw(slide)

    def redraw(self, slide=None):
        self.window_1.redraw(slide)
        self.window_2.redraw(slide)

    def on_key_press(self, key, modifiers):
        print("KEY =", key, "modifiers=", modifiers)
        if key == toga.Key.ESCAPE:
            if self.app.is_full_screen:
                self.toggle_full_screen()
            else:
                print('Not in full screen mode')

        elif key == toga.Key.P and (toga.Key.COMMAND in modifiers):
            if self.app.is_full_screen:
                self.toggle_pause()
            else:
                self.toggle_full_screen()

        elif key == toga.Key.TAB and (toga.Key.COMMAND in modifiers):
            if self.app.is_full_screen:
                self.switch_screens()
            else:
                print('Not in full screen mode')

        elif key == toga.Key.A and (toga.Key.COMMAND in modifiers):
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

        elif key == toga.Key.R and (toga.Key.COMMAND in modifiers):
            self.reload()

        elif key == toga.Key.T and (toga.Key.COMMAND in modifiers):
            self.reset_timer()

    def reset_timer(self):
        print("Reset Timer")

        self.window_1.html_view.evaluate("slideshow.resetTimer()")
        self.window_2.html_view.evaluate("slideshow.resetTimer()")

    def toggle_pause(self):
        if self.app.is_full_screen:
            if self.paused:
                print("Resume presentation")
                self.window_1.html_view.evaluate("slideshow.resume()")
                self.window_2.html_view.evaluate("slideshow.resume()")
                self.paused = False
            else:
                print("Pause presentation")
                self.window_1.html_view.evaluate("slideshow.pause()")
                self.window_2.html_view.evaluate("slideshow.pause()")
                self.paused = True
        else:
            print("Presentation not in fullscreen mode; pause/play disabled")

    def goto_first_slide(self):
        print("Goto first slide")

        self.window_1.html_view.evaluate("slideshow.gotoFirstSlide()")
        self.window_2.html_view.evaluate("slideshow.gotoFirstSlide()")

    def goto_last_slide(self):
        print("Goto previous slide")

        self.window_1.html_view.evaluate("slideshow.gotoLastSlide()")
        self.window_2.html_view.evaluate("slideshow.gotoLastSlide()")

    def goto_next_slide(self):
        print("Goto next slide")

        self.window_1.html_view.evaluate("slideshow.gotoNextSlide()")
        self.window_2.html_view.evaluate("slideshow.gotoNextSlide()")

    def goto_previous_slide(self):
        print("Goto previous slide")

        self.window_1.html_view.evaluate("slideshow.gotoPreviousSlide()")
        self.window_2.html_view.evaluate("slideshow.gotoPreviousSlide()")
