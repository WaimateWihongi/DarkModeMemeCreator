from PIL import Image, ImageOps
from tkinter import filedialog, Menu
import tkinter, webbrowser, piexif
from PIL import Image, ImageTk
###TODO LIST
#Add Contrast Slider
#Maybe add warning for light mode images mainly consisting of black

#VARIABLES
version='2.1'
mode='Light'
darkImage=None
lightImage=None
windowX=400
windowY=400
convertedDark=None
convertedLight=None
convertedFull=None
def convertDark(image,const):
    darkimg=image
    edit=ImageOps.grayscale(darkimg)
    edit=edit.convert('RGBA')
    editD=edit.getdata()
    newImg=[]
    for i in editD:
        newImg.append((255,255,255,i[0]-const))
    edit.putdata(newImg)
    #edit.save('outputDark.png')
    return edit
def convertLight(image,const):
    darkimg=image
    edit=ImageOps.grayscale(darkimg)
    edit=ImageOps.invert(edit)
    edit=edit.convert('RGBA')
    editD=edit.getdata()
    newImg=[]
    for i in editD:
        newImg.append((0,0,0,int(i[0]/2+const)))
    edit.putdata(newImg)
    #edit.save("outputLight.png")
    return edit
def hello():
    print('TODO')
def changeMode():
    global mode
    black='#1a1a1b'
    if(mode=='Light'):
        imgCanvas.config(bg=black)
        sliderLight.configure(bg=black,fg='white')
        sliderDark.configure(bg=black,fg='white')
        txt[0].configure(bg=black,fg='white')
        txt[1].configure(bg=black,fg='white')
        root.configure(background=black)
        mode='Dark'
        return
    if(mode=='Dark'):
        imgCanvas.config(bg='#f0f0ed')
        root.configure(background='#f0f0ed')
        sliderLight.configure(bg='#f0f0ed',fg='black')
        sliderDark.configure(bg='#f0f0ed',fg='black')
        txt[0].configure(bg='#f0f0ed',fg='black')
        txt[1].configure(bg='#f0f0ed',fg='black')
        mode='Light'
        return
def openDarkImage():
    global darkImage
    darkImage=filedialog.askopenfilename(initialdir = "/",title = "Select Dark Image",filetypes = (("all files","*.*"),("PNG images","*.png")))
def openLightImage():
    global lightImage
    lightImage=filedialog.askopenfilename(initialdir = "/",title = "Select Light Image",filetypes = (("all files","*.*"),("PNG images","*.png")))
def generateImage():
    global darkImage, lightImage,convertedDark,convertedLight,convertedFull
    root.title('Generating Image...')
    if(darkImage==None)or(lightImage==None):
        if(darkImage==None):
            darkImage='bin/noPic.png'
        if(lightImage==None):
            lightImage='bin/noPic.png'
    dImg=Image.open(darkImage)
    lImg=Image.open(lightImage)
    dImg=convertDark(dImg,sliderDark.get())
    lImg=convertLight(lImg,sliderLight.get())
    lImg=lImg.resize(dImg.size,Image.ANTIALIAS)
    fullImg=Image.alpha_composite(dImg, lImg)
    fullImg.thumbnail((200,200),Image.ANTIALIAS)
    convertedLight,convertedDark,convertedFull=lImg,dImg,fullImg
    photo=ImageTk.PhotoImage(fullImg)
    imgCanvas.delete('all')
    imgCanvas.create_image(0,0,image=photo,anchor='nw')
    root.title('Dark Mode Meme Creator (v'+version+')')
    root.mainloop()
def saveLight():
    diag=filedialog.asksaveasfile(mode='w',defaultextension='.png',initialfile='Light.png')
    if(diag==None):
        return
    convertedLight.save(diag.name)
def saveDark():
    diag=filedialog.asksaveasfile(mode='w',defaultextension='.png',initialfile='Dark.png')
    if(diag==None):
        return
    convertedDark.save(diag.name)
def saveFull():
    diag=filedialog.asksaveasfile(mode='w',defaultextension='.png',initialfile='Meme.png')
    if(diag==None):
        return
    convertedFull.save(diag.name)
def openWebsite():
    webbrowser.open_new("https://sites.google.com/view/breezy121/programming/dark-mode-meme-creator?authuser=1")

#ROOT
root=tkinter.Tk()
root.title('Dark Mode Meme Creator (v'+version+')')
root.geometry(str(windowX)+'x'+str(windowY))
root.iconbitmap('bin/icon.ico')
menubar = Menu(root)
imgCanvas=None
root.resizable(False, False)

#MENUS
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Open Light Image", command=openLightImage)
filemenu.add_command(label="Open Dark Image", command=openDarkImage)
filemenu.add_separator()
filemenu.add_command(label="Save", command=saveFull)
filemenu.add_command(label='Save Light Image',command=saveLight)
filemenu.add_command(label='Save Dark Image',command=saveDark)
filemenu.add_separator()
filemenu.add_command(label="Website [Updates]", command=openWebsite)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="Menu", menu=filemenu)

#GUI ELEMENTS
b = [tkinter.Button(root, command=generateImage, text="Generate Image"),tkinter.Button(root, command=changeMode, text="Change Mode"),]
txt=[tkinter.Label(root, text='Light Mode'),tkinter.Label(root,text='Dark Mode')]
sliderLight=tkinter.Scale(root, from_=100, to=-100, length=200,highlightthickness=0)
sliderDark=tkinter.Scale(root, from_=100, to=-100, length=200,highlightthickness=0)
imgCanvas=tkinter.Canvas(width=200,height=200,highlightthickness=0)

#GUI PLACING
imgCanvas.place(relx=0.5,rely=0.4,anchor='center')
sliderLight.place(relx=0.1, rely=0.4,anchor='center')
sliderDark.place(relx=0.825, rely=0.4,anchor='center')
b[0].place(relx=0.5,rely=0.9,anchor='center')
b[1].place(relx=0.5,rely=0.1,anchor='center')
txt[0].place(relx=0.135,rely=0.7,anchor='center')
txt[1].place(relx=0.85,rely=0.7,anchor='center')
root.config(menu=menubar)
root.mainloop()
