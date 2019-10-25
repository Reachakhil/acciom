
import React, { Component, Fragment } from 'react';
import { connect } from 'react-redux';
import EditIcon from '@material-ui/icons/Edit';
import GroupIcon from '@material-ui/icons/Group';
import { withStyles } from '@material-ui/core/styles';
import DeleteIcon from '@material-ui/icons/Delete';
import CheckIcon from '@material-ui/icons/Check';
import Clear from '@material-ui/icons/Clear';
import CustomTable from '../components/Table/CustomTable'
import CustomModal from '../components/CommonModal/CustomModal';
import {getProjectList,updateProjectList,deleteProjectDetails,addToProjectList} from '../actions/projectManagementActions';
import { PROJECTS, ORGANIZATION, PROJECTNAME, PROJECTDESCRIPTION, PROJNAME, DESCRIPTION, SMALL, ACTION, ADDPROJECT, ADDORGANIZATION, DELETEMSG, TITLE, DELETE, ADD, PROJDESCTEXT, PROJNAMETEXT, PRJ_TEXTBOX_NAME, PRJ_TEXTBOX_DESC} from '../constants/FieldNameConstants';
import { Button,Modal} from 'react-bootstrap';
import { toast } from 'react-toastify';


const styles = theme => ({

	IconClass:{
		marginBottom:'-5px',
		marginLeft:'3px'
	}
});

class ProjectManagement extends Component {
	componentDidMount(){
		
		const location=window.location.href;

		if(location.includes(PROJECTS)){
		  this.setState({location:PROJECTS});
		}
		  else if(location.includes(ORGANIZATION)){
			this.setState({location:ORGANIZATION});
  
		  }
	  }

	  deleteItemHandler = (deleteProjectId)=>{	 
		  this.setState({showDeleteConfirmationDialog:true, deleteConnectionID:deleteProjectId});
	  }

	  onYesBtnClickHandler=()=>{
		  const connectionId = {
				 
				      rowconnectionID: this.state.deleteConnectionID
			          };
                      this.props.deleteProjectDetails(connectionId);
		              this.hideConfirmationopup();
				
		       }

		onNoBtnClickHandler=()=>{
			this.hideConfirmationopup();
		}

		hideConfirmationopup = () => {
			this.setState({showDeleteConfirmationDialog: false ,deleteConnectionID:null});
		}

		editHandler=(index)=>{	
			this.setState({editIdx:index});
			const localProjectList = [...this.state.projectList];
		
			this.setState({projectName:localProjectList[index].project_name});
			this.setState({projectNameInitialValue:localProjectList[index].project_name});
			this.setState({projectDescription:localProjectList[index].project_description});
			this.setState({projectDescriptionInitialValue:localProjectList[index].project_description});
		
		}

		saveDataHandler=(index)=>{	
		
			const localProjectListHandler = [...this.state.projectList];
		
			localProjectListHandler[index].project_name = this.state.projectName;
			localProjectListHandler[index].project_description = this.state.projectDescription;
		
			let upDateProjectDetails = {};

			upDateProjectDetails={
				project_name:localProjectListHandler[index].project_name,
				project_description:localProjectListHandler[index].project_description,
				project_id:localProjectListHandler[index].project_id
			};
			if(localProjectListHandler[index].project_description.length ==0){
			
				toast.error(PROJDESCTEXT);
			
				
			}
			else 
			if(localProjectListHandler[index].project_name.length ==0){
				toast.error(PROJNAMETEXT);
				
			}
			
	if(localProjectListHandler[index].project_name.length >0 && localProjectListHandler[index].project_description.length>0){
		this.props.updateProjectList(JSON.stringify(upDateProjectDetails));
		this.setState({editIdx:-1});
		
	}
	
	
	
	 			
		}

		clearDataHandler = (index) =>{
			const clearProjectListHandler = [...this.state.projectList];
    
			clearProjectListHandler[index].project_name = this.state.projectName;
			clearProjectListHandler[index].project_description = this.state.projectDescription;
		  
			if(clearProjectListHandler[index].project_description.length ==0){
				clearProjectListHandler[index].project_description=this.state.projectDescriptionInitialValue;
				this.setState({organizationDescription:clearProjectListHandler[index].project_description});
			}
		  if(clearProjectListHandler[index].project_name.length ==0){
			clearProjectListHandler[index].project_name=this.state.projectNameInitialValue;
			this.setState({organizationName: clearProjectListHandler[index].project_name})
	
		  }

			this.setState({editIdx:-1});	
		}

		handleChangeHandler=(event)=>{
			if(event.target.name ===PROJECTNAME){
			
				this.setState({projectName:event.target.value});
			}
			else if(event.target.name ===PROJECTDESCRIPTION){
				
				this.setState({projectDescription:event.target.value});
			}

		}
		hideUserInfoPopUp=()=>{
			this.setState({showAddConfirmationDialog:false,projectNameAdd:'',projectDescriptionAdd:''});
		}
	
		handleAddButtonHandler=()=>{
		
			this.setState({showAddConfirmationDialog:true});
		}
		cancelBtnClicked=()=>{
			this.hideUserInfoPopUp();
		   }
		   
		   validateConditions =()=>{
			const {projectNameAdd ,projectDescriptionAdd} =this.state;
			
			if(projectNameAdd.length>0 && projectDescriptionAdd.length>0){
				return true
               }
			return false
		}
		saveBtnClicked=()=>{
		
			let addToProjectDetails = {};

			addToProjectDetails={
				project_name:this.state.projectNameAdd,
				project_description:this.state.projectDescriptionAdd,
				org_id:this.props.currentOrg.org_id
			};
		

			if(this.validateConditions()){
				this.props.addToProjectList(JSON.stringify(addToProjectDetails));
				this.hideUserInfoPopUp();
			
			

			}

		}
		textFieldHandler=()=>{
			
            if(event.target.name ===PRJ_TEXTBOX_NAME){
			
			 this.setState({projectNameAdd:event.target.value})
		
			}
			
		   else if(event.target.name ===PRJ_TEXTBOX_DESC){
		
			this.setState({projectDescriptionAdd:event.target.value})
		
			}
			
		  }
	
	static getDerivedStateFromProps = (nextProps, prevState) => {
	
	if(nextProps.refreshProjectDetails){
	
		nextProps.getProjectList(nextProps.currentOrg.org_id);
		return {
			prevState
		};
	}
	if(nextProps.projectUserList.length === 0){
		if (nextProps.currentOrg ? nextProps.currentOrg.org_id : false) {
			nextProps.getProjectList(nextProps.currentOrg.org_id);
			return {
				prevState
			};
		}
	}
	if(prevState.projectUserList!== nextProps.projectUserList){
			return {
				...prevState,
				projectList: nextProps.projectUserList
				};

		}
		
	}

	constructor(props) {
		super(props);
		this.state = {
			
			headers : [
				{ id: PROJECTNAME,  label: PROJNAME },
				{ id: PROJECTDESCRIPTION,  label: DESCRIPTION },
			  ],
			  location:PROJECTS,
			  showDeleteConfirmationDialog: false,
			  showAddConfirmationDialog: false,
			  deleteConnectionID: null,
			  editIdx:-1,
			  projectList:[],
			  projectName:'',
			  projectDescription:'',
			  projectNameAdd:'',
			  projectDescriptionAdd:'',
			  projectDescriptionInitialValue:'',
			  projectNameInitialValue:''

			
		};
	}
		
	render() {
		

		const { headers , projectList,isEditable} = this.state;
		const {classes} =this.props;
		let currentButtonName =ADDPROJECT
		let currentHeader =<label>Project Management</label>;
		if(this.state.location == ORGANIZATION){
		  currentHeader =<label>Organization Management</label>;
	      currentButtonName =ADDORGANIZATION;

		}

		const projectModifyData=[];
		if(projectList){
			projectList.forEach((project,index) => {
				projectModifyData.push({
					project_name: project.project_name,
					project_description: project.project_description,
				
					action: (
						<Fragment>
							
							<EditIcon 
								fontSize={SMALL}
								className="editicon2" 
								style={{color:"#696969" ,marginRight:'8px'}} 
								onClick ={() =>{this.editHandler(index);}}
							/>
					  <DeleteIcon 
							  className="cursorhover" 
							  fontSize={SMALL}
							  style={{color:"#696969",marginRight:'8px'}} 
							  onClick ={() =>{this.deleteItemHandler(project.project_id);}}
							   />

						</Fragment>
					
					),
					editingIconAction:(
						<Fragment>
							<CheckIcon
						  style={{color:"#696969" ,marginRight:'8px'}} 
                          onClick ={()=>this.saveDataHandler(index)}
						  /> 
						  <Clear
						   fontSize={SMALL}
						   style={{color:"#696969",marginRight:'8px'}} 
						   onClick={()=>this.clearDataHandler(index)}/>
						</Fragment>

					)
				});

			});
            
		}
        
		return (

			<div>
		
				<div>
				<GroupIcon className=" organizationManagementIcon" />
			&nbsp; &nbsp;

				
					<label className="main_titles projectManagementMargin" >{currentHeader}</label>
					<Button 
					className="backbutton_colors_project addUserButton"
					onClick={this.handleAddButtonHandler}>{currentButtonName}</Button>


				</div>
			
				  	<CustomTable 
					headers={headers}
					bodyData={projectModifyData}
					actionLabel={ACTION}
					editIdx ={this.state.editIdx}
					projectNameValue ={this.state.projectName}
					projectDescriptionValue ={this.state.projectDescription}
					handleChange ={this.handleChangeHandler}
				    />
				 { 
					this.state.showDeleteConfirmationDialog ?
						<CustomModal
						  onYesBtnClicked={this.onYesBtnClickHandler}
						  onNoBtnClicked={this.onNoBtnClickHandler}
						  currentPage ={this.state.location} 
					      variant ={DELETE}
						   />
						: null
				}
			
				{
                  this.state.showAddConfirmationDialog? <CustomModal
				   projectNameAdd={this.state.projectNameAdd}
				   projectDescriptionAdd={this.state.projectDescriptionAdd}
				   onCancelBtnClicked ={this.cancelBtnClicked}
				   onSaveBtnClicked ={this.saveBtnClicked}
				   onTextFieldHandler={this.textFieldHandler} 
				   currentPage ={this.state.location}  
				   validateFields ={this.validateConditions()} 
				   variant ={ADD}/>:null
				}
				
				
			</div>
		);
	 }
}

const mapStateToProps = (state) => {

	return {
		currentOrg: state.appData.currentOrg,
		projectUserList:state.projectManagementData.projectUserList,
		refreshProjectDetails:state.projectManagementData.refreshProjectDetails
	};
};

const mapDispatchToProps = dispatch => ({
	getProjectList: (data) => dispatch(getProjectList(data)),
	updateProjectList:(data)=>dispatch(updateProjectList(data)),
	addToProjectList:(data)=>dispatch(addToProjectList(data)),
	deleteProjectDetails: (data) => dispatch(deleteProjectDetails(data))
});
export default withStyles(styles)(connect(mapStateToProps, mapDispatchToProps)(ProjectManagement));

