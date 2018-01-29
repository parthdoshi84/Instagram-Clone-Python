from PIL import Image, ImageOps, ImageDraw
import os
import csv
import cv2


def circular_image(image,user):
    im = Image.open(image)
    bigsize = (im.size[0] * 2, im.size[0] * 2)
    mask = Image.new('L', bigsize, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(im.size, Image.ANTIALIAS)
    im.putalpha(mask)
    image_name = user + "profile.png"
    im.save(image_name)
    return image_name


'''def crop_circular_image(image,user):


    x_offset = 139
    y_offset = 113

    ID_img = cv2.imread(image)
    x_text = 554 / 2
    y_text = 715

    title = "Administration Executive"

    circle = cv2.imread('Circle.png')
    circle = cv2.cvtColor(circle, cv2.COLOR_BGR2GRAY)
    color = circle[0, 0]

    default = cv2.imread('Default.png')
    defaulter = False


    files = os.listdir("FYs")
    message = ""
    for file in files:
        if file.endswith(".jpg") or file.endswith(".png") or file.endswith(".JPG") or file.endswith(".PNG"):
            s_img = cv2.imread("FYs/" + file)
            message = file[:-4]
        elif file.endswith(".JPEG") or file.endswith(".jpeg"):
            s_img = cv2.imread("FYs/" + file)
            message = file[:-5]
        else:
            s_img = l_img
            continue
        print message

        # s_img = cv2.cvtColor(s_img,cv2.COLOR_BGR2GRAY)
        s_img = cv2.resize(s_img, (276, 277), interpolation=cv2.INTER_CUBIC)
        # s_img = cv2.cvtColor(s_img,cv2.COLOR_GRAY2BGR)

        l_img = ID_img
        for channel in range(0, 3):
            for i in range(0, 277):
                for j in range(0, 276):
                    if circle[i, j] != color:
                        l_img[i + y_offset, j + x_offset, channel] = s_img[i, j, channel]

        cv2.imwrite('ID.png', l_img)

        s_img = Image.open("ID.png")
        draw = ImageDraw.Draw(s_img)
        fontName = ImageFont.truetype('ADAM.CG PRO.ttf', 40)
        fontTitle = ImageFont.truetype('GOTHIC.TTF', 30)
        msgSize = draw.textsize(message, font=fontName)
        xOff = msgSize[0] / 2
        draw.text((x_text - xOff, y_text), message, (0, 0, 0), font=fontName)

        titleSize = draw.textsize(title, font=fontTitle)
        xOff = titleSize[0] / 2
        draw.text((x_text - xOff, y_text + 50), title, (0, 0, 0), font=fontTitle)

        s_img.save("IDs/" + message + " ID.png")
'''

