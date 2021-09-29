window.Network = {}
window.Network.initialize = function () {

    $('.post_media').each(function (){

        let like_button = $(this).find('#like')
        let unlike_button = $(this).find('#unlike')
        let edit_button = $(this).find('#edit')
        let save_button = $(this).find('#save')

        let user_likes_post = $(this).find('#user_likes_post')

        if (user_likes_post.val() === 'true') {
            like_button.hide()
            unlike_button.show()

        }
        else {
            like_button.show()
            unlike_button.hide()
        }

        edit_button.on('click',edit_button_click)
        save_button.on('click', save_button_click)
        like_button.on('click', like_button_click)
        unlike_button.on('click', unlike_button_click)
    });

    let follow_button = $('#follow')
    let unfollow_button = $('#unfollow')
    let user_follows_profile = $('#user_follows_profile')

    if (user_follows_profile.val() === 'true'){
        follow_button.hide()
        unfollow_button.show()
    }
    else {
        follow_button.show()
        unfollow_button.hide()
    }

    follow_button.on('click', follow_button_click)
    unfollow_button.on('click', unfollow_button_click)

};


function follow_button_click () {
    let followers_count = $('#followers_count')
    let followers_count_value = followers_count.text();
    let user_follows_profile = $('#user_follows_profile')

    followers_count_value ++;
    followers_count.text(followers_count_value)

    user_follows_profile.val('true')
    add_profile_follower_in_db()

    $('#follow').hide()
    $('#unfollow').show()

}

function add_profile_follower_in_db() {
    let profile_name = $("#profile_name").text()

    fetch(`/follow/${profile_name}`, {
        method: "PUT",
        headers: new Headers({
            "X-CSRFToken": csrftoken
        }),
        mode: "same-origin"
    });
}


function unfollow_button_click() {
    let followers_count = $('#followers_count')
    let followers_count_value = followers_count.text();
    let user_follows_profile = $('#user_follows_profile')

    followers_count_value --;
    followers_count.text(followers_count_value)

    user_follows_profile.val('false')
    remove_profile_follower_in_db()

    $('#follow').show()
    $('#unfollow').hide()
}

function remove_profile_follower_in_db() {
    let profile_name = $("#profile_name").text()

    fetch(`/unfollow/${profile_name}`, {
        method: "PUT",
        headers: new Headers({
            "X-CSRFToken": csrftoken
        }),
        mode: "same-origin"
    });
}


function edit_button_click() {
    console.log('running edit button click')
        let post = $(this).closest(".post_media");

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
        let post = $(this).closest(".post_media");

        let save_button = $(this);
        let edit_button = post.find("#edit");
        let textarea = post.find("#content_textarea");
        let content = post.find("#content");

        textarea.text(textarea.val());
        content.text(textarea.text());

        update_post_content_in_db(post);

        content.show();
        edit_button.show();
        textarea.hide();
        save_button.hide();
}


function update_post_content_in_db(post) {
    // console.log('running update_post_content_in_db');

    let post_id = post.attr('data-post-id')
    let post_content = post.find('#content').text();

    fetch( `/edit_post/${post_id}`, {
        method: "PUT",
        headers: new Headers({
            "X-CSRFToken": csrftoken
        }),
        mode: "same-origin",
        body: JSON.stringify({
            'content': post_content,
        }),
    });
}


function like_button_click() {
    // console.log('running like_button_click')
    let post = $(this).closest(".post_media");

    let likes_count = post.find('#likes_count');
    let like_button = post.find('#like');
    let unlike_button = post.find('#unlike');

    let likes_count_value = likes_count.text();
    likes_count_value ++;
    likes_count.text(likes_count_value);

    update_post_likes_in_db(post)

    post.find('#user_likes_post').val('true')

    unlike_button.show();
    like_button.hide();
}

function unlike_button_click() {
    // console.log('running unlike_button_click');
    let post = $(this).closest(".post_media");

    let likes_count = post.find('#likes_count');
    let like_button = post.find('#like');
    let unlike_button = post.find('#unlike');

    let likes_count_value = likes_count.text();
    likes_count_value --;
    likes_count.text(likes_count_value);

    update_post_unlikes_in_db(post)
    post.find('#user_likes_post').val('false');

    unlike_button.hide();
    like_button.show();
}

function update_post_unlikes_in_db(post){
    // console.log('running update_post_unlikes_in_db')
    let post_id = post.attr('data-post-id')

    fetch(`/unlike_post/${post_id}`, {
        method: "PUT",
        headers: new Headers({
            "X-CSRFToken": csrftoken
        }),
        mode: "same-origin"
    });

}


function update_post_likes_in_db(post){
    // console.log('running update_post_likes_in_db')
    let post_id = post.attr('data-post-id')

    fetch(`/like_post/${post_id}`, {
        method: "PUT",
        headers: new Headers({
            "X-CSRFToken": csrftoken
        }),
        mode: "same-origin"
    });

}

