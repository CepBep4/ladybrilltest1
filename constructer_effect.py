import numpy as np
#import matplotlib.pyplot as plt
from PIL import Image, ImageOps, ImageDraw, ImageFont
import numpy as np
from effect_function import text_render, dot_pattern, dot_pattern_color, handle_45deg
import pickle
from random import randint
import os

QUALITY = 5
PIXEL=37
size_st={
    'ss5':7,
    'ss6':8,
    'ss8':9,
    'ss10':11,
    'ss12':12,
    'ss16':15,
    'ss20':20
}

class TextEffect:
    def __init__(self,
                x_pos: int | None=0,
                y_pos: int | None=0,
                text: str | None='Text',
                font_size: int | None=64,
                font: str | None='static/arial.ttf',
                straz_size: int | None=2,
                sample: int | None=13,
                threshold: int | None=5,
                distanse: int | None=0,
                coordx_correct: int | None=0,
                coordy_correct: int | None=0,
                del_dots: list | None=[],
                add_dots: list | None=[]
    ) -> None:
        self.params={
            'x_pos':x_pos,
            'y_pos':y_pos,
            'text':text,
            'font_size':font_size,
            'font':font,
            'straz_size':straz_size,
            'sample':sample,
            'threshold':threshold,
            'distanse': distanse,
            'coordx_correct':coordx_correct,
            'coordy_correct':coordy_correct,
            'del_dots': list(del_dots),
            'add_dots':list(add_dots)
        }
    
    def get(self):
        return tuple(self.params.values())
    
class PictureEffect:
    def __init__(self,
                image: str | None='',
                x_pos: int | None=0,
                y_pos: int | None=0,
                sample: int | None=40,
                threshold: int | None=100,
                layout: int | None=100,
                width: int | None=1000,
                height: int | None=1000,
                choice_straz: list | None=[],
                render=False
    ) -> None:
        self.params={
            'image':image,
            'x_pos':x_pos,
            'y_pos':y_pos,
            'sample':sample,
            'threshold':threshold,
            'layout':layout,
            'width': width,
            'height': height,
            'choice_straz': choice_straz
        }
    
    def get(self):
        return tuple(self.params.values())
    
class ColorPictureEffect:
    def __init__(self,
            image: str,
            x_pos: int | None=0,
            y_pos: int | None=0,
            sample: int | None=40,
            scale: float | None=2.8,
            shadow: int | None=30,
            zoom: float | None=1.0,
            choice_straz: list |None=None,
            count_colors: int | None=16,
            old_colors: list | None=[],
            new_color: list | None=[],
            render: bool | None=False
    ) -> None:
        self.params={
            'image':str(image),
            'x_pos':int(x_pos),
            'y_pos':int(y_pos),
            'sample':int(sample),
            'scale':float(scale),
            'shadow': int(shadow),
            'zoom': float(zoom),
            'choice_straz':list(choice_straz),
            'count_colors':int(count_colors),
            'old_colors': list(old_colors),
            'new_color': list(new_color),
            'render':bool(render)
        }
    
    def get(self):
        return tuple(self.params.values())
    
class ColorPictureEffectDia:
    def __init__(self,
        path: str | bytes,
        x_pos: int | None=0,
        y_pos: int | None=0,
        scale: int | None=500,
        max_mean: int | None=254,
        count_color: int | None=17,
        now_color: list | None=[],
        need_color: list | None=[],
        sample: int | None='ss5',
        brightness: int | None=100,
        contrast: int | None=100,
        render: bool | None=False
    ) -> None:
        self.params={
            'path':str(path),
            'x_pos':int(x_pos),
            'y_pos':int(y_pos),
            'scale': int(scale),
            'max_mean':int(max_mean),
            'count_color':int(count_color),
            'now_color':list(now_color),
            'need_color':list(need_color),
            'sample':str(sample),
            'brightness':int(brightness),
            'contrast':int(contrast),
            'render':bool(render),
        }
    
    def get(self):
        return tuple(self.params.values())

class ConstructProgect:
    def __init__(self, width: int | None=None, height: int | None=None, userIP: str | None=None, mode: bool | None=None) -> None:
        if not mode:
            self.size={
                'ширина': (width*PIXEL)*2,
                'высота': (height*PIXEL)*2
            }

            self.objects=[]
            self.lays={}

            #Создание белой подложки
            img=np.zeros([100,100,3],dtype=np.uint8)
            img.fill(255)
            # plt.imshow(img, cmap='gray_r')
            # plt.axis('off')
            # plt.savefig(f'static/projects/{userIP}.jpg')

            #Идентификация и изменение её размеров
            self.image=Image.new(mode='RGB', size=(100,100), color=(255,255,255)).resize((self.size['ширина'], self.size['высота']))
            self.image=self.image.convert(mode='RGB')
            self.image.save(f'static/projects/{userIP}.jpg')
            self.lays['0']={'effect':'Основной слой'}

    def AppendObjectText(self,
                        x_pos: int | None=0,
                        y_pos: int | None=0,
                        text: str | None='ZA',
                        font_size: int | None=64,
                        font: str | None='GajrajOne-Regular(eng)',
                        straz_size: int | None='ss12',
                        sample: int | None=13,
                        threshold: int | None=5,
                        distanse: int | None=16,
                        coordx_correct: int | None=0,
                        coordy_correct: int | None=0,
                        del_dots: str | None=[],
                        add_dots: list | None=[]
    ):  
        params={
                    'x_pos':x_pos,
                    'y_pos':y_pos,
                    'text':text,
                    'font_size':font_size,
                    'font':font,
                    'straz_size':straz_size,
                    'sample':sample,
                    'threshold': threshold,
                    'distanse':distanse,
                    'coordx_correct':coordx_correct,
                    'coordy_correct':coordy_correct,
                    'del_dots':list(del_dots),
                    'add_dots':list(add_dots)
                }
        img, sizes, count, del_dots, add_dots, real_size=text_render(self.image, x_pos, y_pos, text, font_size, font, size_st[straz_size], sample, threshold, distanse, coordx_correct, coordy_correct, del_dots, add_dots)
        #print(f'{(img.width, img.height)} ширина текста')
        self.objects.append([img, 'TEXT', (int(x_pos), int(y_pos)), TextEffect(x_pos, y_pos, text, font_size, font, size_st[straz_size], sample, threshold, distanse, coordx_correct, coordy_correct, del_dots, add_dots)])
        self.lays[f'{max([int(x) for x in self.lays])+1}']={'effect':'Шрифт слой', 'params': params, 'width': sizes[0], 'height': sizes[1], 'count_straz':count, 'del_dots': del_dots, 'add_dots':add_dots, 'realwidth':real_size[0], 'realheight': real_size[1]}

    def AppendObjectDot(self,
                        image: str,
                        x_pos: int | None=0,
                        y_pos: int | None=0,
                        sample: int | None=40,
                        threshold: int | None=100,
                        layout: int | None=100,
                        width: int | None=1000,
                        height : int | None=1000,
                        choice_straz: list | None=[],
                        render=False
        ):
        params={
            'image':str(image),
            'x_pos':int(x_pos),
            'y_pos':int(y_pos),
            'sample':int(sample),
            'threshold':int(threshold),
            'layout': int(layout),
            'width': int(width),
            'height': int(height),
            'choice_straz':list(choice_straz),
            'render':bool(render)
        }
        img, count, choice_straz=dot_pattern(*list(params.values()))
        self.objects.append([img, 'PHOTO', (int(x_pos), int(y_pos)), PictureEffect(*tuple(params.values()))])
        self.lays[f'{max([int(x) for x in self.lays])+1}']={'effect':'Фото слой', 'params': params, 'width': img.width, 'height': img.height, 'photo':image, 'count': count, 'choice_straz':choice_straz}

    def AppendObjectDotColor(self,
                        image: str,
                        x_pos: int | None=0,
                        y_pos: int | None=0,
                        sample: int | None=19,
                        scale: float | None=2.8,
                        shadow: int | None=30,
                        zoom: float | None=1.0,
                        choice_straz: list |None=[],
                        count_colors: int | None=16,
                        old_colors: list | None=[],
                        new_color: list | None=[],
                        render: bool | None=False
        ):
        params={
            'image':str(image),
            'x_pos':int(x_pos),
            'y_pos':int(y_pos),
            'sample':int(sample),
            'scale':float(scale),
            'shadow': int(shadow),
            'zoom': float(zoom),
            'choice_straz':list(choice_straz),
            'count_colors':int(count_colors),
            'old_colors': list(old_colors),
            'new_color':list(new_color),
            'render':bool(render)
        }
        img, color, choice_straz, count_colors, old_colors=dot_pattern_color(*list(params.values()))
        self.objects.append([img, 'PHOTOCOLOR', (int(x_pos), int(y_pos)), ColorPictureEffect(*tuple(params.values()))])
        self.lays[f'{max([int(x) for x in self.lays])+1}']={'effect':'Цветной слой', 'params': params, 'width': img.width, 'height': img.height, 'photo':image, 'zoom': zoom, 'choice_straz': choice_straz, 'color':color, 'count_colors': count_colors, 'old_colors':old_colors}
    def AppendObjectDotColorDia(self,
                        path: str | bytes,
                        x_pos: int | None=0,
                        y_pos: int | None=0,
                        scale: int | None=100,
                        max_mean: int | None=254,
                        count_color: int | None=17,
                        now_color: list | None=[],
                        need_color: list | None=[],
                        sample: int | None='ss5',
                        brightness: int | None=100,
                        contrast: int | None=100,
                        render: bool | None=False,
        ):
        params={
            'path':str(path),
            'x_pos':int(x_pos),
            'y_pos':int(y_pos),
            'scale': int(scale),
            'max_mean':int(max_mean),
            'count_color':int(count_color),
            'now_color':list(now_color),
            'need_color':list(need_color),
            'sample':str(sample),
            'brightness':int(brightness),
            'contrast':int(contrast),
            'render':bool(render),
        }
        img, color=handle_45deg(*list(params.values()))
        self.objects.append([img, 'PHOTOCOLORDIA', (int(x_pos), int(y_pos)), ColorPictureEffectDia(*tuple(params.values()))])
        self.lays[f'{max([int(x) for x in self.lays])+1}']={'effect':'Новый слой', 'params': params, 'width': img.width, 'height': img.height, 'photo':path, 'color':color}

    def EditObjects(self, index: int, effect: str, params: dict):
        index=int(index)-1
        if effect=='Шрифт слой':
            for i in params:
                if i=='straz_size':
                    self.objects[index][3].params[i]=size_st[params[i]]
                    continue
                elif i=='del_dots':
                    if params[i]!=[]:
                        self.objects[index][3].params[i].append(params[i])
                    continue
                elif i=='add_dots':
                    if params[i]!=[]:
                        self.objects[index][3].params[i].append(params[i])
                    continue
                self.objects[index][3].params[i]=params[i]

            img, sizes, count, del_dots, add_dots, real_size=text_render(self.image, *self.objects[index][3].get())
            self.objects[index][0]=img
            self.objects[index][2]=(int(self.objects[index][3].params['x_pos']),int(self.objects[index][3].params['y_pos']))
            self.lays[str(index+1)]['width']=sizes[0]
            self.lays[str(index+1)]['height']=sizes[1]
            self.lays[str(index+1)]['count_straz']=count
            self.lays[str(index+1)]['del_dots']=del_dots
            self.lays[str(index+1)]['add_dots']=add_dots
            self.lays[str(index+1)]['realwidth']=real_size[0]
            self.lays[str(index+1)]['realheight']=real_size[1]
        if effect=='Фото слой':
            for i in params:
                self.objects[index][3].params[i]=params[i]
            img, count, choice_straz=dot_pattern(*self.objects[index][3].get())
            self.objects[index][0]=img
            self.objects[index][2]=(int(self.objects[index][3].params['x_pos']),int(self.objects[index][3].params['y_pos']))
            self.lays[str(index+1)]['width']=img.width
            self.lays[str(index+1)]['height']=img.height  
            self.lays[str(index+1)]['count']=count
            self.lays[str(index+1)]['choice_straz']=choice_straz
        if effect=='Цветной слой':
            for i in params:
                self.objects[index][3].params[i]=params[i]
            img, color, choice_straz, count_colors, old_colors=dot_pattern_color(*self.objects[index][3].get())
            self.objects[index][0]=img
            self.objects[index][2]=(int(self.objects[index][3].params['x_pos']),int(self.objects[index][3].params['y_pos']))
            self.lays[str(index+1)]['choice_straz']=choice_straz
            self.lays[str(index+1)]['color']=color
            self.lays[str(index+1)]['count_colors']=count_colors
            self.lays[str(index+1)]['old_colors']=old_colors
            
        if effect=='Новый слой':
            for i in params:
                if i=='image':
                    continue
                self.objects[index][3].params[i]=params[i]
            img, color=handle_45deg(*self.objects[index][3].get())
            self.objects[index][0]=img
            self.objects[index][2]=(int(self.objects[index][3].params['x_pos']),int(self.objects[index][3].params['y_pos']))
            self.lays[str(index+1)]['width']=img.width
            self.lays[str(index+1)]['height']=img.height
            self.lays[str(index+1)]['color']=color
            # self.lays[str(index+1)]['params']['render']=False

    def DeleteEffect(self, ids):
        del self.objects[int(ids)-1]
        del self.lays[str(ids)]

        new_lays={}

        for index, obj in enumerate(self.lays.copy()):
            new_lays[str(index)]=self.lays[obj]
        self.lays=new_lays

    def GetFullLayout(self, userIP, ImReturn=False, mirror=False):
        img=self.image.copy()
        img: Image=img.convert(mode='RGB')
        state_image=[]
        if not mirror:
            for obj in self.objects:
                if ImReturn:
                    obj[2]=(obj[2][0]*QUALITY, obj[2][1]*QUALITY)
                if obj[1]=='TEXT':
                    if ImReturn:
                        obj[0] = obj[0].resize((obj[0].width*QUALITY, obj[0].height*QUALITY))
                    img.paste(obj[0], obj[2], ImageOps.invert(obj[0]).convert('RGBA'))
                    index=str(self.objects.index(obj)+1)
                    state_image.append((self.lays[index]['params']['straz_size'],self.lays[index]['count_straz']))
                elif obj[1]=='PHOTO':
                    img.paste(obj[0], obj[2], ImageOps.invert(obj[0]).convert('RGBA'))
                    index=str(self.objects.index(obj)+1)
                    for i in self.lays[index]['count']:
                        state_image.append(i)
                elif obj[1]=='PHOTOCOLOR':
                    img.paste(obj[0], obj[2], ImageOps.invert(obj[0]).convert('RGBA'))
                    index=str(self.objects.index(obj)+1)
                elif obj[1]=='PHOTOCOLORDIA':
                    img.paste(obj[0], obj[2], ImageOps.invert(obj[0]).convert('RGBA'))
                    index=str(self.objects.index(obj)+1)
        else:
            for obj in self.objects:
                if obj[1]=='TEXT':
                    if ImReturn:
                        obj[0] = obj[0].resize((obj[0].width*QUALITY, obj[0].height*QUALITY))
                    img.paste(obj[0], obj[2], ImageOps.invert(obj[0]).convert('RGBA'))
                    index=str(self.objects.index(obj)+1)
                    state_image.append((self.lays[index]['params']['straz_size'],self.lays[index]['count_straz']))
                elif obj[1]=='PHOTO':
                    img.paste(obj[0], obj[2], ImageOps.invert(obj[0]).convert('1'))            
                    index=str(self.objects.index(obj)+1)
                    for i in self.lays[index]['count']:
                        state_image.append(i)
                elif obj[1]=='PHOTOCOLOR':
                    img.paste(obj[0], obj[2], ImageOps.invert(obj[0]).convert('1'))
                    index=str(self.objects.index(obj)+1)
                elif obj[1]=='PHOTOCOLORDIA':
                    img.paste(obj[0], obj[2], ImageOps.invert(obj[0]).convert('1'))
                    index=str(self.objects.index(obj)+1)
            img=ImageOps.mirror(img)
                                
        img.save(f'static/projects/{userIP}.jpg')

        #Работа с количеством страз
        count_straz = {
            'ss5':['ss5',0],
            'ss6':['ss6',0],
            'ss8':['ss8',0],
            'ss10':['ss10',0],
            'ss12':['ss12',0],
            'ss16':['ss16',0],
            'ss20':['ss20',0]
        }   
        state_image=list(map(list, state_image))
        for i in state_image: count_straz[i[0]][1]+=i[1]
        state_image=list(count_straz.values())

        if ImReturn:
            stat=[]
            for i in state_image:
                if i[0] not in stat:
                    stat.append([i[0], i[1]])
                else:
                    for ind,j in enumerate(stat):
                        if j == i[0]:
                            stat[ind]+=i[1]
            for i in stat:
                i[1]=str(i[1])
            for index,i in enumerate(stat):
                j=': '.join(stat[index])
                stat[index]=j

            draw=ImageDraw.Draw(img)
            draw.rectangle((0,0, 100, 120), fill='white')
            font = ImageFont.truetype('static/ofontru_Cygre.ttf', 15)
            s='\n'.join(stat)
            draw.text((20, 4), text=f'{s}', fill='black', font=font)

            #Отрисовка инструкции к цветам
            color_straz=[(101, 0, 205),(1, 0, 242),(2, 192, 255),(0, 241, 2),(241, 239, 0),(254, 154, 3),(241, 2, 1)]
            for i in range(0, 112, 16):
                draw.rectangle((5, 5+i,15, 15+i), fill=color_straz[int(i/16)])

            return img

    def RenderProject(self, userIP, mirror: bool):
        #Генерация имени файла
        symbols=['q','w','e','r','t','y','u','i','o','p','a','s','d','f','g','h','j','k','l','z','x','c','v','b','n','m']
        generate_name=''
        for i in range(20):
            generate_name+=symbols[randint(0,len(symbols)-1)]
        generate_name+='.jpg'

        #Рендер
        self.load(userIP, render=True)
        self.GetFullLayout(userIP, ImReturn=True, mirror=mirror).save(f'static/renderproject/lady_brill{userIP}.jpg')

        return f'static/renderproject/lady_brill{userIP}.jpg'

    def load(self, uid, render=False, back_id=False):
        if back_id:
            with open(f'static/userbase/constructor{uid}_back.pickle', 'rb') as file:
                data=pickle.load(file)
        else:
            with open(f'static/userbase/constructor{uid}.pickle', 'rb') as file:
                data=pickle.load(file)

        #print('Загружено -> ',data)
        quality = QUALITY if render else 1
        #Инициализация
        img=np.zeros([100,100,3],dtype=np.uint8)
        img.fill(255)
        # plt.imshow(img, cmap='gray_r')
        # plt.axis('off')
        # plt.savefig(f'static/projects/{uid}.jpg')
        self.image=Image.new(mode='RGB', size=(100,100), color=(255,255,255)).resize((data['width']*quality, data['height']*quality))
        self.image.save(f'static/projects/{uid}.jpg')

        self.lays={'0':{'effect':'Основной слой'}}
        self.objects=[]

        self.size={
            'ширина':data['width'],
            'высота':data['height']
        }

        for lay in data['params']:
            if lay!='0':
                if data['params'][lay]['effect']=='Шрифт слой':
                    data['params'][lay]['params']['del_dots']=data['params'][lay]['del_dots']
                    data['params'][lay]['params']['add_dots']=data['params'][lay]['add_dots']
                    self.AppendObjectText(*tuple(data['params'][lay]['params'].values()))
                elif data['params'][lay]['effect']=='Фото слой':
                    params=data['params'][lay]['params']
                    self.AppendObjectDot(params['image'], params['x_pos'], params['y_pos'], params['sample'], params['threshold'], params['layout'], params['width'], params['height'], params['choice_straz'], render=render)
                elif data['params'][lay]['effect']=='Цветной слой':
                    params=data['params'][lay]['params']
                    self.AppendObjectDotColor(data['params'][lay]['photo'], data['params'][lay]['params']['x_pos'], data['params'][lay]['params']['y_pos'], render=data['params'][lay]['params']['render'], max_mean=params['max_mean'],count_color=params['count_color'],now_color=params['now_color'], need_color=params['need_color'],sample=params['sample'],brightness=params['brightness'],contrast=params['contrast'],scale=params['scale'])
                elif data['params'][lay]['effect']=='Новый слой':
                    params=data['params'][lay]['params']
                    self.AppendObjectDotColorDia(params['path'], params['x_pos'], params['y_pos'], render=render, max_mean=params['max_mean'],count_color=params['count_color'],now_color=params['now_color'], need_color=params['need_color'],sample=params['sample'],brightness=params['brightness'],contrast=params['contrast'],scale=params['scale'])
        return self

    def save(self, uid):
        if os.path.exists(f'static/userbase/constructor{uid}.pickle'):
            with open(f'static/userbase/constructor{uid}.pickle', 'rb') as file:
                data=pickle.load(file)
            with open(f'static/userbase/constructor{uid}_back.pickle', 'wb') as file:
                pickle.dump(data, file)   
        with open(f'static/userbase/constructor{uid}.pickle', 'wb') as file:
            data={'width':self.size['ширина'], 'height':self.size['высота'], 'params':self.lays}
            #print(f'Сохранено -> {data}')
            pickle.dump(data, file)

             
    


if __name__=='__main__':
    a=ConstructProgect(21,29,'10.10.10')
    a.RenderProject('10.10.10', False)