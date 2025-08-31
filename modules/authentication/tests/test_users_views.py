# Use absolute import rather than relatives in tests

# lib
# third-party
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
# local



# Model Tests
class CustomUserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        
        cls.user = User.objects.create_user(
            employee_code='0',
            password='12345678',
            phone_number='0',
            national_code='0',
            role='EMPLOYEE',
        )


    def test_model_content(self):
        self.assertEqual(self.user.employee_code, '0')
        self.assertEqual(self.user.phone_number, '0')
        self.assertEqual(self.user.national_code, '0')        
        self.assertEqual(self.user.role, 'EMPLOYEE')
        self.assertEqual(str(self.user), str(self.user.employee_code))


class UsersViewTest(APITestCase):
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
            # Use as keyword argument: HTTP_AUTHORIZATION='Bearer <token>'
        )

    def test_unauthenticated_access_list_view_is_denied(self):
        # GET users-list
        response = self.client.get(reverse('authentication:users-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # POST users-list
        response = self.client.post(reverse('authentication:users-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthenticated_access_detail_view_is_denied(self):
        # GET users-detail
        response = self.client.get(
            reverse(
                'authentication:users-detail',
                kwargs={'pk': self.employee.id}
            )
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # PUT users-detail
        response = self.client.put(
            reverse(
                'authentication:users-detail',
                kwargs={'pk': self.employee.id}
            )
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # DELETE users-detail
        response = self.client.delete(
            reverse(
                'authentication:users-detail',
                kwargs={'pk': self.employee.id}
            )
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_list_view_get_for_normal_user(self):
        # Render view
        self.authenticate(self.employee)
        response = self.client.get(reverse('authentication:users-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_detail_view_get_for_normal_user(self):
        # Render view
        self.authenticate(self.employee)

        response = self.client.get(
            reverse(
                'authentication:users-detail',
                kwargs={'pk': self.employee.id}
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

#---------------------------------EMPLOYEE-----------------------------------
    def test_employee_can_view_self_list_view(self):
        # auth
        self.authenticate(self.employee)

        # GET users-list
        response = self.client.get(
            reverse(
                'authentication:users-list'
            )
        )

        self.assertEqual(len(response.data.get('results')), 1)
        self.assertContains(response, self.employee)


    def test_employee_can_view_self_detail_view(self):
        
        self.authenticate(self.employee)
        # GET users-detail
        response = self.client.get(
            reverse(
                'authentication:users-detail',
                kwargs={'pk':self.employee.id}
            )
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_employee_not_access_others_profile(self):
        
        self.authenticate(self.employee)
        # GET users-detail
        responses = [
            self.client.get(
                reverse(
                    'authentication:users-detail',
                    kwargs={'pk':self.manager.id}
                )
            ),
            self.client.get(
                reverse(
                    'authentication:users-detail',
                    kwargs={'pk':self.reporter.id}
                )
            )
        ]

        for response in responses:
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_employee_cannot_create_users(self):
        self.authenticate(self.employee)

        # POST users-list
        response = self.client.post(
            reverse(
                'authentication:users-list'
            )
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # 403: when permission_classes not allow action

    
    def test_employee_cannot_update_self(self):    
        self.authenticate(self.employee)

        # PUT users-detail
        # not accessed
        response = self.client.put(
            reverse(
                'authentication:users-detail',
                kwargs={'pk':self.employee.id}
            )
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        
    def test_employee_cannot_delete_self(self):

        self.authenticate(self.employee)
        # DELETE users-detail
        # not accessed
        response = self.client.delete(
            reverse(
                'authentication:users-detail',
                kwargs={'pk':self.employee.id}
            )
        )
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)



#---------------------------------REPORTER-----------------------------------
    def test_reporter_can_view_all_list_view(self):
        # auth
        self.authenticate(self.reporter)

        # GET users-list
        response = self.client.get(
            reverse(
                'authentication:users-list'
            )
        )

        self.assertEqual(len(response.data.get('results')), 3)
        self.assertContains(response, self.employee)
        self.assertContains(response, self.reporter)
        self.assertContains(response, self.manager)


    def test_reporter_can_view_all_detail_view(self):
        self.authenticate(self.reporter)
        # GET users-detail
        responses = [
            self.client.get(
                reverse(
                    'authentication:users-detail',
                    kwargs={'pk':self.employee.id}
                )
            ),
            self.client.get(
                reverse(
                    'authentication:users-detail',
                    kwargs={'pk':self.reporter.id}
                )
            ),
            self.client.get(
                reverse(
                    'authentication:users-detail',
                    kwargs={'pk':self.manager.id}
                )
            ),
        ]
        
        for response in responses:
            self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_reporter_cannot_create_users(self):
        self.authenticate(self.reporter)

        # POST users-list
        response = self.client.post(
            reverse(
                'authentication:users-list'
            )
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # 403: when permission_classes not allow action

    
    def test_reporter_cannot_update_self(self):    
        self.authenticate(self.reporter)

        # PUT users-detail
        # not accessed
        response = self.client.put(
            reverse(
                'authentication:users-detail',
                kwargs={'pk':self.reporter.id}
            )
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        
    def test_reporter_cannot_delete_self(self):

        self.authenticate(self.reporter)
        # DELETE users-detail
        # not accessed
        response = self.client.delete(
            reverse(
                'authentication:users-detail',
                kwargs={'pk':self.reporter.id}
            )
        )
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


#---------------------------------MANAGER-----------------------------------
    def test_manager_view_self_and_employees_list_view(self):
        # auth
        self.authenticate(self.manager)

        # GET users-list
        response = self.client.get(
            reverse(
                'authentication:users-list'
            )
        )

        self.assertEqual(len(response.data.get('results')), 2)
        self.assertContains(response, self.employee)
        self.assertContains(response, self.manager)


    def test_manager_can_view_self_detail_view(self):
        
        self.authenticate(self.manager)
        # GET users-detail
        response = self.client.get(
            reverse(
                'authentication:users-detail',
                kwargs={'pk':self.manager.id}
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_manager_can_view_employees_detail_view(self):
        
        self.authenticate(self.manager)
        # GET users-detail
        response = self.client.get(
            reverse(
                'authentication:users-detail',
                kwargs={'pk':self.employee.id}
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    
    def test_manager_can_create_users(self):
        self.authenticate(self.manager)

        # POST users-list
        User = get_user_model()
        response = self.client.post(
            reverse(
                'authentication:users-list'
            ),
            data={
                'employee_code': '3',
                'first_name': '3', 
                'last_name': '3',
                'phone_number': '3',
                'national_code': '3',
                'role': 'EMPLOYEE',
                'leave_limit': 3,
            }
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # 403: when permission_classes not allow action


    def test_manager_can_update_self(self):    
        
        self.authenticate(self.manager)
        # PUT users-detail
        response = self.client.put(
            reverse(
                'authentication:users-detail',
                kwargs={'pk':self.manager.id}
            ),
            data={
                'employee_code': '0',
                'first_name': '3', 
                'last_name': '3',
                'phone_number': '0',
                'national_code': '0',
                'role': 'MANAGER',
                'leave_limit': 3,
            }
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.manager.refresh_from_db()
        self.assertEqual(self.manager.employee_code, '0')
        self.assertEqual(self.manager.first_name, '3')
        self.assertEqual(self.manager.last_name, '3')
        self.assertEqual(self.manager.phone_number, '0')
        self.assertEqual(self.manager.national_code, '0')        
        self.assertEqual(self.manager.role, 'MANAGER')
        self.assertEqual(self.manager.leave_limit, 3)

        # PATCH users-detail
        response = self.client.patch(
            reverse(
                'authentication:users-detail',
                kwargs={'pk':self.manager.id}
            ),
            data={
                'leave_limit': 4,
            }
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.manager.refresh_from_db()
        self.assertEqual(self.manager.leave_limit, 4)
        


    def test_manager_can_delete_self(self):
        # Cannot delete manager because it's in protected relationships with
        #  it's employees but it accesses
        pass
        # DELETE users-detail
        '''
        response = self.client.delete(
            reverse(
                'authentication:users-detail',
                kwargs={'pk':self.manager.id}
            )
        )

        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        '''


    def test_manager_can_update_employees(self):
        self.authenticate(self.manager)
        # PUT users-detail
        response = self.client.put(
            reverse(
                'authentication:users-detail',
                kwargs={'pk':self.employee.id}
            ),
            data={
                'employee_code': '1',
                'first_name': '1', 
                'last_name': '1',
                'phone_number': '1',
                'national_code': '1',
                'role': 'EMPLOYEE',
                'leave_limit': 3,
            }
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.employee.refresh_from_db()
        self.assertEqual(self.employee.employee_code, '1')
        self.assertEqual(self.employee.first_name, '1')
        self.assertEqual(self.employee.last_name, '1')
        self.assertEqual(self.employee.phone_number, '1')
        self.assertEqual(self.employee.national_code, '1')        
        self.assertEqual(self.employee.role, 'EMPLOYEE')
        self.assertEqual(self.employee.leave_limit, 3)

        # PATCH users-detail
        response = self.client.patch(
            reverse(
                'authentication:users-detail',
                kwargs={'pk':self.employee.id}
            ),
            data={
                'leave_limit': 2,
            }
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.employee.refresh_from_db()
        self.assertEqual(self.employee.leave_limit, 2)


    def test_manager_can_delete_employees(self):
        
        self.authenticate(self.manager)
        # DELETE users-detail
        response = self.client.delete(
            reverse(
                'authentication:users-detail',
                kwargs={'pk':self.employee.id}
            )
        )

        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)