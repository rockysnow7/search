# search

A semi-unsupervised search engine which uses user feedback to guide results.

A search engine should return a list of relevant pages for a given search phrase. We can define "relevance" as the distance between the search phrase and the page in a latent space; this way, the task of the engine in a search is to find the *n* pages closest to the search phrase in the latent space.  
A search phrase and a page are very different, so one autoencoder/latent space will not work for both. Instead, it uses an autoencoder for the pages and places the search phrases within this latent space. Initially, all search phrases are placed randomly, but are moved according to subjective user feedback of relevancy. A neural net trained on these coordinates will then predict the coordinates of future search phrases.

### the algorithm

The engine has three functions: indexing, recommending, and updating. To do this, it consists of the *text autoencoder* and the *search predictor*.

To index a given URL:

1. Get the HTML of the page and keep any text.
2. Train the text autoencoder on the text.
3. Pass the text through the text autoencoder.
4. Save the URL and its latent coordinates.

To recommend a list of *n* URLs, given a search phrase:

1. Pass the search phrase through the search predictor to get a set of coordinates.
2. Find the set of *n* URLs with latent coordinates closest to the search phrase coordinates.

To update its model, given a search phrase, a URL, and a score *s* in {-1, 1}:

1. If the search phrase has not been saved before, pass it through the search predictor and save it with the resulting coordinates.
2. Move the search phrase coordinates *s* closer to the URL's coordinates.
3. Retrain the search predictor on the set of saved search phrases and their coordinates.