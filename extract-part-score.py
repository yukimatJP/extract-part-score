from PIL import Image, ImageDraw
import glob

NUM_OF_LINE_PER_PAGE = 10 # 最終出力の1ページごとの行数

def combine_images_vertically(im_1, im_2):
    im_concat = Image.new('RGB', (im_1.width, im_1.height + im_2.height))
    im_concat.paste(im_1, (0, 0))
    im_concat.paste(im_2, (0, im_1.height))
    return im_concat


############################
##    各行譜面データの抽出    ##
############################

img_list = sorted(glob.glob("ScorePages/ScorePages_*")) # ScorePages/ScorePages_*.png の一覧を取得

for i, img in enumerate(img_list):

  print(img)

  im = Image.open(img)

  for j in range(0,2): # 1ページに2行抽出したい行がある場合
    im_crop = None

    if (j==0):
      im_crop = im.crop((100, 1650, 7000, 2050))  # 1行目： 左上を (0, 0) とし、左・上・右・下の絶対座標を指定
    else:
      im_crop = im.crop((100, 3600, 7000, 4050))  # 2行目： 左上を (0, 0) とし、左・上・右・下の絶対座標を指定

    im_crop.save('ScorePages/' + str(i) + "-" + str(j) + '.png', quality=100) # 抽出したデータ（1行の譜面）を保存（★1）


############################
##    各行譜面データの結合    ##
############################


page_counter = 0 # ページ番号
line_counter = 0 # ページ内行番号

im_combined = None

for i, img in enumerate(img_list):

  for j in range(0,2):

    im = Image.open('ScorePages/' + str(i) + "-" + str(j) + '.png')  # （★1）で保存したデータを読み込み

    if (im_combined == None): # 最初のページのとき
      im_combined = im
    else:
      im_combined = combine_images_vertically(im_combined, im)

    line_counter += 1

    if (line_counter > NUM_OF_LINE_PER_PAGE):
      im_combined.save('ScorePages/_combined_' + str(page_counter) + '.png', quality=100) # ページ p.{page_counter} を保存
      line_counter = 0
      page_counter += 1
      im_combined = None

  if im_combined != None:
    im_combined.save('ScorePages/_combined_' + str(page_counter) + '.png', quality=100) # ページ p.{page_counter} を保存

