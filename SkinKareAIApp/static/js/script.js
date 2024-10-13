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