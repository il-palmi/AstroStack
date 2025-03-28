from gi.repository import Gtk

class FileSelectorDialog(Gtk.FileChooserDialog):
    def __init__(self, parent_widget: Gtk.Window, multiple_files: bool):
        super().__init__()
        self.title = "Please choose a file"
        self.parent = parent_widget
        self.action = Gtk.FileChooserAction.OPEN

        self.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN,
            Gtk.ResponseType.OK,
        )

        # Filter files by image extension
        filter_image = Gtk.FileFilter()
        filter_image.set_name("File immagine")
        filter_image.add_mime_type("image/png")
        filter_image.add_mime_type("image/jpeg")
        filter_image.add_mime_type("image/tiff")
        filter_image.add_mime_type("image/x-fits")
        filter_image.add_pattern("*.png")
        filter_image.add_pattern("*.jpg")
        filter_image.add_pattern("*.jpeg")
        filter_image.add_pattern("*.tif")
        filter_image.add_pattern("*.tiff")
        filter_image.add_pattern("*.cr2")

        self.add_filter(filter_image)

        self.set_select_multiple(multiple_files)