from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
from mainwindow import Ui_MainWindow
from filterdesign_window import Ui_FilterDesign
from addnoise_window import Ui_AddNoise
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import audiofilter as af
import matplotlib
from matplotlib import pyplot as plt
import numpy as np

pi = np.pi
tan = np.tan

matplotlib.use('Qt5Agg')


def hhmmss(ms):
    s = round(ms / 1000)
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    return ("%d:%02d:%02d" % (h, m, s)) if h else ("%d:%02d" % (m, s))


class PlaylistModel(QAbstractListModel):
    def __init__(self, playlist, *args, **kwargs):
        super(PlaylistModel, self).__init__(*args, **kwargs)
        self.playlist = playlist

    def data(self, index, role):
        if role == Qt.DisplayRole:
            media = self.playlist.media(index.row())
            return media.canonicalUrl().fileName()

    def rowCount(self, index):
        return self.playlist.mediaCount()


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.player = QMediaPlayer()
        self.player.error.connect(self.erroralert)

        self.playlist = QMediaPlaylist()
        self.player.setPlaylist(self.playlist)

        # connect control function
        self.playButton.pressed.connect(self.player.play)
        self.pauseButton.pressed.connect(self.player.pause)
        self.stopButton.pressed.connect(self.player.stop)
        self.volumeSlider.valueChanged.connect(self.player.setVolume)

        self.viewButton.toggled.connect(self.output_plt)

        self.previousButton.pressed.connect(self.playlist.previous)
        self.nextButton.pressed.connect(self.playlist.next)

        self.model = PlaylistModel(self.playlist)
        self.playlistView.setModel(self.model)
        self.playlist.currentIndexChanged.connect(self.playlist_position_changed)
        selection_model = self.playlistView.selectionModel()
        selection_model.selectionChanged.connect(self.playlist_selection_changed)

        self.player.durationChanged.connect(self.update_duration)
        self.player.positionChanged.connect(self.update_position)
        self.timeSlider.valueChanged.connect(self.player.setPosition)
        self.open_file_action.triggered.connect(self.open_file)

        self.setAcceptDrops(True)
        self.af_list = []
        self.curr_playing = ()

        # matplotlib figure
        self.fig, self.axes = plt.subplots(1, 2)
        self.canvas = FigureCanvas(self.fig)
        self.currWidget = self.pltlayout.addWidget(self.canvas)

        self.clearall_action.triggered.connect(self.refresh_fig)
        self.save_action.triggered.connect(self.output_plt)

        self.output_file_action.triggered.connect(self.output_audio)

        self.fit_filt_action.triggered.connect(self.fit_filt_window)
        self.add_noise_action.triggered.connect(self.add_noise_windows)

        self.show()

    def add_noise_windows(self):
        if self.curr_playing:
            son = AddNoise(self.curr_playing[0], self.curr_playing[1])
            son.emit_signal.connect(lambda path: self.open_file_with_path(path))
        else:
            self.alert('Error', 'Please input an audio first')

    def fit_filt_window(self):
        if self.curr_playing:
            son = FilterDesign(self.curr_playing[0], self.curr_playing[1])
            son.emit_signal.connect(lambda path: self.open_file_with_path(path))
        else:
            self.alert('Error', 'Please input an audio first')

    def erroralert(self, *args):
        print(args)

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.acceptProposedAction()

    def dropEvent(self, e):
        for url in e.mimeData().urls():
            self.playlist.addMedia(QMediaContent(url))

        self.model.layoutChanged.emit()

        # If not playing, seeking to first of newly added + play.
        if self.player.state() != QMediaPlayer.PlayingState:
            i = self.playlist.mediaCount() - len(e.mimeData().urls())
            self.playlist.setCurrentIndex(i)
            self.player.play()

    def open_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Open file",
            "",
            # "mp3 Audio (*.mp3);;mp4 Video (*.mp4);;Movie files (*.mov);;All files (*.*)",
            "wav Audio (*.wav);;mp3 Audio (*.mp3);;All files (*.*)",
        )

        if path:
            self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(path)))
            # TODO
            if self.actionClear_Axes.isChecked():
                self.refresh_fig()
            audio, sample_rate = af.validate_load_audio(path, None)
            af.display.display_plt(audio, sample_rate, self.axes)
            self.af_list.append((audio, sample_rate))
            self.curr_playing = (audio, sample_rate)
        self.model.layoutChanged.emit()

    def open_file_with_path(self, path):
        if path:
            self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(path)))
            if self.actionClear_Axes.isChecked():
                self.refresh_fig()
            audio, sample_rate = af.validate_load_audio(path, None)
            af.display.display_plt(audio, sample_rate, self.axes)
            self.af_list.append((audio, sample_rate))
            self.curr_playing = (audio, sample_rate)
        self.model.layoutChanged.emit()

    def update_duration(self, duration):
        self.timeSlider.setMaximum(duration)

        if duration >= 0:
            self.totalTimeLabel.setText(hhmmss(duration))

    def update_position(self, position):
        if position >= 0:
            self.currentTimeLabel.setText(hhmmss(position))

        # Disable the events to prevent updating triggering a setPosition event (can cause stuttering).
        self.timeSlider.blockSignals(True)
        self.timeSlider.setValue(position)
        self.timeSlider.blockSignals(False)

    def playlist_selection_changed(self, ix):
        # We receive a QItemSelection from selectionChanged.
        i = ix.indexes()[0].row()
        # TODO
        if self.actionClear_Axes.isChecked():
            self.refresh_fig()
        audio, sample_rate = self.af_list[i]
        af.display.display_plt(audio, sample_rate, self.axes)
        self.playlist.setCurrentIndex(i)
        self.curr_playing = (audio, sample_rate)

    def playlist_position_changed(self, i):
        if i > -1:
            ix = self.model.index(i)
            self.playlistView.setCurrentIndex(ix)

    def output_plt(self):
        if self.curr_playing:
            save_path, _ = QFileDialog.getSaveFileName(
                self,
                "Save View",
                '',
                "Picture files (*.jpg);;",
            )
            if save_path:
                self.fig.savefig(save_path)
        else:
            self.alert('Error', 'Please input an audio first')

    def refresh_fig(self):
        [ax.clear() for ax in self.axes]

    def output_audio(self):
        if self.curr_playing:
            save_path, _ = QFileDialog.getSaveFileName(
                self,
                "Save Audio",
                '',
                "wav Audio (*.wav);;",
            )
            if save_path:
                audio, sample_rate = self.curr_playing
                af.save_audio(audio, sample_rate, save_path)
        else:
            self.alert('Error', 'Please input an audio first')

    def alert(self, title: str, message: str):
        box = QMessageBox(QMessageBox.Warning, title, message)
        box.exec_()


class FilterDesign(QMainWindow, Ui_FilterDesign):
    emit_signal = pyqtSignal(str)

    def __init__(self, audio, sample_rate, *args, **kwargs):
        super(FilterDesign, self).__init__(*args, **kwargs)
        self.setupUi(self)
        [self.band_type_combo.addItem(i) for i in af.filter.ALLOWED_FILTER_TYPES]
        [self.FIR_IRR_type_combo.addItem(i) for i in af.filter.ALLOWED_FILTER]
        [self.FIR_type_combo.addItem(i) for i in af.filter.ALLOWED_WINDOW_TYPES]
        [self.IRR_type_combo.addItem(i) for i in af.filter.ALLOWED_IIR_TYPES]
        self.band_type_combo.currentIndexChanged[str].connect(self.check_band_type)
        self.FIR_IRR_type_combo.currentIndexChanged[str].connect(self.check_fir_irr_type)

        # self.Rp_text.textChanged.connect(self.Rp_As_changed)

        self.band_type = self.band_type_combo.currentText()
        self.fir_irr_type = self.FIR_IRR_type_combo.currentText()

        self.Rp_text.setText(str(af.filter.DEFAULT_RP))
        self.As_text.setText(str(af.filter.DEFAULT_AS))

        self.fig, self.axes = plt.subplots(1, 2)
        self.canvas = FigureCanvas(self.fig)
        self.currWidget = self.verticalLayout.addWidget(self.canvas)

        self.audio, self.sample_rate = audio, sample_rate
        self.plot_audio_wave()

        self.check_band_type()
        self.check_fir_irr_type()

        self.sample_rate_text.setText(str(self.sample_rate))
        self.sample_rate_text.setDisabled(True)

        self.cancel_button.clicked.connect(lambda: self.close())
        self.confirm_button.clicked.connect(self.confirm_act)
        self.apply_button.clicked.connect(self.plot_filter_figure)

        self.tem_audio, self.tem_sample_rate = None, None

        self.show()

    # def Rp_As_changed(self):

    def check_band_type(self):
        self.band_type = self.band_type_combo.currentText()
        if self.band_type == 'bandpass':
            self.fp_2_text.setVisible(True)
            self.fst_2_text.setVisible(True)
            self.fst_2_label.setVisible(True)
            self.fp_2_label.setVisible(True)
        else:
            self.fp_2_text.setVisible(False)
            self.fst_2_text.setVisible(False)
            self.fst_2_label.setVisible(False)
            self.fp_2_label.setVisible(False)

    def check_fir_irr_type(self):
        self.fir_irr_type = self.FIR_IRR_type_combo.currentText()
        if self.fir_irr_type == 'FIR':
            self.FIR_type_combo.setVisible(True)
            self.IRR_type_combo.setVisible(False)
        else:
            self.IRR_type_combo.setVisible(True)
            self.FIR_type_combo.setVisible(False)

    def plot_filter_figure(self):
        try:
            fp1 = float(self.fp_1_text.toPlainText()) if self.fp_1_text.toPlainText() else None
            fst1 = float(self.fst_1_text.toPlainText()) if self.fst_1_text.toPlainText() else None
            fp2 = float(self.fp_2_text.toPlainText()) if self.fp_2_text.toPlainText() else None
            fst2 = float(self.fst_2_text.toPlainText()) if self.fst_2_text.toPlainText() else None
            Rp1 = float(self.Rp_text.toPlainText())
            As1 = float(self.As_text.toPlainText())
            if self.fir_irr_type == 'IIR':
                irr_type = self.IRR_type_combo.currentText()
                if (fp1 and fst1) and self.band_type != 'bandpass':
                    self.axes[1].clear()
                    b, a = af.filter.IIR_filter_design(self.sample_rate,
                                                       self.band_type,
                                                       irr_type,
                                                       fp1,
                                                       fst1,
                                                       Rp=Rp1,
                                                       As=As1)
                    if b.any() and a.any():
                        self.tem_audio, self.tem_sample_rate = af.fit_IIR_filter(self.audio, self.sample_rate, b, a)
                        af.wave_plot(self.tem_audio, self.tem_sample_rate, self.axes[1])
                elif fp1 and fst1 and fp2 and fst2:
                    # TODO bandpass filter
                    pass
            else:
                # TODO IIR Filter
                if (fp1 and fst1) and self.band_type != 'bandpass':
                    self.axes[1].clear()
                    win_type = self.FIR_type_combo.currentText()
                    b = af.filter.FIR_filter_design(self.sample_rate,
                                                    win_type,
                                                    fp1,
                                                    fst1,
                                                    Rp=Rp1,
                                                    As=As1)
                    if b.any():
                        self.tem_audio, self.tem_sample_rate = af.fit_FIR_filter(self.audio, self.sample_rate, b)
                        af.wave_plot(self.tem_audio, self.tem_sample_rate, self.axes[1])
                elif fp1 and fst1 and fp2 and fst2:
                    # TODO bandpass filter
                    pass
        except Exception as e:
            print(e)

    def plot_audio_wave(self):
        af.wave_plot(self.audio, self.sample_rate, self.axes[0])

    def confirm_act(self):
        if self.tem_audio.any() and self.tem_sample_rate:
            sa = af.save_audio(self.tem_audio, self.tem_sample_rate)
            self.emit_signal.emit(sa)
            self.close()


class AddNoise(QMainWindow, Ui_AddNoise):
    emit_signal = pyqtSignal(str)

    def __init__(self, audio, sample_rate, *args, **kwargs):
        super(AddNoise, self).__init__(*args, **kwargs)
        self.setupUi(self)
        [self.method_combo.addItem(i) for i in af.audio.AVAILABLE_NOISE_METHOD]
        self.method_combo.currentIndexChanged[str].connect(self.check_type)

        # self.type = self.method_combo.currentText()
        self.fig, self.axes = plt.subplots(1, 2)
        self.canvas = FigureCanvas(self.fig)
        self.currWidget = self.verticalLayout.addWidget(self.canvas)

        self.audio, self.sample_rate = audio, sample_rate
        self.sample_rate_text.setText(str(self.sample_rate))

        self.plot_audio_wave()
        # self.check_type()

        self.cancel_button.clicked.connect(lambda: self.close())
        self.confirm_button.clicked.connect(self.confirm_act)
        self.apply_button.clicked.connect(self.plot_noise_figure)

        self.tem_audio, self.tem_sample_rate = None, None

        self.show()

    def check_type(self):
        pass

    def plot_noise_figure(self):
        snr_level = float(self.SNR_Level_text.toPlainText()) if self.SNR_Level_text.toPlainText() else None
        if snr_level:
            self.tem_audio, self.tem_sample_rate = af.add_background_noise(
                self.audio, self.sample_rate, snr_level, self.method_combo.currentText()
            )
            af.wave_plot(self.tem_audio, self.tem_sample_rate, self.axes[1])

    def plot_audio_wave(self):
        af.wave_plot(self.audio, self.sample_rate, self.axes[0])

    def confirm_act(self):
        if self.tem_audio.any() and self.tem_sample_rate:
            sa = af.save_audio(self.tem_audio, self.tem_sample_rate)
            self.emit_signal.emit(sa)
        self.close()


if __name__ == "__main__":
    try:
        app = QApplication([])
        app.setApplicationName("Audio Filter")
        app.setStyle("Fusion")

        # Fusion dark palette from https://gist.github.com/QuantumCD/6245215.
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, Qt.white)
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, Qt.black)
        app.setPalette(palette)
        app.setStyleSheet(
            "QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }"
        )

        window = MainWindow()
        # audio, sample_rate = af.examples('me')
        # window = FilterDesign(audio, sample_rate)
        app.exec_()
    except Exception as e:
        print(e)
