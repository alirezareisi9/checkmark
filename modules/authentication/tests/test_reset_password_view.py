# lib
# third-party
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
# local




class ResetPasswordViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()

        cls.manager = User.objects.create_user(

            employee_code='0',
            password='12345678',
            phone_number='0',
            national_code='0',
            role='MANAGER',
        )

        cls.employee = User.objects.create_user(

            employee_code='1',
            password='12345678',
            phone_number='1',
            national_code='1',
            role='EMPLOYEE',
            manager=User.objects.filter(role='MANAGER').first(),
        )

        cls.reporter = User.objects.create_user(

            employee_code='2',
            password='12345678',
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
        # GET reset-password
        response = self.client.get(
            reverse(
                'authentication:reset-password', 
                kwargs={'pk': 1},
            )
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # PUT reset-password
        response = self.client.post(
            reverse(
                'authentication:reset-password',
                kwargs={'pk':1},
            )
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_employee_cannot_access(self):
        
        self.authenticate(self.employee)

        # GET
        response = self.client.get(
            reverse(
                'authentication:reset-password',
                kwargs={'pk':self.employee.id}
            )
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # PUT
        response = self.client.put(
            reverse(
                'authentication:reset-password',
                kwargs={'pk':self.employee.id}
            )
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_reporter_cannot_access(self):

        self.authenticate(self.reporter)

        # GET
        response = self.client.get(
            reverse(
                'authentication:reset-password',
                kwargs={'pk':self.reporter.id}
            )
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # PUT
        response = self.client.put(
            reverse(
                'authentication:reset-password',
                kwargs={'pk':self.reporter.id}
            )
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    
    def test_get_not_allowed(self):
        
        self.authenticate(self.manager)
        # GET
        response = self.client.get(
            reverse(
                'authentication:reset-password',
                kwargs={'pk':self.manager.id}
            )
        )

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        

    def test_post_not_allowed(self):

        self.authenticate(self.manager)
        # POST
        response = self.client.post(
            reverse(
                'authentication:reset-password',
                kwargs={'pk':self.manager.id}
            )
        )

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        
        
    def test_patch_not_allowed(self):

        self.authenticate(self.manager)
        # PATCH
        response = self.client.patch(
            reverse(
                'authentication:reset-password',
                kwargs={'pk':self.manager.id}
            )
        )

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        

    def test_delete_not_allowed(self):

        self.authenticate(self.manager)
        # DELETE
        response = self.client.delete(
            reverse(
                'authentication:reset-password',
                kwargs={'pk':self.manager.id}
            )
        )

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


    def test_manager_reset_self_password(self):
        
        self.authenticate(self.manager)

        password = 'a23456789'
        response = self.client.put(
            reverse(
                'authentication:reset-password',
                kwargs={'pk': self.manager.id}
            ),
            data={'password': password}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.manager.refresh_from_db()
        self.manager.check_password(password)
        self.assertEqual(self.manager.change_password, True)


    def test_manager_reset_employees_password(self):
        self.authenticate(self.manager)

        password = 'a23456789'
        response = self.client.put(
            reverse(
                'authentication:reset-password',
                kwargs={'pk': self.employee.id}
            ),
            data={'password': password}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.employee.refresh_from_db()
        self.employee.check_password(password)
        self.assertEqual(self.employee.change_password, True)


    def test_manager_cannot_reset_non_employees_password(self):
        self.authenticate(self.manager)

        password = 'a34567890'
        response = self.client.put(
            reverse(
                'authentication:reset-password',
                kwargs={'pk': self.reporter.id}
            ),
            data={'password': password}
        )
    
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)