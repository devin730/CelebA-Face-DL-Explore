import sys
import tools_matrix as tools
import caffe
import cv2
import numpy as np
import matplotlib.image as gImage
from PIL import Image

deploy = './model/faceangle_mtcnn_Pnet.prototxt'
caffemodel = './model/faceangle_mtcnn_Pnet.caffemodel'
net_12 = caffe.Net(deploy,caffemodel,caffe.TEST)

deploy = './model/faceangle_mtcnn_Rnet.prototxt'
caffemodel = './model/faceangle_mtcnn_Rnet.caffemodel'
net_24 = caffe.Net(deploy,caffemodel,caffe.TEST)

deploy = './model/faceangle_mtcnn_Onet.prototxt'
caffemodel = './model/faceangle_mtcnn_Onet.caffemodel'
net_48 = caffe.Net(deploy,caffemodel,caffe.TEST)

def detectFace(img_path,threshold):
    img = cv2.imread(img_path)
    caffe_img = (img.copy()-127.5)/128
    origin_h,origin_w,ch = caffe_img.shape
    scales = tools.calculateScales(img)
    out = []
    for scale in scales:
        hs = int(origin_h*scale)
        ws = int(origin_w*scale)
        scale_img = cv2.resize(caffe_img,(ws,hs))
        scale_img = np.swapaxes(scale_img, 0, 2)
        net_12.blobs['data'].reshape(1,3,ws,hs)
        net_12.blobs['data'].data[...]=scale_img
        caffe.set_device(0)
        caffe.set_mode_gpu()
        out_ = net_12.forward()
        out.append(out_)
    image_num = len(scales)
    rectangles = []
    for i in range(image_num):    
        cls_prob = out[i]['prob1'][0][1]
        roi      = out[i]['conv4-2'][0]
        out_h,out_w = cls_prob.shape
        out_side = max(out_h,out_w)
        rectangle = tools.detect_face_12net(cls_prob,roi,out_side,1/scales[i],origin_w,origin_h,threshold[0])
        rectangles.extend(rectangle)
    rectangles = tools.NMS(rectangles,0.7,'iou')

    if len(rectangles)==0:
        return rectangles
    net_24.blobs['data'].reshape(len(rectangles),3,24,24)
    crop_number = 0
    for rectangle in rectangles:
        crop_img = caffe_img[int(rectangle[1]):int(rectangle[3]), int(rectangle[0]):int(rectangle[2])]
        scale_img = cv2.resize(crop_img,(24,24))
        scale_img = np.swapaxes(scale_img, 0, 2)
        net_24.blobs['data'].data[crop_number] =scale_img 
        crop_number += 1
    out = net_24.forward()
    cls_prob = out['prob1']
    roi_prob = out['conv5-2']
    rectangles = tools.filter_face_24net(cls_prob,roi_prob,rectangles,origin_w,origin_h,threshold[1])
    
    if len(rectangles)==0:
        return rectangles
    net_48.blobs['data'].reshape(len(rectangles),3,48,48)
    crop_number = 0
    for rectangle in rectangles:
        crop_img = caffe_img[int(rectangle[1]):int(rectangle[3]), int(rectangle[0]):int(rectangle[2])]
        scale_img = cv2.resize(crop_img,(48,48))
        scale_img = np.swapaxes(scale_img, 0, 2)
        net_48.blobs['data'].data[crop_number] =scale_img 
        crop_number += 1
    out = net_48.forward()
    cls_prob = out['prob1']
    roi_prob = out['conv6-2']
    pts_prob = out['conv6-3']
    rectangles = tools.filter_face_48net(cls_prob,roi_prob,pts_prob,rectangles,origin_w,origin_h,threshold[2])

    return rectangles

threshold = [0.6,0.6,0.7]
imgpath = './image/fourpersons.jpg'
rectangles = detectFace(imgpath,threshold)
# print(len(rectangles))
# print(rectangles)
# image1 = gImage.imread(imgpath)
# print(image1.shape)
# plt.axis('off')
# plt.imshow(image1)
# plt.show()
mat_image = cv2.imread(imgpath)
for rectangle in rectangles:
    cv2.rectangle(mat_image,(int(rectangle[0]),int(rectangle[1])),(int(rectangle[2]),int(rectangle[3])),(255,255,255),3)
save_dir = './image/fourpersons_detect.jpg'
cv2.imwrite(save_dir,mat_image)
image2 = gImage.imread(save_dir)
# print(image2.shape)
# plt.axis('off')
# plt.imshow(image2)
# plt.show()