from application.common.constants import APIMessages
from application.model.models import (Role, RolePermission, Permission)
from index import db


def retrieve_roles_under_org(org_id, permission_id_list):
    """
    Retrieve Roles for given org Id.

    Args:
        org_id (int): Id of the organization

    Returns: list of roles with Id, Name and permission names
    """
    all_roles_obj = db.session.query(
        Role.role_id, Role.role_name, Role.description,
        Permission.permission_id,
        Permission.permission_name).join(
        RolePermission,
        Permission.permission_id == RolePermission.permission_id).join(
        Role,
        RolePermission.role_id == Role.role_id).filter(
        Role.org_id == org_id).all()
    all_roles = []
    # TODO: Improve the code by removing hard-coded index
    # converting list of tuples to list of list
    for each_role in all_roles_obj:
        each_role = list(each_role)
        all_roles.append(each_role)
    main_dict = {}
    for each_role in all_roles:
        if each_role[0] not in main_dict:
            main_dict_value = []
            main_dict_value.append(each_role[1])
            if each_role[2] == None:
                each_role[2] = APIMessages.NO_NAME_DEFINE
            main_dict_value.append(each_role[2])
            permission_id = []
            permission_id.append(each_role[3])
            permission_name = []
            permission_name.append(each_role[4])
            main_dict_value.append(permission_id)
            main_dict_value.append(permission_name)
            main_dict[each_role[0]] = main_dict_value
        else:
            main_dict[each_role[0]][2].append(each_role[3])
            main_dict[each_role[0]][3].append(each_role[4])
    keys = set()
    for key, value in main_dict.items():
        for id in value[2]:
            if id not in permission_id_list:
                keys.add(key)
    for key in keys:
        del main_dict[key]
    roles = []
    for key, value in main_dict.items():
        role_dic = {}
        role_dic["role_id"] = key
        role_dic["role_name"] = value[0]
        role_dic["role_description"] = value[1]
        permission_list = []
        for (permission_id, permission_names) in zip(value[2], value[3]):
            permission_dict = {}
            permission_dict["permission_id"] = permission_id
            permission_dict["permission_name"] = permission_names
            permission_list.append(permission_dict)
        role_dic["permissions"] = permission_list
        roles.append((role_dic))
    return roles
