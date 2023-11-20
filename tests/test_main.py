import pytest 
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation



# Generic add and duplicate tests
def generic_add_test(check_first_entry_present, add_first_entry, check_second_entry_present, add_second_entry):
    assert not check_first_entry_present()
    add_first_entry()
    assert check_first_entry_present()
    assert not check_second_entry_present()
    add_second_entry()
    assert check_second_entry_present()
    
def generic_duplicate_test(db_session, add_entry, add_second_entry):
    add_entry()
    with pytest.raises(IntegrityError) as e:
        add_second_entry()
        db_session.commit()
    assert isinstance(e.value.orig, UniqueViolation)
