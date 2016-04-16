from PIL import Image, ImageFilter, ImageDraw, ImageFont
import sys
import argparse
import os
from os.path import basename


def processImage(grey, addLegend):

	out = Image.new('RGB', grey.size)

	# IRE range and band colors
	IRErange = [-7, 2, 8, 15, 24, 43, 47, 54, 58, 77, 84, 93, 100, 109]
	colorBands = [[77,41,80],[19,102,148],[29,133,160],[71,164,168],[133,133,133],[102,183,77],[159,159,159],[247,129,117],[209,209,209],[240,229,145],[255,253,56],[253,140,37],[252,13,27]]
	numColorBands = len(colorBands)

	if addLegend:
		legendWidth = 50
		outWithLegend = Image.new('RGB', [legendWidth+grey.size[0],grey.size[1]]) 
		draw = ImageDraw.Draw(outWithLegend)

		# create outWithLegend
		for i, color in enumerate(colorBands):
			y0 = int(float(i)/numColorBands*outWithLegend.size[1])
			y1 = int(float(i+1)/numColorBands*outWithLegend.size[1])-1
			outWithLegend.paste(tuple(color),(0,y0,legendWidth, y1))
			draw.text(( 3, y0), str(IRErange[i]), (0,0,0))

	# slow...
	# for y in range(grey.size[1]):
	#     for x in range(grey.size[0]):
	#         for i in range(0,len(IRErange)-1):
	#             if pix[x, y] >= 255/109.0*IRErange[i] and pix[x, y] < 255/109.0*IRErange[i+1]:
	#                 pixout[x, y] = tuple(ColorBands[i])

	# process image
	for i in range(0,len(IRErange)-1):
		vmin = int(255/109.0*IRErange[i])
		vmax = int(255/109.0*IRErange[i+1])
		mask = grey.point(lambda i: i >= vmin and i < vmax and 255 )
		out.paste(tuple(colorBands[i]),None,mask)

	if addLegend:
		outWithLegend.paste(out,(legendWidth,0))
		return outWithLegend
	else:
		return out


	
def main():
	parser = argparse.ArgumentParser(description='Generate false color image.')
	parser.add_argument('images', metavar='image', nargs='+',
	                   help='image path(s)')
	parser.add_argument("--save", help="save output image. Same name, but with _falsecolor suffix",action="store_true")
	parser.add_argument("--legend", help="add legend to output.",action="store_true")
	parser.add_argument("--nodisplay", help="image is not displayed. If active, then image is saved.",action="store_true")
	parser.add_argument("--rgb", help="process RGB channels separately",action="store_true")

	args = parser.parse_args()

	for imgPath in args.images:
		im = Image.open( imgPath )
		# split channels and concatenate them into single image
		if args.rgb and im.mode != 'L' :
			im = im.split()
			r = im[0]
			g = im[1]
			b = im[2]
			grey = Image.new('L', [3*r.size[0],r.size[1]])
			grey.paste(r,(0, 0))
			grey.paste(g,(r.size[0], 0))
			grey.paste(b,(2*r.size[0], 0))
		else:
			grey = im.convert('L')

		outImg = processImage(grey, args.legend)

		if not args.nodisplay:
			outImg.show()
		if args.save or args.nodisplay:
			if args.nodisplay and not args.save:
				print 'saving output image as it is not being displayed'
			outPath = os.path.splitext(basename(imgPath))[0] + '_falsecolor.jpg'
			print outPath
			outImg.save( outPath, 'JPEG' )

if __name__ == "__main__":
    main()



