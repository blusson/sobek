import tkinter
from PIL import Image, ImageDraw
from sobek.network import network
import numpy as np

class Sketchpad(tkinter.Canvas):
    def __init__(self, parent, predictionLabel, **kwargs, ):
        super().__init__(parent, **kwargs)
        self.bind("<Button-3>", self.test)
        self.bind("<B1-Motion>", self.add_line)
        self.PILImage = Image.new("F", (560, 560), 100)
        self.draw = ImageDraw.Draw(self.PILImage)
        self.MNISTNN = network.networkFromFile("MNIST30epoch")
        self.predictionLabel = predictionLabel

    def add_line(self, event):
        self.create_oval((event.x+32, event.y+32, event.x-32, event.y-32), fill="black")
        self.draw.ellipse([event.x-32, event.y-32, event.x+32, event.y+32], fill="black")
        smallerImage = self.PILImage.reduce(20)
        imageAsArray = np.array(smallerImage.getdata())
        imageAsArray = (100 - imageAsArray)/100
        self.predictionLabel['text'] =  ( "Predicted number : "  + str(np.argmax(self.MNISTNN.process(imageAsArray))))

    def test(self, event):
        self.PILImage = Image.new("F", (560, 560), 100)
        self.draw = ImageDraw.Draw(self.PILImage)
        self.delete("all")

window = tkinter.Tk()
window.title("Number guesser")
window.resizable(False, False)
window.columnconfigure(0, weight=1)
window.rowconfigure(0, weight=1)

predictionLabel = tkinter.Label(window, text="Predicted number :")

sketch = Sketchpad(window, predictionLabel, width=560, height=560)
sketch.grid(column=0, row=0, sticky=(tkinter.N, tkinter.W, tkinter.E, tkinter.S))
predictionLabel.grid(column=0, row=1)

window.mainloop()