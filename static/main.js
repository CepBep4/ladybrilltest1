class StateApp {
    constructor() {
        this.layerCount = 0;
        this.elementDict = {};
        this.userID = undefined;
        this.fileFont = undefined;
        this.oldParams = {
            new: {},
            old: {}
        }
        this.checkHotkey = ''
        this.checkUserShrift = false
        this.strazChoiced = []
        this.strazChoicedColor = []
        this.choiceColorButton = undefined
        this.colorInPhoto = []
        this.choicedColorList = []
        this.checkChabgeCountColor = false
    }
};

//Виджет слоя
class Lays {
    constructor() {
        this.obj = undefined
        this.elements = []
    }

    createWidgets(id, name) {
        let element = `
        <div class="lay-${id}" id="lay-${id}" onclick="focusLayer(${id});"> ${name}
            <div id="l-${id}-b${id}" onclick="lays.removeWidgets(${id});"></div>
        </div>
        <style>
            #lay-${id}{
                border-radius: 10px;
                width: 14%;
                font-family: 'Cygre';
                font-size: 21px;
                background: gray;
                position: relative;
                left: 10px;
                top: 10px;
                display: block;
                margin-bottom: 20px;
                margin-top: 20px;
                text-indent: 10px;
                transition: all 0.2s
            }
            
            #l-${id}-b${id}{
                width: 20px;
                height: 20px;
                border-radius: 180px;
                background: red;
                border: 0px;
                display: inline-block;
                float: right;
                translate: -3px 1px;
                text-indent: 10px;
            }        
        </style> 
        `;
        if (stateApp.layerCount == 0) {
            element = `
            <div class="lay-${id}" id="lay-${id}" onclick="focusLayer(${id});"> ${name}</div>
            <style>
                #lay-${id}{
                    border-radius: 10px;
                    width: 14%;
                    font-family: 'Cygre';
                    font-size: 21px;
                    background: gray;
                    position: relative;
                    left: 10px;
                    top: 10px;
                    display: block;
                    margin-bottom: 20px;
                    margin-top: 20px;
                    text-indent: 10px;
                    transition: all 0.2s
                }      
            </style>`
        };
        this.elements.unshift(element)
        document.getElementById('lays-place')
            .innerHTML = this.elements.join().replaceAll(',', '')
        stateApp.layerCount++
    }

    updateWidgets() {
        document.getElementById('lays-place')
            .innerHTML = this.elements.join();
    }

    removeWidgets(id) {
        loadIcon();
        stateApp.oldParams = {
            new: {},
            old: {}
        }
        localStorage.clear()
        document.getElementById('select-visible').value = 100
        this.elements[id] = '';
        stateApp.layerCount--;
        let req = fetch(`${HOST}/setcoockie`, {
            method: "POST",
            body: JSON.stringify({
                delete: 'element',
                id: id
            })
        });
        try { req.then(resp => resp.text()).then(answer => { if (answer == 'True') { refresh(); } }) } catch { refresh(); }
    }

}

const HOST = "https://cepbep4-ladybrilltest1-4b6c.twc1.net"//"http://127.0.0.1:8000" //http://194.87.143.177:8000;
var check = false;
var lays = new Lays();
var stateApp = new StateApp();
const maxEffect = 5;

// document.addEventListener('keydown', (e) => {
//     if(e.key=='Control'){
//         stateApp.checkHotkey='Controll'
//     }
//     else if(stateApp.checkHotkey=='Controll' & e.key=='z' & stateApp.elementDict[`${stateApp.focusId}`]['effect']=='Шрифт слой'){
//         backReturn();
//     }
//     else{
//         stateApp.checkHotkey=undefined
//     }
//     console.log(stateApp.checkHotkey)
// })

// document.addEventListener('keydown', (e) => {
//     if(e.key=='Enter' & stateApp.elementDict[`${stateApp.focusId}`]['effect']=='Фото слой'){
//         editPhoto();
//     }
//     else if(e.key=='Enter' & stateApp.elementDict[`${stateApp.focusId}`]['effect']=='Шрифт слой'){
//         editShrift();
//     }
// })

function refresh() {
    location.reload();
};

function getCookie() {
    try {
        document.getElementsByClassName('control-image-layout')[0].style.zoom = JSON.parse(localStorage.getItem('zoom_parametr'))
        if (JSON.parse(localStorage.getItem('zoom_parametr')) * 100 != 0) {
            document.getElementById('select-visible').value = JSON.parse(localStorage.getItem('zoom_parametr')) * 100
        }
    }
    catch { document.getElementById('select-visible').value = 100 }

    fetch(`${HOST}/getcoockie`,
        { method: "GET" })
        .then(resp => resp.text())
        .then(session => {
            session = JSON.parse(session);
            document.getElementById('border-main-image').style.visibility = 'hidden'
            if (session['project_width']) {
                if (session['project_height'] == 21 & session['project_width'] == 30) {
                    document.getElementById('input-real-width').value = 'A4'
                    document.getElementById('input-real-height').value = 'Горизонтальное'
                }
                else if (session['project_height'] == 30 & session['project_width'] == 21) {
                    document.getElementById('input-real-width').value = 'A4'
                    document.getElementById('input-real-height').value = 'Вертикальное'
                }
                else if (session['project_height'] == 30 & session['project_width'] == 42) {
                    document.getElementById('input-real-width').value = 'A3'
                    document.getElementById('input-real-height').value = 'Горизонтальное'
                }
                else if (session['project_height'] == 42 & session['project_width'] == 30) {
                    document.getElementById('input-real-width').value = 'A3'
                    document.getElementById('input-real-height').value = 'Вертикальное'
                }
            }
            if (!session['user_id']) {
                fetch(`${HOST}/logout`, { method: "GET" });
                location.reload();
            }
            else {
                if (session['user_id'] == '662199') {

                }
                else {
                    document.getElementById('color-dot-add').style.visibility = 'hidden';
                }
            }
            if (session['fontslist']) {
                appendOptions(session['fontslist'])
            }
            if (session['element']) {
                stateApp.elementDict = session['element']
                for (let i = 0; i <= maxEffect; i++) {
                    if (session['element'][i] != undefined) {
                        lays.createWidgets(i, session['element'][i]['effect'])
                        if (session['element'][i]['effect'] == 'Шрифт слой') {
                            if (session['element'][i]['params']) {
                                // alert(JSON.stringify(session['element'][i]['params']))
                                writeParamsFontEffect(session['element'][i]['params']);
                            }
                        }
                    }
                    else {
                        break
                    }

                }
                if (session['focus']) {
                    focusLayer(session['focus']);
                }
            }
            if (session['element']) {
                if (session['element'][0]) {
                    stateApp.userID = session['user_id']
                    stateApp.layOut = document.getElementById('prewiew-image')
                    document.getElementById('prewiew-image').src = `../static/projects/${session['user_id']}.jpg`;
                    document.getElementById('prepare-render-image').src = `../static/projects/${session['user_id']}.jpg`;
                    document.getElementById('delete-dot-image').src = `../static/projects/${session['user_id']}.jpg`;
                }
            }
        });
}

function checkOnLoad() {
    loadIcon();
    getCookie();
    lays.updateWidgets()
    loadIconOff();
    changeFocusLayer();
    document.getElementsByClassName('control-image-layout')[0].style.zoom = localStorage.getItem('zoom_parametr')
    adaptiveVis()
}

function changeSizeProject() {
    loadIcon();
    if (document.getElementById('input-real-width').value == 'A4') {
        if (document.getElementById('input-real-height').value == 'Горизонтальное') {
            realWidth = 30;
            realHeight = 21;
        }
        else {
            realWidth = 21;
            realHeight = 30;
        }
    }
    else if (document.getElementById('input-real-width').value == 'A3') {
        if (document.getElementById('input-real-height').value == 'Горизонтальное') {
            realWidth = 42;
            realHeight = 30;
        }
        else {
            realWidth = 30;
            realHeight = 42;
        }

    }
    fetch(`${HOST}/setcoockie`, {
        method: "POST",
        body: JSON.stringify({
            project_width: realWidth,
            project_height: realHeight
        })
    });

    let req = fetch(`${HOST}/getlayout`, {
        method: "POST",
        body: JSON.stringify({
            project_width: realWidth,
            project_height: realHeight
        })
    });
    try { req.then(resp => resp.text()).then(answer => { if (answer == 'True') { refresh(); } }) } catch { refresh(); }
    // document.getElementById('loads').style.opacity=0;
    // document.getElementById('loads').style.visibility='hidden';
    // document.getElementsByClassName('loader').style.opacity=0;
    // document.getElementsByClassName('loader').style.visibility='hidden';



}

function focusLayer(id) {
    console.log(id)
    if (stateApp.focusId != id) {
        stateApp.focusId = id;
        try { document.getElementById(`lay-${id}`).style.background = '#62ffa4'; } catch { }
        if (lays.elements.length > 1) {
            for (let i = 0; i <= stateApp.layerCount - 1; i++) {
                if (i != id) {
                    try { document.getElementById(`lay-${i}`).style.background = 'gray' } catch { }
                }
            }
        }

    }
    else {
        stateApp.focusId = undefined;
        try { document.getElementById(`lay-${id}`).style.background = 'gray'; } catch { }
    }
    changeFocusLayer();
}

function changeFocusLayer() {
    if (stateApp.focusId == undefined) {
        document.getElementById('default-layer').style.visibility = 'visible'  //Поменять обратно  visible----------------------
        document.getElementById('main-layer').style.visibility = 'hidden'
        document.getElementById('choice-next-layer').style.visibility = 'hidden'
        document.getElementById('settings-text-effect').style.visibility = 'hidden'
        document.getElementById('settings-photo-effect').style.visibility = 'hidden'
        document.getElementById('settings-photo-effect-color').style.visibility = 'hidden'
        document.getElementById('border-main-image').style.visibility = 'hidden'
        document.getElementById('settings-photo-effect-color-diagonal').style.visibility = 'hidden'
        return 0;
    }
    else {
        // document.getElementById('default-layer').style.visibility='hidden'
        document.getElementById('main-layer').style.visibility = 'hidden'
        document.getElementById('choice-next-layer').style.visibility = 'hidden'
        document.getElementById('settings-text-effect').style.visibility = 'hidden'
        document.getElementById('settings-photo-effect').style.visibility = 'hidden'
        document.getElementById('settings-photo-effect-color').style.visibility = 'hidden'
        document.getElementById('border-main-image').style.visibility = 'hidden'
        document.getElementById('settings-photo-effect-color-diagonal').style.visibility = 'hidden'
    }
    if (stateApp.focusId == 0) {
        document.getElementById('choice-next-layer').style.visibility = 'hidden'
        document.getElementById('main-layer').style.visibility = 'visible'
        document.getElementById('default-layer').style.visibility = 'hidden'
        document.getElementById('settings-text-effect').style.visibility = 'hidden'
        document.getElementById('settings-photo-effect').style.visibility = 'hidden'
        document.getElementById('settings-photo-effect-color').style.visibility = 'hidden'
        document.getElementById('border-main-image').style.visibility = 'hidden'
        document.getElementById('settings-photo-effect-color-diagonal').style.visibility = 'hidden'
    }
    else if (stateApp.focusId != 0) {
        if (stateApp.elementDict[`${stateApp.focusId}`]) {
            if (stateApp.elementDict[`${stateApp.focusId}`]['effect'] == 'Шрифт слой') {
                document.getElementById('settings-photo-effect-color-diagonal').style.visibility = 'hidden'
                document.getElementById('settings-text-effect').style.visibility = 'visible'
                document.getElementById('settings-photo-effect-color').style.visibility = 'hidden'
                document.getElementById('default-layer').style.visibility = 'hidden'
                document.getElementById('main-layer').style.visibility = 'hidden'
                document.getElementById('choice-next-layer').style.visibility = 'hidden'
                document.getElementById('settings-photo-effect').style.visibility = 'hidden'
                document.getElementById('border-main-image').style.visibility = 'hidden'
                if (stateApp.elementDict[`${stateApp.focusId}`]['params']) {
                    writeParamsFontEffect(stateApp.elementDict[`${stateApp.focusId}`]['params'])

                    widht = stateApp.elementDict[`${stateApp.focusId}`]['width']
                    height = stateApp.elementDict[`${stateApp.focusId}`]['height']
                    realwidht = stateApp.elementDict[`${stateApp.focusId}`]['realwidth']
                    realheight = stateApp.elementDict[`${stateApp.focusId}`]['realheight']

                    document.getElementById('border-main-image').style.width = `${widht}px`
                    document.getElementById('border-main-image').style.height = `${height}px`
                    document.getElementById('widht-border').textContent = `Ширина - ${realwidht} см`
                    document.getElementById('height-border').textContent = `Высота - ${realheight} см`
                }
            }
            if (stateApp.elementDict[`${stateApp.focusId}`]['effect'] == 'Фото слой') {
                document.getElementById('settings-photo-effect-color-diagonal').style.visibility = 'hidden'
                document.getElementById('settings-photo-effect').style.visibility = 'visible'
                document.getElementById('settings-photo-effect-color').style.visibility = 'hidden'
                document.getElementById('settings-text-effect').style.visibility = 'hidden'
                document.getElementById('default-layer').style.visibility = 'hidden'
                document.getElementById('main-layer').style.visibility = 'hidden'
                document.getElementById('choice-next-layer').style.visibility = 'hidden'
                document.getElementById('border-main-image').style.visibility = 'hidden'
                if (stateApp.elementDict[`${stateApp.focusId}`]['params']) {
                    writeParamsPhotoEffect(stateApp.elementDict[`${stateApp.focusId}`]['params'])
                    widht = stateApp.elementDict[`${stateApp.focusId}`]['width']
                    height = stateApp.elementDict[`${stateApp.focusId}`]['height']
                    straz_choiced = stateApp.elementDict[`${stateApp.focusId}`]['choice_straz']
                    if (straz_choiced.length != 0) {
                        stateApp.strazChoiced = straz_choiced
                        writeSelectedStraz(straz_choiced)
                    }
                    document.getElementById('border-main-image').style.width = `${widht}px`
                    document.getElementById('border-main-image').style.height = `${height}px`
                    document.getElementById('widht-border').textContent = `Ширина - ${Math.round(widht / 37 * 0.5)} см`
                    document.getElementById('height-border').textContent = `Высота - ${Math.round(height / 37 * 0.5)} см`

                }
            }
            if (stateApp.elementDict[`${stateApp.focusId}`]['effect'] == 'Цветной слой') {
                document.getElementById('settings-photo-effect-color').style.visibility = 'visible'
                document.getElementById('settings-photo-effect-color-diagonal').style.visibility = 'hidden'
                document.getElementById('settings-photo-effect').style.visibility = 'hidden'
                document.getElementById('settings-text-effect').style.visibility = 'hidden'
                document.getElementById('default-layer').style.visibility = 'hidden'
                document.getElementById('main-layer').style.visibility = 'hidden'
                document.getElementById('choice-next-layer').style.visibility = 'hidden'
                document.getElementById('border-main-image').style.visibility = 'hidden'
                if (stateApp.elementDict[`${stateApp.focusId}`]['params']) {
                    writeParamsPhotoEffectColor(stateApp.elementDict[`${stateApp.focusId}`]['params'])
                    widht = stateApp.elementDict[`${stateApp.focusId}`]['width']
                    height = stateApp.elementDict[`${stateApp.focusId}`]['height']
                    straz_choiced = stateApp.elementDict[`${stateApp.focusId}`]['choice_straz']
                    if (straz_choiced.length != 0) {
                        stateApp.strazChoicedColor = straz_choiced
                        writeSelectedStraz(straz_choiced)
                    }
                    stateApp.colorInPhoto = stateApp.elementDict[`${stateApp.focusId}`]['color']
                    document.getElementById('slider-count-color-photo-color').value = stateApp.elementDict[`${stateApp.focusId}`]['count_colors']
                    writeRightColor(stateApp.colorInPhoto)
                    document.getElementById('border-main-image').style.width = `${widht}px`
                    document.getElementById('border-main-image').style.height = `${height}px`
                    document.getElementById('widht-border').textContent = `Ширина - ${Math.round(widht / 37 * 0.5)} см`
                    document.getElementById('height-border').textContent = `Высота - ${Math.round(height / 37 * 0.5)} см`

                }
            }
            if (stateApp.elementDict[`${stateApp.focusId}`]['effect'] == 'Новый слой') {
                document.getElementById('settings-photo-effect-color').style.visibility = 'hidden'
                document.getElementById('settings-photo-effect-color-diagonal').style.visibility = 'visible'
                document.getElementById('settings-photo-effect').style.visibility = 'hidden'
                document.getElementById('settings-text-effect').style.visibility = 'hidden'
                document.getElementById('default-layer').style.visibility = 'hidden'
                document.getElementById('main-layer').style.visibility = 'hidden'
                document.getElementById('choice-next-layer').style.visibility = 'hidden'
                document.getElementById('border-main-image').style.visibility = 'hidden'
                if (stateApp.elementDict[`${stateApp.focusId}`]['params']) {
                    stateApp.colorInPhoto = stateApp.elementDict[`${stateApp.focusId}`]['color']
                    writeRightColorDia(stateApp.colorInPhoto)
                    writeParamsPhotoEffectColorDia(stateApp.elementDict[`${stateApp.focusId}`]['params'])
                    widht = stateApp.elementDict[`${stateApp.focusId}`]['width']
                    height = stateApp.elementDict[`${stateApp.focusId}`]['height']
                    document.getElementById('border-main-image').style.width = `${widht}px`
                    document.getElementById('border-main-image').style.height = `${height}px`
                    document.getElementById('widht-border').textContent = `Ширина - ${Math.round(widht / 37 * 0.5)} см`
                    document.getElementById('height-border').textContent = `Высота - ${Math.round(height / 37 * 0.5)} см`

                }
            }
        }
    }
}

function loadIcon() {
    document.getElementById('loads').style.visibility = 'visible';
    document.getElementById('loads').style.opacity = 1;
    document.getElementById('loader').style.visibility = 'visible';
    document.getElementById('loader').style.opacity = 1;
}

function loadIconOff() {
    document.getElementById('loads').style.visibility = 'hidden';
    document.getElementById('loads').style.opacity = 0;
    document.getElementById('loader').style.visibility = 'hidden';
    document.getElementById('loader').style.opacity = 0;
}

function addEffect() {
    document.getElementById('choice-next-layer').style.visibility = 'visible'
    document.getElementById('default-layer').style.visibility = 'hidden'
    document.getElementById('main-layer').style.visibility = 'hidden'
}

function addShrift() {
    if (stateApp.layerCount >= maxEffect + 1) {
        alert('Привышен лимист слоёв');
        return 0;
    }
    loadIcon();
    let req = fetch(`${HOST}/addshrift`, {
        method: "POST",
        body: JSON.stringify({
            project_width: 1,
            project_height: 1
        })
    });
    req.then(text => text.text()).then(answer => { if (answer == 'True') { refresh(); } })
}

function editShrift() {
    loadIcon();
    let fontfamaly = document.getElementById('choice-font-famaly').value
    if (stateApp.fileFont != undefined) {
        fontfamaly = stateApp.fileFont
    }
    document.getElementById('border-main-image').style.visibility = 'hidden'
    checkNormalParamsShrift()

    let backParams = {
        x_pos: document.getElementById('slider-coord-x').value,
        y_pos: document.getElementById('slider-coord-y').value,
        text: document.getElementById('config-text-effect').value,
        font_size: document.getElementById('slider-font-size').value,
        font: fontfamaly,
        straz_size: document.getElementById('choice-straz-size').value,
        sample: document.getElementById('slider-sample').value,
        threshold: 5,
        distanse: document.getElementById('slider-distanse').value,
        coordx_correct: 0,
        coordy_correct: 0,
        del_dots: [],
        add_dots: []
    }
    if (JSON.parse(localStorage.getItem('ShriftParams'))) {
        stateApp.oldParams = JSON.parse(localStorage.getItem('ShriftParams'))
    }
    if (stateApp.oldParams['new'] == {}) {
        stateApp.oldParams['new'] = backParams
        stateApp.oldParams['old'] = backParams
    }
    else {
        stateApp.oldParams['old'] = stateApp.oldParams['new']
        stateApp.oldParams['new'] = backParams
    }
    localStorage.setItem("ShriftParams", JSON.stringify(stateApp.oldParams));

    let req = fetch(`${HOST}/editshrift`, {
        method: "POST",
        body: JSON.stringify({
            params: {
                x_pos: document.getElementById('slider-coord-x').value,
                y_pos: document.getElementById('slider-coord-y').value,
                text: document.getElementById('config-text-effect').value,
                font_size: document.getElementById('slider-font-size').value,
                font: fontfamaly,
                straz_size: document.getElementById('choice-straz-size').value,
                sample: document.getElementById('slider-sample').value,
                threshold: 5,
                distanse: document.getElementById('slider-distanse').value,
                coordx_correct: 0,
                coordy_correct: 0,
                del_dots: [],
                add_dots: []
            },
            index: stateApp.focusId,
            effect: stateApp.elementDict[`${stateApp.focusId}`]['effect'],
            focus: stateApp.focusId
        })
    });
    req.then(text => text.text()).then(answer => { if (answer == 'True') { refresh(); } })
    //setTimeout(() => {refresh();}, 100)
}

function writeParamsFontEffect(params) {
    let font_name = params['font']
    if (params['font'].length > 200 | params['font'] == undefined) {
        if (!stateApp.checkUserShrift) {
            appendOptions(['Пользовательский'])
            stateApp.checkUserShrift = true
        }
        font_name = 'Пользовательский'

        stateApp.fileFont = params['font']
    }
    document.getElementById('slider-coord-x').value = params['x_pos'];
    document.getElementById('slider-coord-y').value = params['y_pos'];
    document.getElementById('config-text-effect').value = params['text'];
    document.getElementById('slider-font-size').value = params['font_size'];
    document.getElementById('choice-font-famaly').value = font_name;
    document.getElementById('choice-straz-size').value = params['straz_size'];
    document.getElementById('slider-sample').value = params['sample'];
    // document.getElementById('slider-quality-x').value=params['coordx_correct'];
    // document.getElementById('slider-quality-x').max=params['sample'];
    // document.getElementById('slider-quality-y').value=params['coordy_correct'];
    // document.getElementById('slider-quality-y').max=params['sample'];
    document.getElementById('slider-distanse').value = params['distanse'];
    document.getElementById('slider-distanse').setAttribute('title', `Значение - ${document.getElementById('slider-distanse').value}`)
}

function writeParamsPhotoEffect(params) {
    document.getElementById('slider-coord-x-photo').value = params['x_pos']
    document.getElementById('slider-coord-y-photo').value = params['y_pos']
    document.getElementById('slider-sample-photo').value = params['sample']
    document.getElementById('slider-shadow-photo').value = params['threshold']
    document.getElementById('slider-shadow-2-photo').value = params['layout']
    document.getElementById('slider-scale-photo').value = params['width']
}

function writeParamsPhotoEffectColorDia(params) {
    document.getElementById('slider-coord-x-photo-dia').value = params['x_pos']
    document.getElementById('slider-coord-y-photo-dia').value = params['y_pos']
    document.getElementById('slider-scale-photo-dia').value = params['scale']
    document.getElementById('slider-porog-photo-dia').value = params['max_mean']
    document.getElementById('slider-sample-photo-dia').value = params['count_color']
    document.getElementById('choice-straz-size-dia').value = params['sample']
    document.getElementById('slider-shadow-photo-dia').value = params['brightness']
    document.getElementById('slider-shadow-2-photo-dia').value = params['contrast']
}

function hitBoxText() {
    let x_c = document.getElementById('slider-coord-x').value
    let y_c = document.getElementById('slider-coord-y').value

    document.getElementById('border-main-image').style.visibility = 'visible'
    document.getElementById('border-main-image').style.translate = `${x_c}px ${y_c}px`
}

function hitBoxPhoto() {
    let x_c = document.getElementById('slider-coord-x-photo').value
    let y_c = document.getElementById('slider-coord-y-photo').value

    document.getElementById('border-main-image').style.visibility = 'visible'
    document.getElementById('border-main-image').style.translate = `${x_c}px ${y_c}px`
}

function hitBoxPhotoColor() {
    let x_c = document.getElementById('slider-coord-x-photo-color').value
    let y_c = document.getElementById('slider-coord-y-photo-color').value

    document.getElementById('border-main-image').style.visibility = 'visible'
    document.getElementById('border-main-image').style.translate = `${x_c}px ${y_c}px`
}

function hitBoxPhotoColorDia() {
    let x_c = document.getElementById('slider-coord-x-photo-dia').value
    let y_c = document.getElementById('slider-coord-y-photo-dia').value

    document.getElementById('border-main-image').style.visibility = 'visible'
    document.getElementById('border-main-image').style.translate = `${x_c}px ${y_c}px`
}

function checkFile() {
    if (stateApp.layerCount >= maxEffect + 1) {
        alert('Привышен лимист слоёв');
        return 0;
    }
    else {
        var reader = new FileReader();
        loadIcon();
        reader.onload = function () {
            let req = fetch(`${HOST}/adddot`, {
                method: "POST",
                body: JSON.stringify({
                    file: this.result,
                })
            });
            req.then(text => text.text()).then(answer => { if (answer == 'True') { refresh(); } })
        };
        reader.readAsDataURL(document.getElementById('file-loader-dotpattern').files[0]);
    }

}

function checkFileColor() {
    if (stateApp.layerCount >= maxEffect + 1) {
        alert('Привышен лимист слоёв');
        return 0;
    }
    else {
        var reader = new FileReader();
        loadIcon();
        reader.onload = function () {
            let req = fetch(`${HOST}/adddotcolor`, {
                method: "POST",
                body: JSON.stringify({
                    file: this.result,
                })
            });
            req.then(text => text.text()).then(answer => { if (answer == 'True') { refresh(); } })
        };
        reader.readAsDataURL(document.getElementById('file-loader-dotpatterncolor').files[0]);
    }

}
function checkFileColorDia() {
    if (stateApp.layerCount >= maxEffect + 1) {
        alert('Привышен лимист слоёв');
        return 0;
    }
    else {
        var reader = new FileReader();
        loadIcon();
        reader.onload = function () {
            let req = fetch(`${HOST}/adddotcolordia`, {
                method: "POST",
                body: JSON.stringify({
                    file: this.result,
                })
            });
            req.then(text => text.text()).then(answer => { if (answer == 'True') { refresh(); } })
        };
        reader.readAsDataURL(document.getElementById('file-loader-dotpatterncolordia').files[0]);
    }

}

function editPhoto() {
    loadIcon();
    document.getElementById('border-main-image').style.visibility = 'hidden'
    checkNormalParamsPhoto()
    let req = fetch(`${HOST}/editphoto`, {
        method: "POST",
        body: JSON.stringify({
            params: {
                x_pos: document.getElementById('slider-coord-x-photo').value,
                y_pos: document.getElementById('slider-coord-y-photo').value,
                sample: document.getElementById('slider-sample-photo').value,
                threshold: document.getElementById('slider-shadow-photo').value,
                layout: document.getElementById('slider-shadow-2-photo').value,
                width: document.getElementById('slider-scale-photo').value,
                height: document.getElementById('slider-scale-photo').value,
                choice_straz: stateApp.strazChoiced
            },
            index: stateApp.focusId,
            effect: stateApp.elementDict[`${stateApp.focusId}`]['effect'],
            focus: stateApp.focusId
        })
    });
    req.then(text => text.text()).then(answer => { if (answer == 'True') { refresh(); } })
    //setTimeout(() => {refresh();}, 100)
}

function editPhotoColor() {
    loadIcon();
    document.getElementById('border-main-image').style.visibility = 'hidden'
    checkNormalParamsPhoto()
    if (!stateApp.checkChabgeCountColor) {
        loadColorChoiced()
    }
    let req = fetch(`${HOST}/editphotocolor`, {
        method: "POST",
        body: JSON.stringify({
            params: {
                x_pos: document.getElementById('slider-coord-x-photo-color').value,
                y_pos: document.getElementById('slider-coord-y-photo-color').value,
                zoom: document.getElementById('slider-scale-photo-color').value / 1000,
                choice_straz: stateApp.strazChoicedColor,
                sample: document.getElementById('slider-sample-photo-color').value,
                shadow: document.getElementById('slider-shadow-photo-color').value,
                count_colors: document.getElementById('slider-count-color-photo-color').value,
                old_colors: stateApp.colorInPhoto,
                new_color: stateApp.choicedColorList
            },
            index: stateApp.focusId,
            effect: stateApp.elementDict[`${stateApp.focusId}`]['effect'],
            focus: stateApp.focusId
        })
    });
    req.then(text => text.text()).then(answer => { if (answer == 'True') { refresh(); } })
    //setTimeout(() => {refresh();}, 100)
}
function editPhotoColorDia() {
    loadIcon();
    document.getElementById('border-main-image').style.visibility = 'hidden'
    let req = fetch(`${HOST}/editphotocolordia`, {
        method: "POST",
        body: JSON.stringify({
            params: {
                x_pos: document.getElementById('slider-coord-x-photo-dia').value,
                y_pos: document.getElementById('slider-coord-y-photo-dia').value,
                scale: document.getElementById('slider-scale-photo-dia').value,
                max_mean: document.getElementById('slider-porog-photo-dia').value,
                count_color: document.getElementById('slider-sample-photo-dia').value,
                now_color: stateApp.colorInPhoto,
                need_color: stateApp.choicedColorList,
                sample: document.getElementById('choice-straz-size-dia').value,
                brightness: document.getElementById('slider-shadow-photo-dia').value,
                contrast: document.getElementById('slider-shadow-2-photo-dia').value,
            },
            index: stateApp.focusId,
            effect: stateApp.elementDict[`${stateApp.focusId}`]['effect'],
            focus: stateApp.focusId
        })
    });
    req.then(text => text.text()).then(answer => { if (answer == 'True') { refresh(); } })
    //setTimeout(() => {refresh();}, 100)
}

function appendOptions(optList) {
    var min = 0, max = optList.length - 1, select = document.getElementById('choice-font-famaly');

    for (var i = min; i <= max; i++) {
        var opt = document.createElement('option');
        // opt.value = optList[i];
        opt.innerHTML = optList[i];
        select.appendChild(opt);
    }
}

function checkNormalParamsShrift() {
    text_size = document.getElementById('slider-font-size');
    text = document.getElementById('config-text-effect');

    if (text_size.value > 200) { text_size.value = 200 }
    else if (text_size.value < 1) { text_size.value = 1 }
    if (text.value == '') { text.value = 'Text' }
    else if (text.value.length > 25) { text.value = 'Text'; alert('Максимальное количество символов в тексте 25!') }
}

function checkNormalParamsPhoto() {
    widht = document.getElementById('slider-scale-photo');

    if (widht.value > 3000) { widht.value = 3000 }
}

function Render() {
    loadIcon();
    document.getElementById('border-main-image').style.visibility = 'hidden'
    var checkMirror = false; if (document.getElementById('selection-mode-render').value != 'Стандарт') { checkMirror = true }
    let req = fetch(`${HOST}/render`, {
        method: "POST",
        body: JSON.stringify({
            mirror: checkMirror
        })
    });
    req.then(text => text.text()).then(answer => {
        // location.replace(`${HOST}/${answer}`)
        let el = document.getElementById('dowload_fil');
        let el1 = document.getElementById('dowload_fil-1');
        el.setAttribute('href', `${HOST}/${answer}`)
        el1.setAttribute('href', `${HOST}/${answer}`)
        el.click()
        refresh();
    })
}

function PrepareRender() {
    document.getElementById('prepare-render-layout').style.visibility = 'visible'
    if (document.getElementById('selection-mode-render').value != 'Стандарт') { document.getElementById('prepare-render-image').style.transform = 'scaleX(-1)'; document.getElementsByClassName('prewiew')[0].style.left = '0'; document.getElementsByClassName('prewiew')[0].style.top = '0'; document.getElementsByClassName('prewiew')[0].style.position = 'relative'; }
}

function detectEditShrift() {
    document.getElementById('show-value').style.display = 'none';
    editShrift()
}

function detectEditPhoto() {
    document.getElementById('show-value').style.display = 'none';
    editPhoto()
}

function detectEditPhotoDia() {
    document.getElementById('show-value').style.display = 'none';
    editPhotoColorDia()
}

function getOffset(el) {
    const rect = el.getBoundingClientRect();
    return {
        left: rect.left + window.scrollX,
        top: rect.top + window.scrollY
    };
}
// Обработчики 

function deleteDot() {
    cursorActive()
    hitBoxText()
}

function addDot() {
    cursorActiveAdd()
    hitBoxText()
}


function cursorActive() {
    let el = document.getElementById('border-main-image');
    let cursor = document.getElementById('cursor');

    cursor.style.visibility = 'visible'

    console.log(el)
    if (el) {
        el.addEventListener('mousemove', (e) => {
            let x = e.pageX;
            let y = e.pageY;

            let offset = el.getBoundingClientRect()
            cursor.style.translate = `${(x - offset.left) - 8}px ${(y - offset.top) - 7}px`;
            console.log(`${cursor.style.translate} ${cursor.style.y}`)
        })
        el.addEventListener('click', (e) => {
            let coord = cursor.style.translate.replace('px', '').replace('px', '').split(' ');
            let x = Math.round(coord[0]);
            let y = Math.round(coord[1]);

            let widht = Number(el.style.width.replace('px', ''));
            let height = Number(el.style.height.replace('px', ''));
            // alert(`x=${widht} y=${height}`)
            let res_x = ((x + 8) / (widht / 100));
            let res_y = ((y + 7) / (height / 100));

            loadIcon();
            document.getElementById('border-main-image').style.visibility = 'hidden'
            checkNormalParamsShrift()
            let fontfamaly = document.getElementById('choice-font-famaly').value
            if (stateApp.fileFont != undefined) {
                fontfamaly = stateApp.fileFont
            }
            let req = fetch(`${HOST}/editshrift`, {
                method: "POST",
                body: JSON.stringify({
                    params: {
                        x_pos: document.getElementById('slider-coord-x').value,
                        y_pos: document.getElementById('slider-coord-y').value,
                        text: document.getElementById('config-text-effect').value,
                        font_size: document.getElementById('slider-font-size').value,
                        font: fontfamaly,
                        straz_size: document.getElementById('choice-straz-size').value,
                        sample: document.getElementById('slider-sample').value,
                        threshold: 5,
                        distanse: document.getElementById('slider-distanse').value,
                        coordx_correct: 0,
                        coordy_correct: 0,
                        del_dots: `${res_x} ${res_y}`,
                        add_dots: []
                    },
                    index: stateApp.focusId,
                    effect: stateApp.elementDict[`${stateApp.focusId}`]['effect'],
                    focus: stateApp.focusId
                })
            });
            req.then(text => text.text()).then(answer => { if (answer == 'True') { refresh(); } })
        })
    }
}

function cursorActiveAdd() {
    let el = document.getElementById('border-main-image');
    let cursor = document.getElementById('cursor');

    cursor.style.visibility = 'visible'

    console.log(el)
    if (el) {
        el.addEventListener('mousemove', (e) => {
            let x = e.pageX;
            let y = e.pageY;

            let offset = el.getBoundingClientRect()
            cursor.style.translate = `${(x - offset.left) - 8}px ${(y - offset.top) - 7}px`;
            console.log(`${cursor.style.translate} ${cursor.style.y}`)
        })
        el.addEventListener('click', (e) => {
            let coord = cursor.style.translate.replace('px', '').replace('px', '').split(' ');
            let x = Math.round(coord[0]);
            let y = Math.round(coord[1]);

            let widht = Number(el.style.width.replace('px', ''));
            let height = Number(el.style.height.replace('px', ''));
            // alert(`x=${widht} y=${height}`)
            let res_x = ((x + 8) / (widht / 100));
            let res_y = ((y + 7) / (height / 100));

            loadIcon();
            document.getElementById('border-main-image').style.visibility = 'hidden'
            checkNormalParamsShrift()
            let fontfamaly = document.getElementById('choice-font-famaly').value
            if (stateApp.fileFont != undefined) {
                fontfamaly = stateApp.fileFont
            }
            let req = fetch(`${HOST}/editshrift`, {
                method: "POST",
                body: JSON.stringify({
                    params: {
                        x_pos: document.getElementById('slider-coord-x').value,
                        y_pos: document.getElementById('slider-coord-y').value,
                        text: document.getElementById('config-text-effect').value,
                        font_size: document.getElementById('slider-font-size').value,
                        font: fontfamaly,
                        straz_size: document.getElementById('choice-straz-size').value,
                        sample: document.getElementById('slider-sample').value,
                        threshold: 5,
                        distanse: document.getElementById('slider-distanse').value,
                        coordx_correct: 0,
                        coordy_correct: 0,
                        del_dots: [],
                        add_dots: `${res_x} ${res_y}`
                    },
                    index: stateApp.focusId,
                    effect: stateApp.elementDict[`${stateApp.focusId}`]['effect'],
                    focus: stateApp.focusId
                })
            });
            req.then(text => text.text()).then(answer => { if (answer == 'True') { refresh(); } })
        })
    }
}

function adaptiveVisual() {
    window.addEventListener('resize', function (event) {
        let widthWindow = window.innerWidth//outerWidth
        document.getElementById('main-head-id').style.zoom = (1 / 1920 * widthWindow)
        document.getElementById('main-pannel-control-id').style.zoom = (1 / 1920 * widthWindow)
        document.getElementById('main-pannel-layout-control-id').style.zoom = (1 / 1920 * widthWindow)
        document.getElementById('window-choice-straz').style.zoom = (1 / 1920 * widthWindow)
        document.getElementById('window-choice-color').style.zoom = (1 / 1920 * widthWindow)
        document.getElementById('fail-window').style.zoom = (1 / 1920 * widthWindow)
        document.getElementById('show-value').style.zoom = (1 / 1920 * widthWindow)
        // main-layout-id
        document.getElementById('main-layout-id').style.height = this.outerHeight - 100
    }, true);
}

function adaptiveVis() {
    let widthWindow = window.innerWidth//outerWidth

    document.getElementById('main-head-id').style.zoom = (1 / 1920 * widthWindow)
    document.getElementById('main-pannel-control-id').style.zoom = (1 / 1920 * widthWindow)
    document.getElementById('main-pannel-layout-control-id').style.zoom = (1 / 1920 * widthWindow)
    document.getElementById('window-choice-straz').style.zoom = (1 / 1920 * widthWindow)
    document.getElementById('window-choice-color').style.zoom = (1 / 1920 * widthWindow)
    document.getElementById('fail-window').style.zoom = (1 / 1920 * widthWindow)
    document.getElementById('show-value').style.zoom = (1 / 1920 * widthWindow)
    // main-layout-id
    document.getElementById('main-layout-id').style.height = this.outerHeight - 100
}

function checkUserFont() {
    if (document.getElementById('choice-font-famaly').value == 'Использовать свой' | document.getElementById('choice-font-famaly').value == 'Пользовательский') {
        var reader = new FileReader();
        reader.onload = function () {
            stateApp.fileFont = this.result
            // let req=fetch(`${HOST}/addfont`,{
            //     method: "POST",
            //     body: JSON.stringify({
            //         newuserfont: this.result
            //     })
            // });
            // req.then(text => text.text()).then(answer => {if(answer=='True'){refresh();}});
        };
        reader.readAsDataURL(document.getElementById('file-loader-font').files[0]);
    }

}

function backReturn() {
    if (JSON.parse(localStorage.getItem("ShriftParams"))) {
        if (JSON.parse(localStorage.getItem("ShriftParams"))['old'] != JSON.parse(localStorage.getItem("ShriftParams"))['new']) {
            loadIcon();
            if (stateApp.fileFont != undefined) {
                fontfamaly = stateApp.fileFont
            }
            document.getElementById('border-main-image').style.visibility = 'hidden'
            checkNormalParamsShrift()
            let req = fetch(`${HOST}/editshrift`, {
                method: "POST",
                body: JSON.stringify({
                    params: JSON.parse(localStorage.getItem("ShriftParams"))['old'],
                    index: stateApp.focusId,
                    effect: stateApp.elementDict[`${stateApp.focusId}`]['effect'],
                    focus: stateApp.focusId
                })
            });

            stateApp.oldParams['old'] = JSON.parse(localStorage.getItem("ShriftParams"))['new']
            stateApp.oldParams['new'] = JSON.parse(localStorage.getItem("ShriftParams"))['old']

            localStorage.setItem("ShriftParams", JSON.stringify(stateApp.oldParams));
            req.then(text => text.text()).then(answer => { if (answer == 'True') { refresh(); } })
        }
    }
}

function changeVisible() {
    visible_parametr = document.getElementById('select-visible').value / 100
    document.getElementsByClassName('control-image-layout')[0].style.zoom = visible_parametr
    localStorage.setItem('zoom_parametr', JSON.stringify(visible_parametr))
}

function showWindowChoiceStraz(color = false) {
    let bg = document.getElementById('black-background');
    let win = document.getElementById('window-choice-straz');
    let strazes = document.getElementsByName('bcs');
    let nums = { ss5: 0, ss6: 1, ss8: 2, ss10: 3, ss12: 4, ss16: 5, ss20: 6 }

    document.getElementById('blur-black').style.visibility = 'visible';
    document.getElementById('label-straz-choice').style.visibility = 'visible';
    document.getElementById('window-choice-straz').style.visibility = 'visible'
    bg.style.filter = 'blur(10px)';
    win.style.opacity = '1';

    setTimeout(() => {
        bg.setAttribute('onclick', 'closeStrazWindow()')
    }, 500)

    if (color) {
        document.getElementById('button-accept-choice-straz').setAttribute('onclick', 'acceptListStraz(true)')
    }
}

function handleChoiceStraz(straz) {
    let strazes = document.getElementsByName('bcs');

    let nums = { ss5: 0, ss6: 1, ss8: 2, ss10: 3, ss12: 4, ss16: 5, ss20: 6 }
    let element = strazes[nums[straz]];

    if (element.className == 'button-choice-straz-selected') {
        element.className = 'button-choice-straz'
    }
    else {
        element.className = 'button-choice-straz-selected'
    }
}

function acceptListStraz(color = false) {
    let strazes = document.getElementsByName('bcs');
    let acceptedStraz = new Array();
    for (i = 0; i < 7; i++) {
        if (strazes[i].className != 'button-choice-straz') {
            acceptedStraz.push(strazes[i].innerHTML)
        }
    }
    if (color) {
        stateApp.strazChoicedColor = acceptedStraz
    }
    else {
        stateApp.strazChoiced = acceptedStraz
    }
    let bg = document.getElementById('black-background');
    let win = document.getElementById('window-choice-straz');
    bg.style.transition = 'all 0s'
    win.style.transition = 'all 0s'

    bg.style.filter = 'none';
    win.style.opacity = '0';
    document.getElementById('blur-black').style.transition = 'all 0s';
    document.getElementById('blur-black').style.visibility = 'hidden';
    if (color) {
        editPhotoColor()
    }
    else {
        editPhoto()
    }
}

function writeSelectedStraz(choice) {
    let strazes = document.getElementsByName('bcs');
    let nums = { ss5: 0, ss6: 1, ss8: 2, ss10: 3, ss12: 4, ss16: 5, ss20: 6 }

    for (i = 0; i < 7; i++) {
        strazes[i].className = 'button-choice-straz'
    }

    for (i = 0; i < choice.length; i++) {
        strazes[nums[choice[i]]].className = 'button-choice-straz-selected'
    }

}

function lowResolutionMode() {
    document.body.style.fontSize = '10px'
}

function showWindowChoiceColor() {
    let bg = document.getElementById('black-background');
    let win = document.getElementById('window-choice-color');
    document.getElementById('blur-black').style.visibility = 'visible';
    setTimeout(() => {
        bg.setAttribute('onclick', 'closeColorWindow()')
    }, 500)
    bg.style.filter = 'blur(10px)';
    win.style.opacity = '1';
    win.style.visibility = 'visible';
    document.getElementById('buts-color').style.visibility = 'visible';
}
function showWindowChoiceColorDia() {
    let bg = document.getElementById('black-background');
    let win = document.getElementById('window-choice-color');
    document.getElementById('blur-black').style.visibility = 'visible';
    setTimeout(() => {
        bg.setAttribute('onclick', 'closeColorWindow()')
    }, 500)
    bg.style.filter = 'blur(10px)';
    win.style.opacity = '1';
    win.style.visibility = 'visible';
    document.getElementById('buts-color').style.visibility = 'visible';
    document.getElementById('button-accept-choice-straz-color').setAttribute('onclick', 'acceptChoiceColor(true)')
}

function acceptChoiceColor(dia = false) {
    let color_buttons = document.getElementsByName('button-select-color')
    let colors = [];
    for (i = 0; i < color_buttons.length; i++) {
        if (color_buttons[i].style.background != 'rgba(255, 255, 255, 0.28)') {
            colors.push(color_buttons[i].style.background)
        }

    }
    stateApp.choicedColorList = colors

    let bg = document.getElementById('black-background');
    let win = document.getElementById('window-choice-color');
    document.getElementById('blur-black').style.transition = 'all 0s';
    document.getElementById('blur-black').style.visibility = 'hidden';
    bg.style.transition = 'all 0s';
    bg.style.filter = 'none';
    win.style.transition = 'all 0s';
    win.style.opacity = '0';
    win.style.visibility = 'hidden';
    document.getElementById('buts-color').style.transition = 'all 0s';
    document.getElementById('buts-color').style.visibility = 'hidden';

    if (!dia) {
        editPhotoColor()
    }
    else {
        editPhotoColorDia()
    }
}

function closeColorWindow() {
    let bg = document.getElementById('black-background');
    let win = document.getElementById('window-choice-color');
    document.getElementById('blur-black').style.transition = 'all 0.5s';
    document.getElementById('blur-black').style.opacity = '0';
    document.getElementById('blur-black').style.visibility = 'hidden';
    bg.style.filter = 'none';
    win.style.opacity = '0';
    win.style.visibility = 'hidden';
    document.getElementById('buts-color').style.visibility = 'hidden';
    setTimeout(() => { refresh() }, 500)
}

function closeStrazWindow() {
    let bg = document.getElementById('black-background');
    let win = document.getElementById('window-choice-straz');
    document.getElementById('blur-black').style.transition = 'all 0.5s';
    document.getElementById('blur-black').style.opacity = '0';
    document.getElementById('blur-black').style.visibility = 'hidden';
    document.getElementById('butts-straz').style.transition = 'all 0.5s';
    document.getElementById('label-straz-choice').style.transition = 'all 0.5s';
    document.getElementById('button-accept-choice-straz').style.transition = 'all 0.5s';
    document.getElementById('butts-straz').style.opacity = '0';
    document.getElementById('label-straz-choice').style.opacity = '0';
    document.getElementById('button-accept-choice-straz').style.opacity = '0';
    bg.style.filter = 'none';
    win.style.opacity = '0';
    win.style.visibility = 'hidden';
    document.getElementById('buts-color').style.visibility = 'hidden';
    setTimeout(() => { refresh() }, 500)
}


function loadColorChoiced() {
    let color_buttons = document.getElementsByName('button-select-color')
    let colors = [];
    for (i = 0; i < color_buttons.length; i++) {
        if (color_buttons[i].style.background != 'rgba(255, 255, 255, 0.28)') {
            colors.push(color_buttons[i].style.background)
        }

    }
    stateApp.choicedColorList = colors
}

function handleChoiceColor(number) {
    let buts_color = document.getElementById('buts-color')
    document.getElementById('button-accept-choice-straz-color').style.opacity = '0';
    document.getElementById('button-accept-choice-straz-color').style.visibility = 'hidden';
    document.getElementById('window-choice-color').style.width = '20%'
    document.getElementById('window-choice-color').style.height = '20%'
    document.getElementById('label-straz-choice-color').innerHTML = 'Введите цвет'
    buts_color.style.opacity = '0'
    buts_color.style.visibility = 'hidden'
    document.getElementById('palette-color').style.visibility = 'visible'
    document.getElementById('input-color-hex').style.visibility = 'visible';
    document.getElementById('button-accept-change-color').style.visibility = 'visible';

    let color_buttons = document.getElementsByName('button-select-color')
    stateApp.choiceColorButton = color_buttons[number - 1]
    picker_open();
}

function acceptChangeColor() {

    let color = document.getElementById('input-color-hex').value

    // Смена цвета
    stateApp.choiceColorButton.style.background = `${color}`
    stateApp.choiceColorButton.addEventListener('mouseenter', () => {
        stateApp.choiceColorButton.style.background = '#ffffff47'
    })

    stateApp.choiceColorButton.addEventListener('mouseleave', () => {
        stateApp.choiceColorButton.style.background = `${color}`
    })

    document.getElementById('input-color-hex').value = ''

    // Возврат к нормальному интерфейсу
    let buts_color = document.getElementById('buts-color')
    document.getElementById('button-accept-choice-straz-color').style.visibility = 'visible';
    document.getElementById('button-accept-choice-straz-color').style.opacity = '1';
    document.getElementById('window-choice-color').style.width = '35%'
    document.getElementById('window-choice-color').style.height = '26%'
    document.getElementById('label-straz-choice-color').innerHTML = 'Выберите цвета для страз'
    buts_color.style.visibility = 'visible'
    buts_color.style.opacity = '1'
    document.getElementById('palette-color').style.visibility = 'hidden'
    document.getElementById('input-color-hex').style.visibility = 'hidden';
    document.getElementById('button-accept-change-color').style.visibility = 'hidden';
}

function writeRightColor(color) {
    let color_buttons = document.getElementsByName('button-select-color')
    for (i = 0; i < 16; i++) {
        if (i < color.length) {
            color_buttons[i].style.background = `rgb(${color[i]})`
            let c = `rgb(${color[i]})`;
            let b = color_buttons[i];
            b.addEventListener('mouseenter', () => {
                b.style.background = '#ffffff47'
            })
            b.addEventListener('mouseleave', () => {
                b.style.background = c
            })
        }
        else {
            color_buttons[i].style.background = '#ffffff47'
            color_buttons[i].setAttribute('onclick', 'none')
        }
    }
}

function writeRightColorDia(color) {
    let color_buttons = document.getElementsByName('button-select-color')
    for (i = 0; i < 16; i++) {
        if (i < color.length) {
            color_buttons[i].style.background = `rgb(${color[i]})`
            let c = `rgb(${color[i]})`;
            let b = color_buttons[i];
            b.addEventListener('mouseenter', () => {
                b.style.background = '#ffffff47'
            })
            b.addEventListener('mouseleave', () => {
                b.style.background = c
            })
        }
        else {
            color_buttons[i].style.background = '#ffffff47'
            color_buttons[i].setAttribute('onclick', 'none')
        }
    }
}

function backEdit() {
    loadIcon();
    let req = fetch(`${HOST}/editshrift`, {
        method: "POST",
        body: JSON.stringify({
            back: true,
            focus: stateApp.focusId
        })
    });
    req.then(text => text.text()).then(answer => { if (answer == 'True') { refresh(); } })
}

function showValue(value) {
    let el = document.getElementById('show-value');
    el.style.opacity = '1';
    setInterval(() => {
        document.getElementById('show-value').innerHTML = document.getElementById(value).value-1;
    }, 100)
    el.addEventListener('change', h)
    // el.className = 'visible-value-show';

}

function hideValue() {
    let el = document.getElementById('show-value');
    el.style.opacity = '0';
    // el.className = 'unvisible-value-show';
}

function picker_open(){
    let picker = document.getElementById("picker");
    picker.setAttribute('open', true);
    const update = e => {
        // UPDATE Callback
        document.getElementById('input-color-hex').value = e.detail.hex.substring(0,7);
    };
    picker.addEventListener('update-color', update);
}
