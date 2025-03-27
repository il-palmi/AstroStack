import MainWindow
from gi.repository import Gtk, GdkPixbuf
from astropy.io import fits
import numpy as np

class AstroStack(MainWindow.MainWindow):
    def __init__(self):
        super().__init__()

        # Header bar connections
        self.openPictureButton.connect("clicked", self.open_picture)
        self.previewFillButton.connect("clicked", self.preview_fill)

    def open_picture(self, widget):
        dialog = Gtk.FileChooserDialog(
            title="Please choose a file", parent=self.window, action=Gtk.FileChooserAction.OPEN
        )

        dialog.add_buttons(
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
        dialog.add_filter(filter_image)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            file_path = dialog.get_filename()

            if file_path.endswith(".fits"):
                self.originalPreviewPixbuf = self.load_fits_image(file_path)
            else:
                self.originalPreviewPixbuf = GdkPixbuf.Pixbuf.new_from_file(file_path)

            self.preview_fill(None)

        dialog.destroy()

    def preview_fill(self, widget):
        # get scrolled window size
        allocation = self.previewScrolledWindow.get_allocation()

        # get image size
        pixbuf_width = self.originalPreviewPixbuf.get_width()
        pixbuf_height = self.originalPreviewPixbuf.get_height()

        # compute scale factor
        scale_factor = min(allocation.width / pixbuf_width, allocation.height / pixbuf_height)

        # resize image
        scaledPixbuf = self.originalPreviewPixbuf.scale_simple(pixbuf_width * scale_factor, pixbuf_height * scale_factor,
                                                               GdkPixbuf.InterpType.HYPER)

        self.previewImage.set_from_pixbuf(scaledPixbuf)

    def load_fits_image(self, file_path):
        """Carica un file FITS e lo converte in un Pixbuf"""
        try:
            hdul = fits.open(file_path)
            data = hdul[0].data

            # Se l'immagine è bidimensionale
            if data.ndim == 2:
                # Normalizzare i valori su una scala [0, 255] per immagine in scala di grigi
                data = data - np.min(data)
                data = (data / np.max(data) * 255).astype(np.uint8)

                # Convertire l'array NumPy in un formato GdkPixbuf
                height, width = data.shape
                image_surface = GdkPixbuf.Pixbuf.new_from_data(
                    data.tobytes(),
                    GdkPixbuf.Colorspace.RGB,
                    False,  # No alpha channel
                    8,  # 8 bit per canale
                    width,
                    height,
                    width * 1,  # rowstride (numero di byte per riga)
                )
                return image_surface
            else:
                print("L'immagine FITS non è bidimensionale e non può essere visualizzata.")
        except Exception as e:
            print(f"Errore durante il caricamento del file FITS: {e}")
        return None


app = AstroStack()
Gtk.main()