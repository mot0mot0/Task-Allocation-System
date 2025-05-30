from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.schemas.requests import UserLogin, UserCreate
from src.schemas.responses import ResponseTemplate
from src.constants import PB, PocketbaseCollections
import aiohttp

router = APIRouter()
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    try:
        async with aiohttp.ClientSession() as client:
            user = await PB.verify_auth(credentials.credentials, client)
            return user
    except Exception as e:
        raise HTTPException(
            status_code=401, detail="Invalid authentication credentials"
        )


@router.post(
    "/init",
    tags=["auth"],
    responses=ResponseTemplate(
        [
            {
                "code": 200,
                "examples": {
                    "Success": {
                        "value": {
                            "token": "auth_token",
                            "user": {
                                "id": "user_id",
                                "email": "admin@example.com",
                                "name": "Admin",
                                "role": "admin",
                            },
                        }
                    }
                },
            }
        ]
    ).create_response(),
)
async def initialize_system():
    try:
        async with aiohttp.ClientSession() as client:
            users = await PB.fetch_records(PocketbaseCollections.USERS, client)
            if users["items"]:
                raise HTTPException(
                    status_code=400, detail="System already initialized with super user"
                )

            admin_data = {
                "email": "admin@example.com",
                "password": "admin123",
                "passwordConfirm": "admin123",
                "name": "Admin",
                "role": "admin",
            }

            result = await PB.create_record(
                PocketbaseCollections.USERS, admin_data, client
            )

            auth_data = {
                "email": admin_data["email"],
                "password": admin_data["password"],
            }

            auth_result = await PB.authenticate(auth_data, client)

            return {
                "token": auth_result["token"],
                "user": {
                    "id": result["id"],
                    "email": result["email"],
                    "name": result["name"],
                    "role": result["role"],
                },
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/register",
    tags=["auth"],
    responses=ResponseTemplate(
        [
            {
                "code": 200,
                "examples": {
                    "Success": {
                        "value": {
                            "token": "auth_token",
                            "user": {
                                "id": "user_id",
                                "email": "user@example.com",
                                "name": "User",
                                "role": "user",
                            },
                        }
                    }
                },
            }
        ]
    ).create_response(),
)
async def register_user(
    user_data: UserCreate, current_user: dict = Depends(get_current_user)
):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Only admins can create new users")

    try:
        async with aiohttp.ClientSession() as client:
            # Создаем пользователя
            result = await PB.create_record(
                PocketbaseCollections.USERS,
                {
                    "email": user_data.email,
                    "password": user_data.password,
                    "passwordConfirm": user_data.password,
                    "name": user_data.name,
                    "role": user_data.role,
                },
                client,
            )

            auth_data = {"email": user_data.email, "password": user_data.password}

            auth_result = await PB.authenticate(auth_data, client)

            return {
                "token": auth_result["token"],
                "user": {
                    "id": result["id"],
                    "email": result["email"],
                    "name": result["name"],
                    "role": result["role"],
                },
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/login",
    tags=["auth"],
    responses=ResponseTemplate(
        [
            {
                "code": 200,
                "examples": {
                    "Success": {
                        "value": {
                            "token": "auth_token",
                            "user": {
                                "id": "user_id",
                                "email": "user@example.com",
                                "name": "User",
                                "role": "user",
                            },
                        }
                    }
                },
            }
        ]
    ).create_response(),
)
async def login(user_data: UserLogin):
    try:
        async with aiohttp.ClientSession() as client:
            auth_result = await PB.authenticate(
                {"email": user_data.email, "password": user_data.password}, client
            )

            user = await PB.fetch_record(
                PocketbaseCollections.USERS, auth_result["record"]["id"], client
            )

            return {
                "token": auth_result["token"],
                "user": {
                    "id": user["id"],
                    "email": user["email"],
                    "name": user["name"],
                    "role": user["role"],
                },
            }
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid credentials")
