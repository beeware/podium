from podium.deck import *

# class SlideView(toga.Window):
#     def __init__(self, title=None, position=(100, 100), size=(640, 480)):
#         super().__init__(title, position, size)

#     def on_close(self):
#         app = NSApplication.sharedApplication()
#         app.terminate_(self._delegate)


class Podium(toga.App):
    def __init__(self):
        super().__init__(
            'Podium',
            app_id='org.pybee.podium',
            icon=toga.Icon(os.path.join(os.path.dirname(__file__), 'icons', 'podium.icns')),
            document_types=['podium']
        )

    def startup(self):
        pass

    def open_document(self, fileURL):
        # print("open doc", fileURL)
        document = SlideDeck(fileURL)
        self.add_document(document)
        document.show()

def main():
    return Podium()
