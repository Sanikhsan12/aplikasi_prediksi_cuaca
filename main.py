# ! variabel nilai input dari html

air_temperature = None
humidity_value = None
pressure_value = None

def set_input_values(suhu, kelembaban, tekanan):
    global air_temperature, humidity_value, pressure_value
    air_temperature = suhu
    humidity_value = kelembaban
    pressure_value = tekanan


# ! domain value
temperature = {
    "cold": [11, 16, 21],
    "warm_1": [20, 23.5, 27],
    "warm_2": [26, 27, 28],
    "warm_3": [27, 29, 31],
    "hot": [29, 34.5, 40]
}

humidity = {
    "dry": [30, 35.5, 41],
    "humid_1": [40, 55.5, 71],
    "humid_2": [70, 75, 80],
    "humid_3": [79, 84, 89],
    "wet": [88, 94, 100]
}

pressure = {
    "low": [980, 993.5, 1007],
    "medium": [1006, 1006.5, 1007],
    "high": [1008, 1011, 1014]
}

rainfall_changes = {
    "no_rain": [0, 0.25, 0.5],
    "light_rain": [0.5, 10.25, 20],
    "moderate_rain": [20, 35, 50],
    "heavy_rain": [50, 75, 100],
    "very_heavy_rain": [100, 125, 150]
}

# ! Rule Base
rule_base = [
    # ! Rules untuk tidak hujan / sunn
    {"temp": "hot", "humidity": "dry", "pressure": "high", "output": "no_rain"},
    {"temp": "hot", "humidity": "dry", "pressure": "medium", "output": "no_rain"},
    {"temp": "hot", "humidity": "humid_1", "pressure": "high", "output": "no_rain"},
    {"temp": "warm_3", "humidity": "humid_1", "pressure": "high", "output": "no_rain"},
    {"temp": "warm_3", "humidity": "humid_2", "pressure": "high", "output": "no_rain"},
    {"temp": "warm_2", "humidity": "humid_2", "pressure": "high", "output": "no_rain"},
    {"temp": "warm_1", "humidity": "dry", "pressure": "high", "output": "no_rain"},
    {"temp": "warm_1", "humidity": "humid_1", "pressure": "high", "output": "no_rain"},
    {"temp": "warm_1", "humidity": "humid_2", "pressure": "high", "output": "no_rain"},
    
    # ! Rules untuk hujan ringan
    {"temp": "warm_3", "humidity": "humid_2", "pressure": "medium", "output": "light_rain"},
    {"temp": "warm_3", "humidity": "humid_2", "pressure": "low", "output": "light_rain"},
    {"temp": "warm_2", "humidity": "humid_3", "pressure": "high", "output": "light_rain"},
    {"temp": "warm_2", "humidity": "humid_2", "pressure": "low", "output": "light_rain"},
    {"temp": "warm_2", "humidity": "humid_3", "pressure": "medium", "output": "light_rain"},
    {"temp": "warm_1", "humidity": "humid_2", "pressure": "low", "output": "light_rain"},
    {"temp": "warm_1", "humidity": "humid_3", "pressure": "high", "output": "light_rain"},
    {"temp": "warm_1", "humidity": "humid_3", "pressure": "medium", "output": "light_rain"},
    
    # ! Rules untuk hujan sedang
    {"temp": "warm_2", "humidity": "wet", "pressure": "low", "output": "moderate_rain"},
    {"temp": "warm_1", "humidity": "wet", "pressure": "low", "output": "moderate_rain"},
    {"temp": "warm_1", "humidity": "wet", "pressure": "high", "output": "moderate_rain"},
    {"temp": "cold", "humidity": "wet", "pressure": "low", "output": "moderate_rain"},
    {"temp": "cold", "humidity": "wet", "pressure": "medium", "output": "moderate_rain"},
    {"temp": "cold", "humidity": "humid_3", "pressure": "low", "output": "moderate_rain"},
    
    # ! Rules unutuk hujan lebat
    {"temp": "cold", "humidity": "wet", "pressure": "high", "output": "heavy_rain"},
    {"temp": "cold", "humidity": "humid_3", "pressure": "high", "output": "heavy_rain"},
    {"temp": "cold", "humidity": "humid_3", "pressure": "medium", "output": "heavy_rain"},
    
    # ! Rules untuk hujan sangat lebat
    {"temp": "cold", "humidity": "humid_2", "pressure": "low", "output": "very_heavy_rain"},
    {"temp": "cold", "humidity": "humid_1", "pressure": "low", "output": "very_heavy_rain"},
    {"temp": "cold", "humidity": "dry", "pressure": "low", "output": "very_heavy_rain"},
    {"temp": "cold", "humidity": "humid_1", "pressure": "medium", "output": "very_heavy_rain"}
]

# * fungsi segitiga
def triangular_membership(x, nilaiAwal, nilaiTengah, nilaiAkhir):
    if x <= nilaiAwal or x >= nilaiAkhir:
        return 0.0
    elif x <= nilaiTengah:
        return (x - nilaiAwal) /  (nilaiTengah  - nilaiAwal)
    else:
        return (nilaiAkhir - x) / (nilaiAkhir - nilaiTengah)

# ? fuzzy set temperature
def fuzifikasi_temprature(value, jangkauan):
    keanggotaan = {}
    
    for key, (nilaiAwal, nilaiTengah, nilaiAkhir) in jangkauan.items():
        anggota = triangular_membership(value, nilaiAwal, nilaiTengah, nilaiAkhir)
        if anggota > 0:
            keanggotaan[key] = anggota
    
    if keanggotaan:
        total = sum(keanggotaan.values())
        normalized_values = {key: val/total for key, val in keanggotaan.items()}
        
        hasil = {key : round(val, 2) for key, val in normalized_values.items()}
        return hasil
    else:
        return ["No membership found"], {}
    
# ? fuzzy set humidity
def fuzifikasi_kelembapan(value, jangkauan):
    keanggotaan = {}
    
    for key, (nilaiAwal, nilaiTengah, nilaiAkhir) in jangkauan.items():
        anggota = triangular_membership(value, nilaiAwal, nilaiTengah, nilaiAkhir)
        if anggota > 0:
            keanggotaan[key] = anggota
    
    if keanggotaan:
        total = sum(keanggotaan.values())
        normalized_values = {key: val/total for key, val in keanggotaan.items()}
        
        hasil = {key : round(val, 2) for key, val in normalized_values.items()}
        return hasil
    else:
        return ["No membership found"], {}
    
# ? fuzzy set pressure
def fuzifikasi_tekanan(value, jangkauan):
    keanggotaan = {}
    
    for key, (nilaiAwal, nilaiTengah, nilaiAkhir) in jangkauan.items():
        anggota = triangular_membership(value, nilaiAwal, nilaiTengah, nilaiAkhir)
        if anggota > 0:
            keanggotaan[key] = anggota
    
    if keanggotaan:
        total = sum(keanggotaan.values())
        normalized_values = {key: val/total for key, val in keanggotaan.items()}
        
        hasil = {key : round(val, 2) for key, val in normalized_values.items()}
        return hasil
    else:
        return ["No membership found"], {}
    
def hasil_fuzifikasi():
    # ! hasil normalisasi
    hasil_termprature = fuzifikasi_temprature(air_temperature, temperature)
    hasil_humidity = fuzifikasi_kelembapan(humidity_value, humidity)
    hasil_pressure = fuzifikasi_tekanan(pressure_value, pressure)

    print("Hasil Fuzifikasi:")
    print("Suhu Udara:", hasil_termprature)
    print("Kelembapan:", hasil_humidity)
    print("Tekanan Udara:", hasil_pressure)
    
    return hasil_termprature, hasil_humidity, hasil_pressure

def apply_rule_base(hasil_termprature, hasil_humidity, hasil_pressure):
    hasil_rule = {}
    
    print("\nRule Matching Details:")
    
    for rule in rule_base:
        temp = rule["temp"]
        humidity = rule["humidity"]
        pressure = rule["pressure"]
        output = rule["output"]
        
        temp_val = hasil_termprature.get(temp, 0)
        hum_val = hasil_humidity.get(humidity, 0)
        press_val = hasil_pressure.get(pressure, 0)
        
        print(f"Rule: {temp}/{humidity}/{pressure} -> {output}")
        print(f"  Values: temp={temp_val}, humidity={hum_val}, pressure={press_val}")
        
        if temp in hasil_termprature and humidity in hasil_humidity and pressure in hasil_pressure:
            min_value = min(hasil_termprature[temp], hasil_humidity[humidity], hasil_pressure[pressure])
            print(f"  Match! Min value: {min_value}")
            
            if output not in hasil_rule:
                hasil_rule[output] = min_value
            else:
                hasil_rule[output] = max(hasil_rule[output], min_value)
        else:
            print("  No match")
    
    return hasil_rule

# ? Clasifikasi
def clasifikasi(value, rainfall_changes):
    highest_value = 0
    best_catergory = "no category"

    for key, (nilaiAwal, nilaiTengah, nilaiAkhir) in rainfall_changes.items():
        membership = triangular_membership(value, nilaiAwal, nilaiTengah, nilaiAkhir)
        if membership > highest_value:
            highest_value = membership
            best_catergory = key

    return best_catergory

# ? defuzifikasi
def defuzifikasi_mamdani(hasil_rule, rainfall_changes):
    if not hasil_rule:
        return 0.0, "No Rules Matched"
    
    sample_point = []
    step = 0.15
    nilaiAwal = 0
    while nilaiAwal <= 150:
        sample_point.append(nilaiAwal)
        nilaiAwal += step

    membership_values = [0] * len(sample_point)

    for index, value in hasil_rule.items():
        if index in rainfall_changes:
            nilaiAwal, nilaiTengah, nilaiAkhir = rainfall_changes[index]
            for i, x in enumerate(sample_point):
                membership_values[i] = max(membership_values[i], triangular_membership(x, nilaiAwal, nilaiTengah, nilaiAkhir))

    # ? defuzifikasi centroid
    numerator = 0.0
    denominator = 0.0
    for i, x in enumerate(sample_point):
        numerator += x * membership_values[i]
        denominator += membership_values[i]

    if denominator == 0:
        return 0.0, "No Membership Found"
    
    crisp_value = numerator / denominator
    best_category = clasifikasi(crisp_value, rainfall_changes)
    return crisp_value, best_category
    

def defuzifikasi_sugeno(hasil_rule, rainfall_changes):
    if not hasil_rule:
        return 0.0, "No Rules Matched"
    
    representative_values = {}
    for key, (nilaiAwal, nilaiTengah, nilaiAkhir) in rainfall_changes.items():
        representative_values[key] = nilaiTengah

    numerator = 0.0
    denominator = 0.0

    for key, value in hasil_rule.items():
        z_value = representative_values[key]

        numerator += z_value * value
        denominator += value

    if denominator == 0:
        return 0.0, "No Membership Found"
    
    crisp_value = numerator / denominator
    best_category = clasifikasi(crisp_value, rainfall_changes)
    return crisp_value, best_category

def main():
    hasil_temperature, hasil_humidity, hasil_pressure = hasil_fuzifikasi()
    hasil_rule = apply_rule_base(hasil_temperature, hasil_humidity, hasil_pressure)
    
    crisp_value_mamdani, category_mamdani = defuzifikasi_mamdani(hasil_rule, rainfall_changes)
    crisp_value_sugeno, category_sugeno = defuzifikasi_sugeno(hasil_rule, rainfall_changes)

    return {
        "mamdani": {
            "value": round(crisp_value_mamdani, 2),
            "category": category_mamdani
        },
        "sugeno": {
            "value": round(crisp_value_sugeno, 2),
            "category": category_sugeno
        }
    }

if __name__ == "__main__":
    main()