from PIL import Image, ImageEnhance
from pytesser.pytesser import image_to_string


def captcha_to_string(filename):
    # get captcha file and size
    img = Image.open(filename)
    nx, ny = img.size
    # enhance image readability
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
    # convert to .gif, resize and convert to .tif
    img.save("input-black.gif", "GIF")
    im_orig = Image.open('input-black.gif')
    big = im_orig.resize((116, 56), Image.NEAREST)
    big.save("input-NEAREST" + ".tif")
    image = Image.open('input-NEAREST.tif')
    # use tesseract OCR engine
    return image_to_string(image)
