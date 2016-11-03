Drew Wetherington
Interview project submission

1. How have you gained confidence in your code?
I gained confidence in the code by using semi-automated testing. While developing this project I did incremental unit and integration tests by incrementally adding commands to the commented-out run_test() function on line 143 of the source/main.py file. The run_test() function simulated a user's input. I would give it correct input, incorrect input, null values, out-of-order commands, and mismatching data to ensure the pathway passed or failed gracefully.

2. One of the things we'll be evaluating is how your code is organized. Why did you choose the structure that you did? What principles were important to you as you organized this code?
The code is organized into a crude model view controller architecture. The main.py script acts as view by extracting data from the user. With the help of functions meant to abstract away handling raw user data, in the extractor.py file sanitizes and gather input from the user.

The data from the user is then passed to an instance of a manager. This is done with a static class variable so different functions have access to the controller without passing around a single instance. The manager accesses and alters the data structures with specific endpoints like 'add_artist' and 'list_tracks'

Finally, models like an artist.py, album.py, and track.py all hold pointers to their related objects.

3. What are the performance characteristics of your implementation? Does it perform some operations faster than others? Explain any tradeoffs you made in architecting your solution.
The main feature of my implementation is that there is very low overhead memory consumption aside from keeping all objects in memory. Artists are stored as as key-value stores from an artists name to an artist object. So an artist lookup happens in O(1) time. From there finding an album or a track happen in O(1) time complexity because those relations are stored as a dictionary of references to the objects that exist in an an array of albums and tracks.

At first I decided to have an array of artists, sorted by name, instead of a map. It would have allowed for O(log(n)) look up time but worst case O(n(log(n))) if sorting needed to happen before searched. I realizing that a user mainly looks up users instead of sequentially listing them, so a map was more appropriate. It also allowed for O(1) lookup time for tracks which exist in the context of an artist and album.

Lastly, I wanted to note why regex was not used. I didn't use regex because data could either be a single word or contains in double quotes. Although, doing regex with keyword such as "by" and "on" could easily give you your data, I thought it was easier to give the user custom feedback such as "please include the artist name after 'by'" by sequentially deconstructing the arguments to simulate a user constructing the arguments.
