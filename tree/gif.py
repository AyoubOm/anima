from PIL import Image

def addToGif(canvas, imageId, images, filebase):
	"""
	The gif is created using captures of drawing state
	"""
	filename = filebase+"out_tree{0:03d}".format(imageId)
	canvas.postscript(file = filename + '.eps')
	img = Image.open(filename + '.eps')
	img.save(filename + '.png', 'png') # appending image from ".eps" directly doesn't work
	img = Image.open(filename + '.png')
	images.append(img)
