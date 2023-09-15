from fastapi.testclient import TestClient


class TestMeta:
    """Tests meta endpoints."""

    async def test_ping(self, server_api: TestClient):
        """
        Tests ping endpoint.
        :param server_api:
        :return:
        """

        # test
        response = server_api.get(url="worker/v1/meta/ping")

        # assert
        assert response.status_code == 200

    async def test_head_ping(self, server_api: TestClient):
        """
        Tests head ping endpoint.
        :param server_api:
        :return:
        """

        # test
        response = server_api.head(url="worker/v1/meta/ping")

        # assert
        assert response.status_code == 200
