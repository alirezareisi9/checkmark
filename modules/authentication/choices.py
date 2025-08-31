class RoleChoices() :  #define variables for role field choices
    EMPLOYEE_CHOICE = 'EMPLOYEE'
    REPORTER_CHOICE = 'REPORTER'
    MANAGER_CHOICE = 'MANAGER'
    ADMIN_CHOICE = 'ADMIN'
    #role field choices

    ROLE_CHOICES = [
        (EMPLOYEE_CHOICE, 'Employee'),
        (REPORTER_CHOICE, 'Reporter'),
        (MANAGER_CHOICE, 'Manager'),
        (ADMIN_CHOICE, 'Admin'),   
    ]