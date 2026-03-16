UNAUTHORIZED_RESPONSE = {
    401: {
        "description": "Unauthorized",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Not authenticated"
                }
            }
        },
    }
}

VALIDATION_ERROR_RESPONSE = {
    422: {
        "description": "Validation Error",
        "content": {
            "application/json": {
                "example": {
                    "detail": [
                        {
                            "loc": ["body", "email"],
                            "msg": "Field required",
                            "type": "missing",
                        }
                    ]
                }
            }
        },
    }
}

NOT_FOUND_RESPONSE = {
    404: {
        "description": "Not Found",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Resource not found"
                }
            }
        },
    }
}

BAD_REQUEST_RESPONSE = {
    400: {
        "description": "Bad Request",
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "detail": {"type": "string"}
                    },
                },
                "example": {
                    "detail": "Bad request"
                }
            },
            "text/plain": {
                "schema": {"type": "string"},
                "example": "Invalid HTTP request received."
            }
        },
    }
}

FORBIDDEN_RESPONSE = {
    403: {
        "description": "Forbidden",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Access forbidden"
                }
            }
        },
    }
}
