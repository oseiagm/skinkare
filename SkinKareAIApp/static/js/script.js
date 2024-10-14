const dropArea = document.getElementById('drop-area');
const fileInput = document.getElementById('file-upload');
const filePreview = document.getElementById('file-preview');
const previewImage = document.getElementById('preview-image');
const previewContainer = document.getElementById('preview-container');

function showFilePreview(file) {
  const reader = new FileReader();
  reader.onload = function (event) {
    previewImage.src = event.target.result;
    filePreview.classList.remove('hidden');
    previewContainer.classList.add('hidden');
  };
  reader.readAsDataURL(file);
}

fileInput.addEventListener('change', (event) => {
  const file = event.target.files[0];
  if (file) showFilePreview(file);
});

dropArea.addEventListener('dragover', (event) => {
  event.preventDefault();
  dropArea.classList.add('border-blue-600');
});

dropArea.addEventListener('dragleave', () => {
  dropArea.classList.remove('border-blue-600');
});

dropArea.addEventListener('drop', (event) => {
  event.preventDefault();
  dropArea.classList.remove('border-blue-600');
  const file = event.dataTransfer.files[0];
  if (file) {
    fileInput.files = event.dataTransfer.files;
    showFilePreview(file);
  }
});

dropArea.addEventListener('click', () => fileInput.click());




function analyzeImage() {
    const fileInput = document.getElementById("fileInput");
    const formData = new FormData();

    formData.append("image", fileInput.files[0]);

    fetch("/analyze", {
            method: "POST",
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            console.log("Server Response:", data); // Debugging

            if (data.error) {
                alert(data.error);
                return;
            }

            // Store result in local storage
            localStorage.setItem("analysisResult", JSON.stringify(data));
            console.log("Data saved to localStorage");

            window.location.href = "/results"; // Redirect to results page
        })
        .catch(error => {
            alert("Error: " + error);
        });
}

// Load analysis result on results page
if (window.location.pathname.includes("results")) { // Check page URL
    const resultContainer = document.getElementById("result-container");
    console.log("Result container:", resultContainer); // Debugging

    const analysisResult = JSON.parse(localStorage.getItem("analysisResult"));
    console.log("Analysis Result from localStorage:", analysisResult); // Debugging

    if (analysisResult) {
        const { condition, analysis, imageBase64 } = analysisResult;

        const resultHTML = `
            <h2>Condition: ${condition}</h2>
            <p>Analysis: ${analysis}</p>
            <img src="${imageBase64}" alt="Analyzed Image">
        `;
        resultContainer.innerHTML = resultHTML;
    } else {
        resultContainer.innerHTML = `<p>No analysis result found.</p>`;
    }
}