"""Recipe tests."""
from pathlib import Path
import pytest
import yaml

from tests.integration.test_recipes_loading import RECIPES, IDS
import esmvaltool

REFERENCES_PATH = Path(esmvaltool.__file__).absolute().parent / 'references'


@pytest.mark.parametrize('recipe_file', RECIPES, ids=IDS)
def test_reference_tags(recipe_file):
    """Check bibtex file is added to REFERENCES_PATH."""
    recipe = yaml.safe_load(recipe_file.read_text())
    tags = recipe.get('documentation', {}).get('references', [])
    for tag in tags:
        bibtex_file = REFERENCES_PATH / f'{tag}.bibtex'
        error_msg = 'The tag {} is mentioned in the recipe {}.' \
                    ' Howevere, its reference file {}.bibtex' \
                    ' is not available in {}.' \
                    ' Please check instructions about' \
                    ' "Contributing a new diagnostic or recipe"' \
                    ' in https://esmvaltool.readthedocs.io/en/latest/' \
                    ''.format(tag, recipe_file, tag, REFERENCES_PATH)
        assert bibtex_file.is_file(), error_msg
