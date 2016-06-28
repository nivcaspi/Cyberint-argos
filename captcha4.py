from PIL import Image, ImageEnhance

def captcha_to_string(filename):
    img = Image.open(filename)
    nx, ny = img.size
    im2 = img.resize((int(nx*5), int(ny*5)), Image.BICUBIC)
    im2.save('temp.png')
    img = Image.open('temp.png')
    enh = ImageEnhance.Contrast(img)
    enh.enhance(1.3).show("30% more contrast")
    img.save('temp2.png')
    img = img.convert("RGBA")
    pixdata = img.load()
    # Clean the background noise, if color != black, then set to white.
    for y in xrange(img.size[1]):
        for x in xrange(img.size[0]):
            if pixdata[x, y][0] < 90:
                pixdata[x, y] = (0, 0, 0, 255)

    for y in xrange(img.size[1]):
        for x in xrange(img.size[0]):
            if pixdata[x, y][1] < 136:
                pixdata[x, y] = (0, 0, 0, 255)

    for y in xrange(img.size[1]):
        for x in xrange(img.size[0]):
            if pixdata[x, y][2] > 0:
                pixdata[x, y] = (255, 255, 255, 255)


    img.save("input-black.gif", "GIF")


    im_orig = Image.open('input-black.gif')
    big = im_orig.resize((116, 56), Image.NEAREST)

    ext = ".tif"
    big.save("input-NEAREST" + ext)


    from pytesser.pytesser import *

    image = Image.open('input-NEAREST.tif')
    return image_to_string(image)
