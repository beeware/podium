from podium.deck import *

# class SlideView(toga.Window):
#     def __init__(self, title=None, position=(100, 100), size=(640, 480)):
#         super().__init__(title, position, size)

#     def on_close(self):
#         app = NSApplication.sharedApplication()
#         app.terminate_(self._delegate)


class Podium(toga.App):
    def __init__(self):
        resource_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        super().__init__(
            'Podium',
            app_id='org.beeware.podium',
            icon=toga.Icon(os.path.join(resource_dir, 'podium.icns')),
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
