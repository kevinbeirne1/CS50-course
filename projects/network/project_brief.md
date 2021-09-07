# NETWORK - CS50W PROJECT 4
*Create a social network where users can make posts, like posts, follow other users*

- Project have following key deliverables
  - [x] **NEW POST**
  - [ ] **ALL POSTS**
  - [ ] **PROFILE PAGE**
  - [ ] **FOLLOWING**
  - [ ] **PAGINATION**
  - [ ] **EDIT POST**
  - [ ] **'LIKE' & 'UNLIKE'**

##NEW POST
- [x] Signed in user can create text based post
  - [x] Fill text in a text area
  - [x] Click submit button
  - [x] New post feature can be included at the top of every page or as a separate page
    - New post link is top of every page, new post on separate page
##ALL POSTS
- [x] 'All Posts' link in nav bar
  - [ ]Shows all posts by all users in chronological order (newest first)
- [ ]Each post should include:
  - [x] username of poster
  - [x] post content
  - [x] date & time of post creation
  - [ ] number of likes post has
##PROFILE PAGE
- [ ] Clicking on a username should load their profile
- [ ] Profile page should include
  - [ ] Number of follower the user has
  - [ ] Number of people the user follows
  - [ ] Display all their posts in reverse chronological order
  - [ ] Follow/Unfollow Button
    - [ ] Only if user is signed in
    - [ ] User can't follow/unfollow themselves
##FOLLOWING
- [ ] 'Following' link in nav bar
  - [ ] Lists all posts by people the user follows
  - [ ] Behaves the same as 'All Posts' page just with limited set of posts
  - [ ] The page is only available to users that are signed in
##PAGINATION
- [ ] On any page, posts are limited to 10
- [ ] If >10 a 'Next' button should appear to take to the next page of posts
- [ ] If not on 1st page of posts, a 'Previous' button should appear 
##EDIT POST
- [ ] On a users own post is 'Edit' to edit the post
  - [ ] On clicking 'Edit', text is replaced by textarea that user can edit the post
  - [ ] User should be able to 'Save' the post
    - [ ] Can do in JS without having to reload page
  - [ ] Ensure that users are unable to edit another persons posts
##LIKE & UNLIKE
- [ ] Users can click a button to 'Like' or 'Unlike' a post
  - [ ] Use JS to update the DB and the page without reloading the page