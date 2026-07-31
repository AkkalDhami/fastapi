from repositories.user import UserRepository
from services.auth import AuthService

user_repository = UserRepository()

auth_service = AuthService(user_repository)
