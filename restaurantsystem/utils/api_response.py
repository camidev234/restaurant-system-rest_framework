class ApiSuccessResponse:
    def __init__(self, status, data, message):
        self.status = status
        self.data = data  
        self.message = message  

    def get_response(self):
        return {
            "status": self.status,
            "message": self.message,
            "data": self.data,
        }


class ApiErrorResponse:
    def __init__(self, status, errors=None, message=None):
        self.status = status
        self.errors = errors
        self.message = message

        self.response = {
            "status": status,
            "message": message
        }

        if errors is not None:
            self.response["errors"] = self.errors

    def get_response(self):
        return self.response