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
    // document.querySelector("#edit").addEventListener('click', create_text_area)
    $('#edit').click(function (){

        let post = $(this).closest("#post_media")

        let edit_button = $(this)
        let save_button = post.find("#save")
        let textarea = post.find("#content_textarea")
        let content = post.find("#content")

        content.hide()
        edit_button.hide()
        textarea.show()
        save_button.show()
    });

    $('#save').click(function (){
        let post = $(this).closest("#post_media")

        let save_button = $(this)
        let edit_button = post.find("#edit")
        let textarea = post.find("#content_textarea")
        let content = post.find("#content")
        // let post_id = 1

        textarea.text(textarea.val())
        content.text(textarea.text())

        update_post_in_db(post)

        content.show()
        edit_button.show()
        textarea.hide()
        save_button.hide()
    });
};

function update_post_in_db(post) {
    console.log('running fetch_edit_post')

    let post_id = post.find('#post_id').val()
    let post_content = post.find('#content').text()

    fetch( "/edit_post", {
        method: "PUT",
        headers: new Headers({
            "X-CSRFToken": csrftoken
        }),
        mode: "same-origin",
        body: JSON.stringify({
            'post_id': post_id,
            'content': post_content,
        })
    })
}