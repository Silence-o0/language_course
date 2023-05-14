from rest_access_policy import AccessPolicy

__all__ = ['LanguageAccessPolicy', 'TeacherAccessPolicy', 'StudentAccessPolicy', 'AdminAccessPolicy',
           'LessonAccessPolicy', 'MarkAccessPolicy', 'GroupAccessPolicy']

class LanguageAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["list", "retrieve"],
            "principal": "*",
            "effect": "allow"
        },
        {
            "action": "*",
            "principal": ["group:admin"],
            "effect": "allow"
        }
    ]


class TeacherAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["list", "retrieve"],
            "principal": "*",
            "effect": "allow"
        },
        {
            "action": ["update", "destroy"],
            "principal": "*",
            "effect": "allow",
            "condition": "is_account_owner"
        },
        {
            "action": "*",
            "principal": ["group:admin"],
            "effect": "allow",
        }
    ]

    def is_account_owner(self, request, view, action) -> bool:
        user = view.get_object().user
        return request.user == user


class StudentAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["list"],
            "principal": "*",
            "effect": "allow"
        },
        {
            "action": ["update", "destroy", "retrieve"],
            "principal": "*",
            "effect": "allow",
            "condition": "is_account_owner"
        },
        {
            "action": ["retrieve"],
            "principal": ["group:teacher"],
            "effect": "allow",
        },
        {
            "action": "*",
            "principal": ["group:admin"],
            "effect": "allow",
        }
    ]

    def is_account_owner(self, request, view, action) -> bool:
        user = view.get_object().user
        return request.user == user


class AdminAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": "*",
            "principal": ["group:admin"],
            "effect": "allow"
        },
    ]


class LessonAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["list", "retrieve"],
            "principal": ["group:teacher", "group:student"],
            "effect": "allow",
        },
        {
            "action": "*",
            "principal": ["group:admin"],
            "effect": "allow",
        }
    ]


class MarkAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["list", "retrieve"],
            "principal": ["group:teacher", "group:student"],
            "effect": "allow",
        },
        {
            "action": ["update", "destroy", "create"],
            "principal": ["group:teacher"],
            "effect": "allow",
        },
        {
            "action": "*",
            "principal": ["group:admin"],
            "effect": "allow",
        }
    ]


class GroupAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["list", "retrieve"],
            "principal": ["group:teacher", "group:student"],
            "effect": "allow",
        },
        {
            "action": ["assign_student_to_group", "remove_student_from_group"],
            "principal": ["group:teacher"],
            "effect": "allow",
        },
        {
            "action": "*",
            "principal": ["group:admin"],
            "effect": "allow",
        }
    ]
