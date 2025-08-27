# lib
# third-party
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
# local

# Model Tests
class CustomUserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create(
            employee_code=0,
            phone_number=0,
            national_code=0,
            role='EMPLOYEE',
        )
    
    def test_model_content(self):
        self.assertEqual(self.user.employee_code, 0)
        self.assertEqual(self.user.phone_number, 0)
        self.assertEqual(self.user.national_code, 0)        
        self.assertEqual(self.user.role, 'EMPLOYEE')
        self.assertEqual(str(self.user), str(self.user.employee_code))


class CustomUserAPITest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create(
            employee_code=0,
            phone_number=0,
            national_code=0,
            role='EMPLOYEE',
        )