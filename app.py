from flask import Flask, request, jsonify, render_template
import main  # pastikan file main.py dan app.py ada di folder sama

app = Flask(__name__,template_folder='view')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/proses', methods=['POST'])
def proses():
    data = request.json
    suhu = float(data['suhu'])
    kelembaban = float(data['kelembaban'])
    tekanan = float(data['tekanan'])

    # simpan ke variabel di main.py
    main.set_input_values(suhu, kelembaban, tekanan)
    hasil = main.main()

    return jsonify({
        'status': 'success',
        'message': 'Data berhasil diproses!',
        'hasil': hasil
    })


if __name__ == '__main__':
    app.run(debug=True)
