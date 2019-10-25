
import {
    GET_DETAILS_ORGANIZATION_LIST_SUCCESS,
	GET_DETAILS_ORGANIZATION_LIST_ERROR,
	ADD_ORGANIZATION_LIST_SUCCESS,
	ADD_ORGANIZATION_LIST_ERROR,
	UPDATE_ORGANIZATION_LIST_SUCCESS,
	UPDATE_ORGANIZATION_LIST_ERROR,
	DELETE_ORGANIZATION_LIST_SUCCESS,
	DELETE_ORGANIZATION_LIST_ERROR} from "../constants/ActionTypes";

import {  BASE_URL, headers} from './appActions';
export const getDetailsOrganizationList = () => {
    
    
	return {
		types: [
			'',
			GET_DETAILS_ORGANIZATION_LIST_SUCCESS,
			GET_DETAILS_ORGANIZATION_LIST_ERROR
		],
		callAPI: () => fetch(`${BASE_URL}/organization`, {
			method: 'get',
			headers
		})
	};	

}


export const addToOrganizationList=(data)=>{

	return{
		types:[
			'',
			ADD_ORGANIZATION_LIST_SUCCESS,
			ADD_ORGANIZATION_LIST_ERROR
	
		],
		callAPI:() => fetch(`${BASE_URL}/organization`,{
			method: 'post',
			headers,
			body: data
	
		}) 
	
	   }
	}

	export const updateOrganizationList=(data)=>{

		return{
			types:[
				'',
				UPDATE_ORGANIZATION_LIST_SUCCESS,
				UPDATE_ORGANIZATION_LIST_ERROR
		
			],
			callAPI:() => fetch(`${BASE_URL}/organization`,{
				method: 'put',
				headers,
				body: data
		
			}) 
		
		   }
		}
		
		export const deleteOrganizationDetails = (data) => {
       
			return {
				types: [
					'',
					DELETE_ORGANIZATION_LIST_SUCCESS,
					DELETE_ORGANIZATION_LIST_ERROR
				],
				
				callAPI: () => fetch(`${BASE_URL}/organization`, {
					method: 'delete',
					headers,
					body:data
				})
			};		
		};