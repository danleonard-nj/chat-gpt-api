from typing import Dict, List

from framework.serialization import Serializable
from quart import Response



class ChatGptResponse(Serializable):
    def __init__(
        self,
        body,
        status_code: int,
        headers: Dict
    ):
        self.body = body
        self.status_code = status_code
        self.headers = headers

    def json(self):
        return self.body


class ChatGptProxyResponse(Serializable):
    @property
    def request_body(self):
        return self.__request_body

    @property
    def response(self):
        return self.__response

    @property
    def duration(self):
        return self.__duration

    def __init__(
        self,
        request_body: Dict,
        response: Response,
        duration: float
    ):
        self.__request_body = request_body
        self.__response = response
        self.__duration = duration

    def to_dict(
        self
    ) -> Dict:
        return {
            'request': {
                'body': self.__request_body,
            },
            'response': {
                'body': self.__response.json(),
                'status_code': self.__response.status_code,
                'headers': dict(self.__response.headers),
            },
            'stats': {
                'duration': f'{self.__duration}s'
            }
        }

    @staticmethod
    def from_dict(data: Dict):
        return ChatGptProxyResponse(
            request_body=data.get('request').get('body'),
            response=ChatGptResponse(
                body=data.get('response').get('body'),
                status_code=data.get('response').get('status_code'),
                headers=data.get('response').get('headers')
            ),
            duration=data.get('stats').get('duration')
        )


class ChatGptHistoryEndpointsResponse(Serializable):
    def __init__(
        self,
        results: List[Dict]
    ):
        self.__results = results

    def __group_results(
        self
    ):
        grouped = dict()
        for result in self.__results:
            if grouped.get(result.endpoint) is None:
                grouped[result.endpoint] = []
            grouped[result.endpoint].append(result)

        return grouped

    def to_dict(self) -> Dict:
        grouped = self.__group_results()

        return {
            'endpoints': list(grouped.keys()),
            'data': grouped
        }
