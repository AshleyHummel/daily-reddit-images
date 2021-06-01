# Changelog

## [2.1] - 2021-05-31
* Gifs are saved to workspace folder but no longer displayed in email (to reduce message size)
* Gifs and gifv's are now differentiated and saved properly

## [2.0] - 2021-05-31
* Sends email to user (same as previous versions) and displays images of the top 5 "hot" posts + links to the images
* Sends and saves gifs properly
  * When a gif is found, only 1 is saved/sent to reduce size of email
  * User is alerted in email of a gif being found
* Email informs user of the file path to find saved images

## [1.2] - 2021-05-30
* Sends email to user (same as previous versions)
* Saves top 5 "hot" subreddit images to workspace folder using unique file names

## [1.1] - 2021-05-28
* Sends email to user stating user-chosen subreddit and titles of the top 5 "hot" posts + the redditor who posted them

## [1.0] - 2021-05-24
* Initial release of project
* Sends basic email to user and prints titles of the top 5 "hot" posts from a subreddit in the console
