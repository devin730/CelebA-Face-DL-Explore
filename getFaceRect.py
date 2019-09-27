from PIL import Image
import face_recognition
import os

#for (int i = 1; i <= 10; i++)
#dir = './hasGlass/'
dir = './noGlass/'
list = os.listdir(dir)
print(len(list))
for i in range(0, len(list)):
    imgName = os.path.basename(list[i])
    print(imgName)
    if (os.path.splitext(imgName)[1] != ".jpg"): continue

    imagePath = dir + imgName

    image = face_recognition.load_image_file(imagePath)

    face_locations = face_recognition.face_locations(image)

    for face_location in face_locations:

        # Print the location of each face in this image
        top, right, bottom, left = face_location
        # print("A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom, right))

        # You can access the actual face itself like this:
        width = right - left
        height = bottom - top
        if (width > height):
            right -= (width - height)
        elif (height > width):
            bottom -= (height - width) 
        face_image = image[top:bottom, left:right]
        pil_image = Image.fromarray(face_image)
        #pil_image.save('./hasGlass_face/face%s'%imgName)
        pil_image.save('./noGlass_face/face%s'%imgName)