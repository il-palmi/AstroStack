import MainWindow
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class AstroStack(MainWindow.MainWindow):
    def __init__(self):
        super().__init__()

        self.openPictureButton.connect("clicked", self.open_picture)

    def open_picture(self, widget):
        print("open picture")


app = AstroStack()
Gtk.main()