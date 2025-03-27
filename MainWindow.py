import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from typing import cast

class MainWindow(Gtk.Application):
    def __init__(self):
        super().__init__()
        builder = Gtk.Builder()
        builder.add_from_file("ui/mainWindow.glade")

        # Main window
        self.window = cast(Gtk.Window, builder.get_object("mainWindow"))
        self.window.connect("destroy", Gtk.main_quit)
        self.window.set_default_size(400, 300)
        self.window.set_resizable(True)

        # Containers
        self.mainBox = cast(Gtk.Box, builder.get_object("mainBox"))
        self.toolBox = cast(Gtk.Box, builder.get_object("toolBox"))

        # Header bar
        self.openPictureButton = builder.get_object("openPictureButton")
        self.homeButton = cast(Gtk.Button, builder.get_object("homeButton"))
        self.previewFillButton = cast(Gtk.Button, builder.get_object("previewFillButton"))

        # Image viewer
        self.previewScrolledWindow = cast(Gtk.ScrolledWindow, builder.get_object("previewScrolledWindow"))
        self.previewViewport = cast(Gtk.Viewport, builder.get_object("previewViewport"))
        self.previewImage = cast(Gtk.Image, builder.get_object("previewImage"))
        self.originalPreviewPixbuf = None

        # Init window
        self.window.show_all()