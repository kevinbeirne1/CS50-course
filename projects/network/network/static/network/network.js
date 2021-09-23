// document.addEventListener('DOMContentLoaded', function() {
//     console.log('running network.js')

    // $("#edit").on("click", function() {
    // do something
        // console.log('button click function')
    // });
    // document.querySelector("#edit").addEventListener('click', create_text_area)
    // document.querySelector("#edit").addEventListener('click', () => {
    //     console.log('running edit listener')

// });
window.Network = {}
window.Network.initialize = function () {
    console.log('initialized network.js')

    $('#edit').click(edit_button_click)
    $('#save').click(save_button_click)
    $('#like').click(like_button_click)
    $('#unlike').click(unlike_button_click)

};

function edit_button_click() {
        let post = $(this).closest("#post_media");

        let edit_button = $(this);
        let save_button = post.find("#save");
        let textarea = post.find("#content_textarea");
        let content = post.find("#content");

        content.hide();
        edit_button.hide();
        textarea.show();
        save_button.show();
}

function save_button_click () {
        let post = $(this).closest("#post_media");

        let save_button = $(this);
        let edit_button = post.find("#edit");
        let textarea = post.find("#content_textarea");
        let content = post.find("#content");

        textarea.text(textarea.val());
        content.text(textarea.text());

        update_post_in_db(post);

        content.show();
        edit_button.show();
        textarea.hide();
        save_button.hide();
}

function update_post_in_db(post) {
    console.log('running fetch_edit_post');

    let post_id = post.find('#post_id').val();
    let post_content = post.find('#content').text();

    fetch( "/edit_post", {
        method: "PUT",
        headers: new Headers({
            "X-CSRFToken": csrftoken
        }),
        mode: "same-origin",
        body: JSON.stringify({
            'post_id': post_id,
            'content': post_content,
        }),
    });
}

function like_button_click() {
    console.log('running like_button_click')
    let post = $(this).closest("#post_media");

    let likes_count = post.find('#likes_count');
    let like_button = post.find('#like');
    let unlike_button = post.find('#unlike');

    let likes_count_value = likes_count.text();
    likes_count_value ++;
    likes_count.text(likes_count_value);

    unlike_button.show();
    like_button.hide();
}

function unlike_button_click() {
    console.log('running unlike_button_click');
    let post = $(this).closest("#post_media");

    let likes_count = post.find('#likes_count');
    let like_button = post.find('#like');
    let unlike_button = post.find('#unlike');

    let likes_count_value = likes_count.text();
    likes_count_value --;
    likes_count.text(likes_count_value);

    unlike_button.hide()
    like_button.show()
}