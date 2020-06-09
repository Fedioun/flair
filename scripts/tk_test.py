from tkinter import Tk, Canvas, Frame, BOTH, Label, Scrollbar, RIGHT, LEFT,  Y, X
from PIL import Image, ImageTk



class App(Frame):


    def __init__(self):
        super().__init__()
        self.pack()

        self.scrollbar = Scrollbar(self.master)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.canvas = Canvas(self, yscrollcommand=self.scrollbar.set, height=500, width=300)
        self.canvas.pack(fill=X, expand=1)

        self.scrollbar.config(command=self.canvas.yview)

    def setBg(self, imagePath):
        img = Image.open(imagePath)
        img.thumbnail([1000, 1000])
        self.photo = ImageTk.PhotoImage(img)
        background_label = Label(self.canvas, image=self.photo, borderwidth=0)
        #background_label.place(x=0, y=0, relwidth=1, relheight=1)

        background_label.bind("<Button-1>", self.callback)


        background_label.pack()

        print(self.master.winfo_screenheight())




    def callback(self, event):
        print("clicked at", event.x, event.y)


def main():
    imagePath = "/home/nosmoth/Documents/Datasets/desfosses_omnipage_et_jsonSimon/desfosses sample/1962_T2_T_0722.jpg"
    root = Tk(height=1000)
    root.resizable(0, 0)
    if False:
        fr = Frame(root)
        img = Image.open(imagePath)
        photo = ImageTk.PhotoImage(img)
        background_label = Label(fr, image=photo)
        #background_label.place(x=0, y=0, relwidth=1, relheight=1)
        background_label.pack()

        fr.pack()
    else:
        ex = App()
        ex.setBg(imagePath)
    #root.geometry("400x250+300+300")
    root.mainloop()


if __name__ == '__main__':
    main()
