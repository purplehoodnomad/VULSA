from domain.exceptions import DomainException


class RoleAlreadyExists(DomainException):
    code = "ROLE_ALREADY_EXISTS"
    message = "Role already exists"

class RoleNotFound(DomainException):
    code = "ROLE_NOT_FOUND"
    message = "Role not found"

class RolePermissionViolation(DomainException):
    code = "ROLE_PERMISSION_VIOLATION"
    message = "Can't execute for this role"

class PermissionNotFound(DomainException):
    code = "PERMISSION_NOT_FOUND"
    message = "Permission not found"