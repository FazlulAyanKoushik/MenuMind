from app.common.utils.slug import generate_slug


def test_generate_slug_length():
    slug = generate_slug(8)
    assert len(slug) == 8


def test_generate_slug_default():
    slug = generate_slug()
    assert len(slug) == 8
    assert slug.isalnum()


def test_generate_slug_unique():
    slugs = {generate_slug() for _ in range(100)}
    assert len(slugs) == 100
