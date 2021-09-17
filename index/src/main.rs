mod index_url;


fn main() {
    index_url::index_url("https://en.wikipedia.org/wiki/Mathematics").unwrap();
}
