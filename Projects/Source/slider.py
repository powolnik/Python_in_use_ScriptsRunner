import unreal
from PySide import QtCore, QtGui, QtUiTools

class VolumeSlider(QtGui.QDialog):

    def __init__(self, parent=None):
        super(VolumeSlider, self).__init__(parent)
        self.setWindowTitle("Volume Slider")
        self.slider = QtGui.QSlider()
        self.slider.sliderMoved.connect(self.slider_fn)
        self.slider.setRange(0,100)
        self.slider.setValue(100)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.slider)
        self.setLayout(layout)

        #load the master SoundClass
        self.master_sound_class = unreal.load_asset(None, name='/Engine/EngineSounds/Master')

    def slider_fn(self):
        volume_float = self.slider.value()/100.00
        #set the volume to the desired value
        self.master_sound_class.properties.set_editor_property(name='volume', value=volume_float)

APP = None
if not QtGui.QApplication.instance():
    APP = QtGui.QApplication(sys.argv)

main_window = VolumeSlider()
main_window.show()