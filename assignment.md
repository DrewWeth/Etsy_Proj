# Music Library

This is a small command line application which allows the user to manage a library of artists, albums, and tracks.

## Using the Library

Your program should accept this set of commands:

1. Add an artist: `add artist <artist>`
2. Add an album: `add album <album> by <artist>`
3. Add a track: `add track <track> on <album> by <artist>`
4. Show albums by artist: `list albums by <artist>`
5. Show tracks by album: `list tracks on <album> by <artist>`
6. Listen to a track (increase its play count): `listen to <track> on <album> by <artist>`
7. List the N most popular tracks by play count: `list top <N> tracks`
8. List the N most popular artists by play count: `list top <N> artists`
9. Quit: `quit`

A file with sample input, `sample_in.txt`, is attached for your convenience.

### Guidelines
* You can use whatever language you like.
* Do not use a database to store the library. Store it in memory.
* You can use any external libraries you want as long as they don't directly implement the solution.
* Even though this application is simple, we're looking for a demonstration of the organization, readability, and correctness. Treat this as if it were "production-ready code".
* That said, don't go off the deep end. This is just a homework assignment. You should be able to finish it in an evening. Please don't work on it more than two evenings -- your time is more valuable than that.
* Reach out if you have any questions.

## Submitting your homework

You can submit your homework by emailing us a zip file with your solution. As part of your submission, please include a README file with instructions on how to run your program. We'd also like you to answer a few questions to help us understand your submission. You can include your responses to these in your README.


### Questions
1. How have you gained confidence in your code?
2. One of the things we'll be evaluating is how your code is organized. Why did you choose the structure that you did? What principles were important to you as you organized this code?
3. What are the performance characteristics of your implementation? Does it perform some operations faster than others? Explain any tradeoffs you made in architecting your solution.
