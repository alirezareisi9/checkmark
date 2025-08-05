from django.contrib.auth import get_user_model
from django.test import TestCase

class UserManagersTests(TestCase):

    def test_create_user(self):
        User = get_user_model()

        # if these below not get an ValueError, output will be :
        #  ValueError not raised
        with self.assertRaises(ValueError):
            User.objects.create_user(employee_code=1, password='123', 
                                       national_code=1)
        with self.assertRaises(ValueError):
            User.objects.create_user(national_code=1, phone_number=1, 
                                       password='123', role='EMPLOYEE') 
        with self.assertRaises(ValueError):
            User.objects.create_user(employee_code=1, password='123', 
                                       national_code=1) 
        
        with self.assertRaises(TypeError):
            User.objects.create_user(employee_code=1, phone_number=1, 
                                       role='EMPLOYEE', national_code=1)
            
        
        user = User.objects.create_user(employee_code=1, phone_number=1,
                                         password='123', national_code=1,
                                           role='EMPLOYEE')
        
        self.assertIsNone(user.username)

        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        
        with self.assertRaises(ValueError):
            User.objects.create_superuser(employee_code=2, password='123',
                                           phone_number=2, national_code=2,
                                             role='EMPLOYEE')
        with self.assertRaises(ValueError):
            User.objects.create_superuser(employee_code=2, password='123',
                                           phone_number=2, national_code=2,
                                            role='REPORTER')
        
        admin_user = User.objects.create_superuser(employee_code=2,
                                                    password='123', phone_number=2, national_code=2, role='MANAGER')

        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)