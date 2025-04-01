import os.path
from datetime import datetime, timezone

from src.AstroStack.gui import MainWindow
from src.AstroStack.gui.CustomDialogs import FileSelectorDialog
from src.AstroStack.utils.flags import *
from gi.repository import Gtk, GdkPixbuf
from astropy.io import fits
import numpy as np


class AstroStack(MainWindow.MainWindow):
    def __init__(self):
        super().__init__()

        # Tables data
        self.lightsListStore = FilesListStore()
        self.lightsTreeView.set_model(self.lightsListStore)
        self.darksListStore = FilesListStore()
        self.flatsListStore = FilesListStore()
        self.biasListStore = FilesListStore()

        # Header bar connections
        self.openPictureButton.connect("clicked", self.open_picture)
        self.previewFillButton.connect("clicked", self.preview_fill)

        # Pictures buttons connections
        self.lightsButton.connect("clicked", self.select_files)
        self.window.connect("size_allocate", self.on_size_allocate)

    def open_picture(self, widget):
        dialog = FileSelectorDialog(parent_widget=self, multiple_files=False)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            file_path = dialog.get_filename()
            if file_path.endswith(".fits"):
                self.originalPreviewPixbuf = self.fits_to_pixbuf(file_path)
            else:
                self.originalPreviewPixbuf = GdkPixbuf.Pixbuf.new_from_file(file_path)
            self.preview_fill(None)
            self.headerBar.set_subtitle(file_path)
        dialog.destroy()

    def select_files(self, widget: Gtk.Button):
        dialog = FileSelectorDialog(parent_widget=self, multiple_files=True)
        response = dialog.run()
        frames_type = widget.get_label().lower()

        if response == Gtk.ResponseType.OK:
            files = dialog.get_filenames()

            match frames_type:
                case t if t == LIGHTS:
                    self.lightsListStore.add_files(files)
                case t if t == DARKS:
                    self.darksListStore.add_files(files)
                case t if t == FLATS:
                    self.flatsListStore.add_files(files)
                case t if t == BIAS:
                    self.biasListStore.add_files(files)

        print(self.lightsListStore)

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


class FilesListStore(Gtk.ListStore):
    def __init__(self):
        super().__init__(str, str, str, str)

    def add_files(self, files: list[str]):
        for file in files:
            file_name = os.path.basename(file).split(".")[0]
            file_date = datetime.fromtimestamp(os.path.getmtime(file), timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
            file_type = os.path.splitext(file)[1]
            file_path = os.path.dirname(file)
            self.append([file_name, file_type, file_date, file_path])


if __name__ == "__main__":
    app = AstroStack()
    Gtk.main()