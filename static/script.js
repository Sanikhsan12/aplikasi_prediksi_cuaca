const prosesBtn = document.getElementById("proses-btn");

prosesBtn.addEventListener("click", async () => {
  const suhu = document.getElementById("suhu").value;
  const kelembaban = document.getElementById("kelembaban").value;
  const tekanan = document.getElementById("tekanan").value;

  const response = await fetch("/proses", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ suhu, kelembaban, tekanan }),
  });

  const result = await response.json();

  if (result.status === "success") {
    const curahHujanSugeno = document
      .querySelectorAll("section")[1]
      .querySelectorAll("input")[0];
    const prediksiSugeno = document
      .querySelectorAll("section")[1]
      .querySelectorAll("input")[1];
    const curahHujanMamdani = document
      .querySelectorAll("section")[2]
      .querySelectorAll("input")[0];
    const prediksiMamdani = document
      .querySelectorAll("section")[2]
      .querySelectorAll("input")[1];
    const saranParagraf = document.getElementById("saran");

    // Representasi Kategori Prediksi
    const kategoriPrediksi = {
      no_rain: "Cerah",
      light_rain: "Gerimis",
      moderate_rain: "Hujan sedang",
      heavy_rain: "Hujan lebat",
      very_heavy_rain: "Badai",
    };

    const kategoriSugeno = result.hasil.sugeno.category.toLowerCase();
    const kategoriMamdani = result.hasil.mamdani.category.toLowerCase();

    curahHujanSugeno.value = result.hasil.sugeno.value;
    prediksiSugeno.value =
      kategoriPrediksi[kategoriSugeno] || "Tidak Dapat Diprediksi";
    curahHujanMamdani.value = result.hasil.mamdani.value;
    prediksiMamdani.value =
      kategoriPrediksi[kategoriMamdani] || "Tidak Dapat Diprediksi";

    // Saran dinamis berdasarkan kategori curah hujan
    let saran = "Cuaca cerah. Nikmati harimu!";
    if (kategoriSugeno === "no_rain" || kategoriMamdani === "no_rain") {
      saran =
        "Nampaknya cuaca akan cerah hari ini, jangan lupa gunakan sunscreen ya!";
    } else if (
      kategoriSugeno === "light_rain" ||
      kategoriMamdani === "light_rain"
    ) {
      saran =
        "Disarankan untuk membawa payung kecil atau jas hujan karena kemungkinan Gerimis.";
    } else if (
      kategoriSugeno === "moderate_rain" ||
      kategoriMamdani === "moderate_rain"
    ) {
      saran =
        "Kemungkinan akan hujan sedang. Disarankan untuk membawa payung atau jas hujan.";
    } else if (
      kategoriSugeno === "heavy_rain" ||
      kategoriMamdani === "heavy_rain"
    ) {
      saran =
        "Karena kemungkinan akan hujan lebat, disarankan untuk menghindari perjalanan jauh, waspada juga terhadap banjir.";
    } else if (
      kategoriSugeno === "very_heavy_rain" ||
      kategoriMamdani === "very_heavy_rain"
    ) {
      saran =
        "Karena kemungkinan akan badai, disarankan untuk tetap di dalam ruangan dan menghindari perjalanan jauh, waspada juga terhadap banjir.";
    }

    saranParagraf.textContent = saran;

    alert(result.message);
  } else {
    alert("Terjadi kesalahan.");
  }
});
