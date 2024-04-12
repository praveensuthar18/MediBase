const searchInput = document.getElementById("searchInput");
const searchButton = document.getElementById("searchButton");
const searchResults = document.getElementById("searchResults");

searchButton.addEventListener("click", async function () {
  const searchTerm = searchInput.value.toLowerCase();
  //   const response = await fetch(`/search?term=${searchTerm}`);
  //   const data = await response.json();

  let data = [
    {
      title: "Test 3",
      url: "https...",
      content: "test",
      comments: ["comment 1"],
    },
  ];

  searchResults.innerHTML = "";
  data.forEach((post) => {
    const card = document.createElement("div");
    card.classList.add("card");

    const title = document.createElement("h2");
    title.textContent = post.title;

    const content = document.createElement("p");
    content.textContent = post.content;

    const url = document.createElement("a");
    url.textContent = "Read more";
    url.href = post.url;
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
});
