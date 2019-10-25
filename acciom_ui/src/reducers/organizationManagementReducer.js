import {
    GET_DETAILS_ORGANIZATION_LIST_SUCCESS,
    GET_DETAILS_ORGANIZATION_LIST_ERROR,
    ADD_ORGANIZATION_LIST_SUCCESS,
    ADD_ORGANIZATION_LIST_ERROR,
    UPDATE_ORGANIZATION_LIST_SUCCESS,
    UPDATE_ORGANIZATION_LIST_ERROR,
    DELETE_ORGANIZATION_LIST_SUCCESS,
    DELETE_PROJECT_LIST_ERROR} from "../constants/ActionTypes";

    const initialState = {
        organizationUserList:[],
        refreshOrganizationDetails:false
    }

    const organizationManagementData = (state = initialState, action) => {
        switch (action.type) {
            
            case GET_DETAILS_ORGANIZATION_LIST_SUCCESS:
              
                return {
                    ...state,
                    organizationUserList:action.response.data.organization_details,
                    refreshOrganizationDetails:false
                }
                case ADD_ORGANIZATION_LIST_SUCCESS:
						
					   return{
							...state,
							refreshOrganizationDetails:true
                        }
                case UPDATE_ORGANIZATION_LIST_SUCCESS :
                        return{
                            ...state,
                            }
                case DELETE_ORGANIZATION_LIST_SUCCESS:
                    
                        return{
                            ...state,
                            refreshOrganizationDetails:true
                              }
                default:
                return state;
            
        }

   

    }

    export default organizationManagementData;