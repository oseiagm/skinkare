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

        console.log(data)
        if (data.error) {
            alert(data.error);
            return;
        }

        // Store result in local storage
        localStorage.setItem("analysisResult", JSON.stringify(data));
        window.location.href = "/results";
    })
    .catch(error => {
        alert("Error: " + error);
    });
}

// Load analysis result on results page
// if (window.location.pathname.includes("results.html")) {
//     const resultContainer = document.getElementById("result-container");
//     const analysisResult = JSON.parse(localStorage.getItem("analysisResult"));
//     if (analysisResult) {
//         const resultHTML = `
//             <h2>Condition: ${analysisResult.condition}</h2>
//             <p>Analysis: ${analysisResult.analysis}</p>
//             <img src="${analysisResult.imageBase64}" alt="Analyzed Image">
//         `;
//         resultContainer.innerHTML = resultHTML;
//     } else {
//         resultContainer.innerHTML = `<p>No analysis result found.</p>`;
//     }
// }

// Load analysis result on results page
if (window.location.pathname.includes("results.html")) {
    const resultContainer = document.getElementById("result-container");
    const analysisResult = JSON.parse(localStorage.getItem("analysisResult"));

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
    
    // if (analysisResult) {
    //     console.log(analysisResult);  // Log this to see what is inside

    //     // Check if analysisResult.condition and analysisResult.analysis are objects
    //     const condition = typeof analysisResult.condition === 'object' ? JSON.stringify(analysisResult.condition) : analysisResult.condition;
    //     const analysis = typeof analysisResult.analysis === 'object' ? JSON.stringify(analysisResult.analysis) : analysisResult.analysis;
        
        
    //     const resultHTML = `
    //         <h2>Condition: ${aResult.condition}</h2>
    //         <p>Analysis: ${aResult.analysis}</p>
    //         <img src="${aResult.analysisResult.imageBase64}" alt="Analyzed Image">
    //     `;
    //     console.log(resultHTML)
    //     resultContainer.innerHTML = resultHTML;
    // } else {
    //     resultContainer.innerHTML = `<p>No analysis result found.</p>`;
    // }
}
