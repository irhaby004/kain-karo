from flask import Flask, render_template, request
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np

app = Flask(__name__)

dic = {
    0: ('UIS BEKAH BULU', 'Uis beka buluh ialah sebuah kain yang ditandakan sebagai kebesaran seorang pria Karo. Uis ini hanya dikenakan oleh orang-orang tertentu yakni orang yang melakukan sebuah pesta adat pada waktu perkawinan, memasuki rumah baru dan upacara kematian. Biasanya uis ini dikenakan di pundak atau bisa juga dijadikan sebagai penutup kepala yang disebut bulang-bulang. Ukuran kain ini, panjang 166 cm, lebar 84 cm, bahan baku benang kapas dan benang emas.'),
    1: ('UIS GATIP JONGKIT', 'Uis gatip jongkit adalah kain yang digunakan untuk sarung di pinggang (gonce rose) untuk laki-laki. Uis ini biasanya digunakan pada saat pesta adat pernikahan, selimut bagi kalimbubu dan pesta adat kerja tahun. Ukuran kain ini panjangnya 164 cm lebar 81 cm bahan baku benang kapas, warna dasar hitam.'),
    2: ('UIS JULU DIBERU', 'Uis julu diberu merupakan kain yang digunakan oleh kalangan wanita yang dibalutkan pada tubuh mulai dari bagian pinggang hingga sedikit dibawah lutut. Uis ini dikenakan pada saat pesata adat penikahan, memasuki rumah baru dan pesta tahunan. Ukuruan kain ini panjangnya 174 cm lebar 96 cm. Bahan baku kain ini dari tenun kain kapas.'),
    3: ('UIS KELAM KELAM', 'Uis kelam-kelam merupakan kain dengan warna hitam polos. Uis ini dipakai sebagai tudung (penutup kepala) oleh wanita pada pesta adat dan pesta guro guro aron (pesta muda-mudi). Panjang kain ini 169 cm lebar 80 cm.'),
    4: ('UIS NIPES', 'Uis nipes padang rusak ialah kain yang dipakai oleh wanita sebagai selendang di bahu pada pesta adat. Pada zaman dulu, uis ini tidak hanya digunakan ketika pesta adat, tetapi juga sering digunakan dalam kehidupan sehari-hari sebagai selendang penghangat tubuh. Panjang kain ini 152 cm dan lebarnya 82 cm.')
}


# Load the model
model = load_model('MobileNetV2-v1-KainKaro-98.40.h5')

# Initialize the predict function
model.make_predict_function()

def predict_label(img_path):
    # Load and preprocess the image
    i = image.load_img(img_path, target_size=(224, 224))
    i = image.img_to_array(i) / 255.0
    i = i.reshape(1, 224, 224, 3)
    
    # Predict the class and probabilities
    prediction = model.predict(i)
    
    # Get the index and probability of the highest value
    p = np.argmax(prediction, axis=-1)  # Index of the highest probability
    accuracy = float(np.max(prediction)) * 100  # Convert to percentage
    
    # Check accuracy threshold
    if accuracy < 95:
        label, description = 'Unknown', 'Gambar tersebut bukan kain Karo.'
    else:
        label, description = dic[p[0]]  # Extract label and description
    
    return label, description, accuracy




# Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/klasifikasi', methods=['GET', 'POST'])
def klasifikasi():
    if request.method == 'POST':
        img = request.files['my_image']
        
        # Save the uploaded image to the static folder
        img_path = "static/" + img.filename
        img.save(img_path)
        
        # Get the predicted label, description, and accuracy
        label, description, accuracy = predict_label(img_path)

        # Render the result on the page
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
