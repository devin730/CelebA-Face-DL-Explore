## 一、数据集的整理

1. CelebA数据集的介绍：http://mmlab.ie.cuhk.edu.hk/projects/CelebA.html
2. 处理筛选CelebA人脸数据集的方法可以参考这个网页: https://www.jianshu.com/p/c1bc1e7f72a7
3. 筛选数据集的代码经过整理和测试、修改分别是process_label.py、image_classify.py、getFaceRect.py三个文件。image_classify中 dir = ".\Img\img_align_celeba\img_align_celeba"，这个Img文件夹来自CelebA数据集。数据集百度盘地址：https://pan.baidu.com/s/1eSNpdRG#list/path=%2F

## 二、Caffe for Python

1. 内容在mtcnn文件夹中