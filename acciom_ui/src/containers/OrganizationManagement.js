import React, { Component, Fragment } from 'react';
import { withStyles } from '@material-ui/core/styles';
import { connect } from 'react-redux';
import {getDetailsOrganizationList,addToOrganizationList,updateOrganizationList,deleteOrganizationDetails} from '../actions/organizationManagementActions';
import { ORGANIZATIONNAME, ORGANIZATIONDESCRIPTION, ORGNAME, DESCRIPTION, ACTION, SMALL, ADDORGANIZATION, ADD, ORGANIZATION, ORG_TEXTBOX_NAME, ORG_TEXTBOX_DESC, DELETE, ORJDESCTEXT, ORJNAMETEXT } from '../constants/FieldNameConstants';
import CustomTable from '../components/Table/CustomTable';
import EditIcon from '@material-ui/icons/Edit';
import DeleteIcon from '@material-ui/icons/Delete';
import CheckIcon from '@material-ui/icons/Check';
import Clear from '@material-ui/icons/Clear';
import GroupIcon from '@material-ui/icons/Group';
import { Button} from 'react-bootstrap';
import CustomModal from '../components/CommonModal/CustomModal';
import { toast } from 'react-toastify';


const styles = theme => ({

	IconClass:{
		marginBottom:'-5px',
		marginLeft:'3px'
	}
});
class OrganizationManagement extends Component {
    
    textFieldHandler=()=>{
  
        if(event.target.name ===ORG_TEXTBOX_NAME){
        
         this.setState({organizationNameAdd:event.target.value})
    
        }
        
       else if(event.target.name ===ORG_TEXTBOX_DESC){
    
        this.setState({organizationDescriptionAdd:event.target.value})
    
        }
        
      }
    
    handleAddButtonHandler=()=>{
       
        this.setState({showAddConfirmationDialog:true});
    }
    cancelBtnClicked=()=>{
        this.hideUserInfoPopUp();
    }
    saveBtnClicked=()=>{
        let addToOrganizationDetails = {};
   
        addToOrganizationDetails={
              org_name:this.state.organizationNameAdd,
			  org_description:this.state.organizationDescriptionAdd,
				
            };
            if(this.validateConditions()){
                this.props.addToOrganizationList(JSON.stringify(addToOrganizationDetails));
                this.hideUserInfoPopUp();
            }
       
    }
    hideUserInfoPopUp=()=>{
        this.setState({showAddConfirmationDialog:false,organizationNameAdd:'',organizationDescriptionAdd:''});
    }
    validateConditions =()=>{
        const {organizationNameAdd ,organizationDescriptionAdd} =this.state;
        
        if(organizationNameAdd.length>0 && organizationDescriptionAdd.length>0){
            return true
           }
        return false
    }
    editHandler=(index)=>{
        
        this.setState({editIdx:index});
            const localOrgList = [...this.state.orgUserList];
        
		
            this.setState({organizationName:localOrgList[index].org_name});
            this.setState({organizationNameInitialValue:localOrgList[index].org_name});
            this.setState({organizationDescription:localOrgList[index].org_description});
            this.setState({organizationDescriptionInitialValue:localOrgList[index].org_description});
         

    }
    saveDataHandler=(index)=>{	
		
        const localOrgListHandler = [...this.state.orgUserList];
    
        localOrgListHandler[index].org_name = this.state.organizationName;
        localOrgListHandler[index].org_description = this.state.organizationDescription;
      
        let upDateOrgDetails = {};

        upDateOrgDetails={
            org_name:localOrgListHandler[index].org_name,
            org_description:localOrgListHandler[index].org_description,
            org_id:localOrgListHandler[index].org_id
        };
        if(localOrgListHandler[index].org_description.length ==0){
      
            toast.error(ORJDESCTEXT);
           
        }
        else 
        if(localOrgListHandler[index].org_name.length ==0){
          
            toast.error(ORJNAMETEXT);

        }
        
if(localOrgListHandler[index].org_name.length >0 && localOrgListHandler[index].org_description.length>0){
    this.props.updateOrganizationList(JSON.stringify(upDateOrgDetails));
    this.setState({editIdx:-1});
}


             
    }
    handleChangeHandler=(event)=>{
       
            if(event.target.name ===ORGANIZATIONNAME  ){
          
                this.setState({organizationName:event.target.value});
                }
                else if(event.target.name ===ORGANIZATIONDESCRIPTION ){
             
                    this.setState({organizationDescription:event.target.value});
                }

    }
  
    clearDataHandler=(index)=>{
        const clearOrgListHandler = [...this.state.orgUserList];
    
        clearOrgListHandler[index].org_name = this.state.organizationName;
        clearOrgListHandler[index].org_description = this.state.organizationDescription;
      
        if(clearOrgListHandler[index].org_description.length ==0){
            clearOrgListHandler[index].org_description=this.state.organizationDescriptionInitialValue;
            this.setState({organizationDescription:clearOrgListHandler[index].org_description});
        }
      if(clearOrgListHandler[index].org_name.length ==0){
        clearOrgListHandler[index].org_name=this.state.organizationNameInitialValue;
        this.setState({organizationName:  clearOrgListHandler[index].org_name})

      }
			this.setState({editIdx:-1});
    }

    deleteItemHandler = (deleteOrgId)=>{	 
        this.setState({showDeleteConfirmationDialog:true, deleteConnectionID:deleteOrgId});
    }

    onYesBtnClickHandler=()=>{
        const organisationId = {
				 
            org_id: this.state.deleteConnectionID
            };
            
            this.props.deleteOrganizationDetails(JSON.stringify(organisationId));
        
        this.hideConfirmationopup();
    }

    onNoBtnClickHandler=()=>{
      
        this.hideConfirmationopup();

     }
     hideConfirmationopup = () => {
        this.setState({showDeleteConfirmationDialog: false ,deleteConnectionID:null});
    }
    static getDerivedStateFromProps = (nextProps, prevState) => {
       
        if(nextProps.refreshOrganizationDetails){
         
	
            nextProps.getDetailsOrganizationList();
            return {
                prevState
            };
        }
     
            if(nextProps.organizationUserList.length === 0){
                nextProps.getDetailsOrganizationList();
                return {
                    prevState
                     };

                  }
                  if(prevState.organizationUserList!== nextProps.organizationUserList){
                    return {
                        ...prevState,
                        orgUserList: nextProps.organizationUserList
                        };
        
                }
            
		
    }
   
    constructor(props) {
		super(props);
		this.state = {
            headers : [
				{ id: ORGANIZATIONNAME,  label: ORGNAME },
				{ id: ORGANIZATIONDESCRIPTION,  label: DESCRIPTION },
              ],
              orgUserList:[],
              showAddConfirmationDialog:false,
              organizationNameAdd:'',
              organizationDescriptionAdd:'',
              organizationName:'',
              organizationDescription:'',
              location:ORGANIZATION,
              editIdx:-1,
              showDeleteConfirmationDialog:false,
              organizationDescriptionInitialValue:'',
              organizationNameInitialValue:'',
              deleteConnectionID:null

        }
    }
    render(){
        const {headers,orgUserList}=this.state;
        const orgModifyData=[];
      
        if(orgUserList){
			orgUserList.forEach((org,index) => {
				orgModifyData.push({
					org_name: org.org_name,
					org_description: org.org_description,
				
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
							  onClick ={() =>{this.deleteItemHandler(org.org_id);}}
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
                           onClick={()=>this.clearDataHandler(index)}
                        />
						</Fragment>

					)
				});

			});
            
		}
        return(
            <Fragment>
                	<div>
				<GroupIcon className=" organizationManagementIcon" />
			&nbsp; &nbsp;

				
                    <label className="main_titles projectManagementMargin" >
                    Organization Management
                    </label>
					<Button 
					className="backbutton_colors_project addUserButton"
					onClick={this.handleAddButtonHandler}
                    >
                    {ADDORGANIZATION}
                    </Button>


				</div>
                <CustomTable
                  headers={headers}
                  bodyData={orgModifyData}
                  actionLabel={ACTION}
                  editIdx ={this.state.editIdx}
                  orgNameValue ={this.state.organizationName}
				  orgDescriptionValue ={this.state.organizationDescription}
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
                  this.state.showAddConfirmationDialog? 
                  <CustomModal
				   organizationNameAdd={this.state.organizationNameAdd}
				   organizationDescriptionAdd={this.state.organizationDescriptionAdd}
				   onCancelBtnClicked ={this.cancelBtnClicked}
				   onSaveBtnClicked ={this.saveBtnClicked}
				   onTextFieldHandler={this.textFieldHandler} 
				   currentPage ={this.state.location}  
				   validateFields ={this.validateConditions()} 
				   variant ={ADD}
                   />:null
				}
            </Fragment>
        )
    }

}
const mapStateToProps = (state) => {
    return{
        currentOrg: state.appData.currentOrg,
        organizationUserList:state.organizationManagementData.organizationUserList,
        refreshOrganizationDetails:state.organizationManagementData.refreshOrganizationDetails
    };
}
const mapDispatchToProps =dispatch=>({
    getDetailsOrganizationList: (data) => dispatch(getDetailsOrganizationList(data)),
    addToOrganizationList:(data)=>dispatch(addToOrganizationList(data)),
    updateOrganizationList:(data)=>dispatch(updateOrganizationList(data)),
    deleteOrganizationDetails:(data)=>dispatch(deleteOrganizationDetails(data)),
   
})
export default withStyles(styles)(connect(mapStateToProps, mapDispatchToProps)(OrganizationManagement));
