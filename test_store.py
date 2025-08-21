from jsonschema import validate
import pytest
import schemas
import api_helpers
from hamcrest import assert_that, contains_string, is_

'''
TODO: Finish this test by...
1) Creating a function to test the PATCH request /store/order/{order_id}
2) *Optional* Consider using @pytest.fixture to create unique test data for each run
2) *Optional* Consider creating an 'Order' model in schemas.py and validating it in the test
3) Validate the response codes and values
4) Validate the response message "Order and pet status updated successfully"
'''
@pytest.mark.parametrize("id", [0, 1, 2])
def test_patch_order_by_id(id):
    # Test for placing a new order
    params = {
        "pet_id": id
    }
    post_response = api_helpers.post_api_data("/store/order", params)
    assert post_response.status_code == 201, f"Failed to create order: {post_response.text}"
    order = post_response.json()
    order_id = order["id"]

    # 1) Test for updating the order
    patch_data = {"status": "sold"}
    patch_response = api_helpers.patch_api_data(f"/store/order/{order_id}", patch_data)

    # 3) Validating the response codes and values
    assert patch_response.status_code == 200, f"Unexpected status {patch_response.status_code}: {patch_response.text}"

    # 4) Validating the response message
    result = patch_response.json()
    assert result["message"] == "Order and pet status updated successfully"
