from aiohttp import web


class TestQuizView:
    async def test_success(self, cli):
        response = await cli.get('/api/quiz.get', params={'id': 1})
        assert response.status == 200
        response = await response.json()
        assert response['data'] == {
                    "answer": "ватикан",
                    "id": 1,
                    "question": "Какое самое маленькое государство в мире?",
                    "points": 100
        }
