import pytest
from prof_api.api import api, app
from prof_api.filters import find_name

@pytest.fixture(autouse=True)
def before_test():
    app.config['DATABASE_NAME'] = '../db.sqlite'

def test_correct_names():
    prof1 = 'Harker-Harry'
    assert find_name(prof1) == 'Harker, Harry'
    prof2 = 'MacLean-Mark-Thomson'
    assert find_name(prof2) == 'MacLean, Mark Thomson'
    prof3 = 'Staub-French-Sheryl'
    assert find_name(prof3) == 'Staub-French, Sheryl'
    prof4 = 'Son-Jai-Yeol'
    assert find_name(prof4) == 'Son, Jai-Yeol'
    prof5 = '*Fischer-Credo-Cornelius'
    assert find_name(prof5) == '*Fischer-Credo, Cornelius'
    prof6 = 'O\'Flynn-Magee-Katherine'
    assert find_name(prof6) == 'O\'Flynn-Magee, Katherine'
    prof7 = 'SUN-XIA0NON'
    assert find_name(prof7) == 'SUN, XIA0NON'
