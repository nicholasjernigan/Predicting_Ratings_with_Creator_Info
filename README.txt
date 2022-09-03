Predicting Ratings With Creator Info README


This repository displays work Nicholas did for a client that wanted to know
if there was any connection between ethnicity, race, religion, and sexuality of
a director or actor and how many reviews and what kinds of reviews the movie received 
from the public and from professionals.

MOVIE_PROJECT.py uses Oscars-demographics-DFE.csv as its list of movies.
For each movie, it attempts to find the movie in Metacritic to see what reviews
the movie received from critics and from regular people. After collecting this data
the data is regressed to see if there is a significant correlation between the characteristics
of the director and the number of reviews received, and the types of reviews received.

movie_project_charts.py is the code used with the output of MOVIE_PROJECT.py to create the visualizations
seen in the write-up.

Oscars-demographics-DFE.csv is the input data used for this experiment.

results_21.csv is the output of MOVIE_PROJECT.py. It is the Oscars-demographics-DFE.csv with the added information from Metacritic. 

Results Writeup.docx is the writeup I made for the client. The client preferred speed over quality, 
consequently, the write-up was made in less than an hour.
