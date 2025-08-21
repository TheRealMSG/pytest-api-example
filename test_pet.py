from jsonschema import validate
import pytest
import schemas
import api_helpers
from hamcrest import assert_that, contains_string, is_

'''
TODO: Finish this test by...
1) Troubleshooting and fixing the test failure
The purpose of this test is to validate the response matches the expected schema defined in schemas.py
'''
def test_pet_schema():
    test_endpoint = "/pets/1"

    response = api_helpers.get_api_data(test_endpoint)

    assert response.status_code == 200

    # Validate the response schema against the defined schema in schemas.py
    validate(instance=response.json(), schema=schemas.pet)

'''
TODO: Finish this test by...
1) Extending the parameterization to include all available statuses
2) Validate the appropriate response code
3) Validate the 'status' property in the response is equal to the expected status
4) Validate the schema for each object in the response
'''
#1) Included all available pet statuses in the parametrize iterable for pytest to run tests on
@pytest.mark.parametrize("status", [("available"), ("sold"), ("pending")])
def test_find_by_status_200(status):
    test_endpoint = "/pets/findByStatus"
    params = {
        "status": status
    }

    response = api_helpers.get_api_data(test_endpoint, params)
    # TODO...
    #2) assert statement to ensure HTTP request was fulfilled succesfully (Status Code 200)
    assert response.status_code == 200
    #3) Validating that the expected and response pet status are equivalent
    #by comparing this function's passed in status parameter (expected status)
    #to response status(es) for each returned pet
    petData = response.json()
    for pet in petData:
        assert pet["status"] == status
    #4) Validating the schema for each object in the response
        validate(instance=pet, schema=schemas.pet)
'''
TODO: Finish this test by...
1) Testing and validating the appropriate 404 response for /pets/{pet_id}
2) Parameterizing the test for any edge cases
'''
# after looking at the new pet creation functionality in app.py, it seems that
# a new pet can be created with any ID so long as that ID is an integer and is
# not already in use by another already created pet. This means that the only
# way a 404 error would occur is if a pet is requested by an ID that is not in
# use by an existing pet, or if a pet is requested by an ID that is not an int
@pytest.mark.parametrize("id", [0, 1, 2, 3, -1, "one", None])
def test_get_by_id_404(id):
    # TODO...
    test_endpoint = f"/pets/{id}"
    params = {
        "id": id
    }

    response = api_helpers.get_api_data(test_endpoint, params)
    # if the requested pet exists when it shouldn't
    if response.status_code == 200:
        pet = response.json()
        validate(instance=pet, schema=schemas.pet)
        # checking that ID in the response matches the one requested
        assert pet["id"] == id, f"Expected pet_id {id}, got {pet['id']}"
    # if the requested pet doesn't exist
    else:
        assert response.status_code == 404