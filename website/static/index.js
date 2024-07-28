window.onscroll = function () {toggleStickyNavbar()};

function toggleStickyNavbar() {
    var navbar = document.getElementById("navbar");
    var banner = document.querySelector(".banner");
    var sticky = banner.offsetHeight;

    if (window.pageYOffset > sticky - navbar.offsetHeight) {
        navbar.classList.add("sticky");
    } else {
        navbar.classList.remove("sticky");
    }
}

function like(postId) {
    const likeCount = document.getElementById(`likes-count-${postId}`);
    const likeButton = document.getElementById(`like-button-${postId}`);

    fetch(`/like-post/${postId}`, { method: "POST" })
        .then((res) => res.json())
        .then((data) => {
            likeCount.innerHTML = data["likes"];
            if (data["liked"] === true) {
                likeButton.className = "fas fa-thumbs-up";
            } else {
                likeButton.className = "far fa-thumbs-up";
            }
        })
        .catch((e) => alert("Could not like post."));
}
