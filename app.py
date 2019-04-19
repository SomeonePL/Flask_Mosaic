from flask import Flask, request, send_file
import requests
import random, re, io
from PIL import Image

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/mozaika')
def mozaika():
    shuffle_img = request.args.get('losowo', default=0, type=int)
    resolution = request.args.get('rozdzielczosc', default='2048x2048', type=str)
    images = request.args.get('zdjecia', default='', type=str)
    if re.search("[1-9][0-9]*x[1-9][0-9]*", resolution):
        width = int(resolution.split('x')[0])
        height = int(resolution.split('x')[1])
    else:
        width = 2048
        height = 2048

    mosaic = Image.new('RGB', (width, height))
    urls = images.split(',')
    urls_amount = len(urls)
    if images == '':
        return '<head><title>Feed me URLs!</title></head>' \
               '<body><font size = 18><b>You haven\'t given a single URL!</b></font><br>'\
                'Hey! I can handle up to <u>8</u> URLs of images at once. Try me!</body>'
    if urls_amount > 8:
        return '<head><title>Whoa there!</title></head>' \
               '<body><font size = 18><b>Too many URLs given!</b></font><br>'\
                'I can handle up to <u>8</u> URLs of images at once.</body>'
    if shuffle_img == 1:
        random.shuffle(urls)

    j = 0
    for i in range(urls_amount):
        req = requests.get(urls[i])
        image = Image.open(io.BytesIO(req.content))
        if urls_amount == 3 or urls_amount == 2 or urls_amount == 1:
            image = image.resize((int(width / urls_amount), height))
            mosaic.paste(image, ((int(width / urls_amount)) * i, 0))
        elif urls_amount == 5:
            image = image.resize((int(width / 2), int(height / 3)))
            if i < 2:
                mosaic.paste(image, ((int(width / 2)) * i, 0))
            if i == 2:
                mosaic.paste(image, (int(1.33 * width / urls_amount), int(height / 3)))
            if i > 2:
                mosaic.paste(image, (int((width / 2)) * j, int(2*height / 3)))
                j += 1
        elif urls_amount == 7:
            image = image.resize((int(width / 3), int(height / 3)))
            if i < 2:
                mosaic.paste(image, (int((width / 3) * (i + 0.5)), 0))
            elif i < 5:
                mosaic.paste(image, (int(width / 3) * (i-2), int(height / 3)))
            elif i > 4:
                mosaic.paste(image, (int((width / 3) * (j+0.5)), int(2*height / 3)))
                j +=1
        else:
            image = image.resize((int(width / (urls_amount / 2)), int(height / 2)))
            if i < (urls_amount / 2):
                mosaic.paste(image, ((int(width / urls_amount)) * i * 2, 0))
            else:
                mosaic.paste(image, (int((width / urls_amount)) * j * 2, int(height / 2)))
                j += 1
        mosaic.save('mosaic.jpeg')
    return send_file('mosaic.jpeg', mimetype='image')


if __name__ == '__main__':
    app.run()
