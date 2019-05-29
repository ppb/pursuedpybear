import hypothesis.strategies as st

from ppb import Vector


def vectors(max_magnitude=1e75):
    return st.builds(
        Vector,
        st.floats(min_value=-max_magnitude, max_value=max_magnitude),
        st.floats(min_value=-max_magnitude, max_value=max_magnitude),
    )
