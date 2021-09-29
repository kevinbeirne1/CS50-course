# NETWORK - CS50W PROJECT 4
*Create a social network where users can make posts, like posts, follow other users*

- Project have following key deliverables
  - [x] **NEW POST**
  - [x] **ALL POSTS**
  - [x] **PROFILE PAGE**
  - [x] **FOLLOWING**
  - [x] **PAGINATION**
  - [x] **EDIT POST**
  - [x] **'LIKE' & 'UNLIKE'**

##NEW POST
- [x] Signed in user can create text based post
  - [x] Fill text in a text area
  - [x] Click submit button
  - [x] New post feature can be included at the top of every page or as a separate page
    - New post link is top of every page, new post on separate page
##ALL POSTS
- [x] 'All Posts' link in nav bar
  - [x] Shows all posts by all users in chronological order (newest first)
- [x] Each post should include:
  - [x] username of poster
  - [x] post content
  - [x] date & time of post creation
  - [x] number of likes post has
##PROFILE PAGE
- [x] Clicking on a username should load their profile
- [ ] Profile page should include
  - [x] Number of follower the user has
  - [x] Number of people the user follows
  - [x] Display all their posts in reverse chronological order
  - [x] Follow/Unfollow Button
    - [x] Only if user is signed in
##FOLLOWING
- [x] 'Following' link in nav bar
  - [x] Lists all posts by people the user follows
  - [x] Behaves the same as 'All Posts' page just with limited set of posts
  - [x] The page is only available to users that are signed in
##PAGINATION
- [x] On any page, posts are limited to 10
- [x] If >10 a 'Next' button should appear to take to the next page of posts
- [x] If not on 1st page of posts, a 'Previous' button should appear 
- [x] Posts are listed in reverse chronological order
##EDIT POST
- [x] On a users own post is 'Edit' to edit the post
  - [x] On clicking 'Edit', text is replaced by textarea that user can edit the post
  - [x] User should be able to 'Save' the post
    - [x] Can do in JS without having to reload page
  - [x] Ensure that users are unable to edit another persons posts
##LIKE & UNLIKE
- [x] Users can click a button to 'Like' or 'Unlike' a post
  - [x] Use JS to update the DB and the page without reloading the page