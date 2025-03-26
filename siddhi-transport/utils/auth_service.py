from rest_framework_simplejwt.tokens import RefreshToken


class AuthService:
    @staticmethod
    def __tokens_for_user(user) -> dict:
        """generate tokens"""
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

    @classmethod
    def get_auth_tokens_for_user(self, user) -> dict:
        """call private method to generate refresh and access token"""
        return self.__tokens_for_user(user)
