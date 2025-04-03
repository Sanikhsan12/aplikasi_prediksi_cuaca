# Rule / Pertanyaan 
# * Kondisi Langit [ Cerah, Berawan, Mendung, Hujan Ringan, Hujan Lebat ]
# ? Seberapa Kuat Angin Bertiup Di Sekitar Anda? [ Tenang, Sedang, Kencang, Sangat Kencang ]
# ? Bagaimana Perkiraan Kelembapan Udara Di Sekitar Anda? [ Kering, Lembab, Sangat Lembab ]
# ? pakah Ada Tanda-tanda Badai Di sekitar Anda? [ Ya, Tidak ]
# ? pakah Ada perubahan Cuaca Yang Signifikan Dalam Beberapa Jam Terakhir? [ Ya, Tidak ]

# ! library
from flask import Flask, render_template, request, jsonify
import skfuzzy as fuzz
import skfuzzy.control as ctrl
import numpy as np

app = Flask(__name__, template_folder='view', static_folder='static')

def hitung_fuzzy(angin, kelembapan, badai, perubahan):
    # * pengelompokan selain rule 
    pengelompokan = {
        (0, 0, 0, 1): "Cerah",
        (0, 0, 1, 0): "Cerah",
        (0, 0, 1, 1): "Cerah",
        (0, 1, 0, 0): "Cerah",
        (0, 1, 0, 1): "Cerah",
        (0, 1, 1, 0): "Cerah",
        (0, 1, 1, 1): "Cerah",
        (1, 0, 0, 1): "Berawan",
        (1, 0, 1, 0): "Berawan",
        (1, 0, 1, 1): "Berawan",
        (1, 1, 0, 1): "Mendung",
        (1, 1, 1, 0): "Mendung",
        (1, 1, 1, 1): "Mendung",
    }

    # ? pengecekan Pengelompokan
    if (angin, kelembapan, badai, perubahan) in pengelompokan:
        return pengelompokan[(angin, kelembapan, badai, perubahan)]
    
    # ! Variabel Fuzzy
    langit = ctrl.Consequent(np.arange(0, 5, 1), 'langit')
    angin_var = ctrl.Antecedent(np.arange(0, 4, 1), 'angin')
    kelembapan_var = ctrl.Antecedent(np.arange(0, 3, 1), 'kelembapan')
    badai_var = ctrl.Antecedent(np.arange(0, 2, 1), 'badai')
    perubahan_var = ctrl.Antecedent(np.arange(0, 2, 1), 'perubahan')

    # ! Keanggotaan
    langit.automf(names=['Cerah', 'Berawan', 'Mendung', 'Hujan_Ringan', 'Hujan_Lebat'])
    angin_var.automf(names=['Tenang', 'Sedang', 'Kencang', 'Sangat_Kencang']) # 4
    kelembapan_var.automf(names=['Kering', 'Lembab', 'Sangat_Lembab']) # 3
    badai_var.automf(names=['Tidak', 'Ya']) # 2
    perubahan_var.automf(names=['Tidak', 'Ya']) # 2

    # ! Aturan
    aturan1 = ctrl.Rule(angin_var['Tenang'] & kelembapan_var['Kering'] & badai_var['Tidak'] & perubahan_var['Tidak'], langit['Cerah'])
    aturan2 = ctrl.Rule(angin_var['Sedang'] & kelembapan_var['Kering'] & badai_var['Tidak'] & perubahan_var['Tidak'], langit['Berawan'])
    aturan3 = ctrl.Rule(angin_var['Sedang'] & kelembapan_var['Lembab'] & badai_var['Tidak'] & perubahan_var['Tidak'], langit['Mendung'])
    aturan4 = ctrl.Rule(angin_var['Kencang'] & kelembapan_var['Lembab'] & badai_var['Tidak'] & perubahan_var['Ya'], langit['Hujan_Ringan'])
    aturan5 = ctrl.Rule(angin_var['Sangat_Kencang'] & kelembapan_var['Sangat_Lembab'] & badai_var['Ya'] & perubahan_var['Ya'], langit['Hujan_Lebat'])

    sistem = ctrl.ControlSystem([aturan1, aturan2, aturan3, aturan4, aturan5])
    kontrol = ctrl.ControlSystemSimulation(sistem)
    
    kontrol.input['angin'] = angin
    kontrol.input['kelembapan'] = kelembapan
    kontrol.input['badai'] = badai
    kontrol.input['perubahan'] = perubahan
    
    kontrol.compute()
    hasil = kontrol.output['langit']

    # ? Pemetaan hasil ke kategori cuaca
    if hasil < 1:
        return "Cerah"
    elif hasil < 2:
        return "Berawan"
    elif hasil < 3:
        return "Mendung"
    elif hasil < 4:
        return "Hujan Ringan"
    else:
        return "Hujan Lebat"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json['message'].strip().lower()
        responses = {
            "halo": "<br/>Halo! Masukkan parameter cuaca dalam format: angin (0-3), kelembapan (0-2), badai (0-1), perubahan (0-1).",
            "siapa kamu": "Saya chatbot prediksi cuaca menggunakan fuzzy logic.",
            "apa kabar": "Saya baik! Bagaimana dengan Anda?"
        }
        
        if data in responses:
            return jsonify({"reply": responses[data]})
        elif "prediksi" in data:
            return jsonify({"reply": "Masukkan parameter cuaca dalam format: angin (0-3), kelembapan (0-2), badai (0-1), perubahan (0-1)."})
        else:
            params = list(map(int, data.split())) 
            if len(params) == 4:
                angin, kelembapan, badai, perubahan = params
                if 0 <= angin <= 3 and 0 <= kelembapan <= 2 and 0 <= badai <= 1 and 0 <= perubahan <= 1:
                    hasil = hitung_fuzzy(angin, kelembapan, badai, perubahan)
                    return jsonify({"reply": f"Prediksi cuaca: {hasil}"})
                else:
                    return jsonify({"reply": "Format salah! Gunakan angka sesuai rentang yang ditentukan."})
            else:
                return jsonify({"reply": "Input tidak lengkap. Silakan masukkan 4 angka sesuai format."})
    except Exception as e:
        return jsonify({"reply": f"Terjadi kesalahan: {str(e)}"})



if __name__ == '__main__':
    app.run(debug=True)
