Suggetions for future work
==========================

This page is a compilation of suggestions for improvements that we haven't had the time to make.

+++++++++++++++++++++++++++++++++++++++++++++++++++++++
Generalizing how to find binaries/libraries in packages
+++++++++++++++++++++++++++++++++++++++++++++++++++++++

**Motivation**: When a package fails to build because of a missing binary file or library header, it can be very hard to figure out which package should be included as a dependency. 
Our current solution is to map known 'failing signatures' to known packages, and then add the package as a dependency, to observe if adding the package solves the problem.
This way of mapping seems to work, for a large amount of packages, since many of the packages on Bioconda, seems to use the same dependecies. 
But it dosn't scale well, since we have to observe and add new signatures manually. 

**Suggestion**: It would be really helpful to index all files in all Bioconda packages, so that we could search for a specific executable or library header file in all Bioconda packages.
By doing this we could generalize finding binaries/library files by extracting the file name with a regular expression and search for the packages containing this file. 
If more than one result comes up, it would be easy to implement some kind of heuristic for choosing the right package or simply ask the user for help. 
As a part of the priliminary study for this project we downloaded, unpacked and made a primitive index of all files in all packages from Bioconda, so we was able to answer questions like "How many packages on Bioconda have a Makefile in it's project root dir?" or "How many packages have a setup.py file?". This was quite fast and could probably be automated a lot with a good CI setup.
Creating such a search engine for Bioconda would not only benefit this tool, but would also benefit developers trying to create a recipe for their software by hand. 
We therefore suggest that such a tool could be developed as a separate piece of software, which we then could integrate in this tool. 

