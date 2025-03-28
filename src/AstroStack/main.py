from src.AstroStack.gui import MainWindow
from src.AstroStack.gui.CustomDialogs import OpenPictureDialog
from gi.repository import Gtk, GdkPixbuf
from astropy.io import fits
import numpy as np

class AstroStack(MainWindow.MainWindow):
    def __init__(self):
        super().__init__()

        # Header bar connections
        self.openPictureButton.connect("clicked", self.open_picture)
        self.previewFillButton.connect("clicked", self.preview_fill)

        self.window.connect("size_allocate", self.on_size_allocate)

    def open_picture(self, widget):
        dialog = OpenPictureDialog(self)

        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            file_path = dialog.get_filename()
            if file_path.endswith(".fits"):
                self.originalPreviewPixbuf = self.fits_to_pixbuf(file_path)
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

    def fits_to_pixbuf(self, fits_file):
        """Carica un file FITS e lo converte in un Pixbuf"""
        try:
            # Apri il file FITS e leggi i dati dell'immagine (HDUs)
            with fits.open(fits_file) as hdul:
                image_data = hdul[0].data  # Accede ai dati dell'immagine

            # Normalizza i dati a un intervallo di 0-255 per creare un'immagine in scala di grigi
            image_data = np.clip(image_data, 0, np.max(image_data))  # Evita valori negativi
            image_data = (image_data / np.max(image_data) * 255).astype(np.uint8)

            # Ottieni le dimensioni dell'immagine
            height, width = image_data.shape

            # Converti l'array NumPy in un GdkPixbuf
            pixbuf = GdkPixbuf.Pixbuf.new_from_data(
                image_data.tobytes(),  # Dati in formato byte
                GdkPixbuf.Colorspace.RGB,  # Spazio di colore
                False,  # Nessun canale alpha
                8,  # Profondità del colore
                width,
                height,
                width * 3,  # Stride: numero di byte per riga (3 per RGB)
            )
            return pixbuf
        except Exception as e:
            print(f"Errore durante il caricamento del file FITS: {e}")
            return None

    def on_size_allocate(self, widget, allocation):
        if self.originalPreviewPixbuf:
            self.preview_fill(None)


if __name__ == "__main__":
    app = AstroStack()
    Gtk.main()