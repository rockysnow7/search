use std::fs;
use pyo3::{prelude::*, types::PyModule};


pub fn encode_tokens(/*tokens: &Vec<Vec<f32>>*/) /*-> Vec<f32>*/ -> PyResult<()> {
    Python::with_gil(|py| {
        let py_code = fs::read_to_string("index_url/models.py").unwrap();
        let py_models_funcs = PyModule::from_code(
            py,
            &py_code,
            "models.py",
            "models",
        )?;
        let test: u32 = py_models_funcs.getattr("collatz")?.call1((3,))?.extract()?;
        println!("collatz(3) = {:?}", test);

        Ok(())
    })
}
