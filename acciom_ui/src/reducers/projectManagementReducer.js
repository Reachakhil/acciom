import {
    GET_PROJECT_LIST_SUCCESS,
	GET_PROJECT_LIST_ERROR,
	UPDATE_PROJECT_LIST_SUCCESS,
	ADD_PROJECT_LIST_SUCCESS,
	DELETE_PROJECT_LIST_SUCCESS} from "../constants/ActionTypes";
export const roleTypes = {
	ORGANIZATION:'ORGANIZATION',
	PROJECT: 'PROJECT',
	NEW: 'NEW' 
};
const initialState = {
    projectUserList:[],
	orgUserList: [],
	orgProjectRolesList: {},
	userOrgRoleList: [],
	userProjectRoleList: [],
	userNewRoleList: [],
	selectedUser: null,
	redirectToUserMgmtHome: false
};
const projectManagementData = (state = initialState, action) => {
    switch (action.type) {
		
	

        case GET_PROJECT_LIST_SUCCESS:
			
                return {
                    ...state,
                    projectUserList: action.response.data.projects_under_organization.project_details,
				}
				case UPDATE_PROJECT_LIST_SUCCESS :
				
					return{
						...state,
					}
					case ADD_PROJECT_LIST_SUCCESS:
						
					   return{
							...state
						}
						case DELETE_PROJECT_LIST_SUCCESS:
							console.log('Delete reducer',action);
							return{
								...state
							}
		
                default:
		return state;
    }

};
export default projectManagementData;