import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf
from typing import cast

class MainWindow(Gtk.Application):
    def __init__(self):
        super().__init__()
        builder = Gtk.Builder()
        builder.add_from_file("src/AstroStack/gui/mainWindow.glade")

        # Main window
        self.window = cast(Gtk.Window, builder.get_object("mainWindow"))
        self.window.connect("destroy", Gtk.main_quit)
        self.window.set_default_size(400, 300)
        self.window.set_resizable(True)

        # Containers
        self.mainBox = cast(Gtk.Box, builder.get_object("mainBox"))
        self.toolBox = cast(Gtk.Box, builder.get_object("toolBox"))

        # Header bar
        self.headerBar = cast(Gtk.HeaderBar, builder.get_object("headerBar"))
        self.openPictureButton = builder.get_object("openPictureButton")
        self.homeButton = cast(Gtk.Button, builder.get_object("homeButton"))
        self.previewFillButton = cast(Gtk.Button, builder.get_object("previewFillButton"))

        # Image viewer
        self.previewScrolledWindow = cast(Gtk.ScrolledWindow, builder.get_object("previewScrolledWindow"))
        self.previewViewport = cast(Gtk.Viewport, builder.get_object("previewViewport"))
        self.previewImage = cast(Gtk.Image, builder.get_object("previewImage"))
        self.originalPreviewPixbuf = None

        # Lights tree view
        self.lightsTreeView = cast(Gtk.TreeView, builder.get_object("lightsTreeView"))
        self.add_treeview_column(self.lightsTreeView, "File name", 0)
        self.add_treeview_column(self.lightsTreeView, "File type", 1)
        self.add_treeview_column(self.lightsTreeView, "Date", 2)
        self.add_treeview_column(self.lightsTreeView, "Path", 3)


        # Pictures tab
        self.lightsButton = cast(Gtk.Button, builder.get_object("lightsButton"))
        self.darksButton = cast(Gtk.Button, builder.get_object("darksButton"))
        self.flatsButton = cast(Gtk.Button, builder.get_object("flatsButton"))
        self.biasButton = cast(Gtk.Button, builder.get_object("biasButton"))

        # Init window
        self.window.show_all()

    @staticmethod
    def add_treeview_column(treeview, titolo, col_index):
        """Crea e aggiunge una colonna al TreeView."""
        renderer = Gtk.CellRendererText()  # Renderer per testo
        column = Gtk.TreeViewColumn(titolo, renderer, text=col_index)
        column.set_sort_column_id(col_index)  # Abilita l'ordinamento
        treeview.append_column(column)