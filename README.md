# cats vs dogs 猫狗大战 主流平台实现

This is the solution of Kaggle cats vs dogs by caffe,tensorflow and keras.

猫狗大战是深度学习应用于计算机视觉的一个典型案例，源于[Kaggle比赛](https://www.kaggle.com/c/dogs-vs-cats)，它一共有25000张训练图片(猫和狗各12500张)![](https://i.imgur.com/v7E4fut.jpg)

现在已经有很多针对各个框架下的实现，但存在以下几个问题:

1.描述简单，未提供完整解决方案及测试结果

2.实现复杂，代码长时间未做更新，以致新版本的库无法使用

3.架构设计不合理，没有可扩展性，需要改动很多代码才能用于新的任务

本项目针对以上这些问题，提供了caffe、tensorflow和keras等主流平台的实现，给出全流程解决方案，可以无缝切换到自己的task。


## 数据下载和结构安排

下载本项目后新建data子文件夹


	git clone https://github.com/imistyrain/cat-vs-dog
	mkdir data

然后去[Kaggle下载页面](https://www.kaggle.com/c/dogs-vs-cats/data)下载，解压train.zip到data文件夹，文件结构组织为:
![](https://i.imgur.com/NpdKPKs.jpg)

## 数据清洗

官网下载的数据存在异常数据，大致可分为图中无目标(15张),猫狗都有(15张)，卡通图(6张),难以区分(28张)和标注反了(7张)等几大类.

	cd Keras
	python filtererrors.py

![](https://i.imgur.com/BqpIVsh.jpg)

经过这个过程处理后图片数量由25000张缩减到24936张.

## caffe

首先安装caffe，网上已有很多相关教程，数不赘述。

然后生成用于训练和验证的文件名列表，可通过

	cd caffe/util
	python preprocess.py

完成，代码执行后会在util文件夹下生成train.txt和val.txt，里面包含了用于训练和验证的文件名列表及其对应的标签

开始训练,

	sh train.sh

调整需要使用的模型及其对应的参数，一键完成训练.

目前能够达到的精度如下:


Name| Acc. test | finetuned Acc. test. | Train time | Forward pass time | On disk model size | Year | Paper
------------------ | --- | --- | --- | --- | --- | --- | ---
AlexNet | 95.62%  | 98.26% | **35m** | **3.01 ms** | 227.5Mb | 2012 | [link](http://papers.nips.cc/paper/4824-imagenet-classification-with-deep-convolutional-neural-networks.pdf)
SqeezeNet v1.1 | 96.20% | 99.44% | ~2h | 3.91 ms| **2.9Mb** | 2016 | [link](http://arxiv.org/pdf/1602.07360v3.pdf)
GoogLeNet | 94.62% | **99.58%** | 50m | 11.73 ms | 41.3Mb | 2014 | [link](http://www.cs.unc.edu/~wliu/papers/GoogLeNet.pdf)
BN-GoogleNet | |99.36% |
VGG-16 | 97.17% | 99.40% | 5h20m | 15.41 ms | 537.1Mb | 2014 | [link](http://arxiv.org/pdf/1409.1556.pdf)
VGG-19 | **97.46%** | 99.50% | 25h50m | 19.23 ms | 558.3Mb | 2014 | [link](http://arxiv.org/pdf/1409.1556.pdf)
Network-In-Network | 93.65% | 98.49% | ~2h | 3.17 ms | 26.3Mb | 2014 | [link](http://arxiv.org/pdf/1312.4400v3.pdf)
ResNet-50 | 96.10% | 99.52% | 18h | 24.91 ms | 94.3Mb | 2015 | [link](https://arxiv.org/pdf/1512.03385.pdf)
ResNet-101 | 96.39% | 99.48% | 1d 20h | 40.95 ms | 170.5Mb | 2015 | [link](https://arxiv.org/pdf/1512.03385.pdf)
MobileNet | 97.22% | 97.8%
ShuffleNet | 93.70 |98.70% |

训练采用的GPU为1080Ti.

部署参考cpp4caffe项目，这是一个C++工程.


## tensorflow

tensorflow使用预训练的VGG19进行微调，精度为96%+

	python train_vgg19.py

如果有多块GPU，可以使用

	python multigpu_train.py

加速训练

如果配备了Intel的计算棒，可以将其转换为graph格式，然后运行

	sh build.sh #编译所必须的程式
	sh train.sh #训练和导出模型
	sh ncs.sh #转换为计算棒需要的格式
	python run_ncs.py #在计算棒上测试

## keras

keras需要先把猫和狗的图片分到两个不同的文件夹下，这可以通过train.py中的mklink函数完成.

![](https://i.imgur.com/lQXG8vC.jpg)

	python train.py #训练模型
	python keras2tf.py #转换为tnsorflow格式

经测试所能达到的精度如下:


Model |	Size |	Accuracy
--- | --- | --- 
VGG16 |	528MB |	
ResNet50 |	99MB |	99.78%
InceptionV3 |	92MB |	
Xception |	88MB |	
InceptionResNetV2 |	215MB |	

![](https://i.imgur.com/xn47OvN.jpg)

## web by flask

	python app.py

打开浏览器，输入网址http://localhost:5000/

点击Choose...选择要识别的文件上传即可，稍等片刻即可得到结果


![](https://i.imgur.com/wBA6uuh.jpg)

![](https://i.imgur.com/plU8eue.jpg)

## 参考

[基于TensorFlow的Cats vs. Dogs（猫狗大战）实现和详解](https://blog.csdn.net/qq_16137569/article/details/72802387)

[kaggle-dogs-vs-cats-solution](https://github.com/mrgloom/kaggle-dogs-vs-cats-solution)

[Cat_or_dog-kaggle-vgg19-tensorflow](https://github.com/2012013382/Cat_or_dog-kaggle-vgg19-tensorflow)

[keras-cats-dogs-tutorial](https://github.com/jkjung-avt/keras-cats-dogs-tutorial)

[利用resnet 做kaggle猫狗大战图像识别，秒上98准确率](https://blog.csdn.net/shizhengxin123/article/details/72473245)

[keras-cats-dogs-tutorial](https://github.com/jkjung-avt/keras-cats-dogs-tutorial)

[Building powerful image classification models using very little data](https://blog.keras.io/building-powerful-image-classification-models-using-very-little-data.html)

[基于Android和微信小程序端的猫狗图像分类](https://github.com/wlkdb/dogs_vs_cats)