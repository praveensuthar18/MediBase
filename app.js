const searchInput = document.getElementById("searchInput");
const searchButton = document.getElementById("searchButton");
const searchResults = document.getElementById("searchResults");

searchButton.addEventListener("click", async function () {
  const searchTerm = searchInput.value.toLowerCase();
  //   const response = await fetch(`/search?term=${searchTerm}`);
  //   const data = await response.json();
  searchResults.style.display = "none";

  const symptomsContainer = document.getElementById("symptomsContainer");
  symptomsContainer.innerHTML = "";

  data = {
    symptoms: ["cough", "headache", "pain"],
  };

  data.symptoms.forEach((symptom) => {
    const pill = document.createElement("div");
    pill.classList.add("pill");

    pill.textContent = symptom;

    // Set the width of the pill based on the text content
    const width = pill.textContent.length * 12; // Adjust the multiplier as needed
    pill.style.width = `${width}px`;

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
  });
});

document
  .getElementById("getPostsButton")
  .addEventListener("click", async () => {
    const selectedSymptoms = document.querySelectorAll(".selected");
    const symptomNames = Array.from(selectedSymptoms).map(
      (symptom) => symptom.textContent
    );

    // // Send a request to get posts containing selected symptoms
    // const response = await fetch(
    //   `your_api_url/posts?symptoms=${JSON.stringify(symptomNames)}`
    // );
    // const data = await response.json();

    var loader = document.getElementById("loader");
    loader.style.display = "block";
    setTimeout(function () {
      loader.style.display = "none";
      searchResults.style.display = "block";

      let data = [
        {
          title: ["Test 3"],
          url: [
            "www.medhelp.org/posts/Gallbladder/Sphincter-of-oddi-dysfunction-is-ruling-my-life-please-hel/show/142363",
          ],
          content: ["test"],
          comments: ["comment 1"],
          symptoms: [
            "Stomach ache",
            "Abdominal Pain",
            "Pain",
            "Vomiting",
            "Nausea",
            "back pain mid back",
          ],
          diagnostic_procedures: [
            "Laser-Induced Fluorescence Endoscopy",
            "Radionuclide Imaging",
            "Cholangiopancreatography, Magnetic Resonance",
            "Scanning",
            "Ultrasonography",
            "Endoscopic Retrograde Cholangiopancreatography",
          ],

          diseases: [
            "FANCONI ANEMIA, COMPLEMENTATION GROUP E",
            "Abetalipoproteinemia",
            "Endometriosis",
            "Brachial Amyotrophic Diplegia",
            "Liver diseases",
            "Stomach Diseases",
          ],
        },
      ];

      searchResults.innerHTML = "";
      data.forEach((post) => {
        const card = document.createElement("div");
        card.classList.add("card");

        const title = document.createElement("h2");
        title.textContent = post.title[0];

        const content = document.createElement("p");
        content.textContent = post.content[0];

        const url = document.createElement("a");
        url.textContent = "Read more";
        url.href = post.url[0];
        url.target = "_blank";

        const comments = document.createElement("div");
        comments.classList.add("comments");
        comments.innerHTML = "<h3>Comments</h3>";
        post.comments.forEach((comment) => {
          const commentText = document.createElement("p");
          commentText.textContent = comment;
          comments.appendChild(commentText);
        });

        card.appendChild(title);
        card.appendChild(content);
        card.appendChild(url);
        card.appendChild(comments);

        searchResults.appendChild(card);
      });
    }, 500);
  });
