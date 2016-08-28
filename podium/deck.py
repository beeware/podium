import os
from ctypes import cast, c_char_p
from rubicon.objc import ObjCClass, objc_classmethod, objc_method
from colosseum import CSS

import toga
from toga_cocoa.libs import NSDocument, NSURL, NSScreen, NSDictionary, NSNumber, NSCursor, NSCommandKeyMask


class TogaSlideDeck(NSDocument):

    @objc_method
    def autosavesInPlace(self) -> bool:
        return True

    @objc_method
    def readFromFileWrapper_ofType_error_(self, fileWrapper, typeName, outError) -> bool:
        print("Read from File Wrapper: %s" % fileWrapper.filename)
        print("   type: %s" % typeName)

        if fileWrapper.isDirectory:
            # Multi-file .podium files must contain slides.md; may contain theme.css
            themeFile = fileWrapper.fileWrappers.valueForKey_("theme.css")
            contentFile = fileWrapper.fileWrappers.valueForKey_("slides.md")
            if contentFile is None:
                return False

            self.content = cast(contentFile.regularFileContents.bytes, c_char_p).value.decode('utf-8')
            if themeFile is None:
                print("NO THEME FILE")
                defaultThemeFileName = "%s/Contents/Resources/default.css" % NSBundle.mainBundle.bundlePath

                self.theme = NSString.alloc().initWithContentsOfFile_encoding_error_(defaultThemeFileName, NSUTF8StringEncoding, None)
            else:
                self.theme = cast(themeFile.regularFileContents.bytes, c_char_p).value.decode('utf-8')

            return True

        return False

class SlideWindow(toga.Window):
    def __init__(self, deck, master):
        self.deck = deck
        self.master = master
        super().__init__("Slides" if master else "Notes",
            position=(200, 200) if master else (100, 100),
            size=(738, 576),
            resizeable=False,
            closeable=True if master else None
        )

    def startup(self):
        super().startup()
        self.content = toga.Container()
        self.html_view = toga.WebView(
            style=CSS(flex=1),
            on_key_down=self.deck.on_key_press
        )
        self.content.add(self.html_view)

    @property
    def template_name(self):
        if self.master:
            return "slide-template.html"
        else:
            return "notes-template.html"

    def redraw(self, slide='1'):
        with open(os.path.join(self.app.resource_path, 'templates', self.template_name), 'r') as data:
            template = data.read()

        content = template % (
            os.path.join(self.app.resource_path, 'templates'),
            self.deck._impl.theme,
            self.deck._impl.content,
            os.path.join(self.app.resource_path, 'templates'),
            slide
        )

        self.html_view.set_content(self.deck._impl.fileURL.absoluteString + '/', content)

    def on_close(self):
        if self.master:
            self.deck.window_2.close()


class SlideDeck:
    def __init__(self, url):
        self.window_2 = SlideWindow(self, master=False)
        self.window_1 = SlideWindow(self, master=True)

        self._app = None

        self.full_screen = False
        self.reversed_displays = False
        self.paused = False

        self.url = url
        self._impl = TogaSlideDeck.alloc().initWithContentsOfURL_ofType_error_(NSURL.URLWithString_(url), "Podium Slide Deck", None)
        self._impl._interface = self

    @property
    def app(self):
        return self._app

    @app.setter
    def app(self, app):
        if self._app:
            raise Exception("Window is already associated with an App")

        self._app = app
        self.window_1.app = app
        self.window_2.app = app

    def show(self):
        self.window_1.redraw()
        self.window_1.show()

        self.window_2.redraw()
        self.window_2.show()

    def switchScreens(self):
        if self.full_screen:
            primaryScreen = NSScreen.screens().objectAtIndex_(0)
            secondaryScreen = NSScreen.screens().objectAtIndex_(1)

            opts = NSDictionary.dictionaryWithObjectsAndKeys_(
                NSNumber.numberWithBool_(True),
                "NSFullScreenModeAllScreens",
                None
            )

            self.window_1.html_view._impl.exitFullScreenModeWithOptions_(opts)
            self.window_2.html_view._impl.exitFullScreenModeWithOptions_(opts)

            if self.reversed_displays:
                self.window_1.html_view._impl.enterFullScreenMode_withOptions_(primaryScreen, opts)
                self.window_2.html_view._impl.enterFullScreenMode_withOptions_(secondaryScreen, opts)
            else:
                self.window_1.html_view._impl.enterFullScreenMode_withOptions_(secondaryScreen, opts)
                self.window_2.html_view._impl.enterFullScreenMode_withOptions_(primaryScreen, opts)
                self.reversed_displays = not self.reversed_displays

            self.window_1.html_view._update_layout(
                width=self.window_1.html_view._impl.frame.size.width,
                height=self.window_1.html_view._impl.frame.size.height
            )

    def toggleFullScreen(self):
        primaryScreen = NSScreen.screens().objectAtIndex_(0)
        secondaryScreen = NSScreen.screens().objectAtIndex_(1)

        opts = NSDictionary.dictionaryWithObjectsAndKeys_(
            NSNumber.numberWithBool_(True),
            "NSFullScreenModeAllScreens",
            None
        )

        if self.full_screen:
            self.window_1.html_view._impl.exitFullScreenModeWithOptions_(opts)
            self.window_2.html_view._impl.exitFullScreenModeWithOptions_(opts)

            NSCursor.unhide()
        else:
            if self.reversed_displays:
                self.window_1.html_view._impl.enterFullScreenMode_withOptions_(secondaryScreen, opts)
                self.window_2.html_view._impl.enterFullScreenMode_withOptions_(primaryScreen, opts)
            else:
                self.window_1.html_view._impl.enterFullScreenMode_withOptions_(primaryScreen, opts)
                self.window_2.html_view._impl.enterFullScreenMode_withOptions_(secondaryScreen, opts)

            self.full_screen = not self.full_screen
            NSCursor.hide()

        self.window_1.html_view._update_layout(
            width=self.window_1.html_view._impl.frame.size.width,
            height=self.window_1.html_view._impl.frame.size.height
        )
        self.window_2.html_view._update_layout(
            width=self.window_2.html_view._impl.frame.size.width,
            height=self.window_2.html_view._impl.frame.size.height
        )

    def reload(self):
        self._impl.readFromURL_ofType_error_(self._impl.fileURL, self._impl.fileType, None)

        slide = self.window_1.html_view.evaluate("slideshow.getCurrentSlideNo()")
        print("Current slide:", slide)

        self.redraw(slide)

    def redraw(self, slide=None):
        self.window_1.redraw(slide)
        self.window_2.redraw(slide)

    def on_key_press(self, key_code, modifiers):
        if key_code == 53:  # escape
            if self.full_screen:
                self.toggleFullScreen()

        elif key_code == 35:
            if self.full_screen:
                self.togglePause()
            else:
                self.toggleFullScreen()

        elif key_code in (7, 48):  # X or <tab>
            self.switchScreens()

        elif key_code in (124, 125, 49, 35):  # <Right>, <Down>, <space>, <Enter>
            self.gotoNextSlide()

        elif key_code in (123, 126):  # <left>, <up>
            self.gotoPreviousSlide()

        elif key_code == 115:  # <home>
            self.gotoFirstSlide()

        elif key_code == 119:  # <end>
            self.gotoLastSlide()

        elif key_code == 15 and (modifiers & NSCommandKeyMask):  # CTRL-R
            self.reload()

        elif key_code == 17:  # T
            self.resetTimer()

    def resetTimer(self):
        print("Reset Timer")

        self.window_1.html_view.evaluate("slideshow.resetTimer()")
        self.window_2.html_view.evaluate("slideshow.resetTimer()")

    def togglePause(self):
        if self.full_screen:
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

    def gotoFirstSlide(self):
        print("Goto first slide")

        self.window_1.html_view.evaluate("slideshow.gotoFirstSlide()")
        self.window_2.html_view.evaluate("slideshow.gotoFirstSlide()")

    def gotoLastSlide(self):
        print("Goto previous slide")

        self.window_1.html_view.evaluate("slideshow.gotoLastSlide()")
        self.window_2.html_view.evaluate("slideshow.gotoLastSlide()")

    def gotoNextSlide(self):
        print("Goto next slide")

        self.window_1.html_view.evaluate("slideshow.gotoNextSlide()")
        self.window_2.html_view.evaluate("slideshow.gotoNextSlide()")

    def gotoPreviousSlide(self):
        print("Goto previous slide")

        self.window_1.html_view.evaluate("slideshow.gotoPreviousSlide()")
        self.window_2.html_view.evaluate("slideshow.gotoPreviousSlide()")
