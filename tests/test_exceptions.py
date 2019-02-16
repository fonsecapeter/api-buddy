from unittest import TestCase
from pytest import raises
from api_buddy.exceptions import APIBuddyException, exit_with_exception

TEST_ERR_TITLE = 'test'
TEST_ERR_MESSAGE = 'exception'


class TestExitWithException(TestCase):
    def test_exits_with_err_code_1(self):
        err = APIBuddyException(
            title=TEST_ERR_TITLE,
            message=TEST_ERR_MESSAGE,
        )
        with raises(SystemExit) as wrapped_exit:
            exit_with_exception(err)
        assert wrapped_exit.type == SystemExit
        assert wrapped_exit.value.code == 1
