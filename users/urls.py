from django.urls import path

from users.controllers.user_controller import UserSaveController, UserGetUserController, UserListController, UserUpdatePasswordController, UserDeleteController, UserUpdateController
from users.controllers.login_controller import LoginController
from users.controllers.cuestom_token_refresh_view import CustomTokenRefreshView
from users.controllers import typology_controller
from users.controllers import api_url_controller
from users.controllers import typology_api_url_controller

urlpatterns = [
    path('users/', UserSaveController.as_view(), name="create_user"),
    path('users/list', UserListController.as_view(), name="users_list"),
    path('users/delete/<int:pk>', UserDeleteController.as_view(), name="user_delete"),
    path('users/update/<int:pk>', UserUpdateController.as_view(), name="upate_user"),
    path('users/find/<int:pk>', UserGetUserController.as_view(), name="users_find"),
    path('users/reset_password/', UserUpdatePasswordController.as_view(), name="update_password"),
    path('login/', LoginController.as_view(), name="obtain_tokens"),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name="token_refresh"),
    path('typologies/', typology_controller.TypologySaveController.as_view(), name="typology_save"),
    path('apiurl/', api_url_controller.ApiUrlSaveController.as_view(), name="create_api_url"),
    path('typology/apiurl/', typology_api_url_controller.TypologyPermissionSaveController.as_view(), name="assign_permission"),
    path('typology/apiurl/delete/<int:pk>', typology_api_url_controller.TypologyPermissionRevokeController.as_view(), name="revoke_permission"),
    path('typologies/list', typology_controller.TypologyListController.as_view(), name="typologies_list"),
    path('typologies/find/<int:pk>', typology_controller.TypologyGetController.as_view(), name="get_typology"),
    path('typologies/update/<int:pk>', typology_controller.TypologyUpdateController.as_view(), name="typology_update"),
    path('apiurl/find/<int:pk>', api_url_controller.ApiUrlGetController.as_view(), name="get_api_url"),
    path('apiurl/list', api_url_controller.ApiUrlListController.as_view(), name="api_url_list"),
    path('apiurl/update/<int:pk>', api_url_controller.ApiUrlUpdateController.as_view(), name="update_api_url"),
]