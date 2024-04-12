const searchInput = document.getElementById("searchInput");
const searchButton = document.getElementById("searchButton");
const searchResults = document.getElementById("searchResults");

searchButton.addEventListener("click", async function () {
  const searchTerm = searchInput.value.toLowerCase();
  //   const response = await fetch(`/search?term=${searchTerm}`);
  //   const data = await response.json();

  let data = [
    {
      post_title: "Test 3",
      post_url: "https...",
      post_content: "test",
    },
  ];

  searchResults.innerHTML = "";
  data.forEach((post) => {
    const postElement = document.createElement("div");
    postElement.textContent = post.post_title;
    searchResults.appendChild(postElement);
  });
});
