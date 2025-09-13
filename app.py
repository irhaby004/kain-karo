from flask import Flask, render_template, request
import numpy as np

app = Flask(__name__)

dic = {
    0: ('UIS BEKAH BULU', 'Uis beka buluh ialah sebuah kain yang ditandakan sebagai kebesaran seorang pria Karo. ...'),
    1: ('UIS GATIP JONGKIT', 'Uis gatip jongkit adalah kain yang digunakan untuk sarung di pinggang ...'),
    2: ('UIS JULU DIBERU', 'Uis julu diberu merupakan kain yang digunakan oleh kalangan wanita ...'),
    3: ('UIS KELAM KELAM', 'Uis kelam-kelam merupakan kain dengan warna hitam polos ...'),
    4: ('UIS NIPES', 'Uis nipes padang rusak ialah kain yang dipakai oleh wanita sebagai selendang ...')
}

# Hapus semua kode TensorFlow
model = None

def predict_label(img_path):
    # Dummy prediksi: pilih random
    idx = np.random.randint(0, len(dic))
    label, description = dic[idx]
    accuracy = 100.0  # set dummy accuracy 100%
    return label, description, accuracy


# Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/klasifikasi', methods=['GET', 'POST'])
def klasifikasi():
    if request.method == 'POST':
        img = request.files['my_image']
        
        # Simpan gambar di folder static
        img_path = "static/" + img.filename
        img.save(img_path)
        
        # Prediksi dummy
        label, description, accuracy = predict_label(img_path)

        return render_template(
            "klasifikasi.html",
            prediction=label,
            description=description,
            accuracy=accuracy,
            img_path=img_path
        )
    
    return render_template("klasifikasi.html")


@app.route('/jenis')
def jenis():
    return render_template('jenis.html')

if __name__ == '__main__':
    app.run(debug=True)
