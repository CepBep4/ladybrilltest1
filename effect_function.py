from PIL import Image, ImageStat, ImageDraw, ImageFont, ImageOps, ImageEnhance
import numpy as np
from numpy import array, arange
from random import randint
import base64
import io
import math
import time

QUALITY = 5

size_st_ret={
    '7':'5',
    '8':'6',
    '9':'8',
    '11':'10',
    '12':'12',
    '15':'16',
    '20':'20',
}

size_st_bounds={
    '7':1.29,
    '8':1.43,
    '9':1.71,
    '11':2.0,
    '12':2.21,
    '15':2.79,
    '20':3.36
}


Image.MAX_IMAGE_PIXELS = 10**10

def text_render(image,
                x,
                y, 
                text: str| None=None,
                text_size: int | None=200,
                text_font: str | None='arial',
                straz_size: int | None=2,
                sample: int | None=19,
                threshold: int | None=5,
                distanse: int | None=0,
                coordx_correct: int | None=0,
                coordy_correct: int | None=0,
                skip_coords: list | None=[],
                add_coords: list | None=[]) -> Image:
    
    #Константы
    scale=1
    angle=90

    #print(add_coords, ' <- Новые координаты')

    #Корректировка координат
    coordx_correct=20#int(coordx_correct)
    coordy_correct=20#int(coordy_correct)

    distanse=int(distanse)

    x=int(x)
    y=int(y)
    sample=int(sample)
    threshold=int(threshold)/100
    threshold=0

    def get_pil_text_size(text, font_size, font_name):
        font = font_name
        size = font.getsize(text)
        return size

    #Открытие изображения
    img=image.copy()
    size_text=[0,0]
    if len(text_font) > 200:
        font=ImageFont.truetype(io.BytesIO(base64.b64decode(text_font.replace('data:application/octet-stream;base64,',''))), round(int(text_size)*7*0.5))
    else:
        text_font=f'fonts/{text_font}.ttf'
        font = ImageFont.truetype(text_font, round(int(text_size)*7*0.5))
    word_list=list(text)
    word_list.append(' ')
    draw = ImageDraw.Draw(img)
    for index,w in enumerate(word_list):
        #size_text=get_pil_text_size(text, round(int(text_size)*7*0.5), text_font) 
        if index==0:
            xy=(coordx_correct,coordy_correct)
        else:
            xy=(get_pil_text_size(word_list[index-1], round(int(text_size)*7*0.5), font)[0] ,0)
            size_text[0]+=xy[0]+distanse
            size_text[1]=get_pil_text_size(word_list[index-1], round(int(text_size)*7*0.5), font)[1]
        draw.text((coordx_correct+size_text[0],coordy_correct),w,(0,0,0),font=font, align='center')

        # draw = ImageDraw.Draw(img)
        # text_font=f'fonts/{text_font}.ttf'
        # font = ImageFont.truetype(text_font, round(int(text_size)*7*0.5))
        # size_text=get_pil_text_size(text, round(int(text_size)*7*0.5), text_font) 
        # draw.text((0, 0),text,(0,0,0),font=font, align='center')
    #Конвертация изображения в чёрно белое
    img=img.convert('L')
    img=ImageOps.invert(img)
    img=img.point(lambda x: 255 if x > threshold else 0, "1")
    img=img.crop((0,0,size_text[0],size_text[1]+50))
    cx, cy = [], []
    for x in np.arange(0,img.width):
        for y in np.arange(0,img.height):
            if img.getpixel((x,y)):
                cx.append(x)
                cy.append(y)
    xmax, xmin=max(cx)+sample, min(cx)-sample
    ymax, ymin=max(cy)+sample, min(cy)-sample
    img=img.crop((xmin,ymin,xmax,ymax))
    size_text[0]=xmax-xmin
    size_text[1]=ymax-ymin

    dot_spacing=sample

    image_array=np.array(img.convert('L'))
    height, width=image_array.shape
    dots_image=Image.new('RGB', (size_text[0], size_text[1]),"white")
    draw = ImageDraw.Draw(dots_image)
    dot_size=10
    count_straz=0
    # Размер кахдой точки
    coordx=[]
    coordy=[]
    for y in np.arange(0, height, dot_spacing):
        for x in np.arange(0, width, dot_spacing):
            global_check_add=False
            for j in add_coords:
                x_add, y_add = [float(x) for x in j.split()]
                x_add=round((dots_image.width/100)*x_add)
                y_add=round((dots_image.height/100)*y_add)
                #draw.ellipse([(x_skip-dot_size/2, y_skip-dot_size/2), (x_skip+dot_size/2,y_skip+dot_size/2)],fill="black")
                if x_add in np.arange(x, x+dot_spacing) and y_add in np.arange(y, y+dot_spacing):
                    global_check_add=True
            if image_array[y][x] > 225 and image_array[y-threshold][x] and image_array[y+threshold][x] or global_check_add:
                coordx.append(x)
                coordy.append(y)
                glob_check=False
                for i in skip_coords:
                    x_skip, y_skip = [float(x) for x in i.split()]
                    x_skip=round((dots_image.width/100)*x_skip)
                    y_skip=round((dots_image.height/100)*y_skip)
                    #draw.ellipse([(x_skip-dot_size/2, y_skip-dot_size/2), (x_skip+dot_size/2,y_skip+dot_size/2)],fill="black")
                    if x_skip in np.arange(x, x+dot_spacing) and y_skip in np.arange(y, y+dot_spacing) and not global_check_add:
                        glob_check=True
                if not glob_check:
                    count_straz+=1
                    draw.ellipse([(x-dot_size/2, y-dot_size/2), (x+dot_size/2,y+dot_size/2)],fill="black")
    # new_img=dots_image.crop((coordx_correct,coordy_correct,size_text[0],size_text[1]+50))
    coof=size_st_bounds[str(straz_size)]
    xmin=min(coordx)-20
    xmax=max(coordx)+20
    ymin=min(coordy)-20
    ymax=max(coordy)+20
    allx=dots_image.width
    ally=dots_image.height
    real_size=(round(((allx-(allx-xmax)-xmin)*coof)/74,2), round(((ally-(ally-ymax)-ymin)*coof)/74,2))

    return (dots_image.convert('1').resize((round(dots_image.width*coof),round(dots_image.height*coof))).convert('RGB'),\
            (round(dots_image.width*coof), round(dots_image.height*coof)),\
            count_straz, skip_coords, add_coords, real_size)



def dot_pattern(image,x,y, sample, shadow, layout, width, heidht, choice_straz, render=False):
    img=Image.open(io.BytesIO(base64.b64decode(image.replace('data:image/jpeg;base64','').replace('data:image/png;base64',''))))
    img=img.convert('RGB')
    img=ImageOps.invert(img)
    img.thumbnail((200,200))
    br_img = ImageEnhance.Brightness(img)
    img = br_img.enhance(int(shadow)/100) 
    width=int(width)
    heidht=int(width)
    real_size=(int(width), int(heidht))
    sample=int(sample)
    shadow=int(shadow)
    shadow=int(layout)
    siz=1

    size_straz={
        'ss5':7,
        'ss6':8,
        'ss8':9,
        'ss10':11,
        'ss12':12,
        'ss16':15,
        'ss20':19,
    }

    color_straz={
        'ss5':(101, 0, 205),
        'ss6':(1, 0, 242),
        'ss8':(2, 192, 255),
        'ss10':(0, 241, 2),
        'ss12':(241, 239, 0),
        'ss16':(254, 154, 3),
        'ss20':(241, 2, 1)
    }

    count_straz = {
        'ss5':['ss5',0],
        'ss6':['ss6',0],
        'ss8':['ss8',0],
        'ss10':['ss10',0],
        'ss12':['ss12',0],
        'ss16':['ss16',0],
        'ss20':['ss20',0]
    }   

    def halftone_child(img, sample, scale, format_paper,choice_straz, angle=90):
        format_paper=(round(img.width+format_paper[0]), round(img.height+format_paper[1]))
        img=img.resize(format_paper)
        img_grey = img.convert('L')
        img_grey = ImageOps.invert(img_grey)
        # img_grey.show()  # Convert to greyscale.
        channel = img_grey.split()[0]  # Get grey pixels.
        #channel = channel.rotate(angle, expand=1)
        size = format_paper
        bitmap = Image.new('RGB', (size[0], size[1]),color='white')
        bitmap = bitmap.convert('RGB')
        draw = ImageDraw.Draw(bitmap)
        sizeses=[]
        for x in np.arange(0, channel.size[0], sample):
            for y in np.arange(0, channel.size[1], sample):
                box = channel.crop((x, y, x+sample, y+sample))
                mean = ImageStat.Stat(box).mean[0]
                x_pos, y_pos = (x+box.size[1]/2) * scale, (y+box.size[1]/2) * scale
                box_edge = None
                straz = None
                
                if choice_straz == [] or len(choice_straz)==7:
                    mean_step, choice_straz = int((55+shadow)/7), ['ss5','ss6','ss8','ss10','ss12','ss16','ss20']
                else:
                    mean_step=int(55+shadow/len(choice_straz))

                if mean>240.0:
                    continue

                for index, straz in enumerate(reversed(choice_straz)):
                    if int(mean) in range(mean_step*index, mean_step*(index+1)):
                        box_edge=size_straz[straz]
                        straz=straz
                        break

                if box_edge:
                    if x_pos<channel.width-30 and y_pos<channel.height-30:
                        count_straz[straz][1]+=1
                        draw.ellipse((x_pos-box_edge, y_pos-box_edge, x_pos+box_edge, y_pos+box_edge),
                                    fill=0)
                        if render:
                            draw.ellipse((x_pos-(box_edge-3), y_pos-(box_edge-3), x_pos+(box_edge-3), y_pos+(box_edge-3)),
                                        fill=color_straz[straz])
                            if len(straz.replace('ss',''))==2:
                                draw.text((x_pos-5, y_pos-4.5), text=straz.replace('ss',''), fill=(0,0,0))
                            else:
                                if straz=='ss8':
                                    draw.text((x_pos-2, y_pos-4.5), text=straz.replace('ss',''), fill=(0,0,0))
                                else:
                                    draw.text((x_pos-2, y_pos-4.5), text=straz.replace('ss',''), fill=(255,255,255))
                

        strz=['ss5','ss6','ss8','ss10','ss12','ss16','ss20']
        count_strz=[]
        for i,j in zip(count_straz, strz):
            if i!=0:
                count_strz.append((j,i))
        #bitmap = bitmap.rotate(-angle, expand=1)
        return (bitmap, list(count_straz.values()))
    img_ht, count = halftone_child(img, sample, int(siz), real_size, choice_straz)
    return (img_ht if not render else img_ht.resize((img_ht.width*QUALITY, img_ht.height*QUALITY)), count, choice_straz)

def calligraphy(image: Image,
                min_dot: int | None=1,
                max_dot: int | None=27,
                speed: int | None=100,
                margin: float | None=0.9):
    # read image into numpy array
    img = np.asarray(image)
    # binarize and coarse-graining
    img = (img[::2, ::2, 0] < 128).astype(int)

    def make_dots(
        img, # 2d np array of 1s and 0s
        spd=speed, # speed up factor
        marg=margin, # minimum spacing between dots relative to dot size,
        max_ds=max_dot, # maximum dot diameter in pixels
        min_ds=min_dot, # minimum dot diameter in pixels    
    ):

        # start with blank image
        img2 = np.zeros(img.shape)
        h, w = img.shape

        # keep track of areas occupied by dots
        occ = set()
        
        ofs = int(spd ** 0.5)

        # iterate over dot sizes, decreasing
        for t in np.arange(max_ds, min_ds, -5):
            # iterate over pixels
            for i in np.arange(0, h, ofs):
                for j in np.arange(0, w, ofs):
                    d = 0
                    # increase dot diameter while 1. within bounds, b. corners of bounding box are black and 3. not already occupied
                    while (
                        i + d < h and j + d < w
                    ) and all(
                        [img[i + d, j + d], img[i, j + d], img[i + d, j]]
                    ) and not any(
                        [(i + d1, j + d2) in occ for d1, d2 in [(0, d), (d, 0), (d, d)]]
                    ):
                        d += 1
                    # consider dot only if exceeding threshold
                    if d > t:
                        m = int(marg * d)
                        ci = i + d // 2
                        cj = j + d // 2
                        d2 = (d//2) ** 2
                        # iterate over pixels in bounding box of dot + margin
                        for a in np.arange(i-m, i+d+m):
                            for b in np.arange(j-m, j+d+m):
                                # mark pixel as occupied by dot
                                occ.add((a, b))
                                # if within radius, draw to image
                                if (ci - a) ** 2 + (cj - b) ** 2 < d2:
                                    img2[a, b] = 1
        return img2


    # plt.imshow(make_dots(img), cmap='gray_r')
    # plt.axis('off')
    # idImage=randint(999999999999,9999999999999)
    # plt.savefig(f'loggs/{idImage}.jpg')

    threshold=30
    # return Image.open(f'loggs/{idImage}.jpg').convert('L').point(lambda x: 255 if x > threshold else 0, "1")

def dot_pattern_color(
            img: str,
            x_pos: int | None=0,
            y_pos: int | None=0,
            sample: int | None=19,
            scale: float | None=2.8,
            shadow: int | None=30,
            zoom: float | None=1.0,
            choice_straz: list |None=None,
            count_colors: int | None=16,
            old_colors: list | None=[],
            new_color: list | None=[],
            render: bool | None=False
        ):
    
    img=Image.open(io.BytesIO(base64.b64decode(img.replace('data:image/jpeg;base64','').replace('data:image/png;base64',''))))
    img.thumbnail((500,500))
    zoom=float(zoom)
    shadow=int(shadow)
    sample=int(sample)
    count_colors=int(count_colors)
    new_color = list(map(lambda x: tuple(map(int, x.replace('rgb','').replace('(','').replace(')','').replace(',','').split(' '))), new_color))

    def halftone_child(img, sample, scale, zoom, choice_straz=None, count_colors=16, old_colors=[], new_color=[], render=False,  angle=90):

        size_straz={
            'ss5':7,
            'ss6':8,
            'ss8':9,
            'ss10':11,
            'ss12':12,
            'ss16':15,
            'ss20':19,
        }

        format_paper=(round(img.width*zoom), round(img.height*zoom))
        img=img.resize(format_paper)
        img_color=img
        img_grey = img.convert('L')  # Convert to greyscale.
        channel = img_grey.split()[0]  # Get grey pixels.
        #channel = channel.rotate(angle, expand=1)
        size = channel.size[0]*scale, channel.size[1]*scale
        render_coords_text=[]

        if render:
            bitmap = Image.new('RGB', size,color='white')
        else:
            bitmap = Image.new('RGB', size,color='white')
        #bitmap = bitmap.convert('RGB')
        draw = ImageDraw.Draw(bitmap)
        for x in range(0, channel.size[0], sample):
            for y in range(0, channel.size[1], sample):
                box = channel.crop((x, y, x+sample, y+sample))
                box_color = img_color.crop((x, y, x+sample, y+sample))
                obj_for_count=box_color.load()
                sq=[0,0,0]
                count_c=box_color.width*box_color.height
                for i in range(box_color.width): #Цикл по ширине
                    for j in range(box_color.height): #Цикл по высоте
                        sq[0] += obj_for_count[i, j][0] #r
                        sq[1] += obj_for_count[i, j][1] #g
                        sq[2] += obj_for_count[i, j][2] #b

                color=(int(sq[0]/count_c), int(sq[1]/count_c), int(sq[2]/count_c))
                # if new_color!=[]:
                #     arr_val=[]
                #     for c in new_color:
                #         arr_val.append((color[0]-c[0])+(color[1]-c[1])+(color[2]-c[2]))

                #     color=new_color[arr_val.index(arr_val)]


                mean = ImageStat.Stat(box).mean[0]
                x_pos, y_pos = (x+box.size[1]/2) * scale, (y+box.size[1]/2) * scale
                box_edge = None
                straz = None
                
                if not choice_straz or choice_straz==[] or len(choice_straz)==7:
                    mean_step, choice_straz = 33, ['ss5','ss6','ss8','ss10','ss12','ss16','ss20']
                else:
                    mean_step=int(230/len(choice_straz))

                if mean<shadow:
                    continue

                for index, straz in enumerate(reversed(choice_straz)):
                    if int(mean) in range(mean_step*index, mean_step*(index+1)):
                        box_edge=size_straz[straz]
                        straz=straz
                        break
                if box_edge:
                    if x_pos<bitmap.width-30 and y_pos<bitmap.height-30:
                        if not render:
                            draw.ellipse((x_pos-box_edge, y_pos-box_edge, x_pos+box_edge, y_pos+box_edge),
                                        fill=color)
                            # draw.ellipse((x_pos-(box_edge-3.5), y_pos-(box_edge-3.5), x_pos+(box_edge-3.5), y_pos+(box_edge-3.5)),
                            #             fill='black')
                            if len(straz.replace('ss',''))==2:
                                draw.text((x_pos-5, y_pos-4.5), text=straz.replace('ss',''), fill=(255,255,255))
                            else:
                                if straz=='ss8':
                                    draw.text((x_pos-2, y_pos-4.5), text=straz.replace('ss',''), fill=(255,255,255))
                                else:
                                    draw.text((x_pos-2, y_pos-4.5), text=straz.replace('ss',''), fill=(255,255,255))
                            render_coords_text.append((x_pos-5, y_pos-5, straz.replace('ss','')))
                        else:
                            draw.ellipse((x_pos-box_edge, y_pos-box_edge, x_pos+box_edge, y_pos+box_edge),
                                        fill=color)                    

        if render:
            draw=ImageDraw.Draw(bitmap)
            for xy in render_coords_text:
                if len(xy[2])==2:
                    draw.text(xy[:2], xy[2], fill='white')
                else:
                    draw.text((xy[0]+2.5, xy[1]), xy[2], fill='white')

        res_img=bitmap
        #Работа с палитрой

        res_img=res_img.convert('P', colors=count_colors, palette=Image.ADAPTIVE)
        res_img=res_img.convert('RGB')
        old_colors=list(set(res_img.getdata()))
        #Замена цветов
        if new_color!=[] and list(map(tuple, old_colors))!=new_color:
            new_image=[]
            for item in res_img.convert("RGB").getdata():
                if item in list(map(tuple, old_colors)):
                    for index, i in enumerate(old_colors):
                        if tuple(i)==item:
                            new_image.append(new_color[index])
                else:
                    new_image.append(item)
            res_img.putdata(new_image)

        
        
        colors=list(set(res_img.getdata()))
        #Сбор цветов
        # rgbs=[]
        # for i in range(3,len(colors)+3, 3): rgbs.append((colors[i-3],colors[i-2],colors[i-1]))
        # colors=list(set(rgbs))

        return (res_img, colors, len(colors), old_colors)
    img_ht, colors, count_colors, old_color = halftone_child(img, int(sample), int(scale), zoom, choice_straz, count_colors, render=render, old_colors=old_colors, new_color=new_color)
    return (img_ht, colors, choice_straz, count_colors, old_color)

def closest_color(rgb_color, colors):
    min_distance = float('inf')
    closest_color = None

    for color in colors:
        distance = math.sqrt(sum([(c1 - c2)**2 for c1, c2 in zip(rgb_color, color)]))
        if distance < min_distance:
            min_distance = distance
            closest_color = color

    return closest_color

def correct_color(img: Image, count_color) -> Image:
    img = img.quantize(int(count_color)).convert('RGB')
    im_array = array(img)
    palette = []
    for x in im_array:
        for y in x:
            color = (int(y[0]),int(y[1]),int(y[2]))
            if color not in palette and color != (255,255,255):
                palette.append(color)
    return (img, palette)

def handle_45deg(path: str | bytes,
        x_pos: int | None=0,
        y_pos: int | None=0,
        scale: int | None=100,
        max_mean: int | None=255,
        count_color: int | None=17,
        now_color: list | None=None,
        need_color: list | None=None,
        sample: int | None=10,
        brightness: int | None=100,
        contrast: int | None=100,
        render: bool | None=False,      
    ) -> Image:
    print('need_color -> ', need_color)
    print('now_color -> ', now_color)
    if need_color!=[]:
        try:
            for index,i in enumerate(need_color):
                need_color[index]=i.replace('rgb(','').replace(')','').replace(' ','').split(',')
                need_color[index] = tuple(map(int, need_color[index]))
        except AttributeError:
            pass
            
    t_start = time.time()
    quality = QUALITY if render else 2
    img: Image = Image.open(io.BytesIO(base64.b64decode(path.replace('data:image/jpeg;base64','').replace('data:image/png;base64','')))).convert(mode="RGB")
    # img = img.resize((round(img.width*(int(scale)/100)), round(img.height*(int(scale)/100))))
    img.thumbnail((int(scale), int(scale)))
    img = img.resize((round(img.width*(int(scale)/100)), round(img.height*(int(scale)/100))))
    br = ImageEnhance.Brightness(img)
    img = br.enhance(round(int(brightness)/100))
    en = ImageEnhance.Contrast(img)
    img = en.enhance(round(int(contrast)/100))
    img, palette = correct_color(img, int(count_color))
    img = img.resize((img.width*quality,img.height*quality))
    img_border = Image.new(mode='RGB', size=(img.width if img.width>img.height else img.height, img.width if img.width>img.height else img.height), color=(255,255,255))
    img_border.paste(im=img, box=(0,0, img.width, img.height))
    img = img_border.convert("RGB")
    img_work = array(img.rotate(90))
    img_result = Image.new(mode='RGB', size=(img.height, img.width), color=(255,255,255))
    draw = ImageDraw.Draw(img_result)
    
    size_straz={
        'ss5':7,
        'ss6':8,
        'ss8':9,
        'ss10':11,
        'ss12':12,
        'ss16':15,
        'ss20':19,
    }
    try:
        #Переменные для ввода
        sample = int(size_straz[sample])*quality
    except:
        sample = int(sample)*quality

    border = -3
    
    #Переменные для вывода
    now_color = palette #if now_color == [] else list(map(tuple,now_color))
    count_straz = 0
    
    for x in arange(0, img.width, sample):
        parity = False
        for y in arange(0, img.height, round(sample/1.15)):
            parity = not parity
            
            block = img_work[x:x+sample, y:y+round(sample/2)]
            mean_color = block.mean((0,1))
            mean_brithgnes = block.mean()
            
            #color = (img_work[x,y][0], img_work[x,y][1], img_work[x,y][2])
            color = (round(mean_color[0]),round(mean_color[1]),round(mean_color[2]))
            color = closest_color(color, now_color)
            if need_color != []:
                color = need_color[now_color.index(color)]
            
            if int(mean_brithgnes) < int(max_mean):
                count_straz+=1
                if parity:
                    if render: 
                        draw.ellipse((x,y,x+sample, y+sample), fill=(0,0,0))
                        draw.ellipse((x-border,y-border,x+sample+border, y+sample+border), fill=color) 
                    else:
                        draw.ellipse((x,y,x+sample, y+sample), fill=color)
                else:       
                    if render:
                        draw.ellipse((x-round(sample/2),y,x+sample-round(sample/2), y+sample), fill=(0,0,0)) 
                        draw.ellipse((x-round(sample/2)-border,y-border,x+sample-round(sample/2)+border, y+sample+border), fill=color)
                    else:
                        draw.ellipse((x-round(sample/2),y,x+sample-round(sample/2), y+sample), fill=color) 
    img_result = img_result.crop((0,0, img.width, img.height))
    t_end = time.time()
    print('Время обработки ',t_end-t_start)
    return (img_result if render else img_result.resize((round(img.width/quality),round(img.height/quality))).resize((round(img.width/quality),round(img.height/quality)), Image.BICUBIC),
            now_color if need_color==[] else need_color)

if __name__=='__main__':
    #calligraphy(Image.open('test_ktext.jpg'))
    #dot_pattern(Image.open('test.png'), 19, 2.8, 30, 20, (3000,1000)).show()
    text_render(Image.open('10.10.10.jpg'),0,0).show()