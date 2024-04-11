from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets, QtNetwork, uic
import sys, os, subprocess, time, datetime, re
from subprocess import Popen, PIPE, STDOUT
import base64
from gambar import *
from jendela_kemajuan import ProgressBarWidget


class SinyalWorkerEncoding(QObject):
    selesai = pyqtSignal()
    error = pyqtSignal(tuple)
    hasil = pyqtSignal(object)
    progres = pyqtSignal(object)
    persentase_kemajuan = pyqtSignal(int)
    ProsesBerhasil = pyqtSignal(object)
    ProsesTotal = pyqtSignal(object)
    ProsesFPS = pyqtSignal(object)
    ProsesPerkiraanUkuran = pyqtSignal(object)
    ProsesPerkiraanSelesai = pyqtSignal(object)
    ProsesNamaFileEncode = pyqtSignal(object)


class WorkerEncoding(QRunnable):
    def __init__(self):
        super().__init__()
        self.sinyal = SinyalWorkerEncoding()

    def run(self):
        try:
            input_mentah = window.PathInput.text().split(" || ")
            output_paths = window.PathOutput.text().split(" || ")

            waktu_mulai = datetime.datetime.now()
            for inputFile, outputFile in zip(input_mentah, output_paths):
                window.SedangEncode.setAlignment(QtCore.Qt.AlignLeft)
                self.sinyal.ProsesNamaFileEncode.emit(str(os.path.basename(inputFile)) + str(f" ({str(input_mentah.index(inputFile)+1)} dari {str(len(input_mentah))})"))

                Nama_File_Saja = os.path.basename(inputFile)
                Nama_File_Saja_tanpa_ekstensi, nama_file_Ekstensi = os.path.splitext(Nama_File_Saja)
                Mode_Terpilih = window.OpsiMode.currentText()
                Resolusi_Terpilih = window.OpsiResolusi.currentText()


                resolutions = ["1080p", "1080P", "720p", "720P", "480p", "480P", "360p", "360P", "240p", "240P", "144p", "144P", "1080", "720", "480", "360", "240", "144", "4K", "8K", "2K", "1080p60", "1080P60", "720p60", "720P60", "480p60", "480P60", "360p60", "360P60", "240p60", "240P60", "144p60", "144P60", "1080p30", "1080P30", "720p30", "720P30", "480p30", "480P30", "360p30", "360P30", "240p30", "240P30", "144p30", "144P30", "1080p60fps", "1080P60fps", "720p60fps", "720P60fps", "480p60fps", "480P60fps", "360p60fps", "360P60fps", "240p60fps", "240P60fps", "144p60fps", "144P60fps", "1080p30fps", "1080P30fps", "720p30fps", "720P30fps", "480p30fps", "480P30fps", "360p30fps", "360P30fps", "240p30fps", "240P30fps", "144p30fps", "144P30fps", "1080p60FPS", "1080P60FPS", "720p60FPS", "720P60FPS", "480p60FPS", "480P60FPS", "360p60FPS", "360P60FPS", "240p60FPS", "240P60FPS", "144p60FPS", "144P60FPS", "1080p30FPS", "1080P30FPS", "720p30FPS", "720P30FPS", "480p30FPS", "480P30FPS", "360p30FPS", "360P30FPS", "240p30FPS", "240P30FPS", "144p30FPS", "144P30FPS", "1080p60Fps", "1080P60Fps", "720p60Fps", "720P60Fps", "480p60Fps", "480P60Fps", "360p60Fps", "360P60Fps", "240p60Fps", "240P60Fps", "144p60Fps", "144P60Fps", "1080p30Fps", "1080P30Fps", "720p30Fps", "720P30Fps", "480p30Fps", "480P30Fps", "360p30Fps", "360P30Fps", "240p30Fps", "240P30Fps", "144p30Fps", "144P30Fps", "1080p60fps", "1080P60fps", "720p60fps", "720P60fps", "480p60fps", "480P60fps", "360p60fps", "360P60fps", "240p60fps", "240P60fps", "144p60fps", "144P60fps", "1080p30fps", "1080P30fps", "720p30fps", "720P30fps", "480p30fps", "480P30fps", "360p30fps", "360P30fps", "240p30fps", "240P30fps", "144p30fps", "144P30fps", "1080p60FPS", "1080P60FPS", "720p60FPS", "720P60FPS", "480p60FPS", "QHD", "qhd", "UHD", "uhd", "1080pUHD", "1080PUHD", "720pUHD", "720PUHD", "480pUHD", "480PUHD", "360pUHD", "360PUHD", "240pUHD", "240PUHD", "144pUHD", "144PUHD", "1080p4K", "1080P4K", "720p4K", "720P4K", "480p4K", "480P4K", "360p4K", "360P4K", "240p4K", "240P4K", "144p4K", "144P4K", "1080p8K", "1080P8K", "720p8K", "720P8K", "480p8K", "480P8K", "360p8K", "360P8K", "240p8K", "240P8K", "144p8K", "144P8K", "1080p2K", "1080P2K", "720p2K", "720P2K", "480p2K", "480P2K", "360p2K", "360P2K", "240p2K", "240P2K", "144p2K", "144P2K", "1080p4k", "1080P4k", "720p4k", "720P4k", "480p4k", "480P4k", "360p4k", "360P4k", "240p4k", "240P4k", "144p4k", "144P4k", "1080p8k", "1080P8k", "720p8k", "720P8k", "480p8k", "480P8k", "360p8k", "360P8k", "240p8k", "240P8k", "144p8k", "144P8k", "1080p2k", "1080P2k", "720p2k", "720P2k", "480p2k", "480P2k", "360p2k", "360P2k", "240p2k", "240P2k", "144p2k"]

                nama_file_jadi = None

                for resolution in resolutions:
                    if resolution in Nama_File_Saja_tanpa_ekstensi:
                        nama_file_jadi = Nama_File_Saja_tanpa_ekstensi.replace(resolution, str(Resolusi_Terpilih))
                        break

                if not nama_file_jadi:
                    nama_file_jadi = f"{str(Nama_File_Saja_tanpa_ekstensi)} {str(Resolusi_Terpilih)}"

                
                if Nama_File_Saja_tanpa_ekstensi == nama_file_jadi:
                    nama_file_jadi = f"{str(Nama_File_Saja_tanpa_ekstensi)} Shader"

                modes = {
                    "A+A": "ModeA+A.glsl",
                    "B+B": "ModeB+B.glsl",
                    "C+A": "ModeC+A.glsl",
                    "A": "ModeA.glsl",
                    "B": "ModeB.glsl",
                    "C": "ModeC.glsl"
                }

                Mode = modes.get(Mode_Terpilih, "")

                list_resolusi_menu = {
                    "8K": (7680, 4320),
                    "4K(TV)": (4096, 2160),
                    "UHD": (3840, 2160),
                    "QHD": (2560, 1440),
                    "2K(TV)": (2048, 1080),
                    "1080P": (1920, 1080),
                    "720P": (1280, 720)
                }

                ResolusiW, ResolusiH = list_resolusi_menu.get(Resolusi_Terpilih, (0, 0))
            
                folder_kerja = os.path.abspath(os.path.dirname(sys.argv[0]))
                perintah = f'"{str(folder_kerja)}/mpv/mpv.exe" "{str(inputFile)}" -glsl-shaders="{str(folder_kerja)}/shaders/{Mode}" -vf=gpu="w={ResolusiW}:h={ResolusiH}" -scale=ewa_lanczossharp -cscale=ewa_lanczossharp --o="{str(outputFile)}/{str(nama_file_jadi)}{str(nama_file_Ekstensi)}"'
                self.sinyal.progres.emit("Waktu Mulai: " + str(waktu_mulai.strftime("%H:%M:%S")))
                proses = subprocess.Popen(perintah, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, encoding='utf-8')
                while True:
                    output = proses.stdout.readline().strip()
                    if output:
                        if "AV:" in output:
                            self.sinyal.progres.emit(output)
                            try:
                                self.sinyal.persentase_kemajuan.emit(int(output.split(" ")[4].replace("(", "").replace("%)", "")))
                                self.sinyal.ProsesBerhasil.emit(output.split(" ")[1])
                                self.sinyal.ProsesTotal.emit(output.split(" ")[3])
                                self.sinyal.ProsesFPS.emit(output.split(" ")[8].replace("{", ""))
                                self.sinyal.ProsesPerkiraanUkuran.emit(output.split(" ")[9].replace("}", ""))
                                self.sinyal.ProsesPerkiraanSelesai.emit(output.split(" ")[7].replace("{", ""))
                            except:
                                pass
                        else:
                            self.sinyal.progres.emit(output)

                    if not output and proses.poll() is not None:
                        break

                proses.wait()


            waktu_selesai = datetime.datetime.now()
            self.sinyal.progres.emit("Waktu Selesai: " + str(waktu_selesai.strftime("%H:%M:%S")))
            waktu_yang_dibutuhkan = waktu_selesai - waktu_mulai
            self.sinyal.progres.emit("Waktu Yang Dibutuhkan: " + str(waktu_yang_dibutuhkan))

            if window.CekHibernasi.isChecked():
                time.sleep(5)
                subprocess.call("shutdown /h")
            else:
                pass

        except Exception as e:
            self.sinyal.error.emit((f"Terjadi kesalahan: {str(e)}",))

        self.sinyal.selesai.emit()




class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.threadencode = QThreadPool()
        self.baca_icon = QtGui.QPixmap()
        self.baca_icon.loadFromData(base64.b64decode(Gambar_Icon_App))  
        self.setWindowIcon(QtGui.QIcon(self.baca_icon))
        self.setObjectName("self")
        self.resize(683, 600)
        self.setAcceptDrops(True)
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Light")
        font.setPointSize(12)
        self.setFont(font)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        self.widget_2 = QtWidgets.QWidget(self.centralwidget)
        self.widget_2.setObjectName("widget_2")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.widget_2)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.log = QtWidgets.QPlainTextEdit(self.widget_2)
        self.log.setReadOnly(True)
        self.log.setPlainText("")
        self.log.setObjectName("log")
        self.gridLayout_4.addWidget(self.log, 0, 0, 1, 2)
        self.SedangEncode = QtWidgets.QLineEdit(self.widget_2)
        self.SedangEncode.setFrame(False)
        self.SedangEncode.setReadOnly(True)
        self.SedangEncode.setObjectName("SedangEncode")
        self.SedangEncode.setAlignment(QtCore.Qt.AlignCenter)
        self.SedangEncode.setText("Siap Digunakan")
        self.gridLayout_4.addWidget(self.SedangEncode, 1, 0, 1, 1)
        self.TombolPersentase = QtWidgets.QPushButton(self.widget_2)
        self.TombolPersentase.setObjectName("TombolPersentase")
        self.TombolPersentase.clicked.connect(self.lihatpersentase)
        self.TombolPersentase.setText("%")
        self.gridLayout_4.addWidget(self.TombolPersentase, 1, 1, 1, 1)
        self.gridLayout.addWidget(self.widget_2, 1, 0, 1, 1)


        self.widget_3 = QtWidgets.QWidget(self.centralwidget)
        self.widget_3.setObjectName("widget_3")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.widget_3)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.WaktuBerhasil = QtWidgets.QLineEdit(self.widget_3)
        self.WaktuBerhasil.setAlignment(QtCore.Qt.AlignCenter)
        self.WaktuBerhasil.setReadOnly(True)
        self.WaktuBerhasil.setObjectName("WaktuBerhasil")
        self.gridLayout_2.addWidget(self.WaktuBerhasil, 1, 0, 1, 1)
        self.PerkiraanSelesai = QtWidgets.QLineEdit(self.widget_3)
        self.PerkiraanSelesai.setAlignment(QtCore.Qt.AlignCenter)
        self.PerkiraanSelesai.setReadOnly(True)
        self.PerkiraanSelesai.setObjectName("PerkiraanSelesai")
        self.gridLayout_2.addWidget(self.PerkiraanSelesai, 1, 4, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.widget_3)
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.gridLayout_2.addWidget(self.label_8, 0, 2, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.widget_3)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 0, 4, 1, 1)
        self.Kemajuan = QtWidgets.QProgressBar(self.widget_3)
        self.Kemajuan.setProperty("value", 0)
        self.Kemajuan.setObjectName("Kemajuan")
        self.gridLayout_2.addWidget(self.Kemajuan, 2, 0, 1, 5)
        self.WaktuTotal = QtWidgets.QLineEdit(self.widget_3)
        self.WaktuTotal.setAlignment(QtCore.Qt.AlignCenter)
        self.WaktuTotal.setReadOnly(True)
        self.WaktuTotal.setObjectName("WaktuTotal")
        self.gridLayout_2.addWidget(self.WaktuTotal, 1, 1, 1, 1)
        self.FPS = QtWidgets.QLineEdit(self.widget_3)
        self.FPS.setAlignment(QtCore.Qt.AlignCenter)
        self.FPS.setReadOnly(True)
        self.FPS.setObjectName("FPS")
        self.gridLayout_2.addWidget(self.FPS, 1, 2, 1, 1)
        self.label = QtWidgets.QLabel(self.widget_3)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.widget_3)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.widget_3)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 0, 3, 1, 1)
        self.PerkiraanUkuran = QtWidgets.QLineEdit(self.widget_3)
        self.PerkiraanUkuran.setAlignment(QtCore.Qt.AlignCenter)
        self.PerkiraanUkuran.setReadOnly(True)
        self.PerkiraanUkuran.setObjectName("PerkiraanUkuran")
        self.gridLayout_2.addWidget(self.PerkiraanUkuran, 1, 3, 1, 1)
        self.gridLayout.addWidget(self.widget_3, 2, 0, 1, 1)
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setObjectName("widget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.widget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.OpsiMode = QtWidgets.QComboBox(self.widget)
        self.OpsiMode.setObjectName("OpsiMode")
        self.OpsiMode.addItem("")
        self.OpsiMode.addItem("")
        self.OpsiMode.addItem("")
        self.OpsiMode.addItem("")
        self.OpsiMode.addItem("")
        self.OpsiMode.addItem("")
        self.OpsiMode.currentIndexChanged.connect(self.mode_berubah)
        self.gridLayout_3.addWidget(self.OpsiMode, 0, 4, 1, 1)
        self.PathOutput = QtWidgets.QLineEdit(self.widget)
        self.PathOutput.setReadOnly(True)
        self.PathOutput.setObjectName("PathOutput")
        self.gridLayout_3.addWidget(self.PathOutput, 1, 1, 1, 1)
        self.TombolInput = QtWidgets.QPushButton(self.widget)
        self.TombolInput.setObjectName("TombolInput")
        self.TombolInput.clicked.connect(self.Pilih_Input_File)
        self.gridLayout_3.addWidget(self.TombolInput, 0, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.widget)
        self.label_5.setObjectName("label_5")
        self.gridLayout_3.addWidget(self.label_5, 0, 3, 1, 1, QtCore.Qt.AlignRight)
        self.PathInput = QtWidgets.QLineEdit(self.widget)
        self.PathInput.setReadOnly(True)
        self.PathInput.setObjectName("PathInput")
        self.gridLayout_3.addWidget(self.PathInput, 0, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.widget)
        self.label_6.setObjectName("label_6")
        self.gridLayout_3.addWidget(self.label_6, 1, 3, 1, 1, QtCore.Qt.AlignRight)
        self.TombolOutput = QtWidgets.QPushButton(self.widget)
        self.TombolOutput.setObjectName("TombolOutput")
        self.TombolOutput.clicked.connect(self.Pilih_Output_Folder)
        self.gridLayout_3.addWidget(self.TombolOutput, 1, 0, 1, 1)
        self.OpsiResolusi = QtWidgets.QComboBox(self.widget)
        self.OpsiResolusi.setObjectName("OpsiResolusi")
        self.OpsiResolusi.addItem("")
        self.OpsiResolusi.addItem("")
        self.OpsiResolusi.addItem("")
        self.OpsiResolusi.addItem("")
        self.OpsiResolusi.addItem("")
        self.OpsiResolusi.addItem("")
        self.OpsiResolusi.addItem("")
        self.OpsiResolusi.currentIndexChanged.connect(self.resolusi_berubah)
        self.gridLayout_3.addWidget(self.OpsiResolusi, 1, 4, 1, 1)
        self.CekHibernasi = QtWidgets.QCheckBox(self.widget)
        self.CekHibernasi.setObjectName("CekHibernasi")
        self.CekHibernasi.stateChanged.connect(self.cek_hibernasi)
        self.gridLayout_3.addWidget(self.CekHibernasi, 0, 5, 1, 1)
        self.TombolJalan = QtWidgets.QPushButton(self.widget)
        self.TombolJalan.setObjectName("TombolJalan")
        self.TombolJalan.clicked.connect(self.encode)
        self.gridLayout_3.addWidget(self.TombolJalan, 1, 5, 1, 1)
        self.gridLayout.addWidget(self.widget, 0, 0, 1, 1)
        self.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_8.setText(_translate("MainWindow", "FPS"))
        self.label_4.setText(_translate("MainWindow", "Perkiraan Selesai"))
        self.label.setText(_translate("MainWindow", "Berhasil"))
        self.label_7.setText(_translate("MainWindow", "Total"))
        self.label_2.setText(_translate("MainWindow", "Perkiraan Ukuran"))
        self.OpsiMode.setItemText(0, _translate("MainWindow", "A+A"))
        self.OpsiMode.setItemText(1, _translate("MainWindow", "B+B"))
        self.OpsiMode.setItemText(2, _translate("MainWindow", "C+A"))
        self.OpsiMode.setItemText(3, _translate("MainWindow", "A"))
        self.OpsiMode.setItemText(4, _translate("MainWindow", "B"))
        self.OpsiMode.setItemText(5, _translate("MainWindow", "C"))
        self.TombolInput.setText(_translate("MainWindow", "Input"))
        self.label_5.setText(_translate("MainWindow", "Mode Optimalisasi"))
        self.label_6.setText(_translate("MainWindow", "Resolusi Output"))
        self.TombolOutput.setText(_translate("MainWindow", "Output"))
        self.OpsiResolusi.setItemText(0, _translate("MainWindow", "8K"))
        self.OpsiResolusi.setItemText(1, _translate("MainWindow", "4K(TV)"))
        self.OpsiResolusi.setItemText(2, _translate("MainWindow", "UHD"))
        self.OpsiResolusi.setItemText(3, _translate("MainWindow", "QHD"))
        self.OpsiResolusi.setItemText(4, _translate("MainWindow", "2K(TV)"))
        self.OpsiResolusi.setItemText(5, _translate("MainWindow", "1080P"))
        self.OpsiResolusi.setItemText(6, _translate("MainWindow", "720P"))
        self.CekHibernasi.setText(_translate("MainWindow", "Hibernasi"))
        self.TombolJalan.setText(_translate("MainWindow", "Jalan"))
        self.WaktuBerhasil.setText(_translate("MainWindow", "-"))
        self.WaktuTotal.setText(_translate("MainWindow", "-"))
        self.FPS.setText(_translate("MainWindow", "-"))
        self.PerkiraanUkuran.setText(_translate("MainWindow", "-"))
        self.PerkiraanSelesai.setText(_translate("MainWindow", "-"))
        QtCore.QMetaObject.connectSlotsByName(self)
        
        
        
        self.PersentaseBerubah = 0
        self.customText = "Siap Digunakan"
        self.progressWidget = ProgressBarWidget()
        

    def closeEvent(self, event):
        self.progressWidget.close()
        event.accept()


    def Pilih_Output_Folder(self):
        self.FolderOutput = QtWidgets.QFileDialog.getExistingDirectory(self, 'Pilih Folder Output')
        self.PathOutput.setText(self.FolderOutput)
        self.log.appendPlainText("Folder Output :\n" + self.FolderOutput)

    def Pilih_Input_File(self):
        self.FileInput = QFileDialog.getOpenFileNames(self, 'Pilih File Input', '', 'File Video (*.mp4 *.avi *.mkv *.mov *.wmv *.flv *.mpeg *.mpg *.webm *.ogg *.ogv *.m4v)')
        self.PathInput.setText(" || ".join(self.FileInput[0]))
        self.log.appendPlainText("File Input :\n" + str("\n".join(self.FileInput[0])))



    def lihatpersentase(self):
        self.progressWidget.setPercentage(self.PersentaseBerubah, self.customText)
        self.progressWidget.show()
    

    def Saat_encode(self, n):
        self.TombolJalan.setEnabled(False)
        self.TombolInput.setEnabled(False)
        self.TombolOutput.setEnabled(False)
        self.OpsiMode.setEnabled(False)
        self.OpsiResolusi.setEnabled(False)
        self.CekHibernasi.setEnabled(False)
        self.log.appendPlainText(n)

    def Selesai_encode(self):
        self.TombolJalan.setEnabled(True)
        self.TombolInput.setEnabled(True)
        self.TombolOutput.setEnabled(True)
        self.OpsiMode.setEnabled(True)
        self.OpsiResolusi.setEnabled(True)
        self.CekHibernasi.setEnabled(True)
        self.SedangEncode.setAlignment(QtCore.Qt.AlignCenter)
        self.SedangEncode.setText("Selesai")
        self.progressWidget.setPercentage(100, "Selesai")

    def encode(self):
        if self.PathInput.text() == "" or self.PathOutput.text() == "":
            self.log.appendPlainText("Pilih Path Input/Output terlebih dahulu")
            pass

        else:
            self.TombolJalan.setEnabled(False)
            self.TombolInput.setEnabled(False)
            self.TombolOutput.setEnabled(False)
            self.OpsiMode.setEnabled(False)
            self.OpsiResolusi.setEnabled(False)
            self.CekHibernasi.setEnabled(False)
            self.Kemajuan.setValue(0)

            worker = WorkerEncoding()
            worker.sinyal.selesai.connect(self.Selesai_encode)
            worker.sinyal.hasil.connect(lambda hasil: self.log.appendPlainText(hasil))
            worker.sinyal.error.connect(lambda error: self.log.appendPlainText(error[0]))
            worker.sinyal.progres.connect(self.Saat_encode)
            #worker.sinyal.persentase_kemajuan.connect(lambda persentase_kemajuan: self.Kemajuan.setValue(persentase_kemajuan))
            worker.sinyal.persentase_kemajuan.connect(self.update_persentase)
            worker.sinyal.ProsesBerhasil.connect(lambda ProsesBerhasil: self.WaktuBerhasil.setText(ProsesBerhasil))
            worker.sinyal.ProsesTotal.connect(lambda ProsesTotal: self.WaktuTotal.setText(ProsesTotal))
            worker.sinyal.ProsesFPS.connect(lambda ProsesFPS: self.FPS.setText(ProsesFPS))
            worker.sinyal.ProsesPerkiraanUkuran.connect(lambda ProsesPerkiraanUkuran: self.PerkiraanUkuran.setText(ProsesPerkiraanUkuran))
            worker.sinyal.ProsesPerkiraanSelesai.connect(lambda ProsesPerkiraanSelesai: self.PerkiraanSelesai.setText(ProsesPerkiraanSelesai))
            #worker.sinyal.ProsesNamaFileEncode.connect(lambda ProsesNamaFileEncode: self.SedangEncode.setText(f"Sedang Encode: {ProsesNamaFileEncode}"))
            worker.sinyal.ProsesNamaFileEncode.connect(self.detail_kemajuan_encode)
            self.threadencode.start(worker)
    
    def detail_kemajuan_encode(self, text):
        self.SedangEncode.setText(f"Sedang Encode: {text}")
        match = re.search(r'\((\d+ dari \d+)\)', text)
        if match:
            result = match.group(1)
            self.customText = result



    def update_persentase(self, persentase_kemajuan):
        self.PersentaseBerubah = persentase_kemajuan 
        self.Kemajuan.setValue(persentase_kemajuan)
        self.progressWidget.setPercentage(persentase_kemajuan, f"{str(persentase_kemajuan)}% | {self.customText}")




    def mode_berubah(self, index):
        self.log.appendPlainText("Mode : " + self.OpsiMode.itemText(index))
        if self.OpsiMode.itemText(index) == "A+A":
            self.log.appendPlainText("Mode Paling Bagus, Kualitas persepsi tertinggi, Merekonstruksi hampir semua garis yang terdegradasi, Efek yang sama dari mode A")
        elif self.OpsiMode.itemText(index) == "B+B":
            self.log.appendPlainText("Mode yang bagus, kualitas persepsi yang tinggi, Efek yang sama dari mode B")
        elif self.OpsiMode.itemText(index) == "C+A":
            self.log.appendPlainText("Kualitas persepsi sedikit lebih tinggi, Efek yang sama dari mode C")
        elif self.OpsiMode.itemText(index) == "A":
            self.log.appendPlainText("Kualitas persepsi yang tinggi, Mengurangi artefak kompresi, Merekonstruksi garis yang paling terdegradasi, Mengurangi blur dalam jumlah besar, Mengurangi noise")
        elif self.OpsiMode.itemText(index) == "B":
            self.log.appendPlainText("Mengurangi artefak kompresi, Merekonstruksi beberapa garis yang terdegradasi, Mengurangi beberapa buram, Mengurangi noise, Mengurangi getaran, Mengurangi aliasing")
        elif self.OpsiMode.itemText(index) == "C":
            self.log.appendPlainText("Mengurangi noise")

    
    def resolusi_berubah(self, index):
        if self.OpsiResolusi.itemText(index) == "8K":
            self.log.appendPlainText("Resolusi 8K (7680x4320)")
            self.log.appendPlainText("Rekomendasi RAM : 32GB atau lebih")
        elif self.OpsiResolusi.itemText(index) == "4K(TV)":
            self.log.appendPlainText("Resolusi 4K untuk TV (4096x2160)")
            self.log.appendPlainText("Rekomendasi RAM : 16GB atau lebih")
        elif self.OpsiResolusi.itemText(index) == "UHD":
            self.log.appendPlainText("Resolusi UHD (3840x2160)")
            self.log.appendPlainText("Rekomendasi RAM : 16GB atau lebih")
        elif self.OpsiResolusi.itemText(index) == "QHD":
            self.log.appendPlainText("Resolusi QHD (2560x1440)")
            self.log.appendPlainText("Rekomendasi RAM : 16GB atau lebih")
        elif self.OpsiResolusi.itemText(index) == "2K(TV)":
            self.log.appendPlainText("Resolusi 2K untuk TV (2048x1080)")
            self.log.appendPlainText("Rekomendasi RAM : 16GB atau lebih")
        elif self.OpsiResolusi.itemText(index) == "1080P":
            self.log.appendPlainText("Resolusi 1080P (1920x1080)")
            self.log.appendPlainText("Rekomendasi RAM : 8GB atau lebih")
        elif self.OpsiResolusi.itemText(index) == "720P":
            self.log.appendPlainText("Resolusi 720P (1280x720)")
            self.log.appendPlainText("Rekomendasi RAM : 8GB atau lebih")

    def cek_hibernasi(self, nilai):
        if nilai == 2:
            self.log.appendPlainText("Hibernasi PC setelah selesai Diaktifkan")
        else:
            self.log.appendPlainText("Hibernasi PC setelah selesai Dinonaktifkan")

            #format_file_video = [".mp4", ".mkv", ".avi", ".flv", ".wmv", ".mov", ".webm", ".m4v", ".mpg", ".mpeg", ".vob", ".ogv", ".ogg", ".3gp", ".3g2", ".mxf", ".mts", ".m2ts", ".ts", ".rm", ".rmvb", ".m4p", ".m4b", ".m4r", ".m4a", ".m4v"]


    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            format_file_video = [".mp4", ".mkv", ".avi", ".flv", ".wmv", ".mov", ".webm", ".m4v", ".mpg", ".mpeg", ".vob", ".ogv", ".ogg", ".3gp", ".3g2", ".mxf", ".mts", ".m2ts", ".ts", ".rm", ".rmvb", ".m4p", ".m4b", ".m4r", ".m4a", ".m4v"]
            
            url = event.mimeData().urls()[0]
            file_path = url.toLocalFile()
            
            if os.path.isdir(file_path):
                for file in os.listdir(file_path):
                    if file.endswith(tuple(format_file_video)):
                        if "Sedang Encode:" in self.SedangEncode.text():
                            event.ignore()
                        else:
                            event.accept()
                        break
                else:
                    self.log.appendPlainText("Tidak ada video dalam folder")
                    event.ignore()
            elif file_path.endswith(tuple(format_file_video)):
                if "Sedang Encode:" in self.SedangEncode.text():
                    event.ignore()
                else:
                    event.accept()
            else:
                self.log.appendPlainText("Format file tidak didukung")
                event.ignore()
        else:
            event.ignore()


    def dropEvent(self, event):
        urls = event.mimeData().urls()
        format_file_video = [".mp4", ".mkv", ".avi", ".flv", ".wmv", ".mov", ".webm", ".m4v", ".mpg", ".mpeg", ".vob", ".ogv", ".ogg", ".3gp", ".3g2", ".mxf", ".mts", ".m2ts", ".ts", ".rm", ".rmvb", ".m4p", ".m4b", ".m4r", ".m4a", ".m4v"]
            
        files = []
        output_dirs = []
        for url in urls:
            file_path = url.toLocalFile()

            if os.path.isdir(file_path):
                for file in os.listdir(file_path):
                    if file.endswith(tuple(format_file_video)):
                        files.append(os.path.join(file_path, file))
                        output_dirs.append(file_path)
            elif file_path.endswith(tuple(format_file_video)):
                files.append(file_path)
                output_dirs.append(os.path.dirname(file_path))

        if files:
            self.PathInput.setText(" || ".join(files))
            self.log.appendPlainText("File Input :\n" + str("\n".join(files)))

            self.PathOutput.setText(" || ".join(output_dirs))
            self.log.appendPlainText("Folder Output :\n" + str("\n".join(output_dirs)))
        else:
            self.log.appendPlainText("Tidak ada file video yang valid")




if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)    
    window = MainWindow()
    window.setWindowTitle("Anime4K Encoding | Copyright (c) 2023 by Arif Maulana")
    window.show()
    try:

        with open("./tema/aqua.qss", "r") as f:
            _style = f.read()
            app.setStyleSheet(_style)
    
    except:
        pass

    sys.exit(app.exec_())
