"""SQL helper to generate EAV pivot expressions."""


def build_pivot_expressions(stat_columns: list[str]) -> str:
    """Generate MAX(CASE WHEN ...) expressions for EAV → columnar pivot.

    Returns a comma-separated string of SQL expressions like:
        MAX(CASE WHEN st.stat_name = 'core_goals' THEN s.value END) AS core_goals,
        MAX(CASE WHEN st.stat_name = 'boost_bpm' THEN s.value END) AS boost_bpm
    """
    lines = []
    for col in stat_columns:
        lines.append(
            f"MAX(CASE WHEN st.stat_name = '{col}' THEN s.value END) AS {col}"
        )
    return ",\n    ".join(lines)
