import React from 'react';
import TableRow from '@material-ui/core/TableRow';
import TableCell from '@material-ui/core/TableCell';
import TableBody from '@material-ui/core/TableBody';
import { TextField } from '@material-ui/core';
import MenuItem from '@material-ui/core/MenuItem';
import '../../../css/Db-ui-styles.css'
import IconButton from '@material-ui/core/IconButton';
import MinusCircle from '@material-ui/icons/RemoveCircle';
import EditRounded from '@material-ui/icons/EditRounded';
import Select from '@material-ui/core/Select';
import Tooltip from '@material-ui/core/Tooltip';
import { ISSPACE } from '../../../constants/FieldNameConstants';


class BodyTable extends React.Component {
    constructor(props){
        super(props);
    }
    handleChange = (e,index,v_index) =>{
        this.props.handleChangeWrap(e,index,v_index)
    }
    render(){
    return(
        <TableBody> 
            {this.props.BodyData.map((eachrow,index) =>{
            return(
            <TableRow className="table-create-suite-row">
                    {
                    <TableCell className="DropDown-SelectClass">
                        <Select
                            style={{width:'10vw'}}
                            value={eachrow['test_case_class']}
                             > 
                            {/* {this.showClass(this.props.classNameList,classes)} */}
                           
                            {this.props.showClass}
                            
                        </Select>
                    </TableCell>
                    }
                    {
                    <TableCell>
                        <TextField autoFocus={true}
                            placeholder="description" value={eachrow.test_description}
                            onChange={()=> this.handleChange(event,index,2) }
                           />
                    </TableCell>}              
                    <TableCell >
                                
                        <Select
                        style={{width:'10vw'}}
                        > 
                        {this.props.renderExistingDBTypes}
                        </Select>
                    </TableCell>
                    <TableCell>
                        <Select
                        // disabled={!this.state.suiteData[index]['test_case_class']}
                        style={{width:'10vw'}}> 
                        {this.props.renderExistingDBTypes}
                        </Select>
                    </TableCell>        

                    <TableCell  >
                        <TextField autoFocus={true} 
                        // disabled={!this.state.suiteData[index]['test_case_class']}
                        value={eachrow.source_table} 
                        placeholder="source table"
                        error={(ISSPACE).test((eachrow.source_table).trim())}
                        helperText={(ISSPACE).test((eachrow.source_table).trim())?"Table cannot have space":""}
                          />
                    </TableCell>  

                    <TableCell>
                        <TextField autoFocus={true}
                        error={(ISSPACE).test((eachrow.target_table).trim())}
                        placeholder="target table"
                        // disabled={!this.state.suiteData[index]['test_case_class']}
                        helperText={(ISSPACE).test((eachrow.target_table).trim())?"Table cannot have space":""}
                        value={eachrow.target_table}
                         />
                    </TableCell>
                    <TableCell >
                        <TextField autoFocus={true}  placeholder="column" value={eachrow.columns}
                        // disabled={!this.state.suiteData[index]['test_case_class']}
                        />
                    </TableCell>           
                    
                    
                    <TableCell >
                        <Tooltip aria-label="add">
                        <EditRounded />
                        </Tooltip>
                    {/* <div className={classes.tablepopup} style={{textDecoration:"underline", color:"blue", cursor:"pointer"}} onClick={(e) => {this.showDialog(index,8)}}>{this.showData(eachrow.source_query,8)}</div> */}
                    
                    </TableCell>           
                    
                    <TableCell>
                        <Tooltip aria-label="add">
                            <EditRounded />
                            {/* <div className={classes.tablepopup} style={{textDecoration:"underline", color:"blue", cursor:"pointer"}} onClick={(e) => {this.showDialog(index,9)}}>{this.showData(eachrow.target_query,9)}</div> */}
                            </Tooltip>
                    </TableCell>
                    
                    <TableCell >
                       
                        
                            <IconButton >
                                <MinusCircle />
                            </IconButton>
                    </TableCell>
            </TableRow>
            
            )})}
        </TableBody>
        ) 
        
                    }
}
export default (BodyTable);
