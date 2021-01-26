import mne
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QMessageBox, QPushButton, QVBoxLayout, QWidget

from mne_pipeline_hd.gui.gui_utils import WorkerDialog
from mne_pipeline_hd.gui.parameter_widgets import SliderGui


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.file_path = None
        self.raw = None
        self.filtered = None
        self.parameters = {
            'Highpass': 1,
            'Lowpass': 100
        }

        self.init_ui()
        self.show()

    def init_ui(self):
        layout = QVBoxLayout()
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        get_file_button = QPushButton('Datei öffnen')
        get_file_button.clicked.connect(self.open_file)
        layout.addWidget(get_file_button)

        plot_raw_button = QPushButton('Plot ohne Filter')
        plot_raw_button.clicked.connect(self.plot_raw)
        layout.addWidget(plot_raw_button)

        highpass_widget = SliderGui(self.parameters, 'Highpass')
        layout.addWidget(highpass_widget)

        lowpass_widget = SliderGui(self.parameters, 'Lowpass')
        layout.addWidget(lowpass_widget)

        filter_button = QPushButton('Filtern')
        filter_button.clicked.connect(self.filter_raw)
        layout.addWidget(filter_button)

        plot_filter_button = QPushButton('Plot mit Filter')
        plot_filter_button.clicked.connect(self.plot_filtered)
        layout.addWidget(plot_filter_button)

        close_bt = QPushButton('Close')
        close_bt.clicked.connect(self.close)
        layout.addWidget(close_bt)

    def _load_raw(self):
        self.raw = mne.io.read_raw_fif(self.file_path, preload=True)

    def open_file(self):
        self.file_path = QFileDialog.getOpenFileName(self, 'Wähle eine EEG-Datei aus', filter='EEG-Datei (*fif)')[0]

        if self.file_path:
            WorkerDialog(self, self._load_raw)

    def plot_raw(self):
        if self.raw:
            self.raw.plot()
        else:
            QMessageBox.warning(self, 'Keine Datei geladen', 'Achtung, Sie haben keine Datei geladen')

    def _filter_raw(self):
        self.filtered = self.raw.filter(self.parameters['Highpass'], self.parameters['Lowpass'])

    def filter_raw(self):
        if self.raw:
            WorkerDialog(self, self._filter_raw)
        else:
            QMessageBox.warning(self, 'Keine Datei geladen', 'Achtung, Sie haben keine Datei geladen')

    def plot_filtered(self):
        if self.filtered:
            self.filtered.plot()
        else:
            QMessageBox.warning(self, 'Keine Datei geladen', 'Achtung, Sie haben keine Datei geladen')
