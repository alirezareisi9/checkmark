from rest_framework import permissions



# roles = admin(temp superuser for test),manager,employee,reporter

################
#HOW TO USE PERMISSIONS PERMISSIONS :
#levels :

    # top = admin
    # manager = manager and admin
    # watcher = reporter and manager
    # base =  employee

#view():
    
################



class Top(permissions.BasePermission):
    message = 'admin access required , you do not have the role required to access this page'
    
    def has_persmission(self, request, view):
        return request.user.role == 'ADMIN'

    def has_object_permission(self ,request, view, obj):
        if request.method in ['GET','OPTIONS','PUT','POST','PATCH','DELETE']:
            return request.user.role == 'ADMIN'

        


class Base(permissions.BasePermission):
    message = 'employee access required , you do not have the role required to access this page'

    def has_persmission(self,request,view):       
        return (request.user.role=='EMPLOYEE' or request.user.role=='MANAGER'
        or request.user.role == 'ADMIN' or request.user.role == 'REPORTER')

    def has_object_permission(self,request,view,obj):
        if request.method in ['OPTIONS','HEAD']:
            return (request.user.role == 'EMPLOYEE' or request.user.role=='MANAGER' 
            or request.user.role == 'ADMIN' or request.user.role == 'REPORTER')
            


class Manager(permissions.BasePermission):
    message = 'admin or manager access required , you do not have the role required to access this page'

    def has_persmission(self,request,view):
        return request.user.role=='MANAGER' or request.user.role == 'ADMIN'

    def has_object_permission(self,request,view,obj):
        if request.method in ['GET','OPTIONS','PUT','POST','PATCH','DELETE']:
            return request.user.role=='MANAGER' or request.user.role == 'ADMIN'

class Watcher(permissions.BasePermission):
    message = 'watcher access required , you do not have the role required to access this page'
    
    def has_persmission(self,request,view):        
        return request.user.role=='REPORTER' or request.user.role=='MANAGER'
        
    def has_object_permission(self,request,view,obj):
        if request.method in ['GET','OPTIONS']:      
            return request.user.role=='REPORTER'or request.user.role=='MANAGER'


class IsManagerOrReadOnly(permissions.BasePermission) :
    def has_permission(self, request, view) :
        if request.user.is_authenticated :
            if request.user.role == 'MANAGER' :
                return True
            if request.user.role == 'REPORTER' :
                if request.method in permissions.SAFE_METHODS :  # SAFE_METHODS : ['GET', 'HEAD', 'OPTIONS']
                    return True
                return False
            if request.user.role == 'EMPLOYEE' :
                if request.method in permissions.SAFE_METHODS :
                    return True
                return False
        return False
    
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated :
            if request.user.role == 'MANAGER' :
                return True
            if request.user.role == 'REPORTER' :
                if request.method in permissions.SAFE_METHODS :  # SAFE_METHODS : ['GET', 'HEAD', 'OPTIONS']
                    return True
                return False
            if request.user.role == 'EMPLOYEE' :
                if request.method in permissions.SAFE_METHODS :
                    return True
                return False
        return False

