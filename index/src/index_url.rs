use isahc::prelude::*;
use regex::Regex;

mod models;


const MAX_TOKEN_LEN: usize = 100;
const MAX_CHAR: char = '\u{3ff}';


fn html_to_float_tokens(html: &str) -> Vec<Vec<f32>> {
    // html -> just text -> Vec<token> -> Vec<valid token> -> Vec<Vec<float>>
    let text = Regex::new(r"<[^<>]+>").unwrap()
        .split(&html)
        .into_iter()
        .collect::<Vec<&str>>()
        .join("");

    let tokens = Regex::new(r"([\n\t]|[ -/]|[:-@]|[\[-`]|[{-~])+").unwrap()  // whitespace + punctuation (ASCII)
        .split(&text)
        .into_iter()
        .collect::<Vec<&str>>();
    let tokens_filtered = tokens.iter()
        .filter(|tok| 0 < tok.len() && tok.len() <= MAX_TOKEN_LEN)
        .filter(|tok| !tok.to_string().chars().map(|c| c <= MAX_CHAR)
                .collect::<Vec<bool>>()
                .contains(&false))
        .map(|tok| format!("{}{}", tok, "\0".repeat(MAX_TOKEN_LEN - tok.len())))
        .map(|tok| tok.chars().map(|c| (c as u32 as f32) / (MAX_CHAR as u32 as f32)).collect::<Vec<f32>>())
        .collect::<Vec<Vec<f32>>>();

    tokens_filtered
}

pub fn index_url(url: &str) -> Result<(), isahc::Error> {
    // url -> html -> Vec<Vec<float>> -> better Vec<float>
    /*let html = isahc::get(url)?.text()?;
    let tokens = html_to_float_tokens(&html);*/
    let tokens_floats = models::encode_tokens(/*&tokens*/);

    /*println!("{:?}", &tokens[1000..1200]);*/

    Ok(())
}
