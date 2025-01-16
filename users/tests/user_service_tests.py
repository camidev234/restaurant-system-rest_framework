from django.test import TestCase
from users.services.user_service import UserService
from users.models.users import User
from rest_framework.exceptions import ValidationError

class UserServiceTestCase(TestCase):
    def setUp(self):
        self.user_service = UserService()
        
        self.valid_data = {
            "first_name": "test",
            "last_name": "user",
            "email": "testuser@gmail.com",
            "password": "12345670",
            "phone": "3003130618",
            "address": "cra 7b #2a 68",
            "typology_id": 4,
            "restaurant_id" : 1
        }
        
    def test_save_valid_user(self):
        saved_user = self.user_service.save(self.valid_data)
        
        self.assertEqual(saved_user["first_name"], "test")
        self.assertEqual(saved_user["last_name"], "user")
        self.assertEqual(saved_user["phone"], "3003130618")
        self.assertEqual(saved_user["address"], "cra 7b #2a 68")
        self.assertEqual(saved_user["email"], "testuser@gmail.com")
        self.assertEqual(saved_user["typology_id"], 4)
        self.assertEqual(saved_user["restaurant_id"], 1)
        
        self.assertNotEqual(saved_user["password"], "12345670")
        user_in_db = User.objects.get(email="testuser@gmail.com")
        
        self.assertEqual(user_in_db.email, "testuser@gmail.com")
        self.assertTrue(user_in_db.check_password("12345670"))
        
    def test_save_user_with_missing_required_field(self):
        invalid_data = self.valid_data.copy()
        
        del invalid_data["email"]
        
        with self.assertRaises(ValidationError) as context:
            self.user_service.save(invalid_data)
            
        self.assertIn("email", context.exception.detail)