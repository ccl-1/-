import dota_utils as util
from dota_utils import GetFileFromThisRootDir
from PIL import Image
import os

def SplitSingle(img_path,out_path):
	imagelist = GetFileFromThisRootDir(img_path)
	imagenames = [util.custombasename(x) for x in imagelist if (util.custombasename(x) != 'Thumbs')]
	for name in imagenames:
		width,height = 628,600
		IMAGE_PATH = os.path.join(img_path, name + ".png")
		im = Image.open(IMAGE_PATH) #打开图片句柄
		pSize = im.size
		xNum = int(pSize[0]/width)
		yNum = int(pSize[1]/height)
		print("size  " ,xNum,'  ',yNum)
		for yIndex in range(yNum):
			for xIndex in range(xNum):
				# print("pic : " , xIndex , "_" , yIndex)
				box = (xIndex*width,yIndex*height,(xIndex+1)*width,(yIndex+1)*height) #设定裁剪区域
				region = im.crop(box)  #裁剪图片，并获取句柄region
				name2 = os.path.join(out_path,name + "_%s_%s.png" % (yIndex,xNum-1-xIndex))
				print(name2)
				region.save(name2)


basepath = "F:\data\\berlin-aoi-dataset\\data_CitySegmentation\\test"
outpath = "F:\data\\berlin-aoi-dataset\\data_CitySegmentation\\test_split"
imagepath = os.path.join(basepath, 'images')
outimagepath = os.path.join(outpath, 'images')

labelpath = os.path.join(basepath, 'labelTxt')
outlabelpath = os.path.join(outpath, 'labelTxt')

if not os.path.isdir(outpath):
	os.mkdir(outpath)
if not os.path.isdir(outimagepath):
	os.mkdir(outimagepath)
if not os.path.isdir(outlabelpath):
	os.mkdir(outlabelpath)

# 分割图像
SplitSingle(imagepath,outimagepath)
# 分割标签
SplitSingle(labelpath,outlabelpath)


