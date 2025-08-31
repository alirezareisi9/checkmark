# lib
# third-party
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
# local



class ChangePasswordViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()

        cls.old_password = '12345678'
        cls.manager = User.objects.create_user(

            employee_code='0',
            password=cls.old_password,
            phone_number='0',
            national_code='0',
            role='MANAGER',
        )

        cls.employee = User.objects.create_user(

            employee_code='1',
            password=cls.old_password,
            phone_number='1',
            national_code='1',
            role='EMPLOYEE',
            manager=User.objects.filter(role='MANAGER').first(),
        )

        cls.reporter = User.objects.create_user(

            employee_code='2',
            password=cls.old_password,
            phone_number='2',
            national_code='2',
            role='REPORTER',
        )

    
    def get_auth_header(self, user):
        refresh = RefreshToken.for_user(user)
        return {'HTTP_AUTHORIZATION': f'Bearer {refresh.access_token}'}
    
    def authenticate(self, user):
        self.client.credentials(
            **self.get_auth_header(user)
        )
    
    def test_unauthenticated_access_is_denied(self):
        # GET change-password
        response = self.client.get(reverse('authentication:change-password'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # POST change-password
        response = self.client.post(
            reverse(
                'authentication:change-password',
            )
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_employee_get_not_allowed(self):
        self.authenticate(self.employee)
        # GET change-password
        response = self.client.get(reverse('authentication:change-password'))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


    def test_employee_change_password(self):
        self.authenticate(self.employee)
        # POST change-password
        new_password = 'a23456789'
        response = self.client.post(
            reverse('authentication:change-password'),
            data={
                'old_password': self.old_password,
                'new_password': new_password
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check password changed
        self.employee.refresh_from_db()
        self.assertEqual(self.employee.change_password, True)
        self.assertEqual(self.employee.check_password(new_password), True)

    
    def test_reporter_get_not_allowed(self):
        self.authenticate(self.reporter)
        # GET change-password
        # not allowed
        response = self.client.get(reverse('authentication:change-password'))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


    def test_reporter_change_password(self):
        self.authenticate(self.reporter)
        # POST change-password
        new_password = 'a34567890'
        response = self.client.post(
            reverse('authentication:change-password'),
            data={
                'old_password': self.old_password,
                'new_password': new_password
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check password changed
        self.reporter.refresh_from_db()
        self.assertEqual(self.reporter.change_password, True)
        self.assertEqual(self.reporter.check_password(new_password), True)

    
    def test_manager_get_not_allowed(self):
        self.authenticate(self.manager)
        # GET change-password
        # not allowed
        response = self.client.get(reverse('authentication:change-password'))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


    def test_manager_change_password(self):
        self.authenticate(self.manager)
        # POST change-password
        new_password = 'a2345678'
        response = self.client.post(
            reverse('authentication:change-password'),
            data={
                'old_password': self.old_password,
                'new_password': new_password
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check password changed
        self.manager.refresh_from_db()
        self.assertEqual(self.manager.change_password, True)
        self.assertEqual(self.manager.check_password(new_password), True)