import unittest
from unittest.mock import Mock

from backend.main import create_app


class CreateAppTests(unittest.IsolatedAsyncioTestCase):
    async def test_resources_are_owned_by_the_application_lifespan(self) -> None:
        resources = Mock()
        resource_factory = Mock(return_value=resources)

        app = create_app(resource_factory=resource_factory)

        resource_factory.assert_not_called()
        self.assertFalse(hasattr(app.state, "resources"))

        async with app.router.lifespan_context(app):
            resource_factory.assert_called_once_with()
            self.assertIs(app.state.resources, resources)
            resources.close.assert_not_called()

        resources.close.assert_called_once_with()
        self.assertFalse(hasattr(app.state, "resources"))


if __name__ == "__main__":
    unittest.main()
