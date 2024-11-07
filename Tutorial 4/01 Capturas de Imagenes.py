import wx
import cv2
import os
import imutils
from datetime import datetime
import time

#Variables a utilizar 
TIMER_ID1 = 2000
TIMER_ID2 = 2001

#Camara de captura, cambiar el numero 0 segun el dispositivo que usara (0 = camara incorporda, 1,2,3... = camaras externas)
capture = cv2.VideoCapture(0 + cv2.CAP_DSHOW)
width, height = (640, 360)
tag = ''
count = 0

#Direccion donde se guardaran las fotos, cambiar al usar en otra pc
personPath = r'C:\Users\oicas\Documents\vscode\Practica\Tutorial 4\CapturasTuto4-01'

class Imagenes(wx.Frame):
    #Aplicacion
    def __init__(self, parent, title):
        super(Imagenes, self).__init__(parent, title=title)
        self.InitUI()
        self.Centre()
    #Panel y sus Atributos
    def InitUI(self):
        #Panel donde estaran los elementos
        self.panel = wx.Panel(self,wx.ID_ANY)
        self.sizer = wx.GridBagSizer(3, 3)
        #Fecha del tag
        self.now = datetime.now()
        #Timer de la camara continua
        self.timer = wx.Timer(self, id=TIMER_ID1)
        self.Bind(wx.EVT_TIMER, self.update, self.timer)
        #Boton de captura singular
        self.takeButton = wx.Button(self.panel, size=(60, 60), label="Singular")
        #Boton de captura continua
        self.toggle = wx.ToggleButton(self.panel, size=(60, 60), label="Continua")
        #Panel de imagen de la camara
        self.panelDeImagen = wx.Panel(self.panel, -1, size=(640, 360))
        self.capture = webcamPanel(self.panelDeImagen, capture)
        #Agrega los elementos al panel con sus tamaños
        self.sizer.Add(self.takeButton, pos=(3, 1), span=(0, 0), flag=wx.BOTTOM | wx.TOP | wx.LEFT | wx.RIGHT, border=15)
        self.sizer.Add(self.toggle, pos=(3, 2), span=(0, 0), flag=wx.BOTTOM | wx.TOP | wx.LEFT | wx.RIGHT, border=15)
        self.sizer.Add(self.panelDeImagen, pos=(0, 0), span=(2, 3), flag=wx.TOP | wx.LEFT | wx.BOTTOM | wx.RIGHT, border=15)
        self.panel.SetSizer(self.sizer)
        self.sizer.Fit(self)
        #Binding de los elementos a sus funciones
        self.takeButton.Bind(wx.EVT_BUTTON, self.take_picture)
        self.toggle.Bind(wx.EVT_TOGGLEBUTTON, self.take_continuouspicture)
    #Timer de la captura continua
    def update(self, event):
        #Contador de elementos
        global count
        count = count + 1
        #Atributos de la camara
        self.camera = capture
        self.camera.set(3, width)
        self.camera.set(4, height)
        ret, image = self.camera.read()
        #Tag de la imagen
        self.tag = str(self.now.hour) +\
                "_" + str(self.now.minute) + "_" + str(self.now.second) +\
                "_" + str(self.now.day) + "_" + str(self.now.month) + "_" + str(self.now.year)
        #Captura de la imagen
        cv2.imwrite(personPath +"_" + self.tag + "_" + str(count) + ".jpg", image)
        print(count)
    #Funcion de captura singular
    def take_picture(self, e):
        global height
        global width
        global tag
        #Crea la carpeta en caso de que no exista
        if not os.path.exists(personPath):
            print('Carpeta creada: ', personPath)
            os.makedirs(personPath)
        #Atributos de la camara
        self.camera = capture
        self.camera.set(3, width)
        self.camera.set(4, height)
        return_value, image = self.camera.read()
        #Tag de la imagen
        self.tag = str(self.now.hour) +\
        "_" + str(self.now.minute) + "_" + str(self.now.second) +\
        "_" + str(self.now.day) + "_" + str(self.now.month) + "_" + str(self.now.year) + ".jpg"
        #Captura de la imagen
        cv2.imwrite(personPath +"_" + self.tag + "_" + ".jpg", image)
        cv2.imwrite(personPath +"_" + self.tag + "_" + ".jpg", image)
    def take_continuouspicture(self, e):
        #Estado del boton (ON/OFF)
        state = e.GetEventObject().GetValue()
        #Atributos de la camara
        self.camera = capture
        self.camera.set(3, width)
        self.camera.set(4, height)
        ret, image = self.camera.read()
        #Crea la carpeta en caso de que no exista
        if not os.path.exists(personPath):
            print('Carpeta creada: ', personPath)
            os.makedirs(personPath)
        #Switch del timer utilizado
        if state:
            self.toggle.SetLabel("Pause")
            self.timer.Start(1000)
        else:
            self.toggle.SetLabel("Start")
            self.timer.Stop()

#Panel de la camara
class webcamPanel(wx.Panel):
    #Atributos de la camara
    def __init__(self, parent, capture, fps=30):
        wx.Panel.__init__(self, parent)
        self.camera = capture
        capture.set(3, 640)
        capture.set(4, 360)
        return_value, frame = self.camera.read()
        height, width = frame.shape[:2]
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        #Elementos del panel de la webcam
        self.SetSize((width, height))
        self.bmp = wx.Bitmap.FromBuffer(width, height, frame)
        self.timer2 = wx.Timer(self,id=TIMER_ID2)
        self.timer2.Start(int(1000 / fps))
        self.timer = wx.Timer(self,id=TIMER_ID1)
        self.timer.Start(1000)
        #Binding de los elementos a sus funciones
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_TIMER, self.NextFrame)
    #Creacion de la imagen de la webcam
    def OnPaint(self, e):
        dc = wx.BufferedPaintDC(self)
        dc.DrawBitmap(self.bmp, 0, 0)
    #Generacion del frame per second
    def NextFrame(self, e):
        return_value, frame = self.camera.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.bmp.CopyFromBuffer(frame)
        self.Refresh(eraseBackground=False)

#main loop
if __name__ == "__main__":
    app = wx.App()
    Imagenes(None, title='Imagenes').Show()
    app.MainLoop()
    capture.release
    cv2.destroyAllWindows
