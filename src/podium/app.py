import toga

from podium.deck import SlideDeck


class Podium(toga.DocumentApp):
    def __init__(self):
        super().__init__(
            document_types={'podium': SlideDeck},
        )

    # FILE commands ##################################################

    async def reload(self, widget, **kwargs):
        await self.current_window.deck.reload()

    # PLAY commands ##################################################

    def play(self, widget, **kwargs):
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
                label='Reload slide deck',
                shortcut=toga.Key.MOD_1 + 'r',
                group=toga.Group.FILE,
                section=1
            ),
        )
        self.commands.add(
            toga.Command(
                self.play,
                label='Play slideshow',
                shortcut=toga.Key.MOD_1 + 'p',
                group=play_group,
                section=0,
                order=0,
            ),
            toga.Command(
                self.reset_timer,
                label='Reset timer',
                shortcut=toga.Key.MOD_1 + 't',
                group=play_group,
                section=0,
                order=1,
            ),
            toga.Command(
                self.next_slide,
                label='Next slide',
                shortcut=toga.Key.RIGHT,
                group=play_group,
                section=1,
                order=0,
            ),
            toga.Command(
                self.previous_slide,
                label='Previous slide',
                shortcut=toga.Key.LEFT,
                group=play_group,
                section=1,
                order=1,
            ),
            toga.Command(
                self.first_slide,
                label='First slide',
                shortcut=toga.Key.HOME,
                group=play_group,
                section=1,
                order=2,
            ),
            toga.Command(
                self.last_slide,
                label='Last slide',
                shortcut=toga.Key.END,
                group=play_group,
                section=1,
                order=3,
            ),
        )
        self.commands.add(
            toga.Command(
                self.switch_screens,
                label='Switch screens',
                shortcut=toga.Key.MOD_1 + toga.Key.TAB,
                group=view_group,
            ),
            toga.Command(
                self.change_aspect_ratio,
                label='Change aspect ratio',
                shortcut=toga.Key.MOD_1 + 'a',
                group=view_group,
            ),
        )


def main():
    return Podium()
