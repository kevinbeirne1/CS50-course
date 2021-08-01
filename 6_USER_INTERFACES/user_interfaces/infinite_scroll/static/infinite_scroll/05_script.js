// Start with first post
let counter = 1;
console.log(`first counter ${counter}`)

// Load posts at 20 a time
const quantity = 20;

// When DOM loads, render the first 20 posts
document.addEventListener("DOMContentLoaded", load);

// If scrolled to the bottom, load the next 20 posts
window.onscroll = () => {
    if (window.innerHeight + window.scrollY >= document.body.offsetHeight) {
        load();
    }
};

// Load next set of posts
function load() {

    // Set start and end post numbers, and update counter
    const start = counter;
    const end = start + quantity - 1;
    counter = end + 1;
    console.log(`counter ${counter}`)

    // Get new posts and add posts
    fetch(`/posts?start=${start}&end=${end}`)
        .then(response => response.json())
        .then(data => {
            data.posts.forEach(add_post);
        })
};

function add_post(contents){

    // Create new post
    const post = document.createElement('div');
    post.className = 'post';
    post.innerHTML = `${contents} <button class="hide">Hide</button>`;

    // Add post to DOM
    document.querySelector('#posts').append(post);
};

// if hide button is clicked, delete the post
document.addEventListener('click', event => {
    // Find what was clicked on
    const element = event.target;

    // Check if the user clicked on a hide button
    if (element.className === 'hide') {
        element.parentElement.style.animationPlayState = 'running';
        element.parentElement.addEventList
        // element.parentElement.remove()
    }
});