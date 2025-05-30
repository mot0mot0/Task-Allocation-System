from pydantic import BaseModel


class ResponseTemplate:
    def __init__(self, contents):
        self.contents = contents

    def create_response(self):
        return {
            content["code"]: {
                "content": {"application/json": {"examples": content["examples"]}}
            }
            for content in self.contents
        }
