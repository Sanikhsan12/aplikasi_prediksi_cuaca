const prosesBtn = document.querySelector("button");

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
    // Ambil elemen input output hasil
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
    const saranParagraf = document.querySelector("section:nth-of-type(4) p");

    // Update nilainya
    curahHujanSugeno.value = result.hasil.sugeno.value;
    prediksiSugeno.value = result.hasil.sugeno.category;
    curahHujanMamdani.value = result.hasil.mamdani.value;
    prediksiMamdani.value = result.hasil.mamdani.category;

    // Saran dinamis
    let saran = "Cuaca cerah. Nikmati harimu!";
    if (
      result.hasil.sugeno.category.toLowerCase().includes("hujan") ||
      result.hasil.mamdani.category.toLowerCase().includes("hujan")
    ) {
      saran =
        "Disarankan membawa payung jika hendak bepergian karena diprediksi hujan.";
    }
    saranParagraf.textContent = saran;

    // Optional: alert success
    alert(result.message);
  } else {
    alert("Terjadi kesalahan.");
  }
});
