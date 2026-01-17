function generateSite() {
  const prompt = document.getElementById("prompt").value.trim();
  const previewFrame = document.getElementById("preview");

  if (!prompt) {
    alert("Please enter a website description");
    return;
  }

  // Show loading state
  previewFrame.srcdoc = "<h3 style='font-family:Arial'>Generating website...</h3>";

  fetch("/generate", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ prompt: prompt })
  })
    .then(async (response) => {
      const data = await response.json();

      // ❌ Backend error
      if (!response.ok) {
        previewFrame.srcdoc = `
          <h3 style="color:red;font-family:Arial">Error generating website</h3>
          <pre>${JSON.stringify(data, null, 2)}</pre>
        `;
        return;
      }

      // ✅ Success
      previewFrame.srcdoc = data.html;
    })
    .catch((error) => {
      previewFrame.srcdoc = `
        <h3 style="color:red;font-family:Arial">Request failed</h3>
        <pre>${error}</pre>
      `;
    });
}

// Optional: download generated website
function downloadSite() {
  window.location.href = "/download";
}
