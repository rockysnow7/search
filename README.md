# search

A semi-unsupervised search engine which uses user feedback to guide results.

A search engine should return a list of relevant pages for a given search phrase. We can define "relevance" as the distance between the search phrase and the page in a latent space; this way, the task of the engine in a search is to find the *n* pages closest to the search phrase in the latent space.  
A search phrase and a page are very different, so one autoencoder/latent space will not work for both. Instead, it uses an autoencoder for the pages and places the search phrases within this latent space. Initially, all search phrases are placed randomly, but are moved according to subjective user feedback of relevancy. A neural net trained on these coordinates will then predict the coordinates of future search phrases.

### the algorithm

The engine has three functions: indexing, recommending, and updating. To do this, it consists of the *search autoencoder*, the *text autoencoder*, and the *search-text map*.

To index a given URL:

1. Get the HTML of the page and keep any text.
2. Train the text autoencoder on the text.
3. Split the set of latent points of the text autoencoder into clusters, and save the coordinates of the centre of each cluster.
4. Save the URL and its latent coordinates.

To recommend a list of URLs, given a search:

1. ...

### dev notes

1. Get search phrase.
2. For any URL, get score *s* in {-1, 0, 1}.
3. Move search point *s* units closer to URL point.
4. Train the 
