from PIL import Image, ImageOps
def convertDark(image,const):
    darkimg=Image.open(image)
    edit=ImageOps.grayscale(darkimg)
    edit=edit.convert('RGBA')
    editD=edit.getdata()
    newImg=[]
    for i in editD:
        newImg.append((255,255,255,i[0]-const))
    edit.putdata(newImg)
    edit.save('outputDark.png')
    return edit

def convertLight(image,const):
    darkimg=Image.open(image)
    edit=ImageOps.grayscale(darkimg)
    edit=ImageOps.invert(edit)
    edit=edit.convert('RGBA')
    editD=edit.getdata()
    newImg=[]
    for i in editD:
        newImg.append((0,0,0,int(i[0]/2+const)))
    edit.putdata(newImg)
    edit.save("outputLight.png")
    return edit
dark=convertDark('dark.jpg',50)
light=convertLight('light.jpg',50)
final=Image.alpha_composite(dark, light).save("output.png")
final.save("output.png")
