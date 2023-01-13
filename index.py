import PIL
from flask import Flask, render_template, request, jsonify, make_response
from io import BytesIO
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from PIL import Image, ImageDraw, ImageFont
import qrcode

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

class QRForm(FlaskForm):
    url = StringField('Convert this to QR:')
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
@app.route('/qr', methods=['GET', 'POST'])
def qr_code():
    form = QRForm()
    if form.validate_on_submit():
>>>>>>> parent of 15700f2 (Update index.py)
        url = form.url.data
        qr = qrcode.QRCode(version=1, box_size=10, border=2)
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img = img.convert("RGBA")
        img_w, img_h = img.size
        logo_size = int(img_w/5)
        logo = Image.open("ddlogo.png").resize((logo_size, logo_size))
        img_w, img_h = img.size
        logo_w, logo_h = logo.size
        logo_pos = (img_w//2 - logo_w//2, img_h//2 - logo_h//2)
        img.alpha_composite(logo, logo_pos)

         # Draw text on the QR code
        draw = ImageDraw.Draw(img)
        text = "digidream.in"
        font = ImageFont.truetype("arial.ttf", 10)
        text_w, text_h = draw.textsize(text, font)
        pos = ((img_w - text_w) / 2, img_h - text_h - 2)
        draw.text(pos, text, font=font, fill=(0, 0, 0, 255))


        img_io = BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)
        response = make_response(img_io.read())
        response.headers.set('Content-Type', 'image/png')
        response.headers.set('Content-Disposition', 'attachment', filename='qr.png')
        return response
    return render_template('qr_form.html', form=form)

if __name__ == '__main__':
    app.run()
