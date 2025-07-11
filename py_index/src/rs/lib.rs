mod index;

use pyo3::prelude::*;
use index::Index;
use index::Indexable;
use index::PyQueryExpr;

/// Formats the sum of two numbers as string.
#[pyfunction]
fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
    Ok((a + b).to_string())
}

/// A Python module implemented in Rust.
#[pymodule]
fn py_index(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;
    m.add_class::<Index>()?;
    m.add_class::<Indexable>()?;
    m.add_class::<PyQueryExpr>()?;
    Ok(())
}
