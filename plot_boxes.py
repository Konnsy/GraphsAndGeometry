from PIL import ImageDraw, Image
import uuid
import cv2
import os

def writeBoxesToImage(img, boxes, fill_color=(255,0,0), lineWidth = 2):
    """
    write coloured boxes to an image of gray values
    img shape: (x, y)
    boxes format: (x1, y1, x2, y2)
    """
	tmpPath = "tmp_" + str(uuid.uuid4()) + ".png"
	cv2.imwrite(tmpPath, img)
	imOut = Image.open(tmpPath).convert("RGB")
	os.remove(tmpPath)
	d = ImageDraw.Draw(imOut)

	for box in boxes:
		[x1, y1, x2, y2] = box
		d.line([(x1,y1),(x2,y1)], fill=fill_color, width=lineWidth)
		d.line([(x2,y1),(x2,y2)], fill=fill_color, width=lineWidth)
		d.line([(x2,y2),(x1,y2)], fill=fill_color, width=lineWidth)
		d.line([(x1,y2), (x1,y1)], fill=fill_color, width=lineWidth)
				
	imOut.save(tmpPath)
	img = cv2.imread(tmpPath)
	os.remove(tmpPath)
	return img