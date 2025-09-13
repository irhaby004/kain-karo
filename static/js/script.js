const video = document.getElementById("video");
const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");

// Atur ukuran canvas agar sesuai dengan video
navigator.mediaDevices.getUserMedia({ video: true }).then((stream) => {
  video.srcObject = stream;

  video.addEventListener("loadedmetadata", () => {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    startDetection();
  });
});

async function startDetection() {
  const apiEndpoint = "/api/realtime_detection";

  while (true) {
    // Tangkap frame dari video
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    const frame = canvas.toDataURL("image/jpeg");

    // Kirim frame ke server
    const response = await fetch(apiEndpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ image: frame.split(",")[1] }), // Kirim tanpa header Base64
    });

    if (!response.ok) {
      console.error("Error:", await response.text());
      continue;
    }

    // Bersihkan canvas sebelum menggambar
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Gambar kotak deteksi dari hasil API
    const results = await response.json();
    results.forEach((detection) => {
      ctx.strokeStyle = "green";
      ctx.lineWidth = 2;
      ctx.strokeRect(
        detection.x,
        detection.y,
        detection.width,
        detection.height
      );
    });

    // Tunggu sebelum mengirim frame berikutnya
    await new Promise((resolve) => setTimeout(resolve, 100));
  }
}
