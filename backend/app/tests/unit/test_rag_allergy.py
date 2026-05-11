from app.modules.ai.rag.pipeline import check_allergy_safety


def test_allergy_safety_no_allergies():
    result = check_allergy_safety("This dish contains chicken and rice.", [])
    assert result is None


def test_allergy_safety_no_trigger():
    result = check_allergy_safety("This dish contains chicken and rice.", ["peanuts"])
    assert result is None


def test_allergy_safety_triggered():
    result = check_allergy_safety("This dish contains peanuts and chicken.", ["peanuts"])
    assert result is not None
    assert "Allergy Warning" in result
    assert "peanuts" in result


def test_allergy_safety_multiple_triggers():
    result = check_allergy_safety(
        "This dish contains gluten, peanuts, and dairy.",
        ["peanuts", "gluten"],
    )
    assert result is not None
    assert "peanuts" in result
    assert "gluten" in result
