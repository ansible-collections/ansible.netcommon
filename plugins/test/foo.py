
def foo(value):
    return True


class TestModule(object):
    """ network jinja tests
    """

    test_map = {
        "foo": foo,
    }

    def tests(self):
        return self.test_map 