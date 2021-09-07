# search

A semi-unsupervised search engine which uses user feedback to guide results.

### the algorithm

The engine has three functions: indexing, recommending, and updating. To do this, it consists of the *search autoencoder*, the *text autoencoder*, and the *search-text map*.

To index a given URL:

1. Get the HTML of the page and keep any text.
2. Train the text autoencoder on the text.
3. Split the set of latent points of the text autoencoder into clusters, and save the coordinates of the centre of each cluster.
4. Save the URL and its latent coordinates.

To recommend a list of URLs, given a search:

1. 