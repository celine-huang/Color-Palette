import math
import sys
from PIL import Image
import matplotlib.colors as scheme
import matplotlib.pyplot as plt
import matplotlib.patches as patch

#將matplotlib內建色碼表存入colors這個list
colors = []
for name, hexa in scheme.cnames.items():
    pixels = 0
    colors.append([name, hexa, pixels])

#讀入圖片
imgname = input('choose a picture: ')
try:
    img = Image.open(imgname)
except FileNotFoundError:
    print("File not found.")
    sys.exit()

#輸入色板顏色數量(matplotlib內建顏色其實有一百多種，但所選擇的圖片不一定有那麼多色塊，而色板太多顏色會太密密麻麻反而看不清楚，1-30間效果最好)
colornum = int(input('Quantity of color samples (1-30): '))
if colornum < 1 or colornum > 30:
    print("Invalid quantity, please enter a number between 1 and 30.")
    sys.exit()

#命名色板
palette = input('Name your palette: ')

#輸入色板副檔名
extension = input('Filename Extension: ')

#縮小圖片長寬各1/2(為了運算變快)/將圖片轉成RGB格式
x, y = img.size
x //= 2
y //= 2
img.thumbnail((x, y))
imgRGB = img.convert('RGB')

#以最小平方法求得每個pixel最接近的color code，算出最接近每種color code的pixel數量
for i in range(x-1):
    for j in range(y-1):
        r, g, b = imgRGB.getpixel((i, j))
        leastsquare = 0
        code = 0
        for k in range(len(colors)):
            r_err = pow((r - int(colors[k][1][1:3], 16)), 2)
            g_err = pow((g - int(colors[k][1][3:5], 16)), 2)
            b_err = pow((b - int(colors[k][1][5:], 16)), 2)
            err = r_err + g_err + b_err
            if k == 0 or err < leastsquare:
                leastsquare = err
                code = k
        colors[code][2] += 1

#由多至少排序所有color code
def takenum(ele):
    return ele[2]
colors = sorted(colors, key = takenum, reverse = True)

#使用matplotlib畫出色板
fig, ax = plt.subplots()
ax.invert_yaxis()
for i in range(colornum):
    rec = patch.Rectangle((0, (1/colornum)*i), 0.5, (1/colornum), facecolor = colors[i][0], fill=True)
    ax.add_patch(rec)
    colorcode = (colors[i][0], colors[i][1])
    ax.text(0, (1/colornum)*(i+1), " ".join(colorcode), fontsize=12)
plt.axis('off')
plt.title(palette, fontsize=14, loc='left')
try:
    plt.savefig(palette+'.'+extension, format=extension)
except ValueError:
    print("Format '%s' is not supported, supported formats: eps, jpeg, jpg, pdf, pgf, png, ps, raw, rgba, svg, svgz, tif, tiff." %extension)