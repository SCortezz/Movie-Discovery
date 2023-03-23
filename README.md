# project1-samir-cortez
A simple "Movie Discovery" web application that provides information about my favorite movies, as well as links to Wikipedia pages for each one.

#### What are at least 2 technical issues I encountered with my project? 
1. One technical issue that I encountered was when I was printing out unwanted information for my genre of the movie. I didn't realize until later that I was working with an array of objects and I had to take a different approach.

2. It wasn't really a technical issue, but I had difficulty getting the Wikipedia link for the movie using the Wiki API.

3. In addition, I encountered a technical problem when trying to deploy my app on fly.io. This occurred because the Python file couldn't be found when the app was deployed.

#### How did I fix them?
1. I when to google and search for ways that I could approach my problem and found some solutions that allowed me to print out the information that I only need it.

2. As a solution to my issue, I searched the internet for a solution, asked classmates for assistance, and took advantage of youtube videos, google docs, and office hours provided by my professor.

3. To find a solution, I went to fly.io's troubleshoot page, but with the help of some of my classmates, I was able to fix the issue.

#### Things needed to clone the repository and set up to run project locally:

⋅⋅*A git clone of this repository: [git@github.com:SCortezz/project1-samir-cortez.git]
⋅⋅*A TMDB API KEY from the TMDB's website thru: https://developers.themoviedb.org/3/getting-started/introduction
⋅⋅*A new .env file with the TMDB API KEY set to TMDB_API_KEY. (Ex. TMDB_API_KEY = ######)

FRAMEWORKS AND LIBRARIES NEEDED TO RUN APP, MAKE SURE TO HAVE THESE INSTALLED!
1. flask
2. requests
3. random
4. json
5. os

URL to the deployed app:
[https://moviediscovery.fly.dev/]
