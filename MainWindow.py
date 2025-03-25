import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class MainWindow(Gtk.Application):
    def __init__(self):
        super().__init__()
        # GLib.set_application_name("AstroStack")
        builder = Gtk.Builder()
        builder.add_from_file("ui/mainWindow.glade")

        self.window = builder.get_object("mainWindow")
        self.window.connect("destroy", Gtk.main_quit)

        self.openPictureButton = builder.get_object("openPictureButton")


        self.window.show_all()