const searchInput = document.getElementById("searchInput");
const searchButton = document.getElementById("searchButton");
const searchResults = document.getElementById("searchResults");
const symptomsContainer = document.getElementById("symptomsContainer");
const addSymptoms = document.getElementById("addSymptoms");
const addSymptomButton = document.getElementById("addSymptomButton");
const symptomsDiv = document.getElementById("add-symptoms")

searchButton.addEventListener("click", async function () {
  symptomsDiv.style.visibility = "visible"
  const searchTerm = searchInput.value.toLowerCase();

  const requestBody = {
    query: searchTerm
  };
  
  const response = await fetch('http://localhost:8080/process-query', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(requestBody)
  });
  
  const data = await response.json();
  searchResults.style.display = "none";
  symptomsContainer.innerHTML = "";

  addSymptomButton.addEventListener("click", async () => {
    if(addSymptoms.value != "") {
      drawPill(addSymptoms.value.toLowerCase(), true)
    }
    addSymptoms.value = ""

  })
  data.symptoms.forEach((symptom) => {
    drawPill(symptom)
  });



});

document
  .getElementById("getPostsButton")
  .addEventListener("click", async () => {
    const selectedSymptoms = document.querySelectorAll(".selected");
    const symptomNames = Array.from(selectedSymptoms).map(
      (symptom) => symptom.textContent
    );

    const requestBody = {
      query: symptomNames
    };
    
    const response = await fetch('http://localhost:8080/search', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(requestBody)
    });
    
    const data = await response.json();
    
    var loader = document.getElementById("loader");
    loader.style.display = "block";
    setTimeout(function () {
      loader.style.display = "none";
      searchResults.style.display = "block";

      searchResults.innerHTML = "";
      data.forEach((post) => {
        const card = document.createElement("div");
        card.classList.add("card");

        // const title = document.createElement("h2");
        // title.textContent = post.post_content[0];
  
        if (post.hasOwnProperty("post_content") && post.post_content[0] != "") {
          const content = document.createElement("p");
          content.textContent = post.post_content[0];
          card.appendChild(content);
        
          if(post.hasOwnProperty("post_url") && post.post_url[0] != "") {
            const url = document.createElement("a");
          url.textContent = "Read more";
          url.href = `https://${post.post_url[0].trim()}`;
          url.target = "_blank";
          card.appendChild(url);
          }
          
        
          if (post.hasOwnProperty("symptoms") && post.symptoms.length > 0) {
            const symptoms = document.createElement("div");
            symptoms.classList.add("symptoms");
            symptoms.innerHTML = "<h3>Symptoms</h3>";
            post.symptoms.forEach((symptom) => {
              const symptomPill = document.createElement("div");
              symptomPill.classList.add("pill");
              symptomPill.textContent = symptom;
              symptoms.appendChild(symptomPill);
            });
            card.appendChild(symptoms);
          }
        
          if (post.hasOwnProperty("diseases") && post.diseases.length > 0) {
            const diseases = document.createElement("div");
            diseases.classList.add("diseases");
            diseases.innerHTML = "<h3>Diseases</h3>";
            post.diseases.forEach((disease) => {
              const diseasePill = document.createElement("div");
              diseasePill.classList.add("pill");
              diseasePill.textContent = disease;
              diseases.appendChild(diseasePill);
            });
            card.appendChild(diseases);
          }
        
          if (post.hasOwnProperty("diagnostic_procedures") && post.diagnostic_procedures.length > 0) {
            const diagnosticProcedures = document.createElement("div");
            diagnosticProcedures.classList.add("diagnostic-procedures");
            diagnosticProcedures.innerHTML = "<h3>Diagnostic Procedures</h3>";
            post.diagnostic_procedures.forEach((procedure) => {
              const procedurePill = document.createElement("div");
              procedurePill.classList.add("pill");
              procedurePill.textContent = procedure;
              diagnosticProcedures.appendChild(procedurePill);
            });
            card.appendChild(diagnosticProcedures);
          }
        
          searchResults.appendChild(card);
        }

      });
    }, 500);
  });

function drawPill(symptom, selected = false) {
  const pill = document.createElement("div");
    pill.classList.add("pill");

    pill.textContent = symptom;

    // Set the width of the pill based on the text content
    const width = pill.textContent.length * 12; // Adjust the multiplier as needed
    pill.style.width = `${width}px`;
    if(selected) {
      pill.classList.toggle("selected");
      document.getElementById("getPostsButton").style.display = "block";
    }

    pill.addEventListener("click", () => {
      // Toggle selection
      pill.classList.toggle("selected");

      // Show the 'Get Posts' button if at least one symptom is selected
      const selectedSymptoms = document.querySelectorAll(".selected");
      const getPostsButton = document.getElementById("getPostsButton");
      getPostsButton.style.display =
        selectedSymptoms.length > 0 ? "block" : "none";
    });
    symptomsContainer.appendChild(pill);
}