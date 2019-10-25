import { createStore, applyMiddleware, compose } from 'redux';
import { toast } from 'react-toastify';
import logger from 'redux-logger';

import rootReducer from '../reducers';
import { authenticationExpired } from '../actions/appActions';
import { POP_UP_SUCCESS_MESSAGE, POP_UP_ORG_SUCCESS_MSG } from '../constants/FieldNameConstants';

const hasStandardErrorStatus = (status) => {
	return ((status >= 300 && status <= 307) || 
		(status >= 400 && status <= 417) || 
		(status >= 500 && status <= 505));
};

function callAPIMiddleware({ dispatch, getState }) {
	return next => action => {
		 const { 
			types, 
			callAPI, 
			shouldCallAPI = () => true, 
			payload = {}, 
			args, 
			showSuccessMsg 
		} = action;
  
		if (!types) {
			// Normal action: pass it on
			return next(action);
		}
  
		if (
			!Array.isArray(types) ||
			types.length !== 3 ||
			!types.every(type => typeof type === 'string')
		) {
			throw new Error('Expected an array of three string types.');
		}

		if (typeof callAPI !== 'function') {
			throw new Error('Expected callAPI to be a function.')
		}
  
		if (!shouldCallAPI(getState())) {
			return;
		}
  
		const [requestType, successType, failureType] = types;
  
		if (requestType) {
			dispatch(
				Object.assign({}, payload, {
					type: requestType
				})
			);
		}

		let fullResponse = null;
		return callAPI()
			.then(response => {
				fullResponse = response;
				return response.json();
			})
			.then(
				response => {
					if (hasStandardErrorStatus(fullResponse.status)) {
					
						if (fullResponse.statusText === "UNAUTHORIZED") {
							
							dispatch(authenticationExpired());
						} else {
						
							const message = (response.message) ? response.message : 'Unidentified Error!!';
							toast.error(message);
							dispatch(
								Object.assign({}, payload, {
									response,
									type: failureType
								})
							);
						}

					} else {
						
						
						if (response.data && Object.keys(response.data).length === 0 && response.message) {
							
							if (response.success) {
							
								toast.success(response.message);
							} else {
							
								if (response.message.length > 0) {
								
									toast.warn(response.message);
								}
							
								toast.warn(response.message);
							}
						
						} 
						else{
							if(response.success ===false){
							
								toast.error(response.message);
							}
						
							  else{
								
								if(response.message ===POP_UP_SUCCESS_MESSAGE){
								
									toast.success(response.message);
								}
								else{
									if(response.message ===POP_UP_ORG_SUCCESS_MSG){
										toast.success(response.message);
									}
								}
								
							    }
							
							
						}
						dispatch(
							Object.assign({}, payload, {
								response,
								type: successType,
								args
							})
						);
					}
				},	
				error =>
					dispatch(
						Object.assign({}, payload, {
							error,
							type: failureType
						})
					)
			);
	};
}

// const middleware = applyMiddleware(thunk, logger);
const middleware = applyMiddleware(callAPIMiddleware, logger);

const reduxDevTools = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;

const store = createStore(
	rootReducer,
	reduxDevTools(
		middleware
	)
);

export default store;