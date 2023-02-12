Author: Andrea Kučerová
Purpose: exercise for a job interview

DATA:
I used the csv format of the data from http://www2.informatik.uni-freiburg.de/~cziegler/BX/
The whole unziped file needs to be placed in the same directory as the DataSentics_exercise.py. If need be, you can change the corresponding addresses in the top of DataSentics_exercise.py.

I found out that there are some mismatches in the ISBN of the books in BX-Books and BX-Book-Ratings. They lead to occasional blank spaces in the output (because the program cannot find in BX-Books the corresponding name to the ISBN from a review in BX-Book-Ratings). This is for example the case of Memoirs of a Geisha and the problem appears when I try to find recommendatios based on the book The Pillars of the Earth in the original main branch.

In the branch feature I fixed the problem of searching specific ISBN instead of title itself.
In the branch clearthebug I fixed a bug with sorting the books into suggestions_titles.

STRUCTURE:
I described the structure of the code in the comments. The basic idea was to find people that also liked the given book and then compare books these people also rated highly. Result is a list of 10 suggestions.

I decided to restrict to this idea for the first draft of the solution. Some other ideas came to mind that could be used as a criteria or a secundary criteria, such as:
- books from the same author
- books published around the same time
- same publisher
- similar cover -> image recognition
- liked by people from the same area as the ones that liked the given book

One issue that I found was that in this basic setting I might get several candidates for a book suggestion on the same level, it might be solved by adding a second criteria and sort these books according to their average rating. I didn't implement this upgread. Also if there is no user that rated the given book 6 or higher, the program will not offer any suggestions (e.g. for The Middle Stories).