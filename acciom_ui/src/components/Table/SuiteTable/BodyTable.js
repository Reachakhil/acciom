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

function BodyTable(props) {
    console.log("9")
    console.log(props.BodyData)
    return(
        <TableBody> 
            {props.BodyData.map((eachrow,index) =>{
            return(
            <TableRow className="table-create-suite-row">
                    {
                    <TableCell className="DropDown-SelectClass">
                        <Select
                            style={{width:'10vw'}}
                            value={eachrow['test_case_class']}
                             > 
                            {/* {this.showClass(this.props.classNameList,classes)} */}
                            <MenuItem >
                                22
                                </MenuItem>
                        </Select>
                    </TableCell>
                    }
                    {
                    <TableCell>
                        <TextField autoFocus={true}
                        // disabled={!this.state.suiteData[index]['test_case_class']}
                        placeholder="description" value={eachrow.test_description}
                        onChange={()=> this.handleChange(event,index,2) }/>
                    </TableCell>}              
                    <TableCell >
                                
                        <Select
                        // disabled={!this.state.suiteData[index]['test_case_class']}
                        style={{width:'10vw'}}
                        value={this.state.suiteData[index]['source_db_existing_connection']}
                        onChange={ (e) => this.handleExistingDBTypeChange(index,e,3) }> 
                        {this.renderExistingDBTypes(this.props.allConnections,classes)}
                        </Select>
                    </TableCell>
                    <TableCell>
                    
                        <Select
                        // disabled={!this.state.suiteData[index]['test_case_class']}
                        style={{width:'10vw'}}
                        value={this.state.suiteData[index]['target_db_existing_connection']}
                        onChange={ (e) => this.handleExistingDBTypeChange(index,e,4) }> 
                        {this.renderExistingDBTypes(this.props.allConnections,classes)}
                        </Select>
                    </TableCell>        

                    <TableCell  >
                        <TextField autoFocus={true} 
                        // disabled={!this.state.suiteData[index]['test_case_class']}
                        value={eachrow.source_table} 
                        placeholder="source table"
                        error={(ISSPACE).test((eachrow.source_table).trim())}
                        helperText={(ISSPACE).test((eachrow.source_table).trim())?"Table cannot have space":""}
                        onChange={()=> this.handleChange(event,index,5)}  />
                    </TableCell>  

                    <TableCell>
                        <TextField autoFocus={true}
                        error={(ISSPACE).test((eachrow.target_table).trim())}
                        placeholder="target table"
                        // disabled={!this.state.suiteData[index]['test_case_class']}
                        helperText={(ISSPACE).test((eachrow.target_table).trim())?"Table cannot have space":""}
                        value={eachrow.target_table}
                        onChange={()=> this.handleChange(event,index,6)}  />
                    </TableCell>
                    <TableCell >
                        <TextField autoFocus={true}  placeholder="column" value={eachrow.columns}
                        // disabled={!this.state.suiteData[index]['test_case_class']}
                        onChange={()=> this.handleChange(event,index,7)} />
                    </TableCell>           
                    
                    
                    <TableCell >
                        <Tooltip  title={this.showData(eachrow.source_query,8)} aria-label="add">
                        <EditRounded onClick={(e) => {this.showDialog(index,8)}}/>
                        </Tooltip>
                    {/* <div className={classes.tablepopup} style={{textDecoration:"underline", color:"blue", cursor:"pointer"}} onClick={(e) => {this.showDialog(index,8)}}>{this.showData(eachrow.source_query,8)}</div> */}
                    
                    </TableCell>           
                    
                    <TableCell className={classes.tablecell}>
                        <Tooltip title={this.showData(eachrow.source_query,9)}  aria-label="add">
                            <EditRounded onClick={(e) => {this.showDialog(index,9)}}/>
                            {/* <div className={classes.tablepopup} style={{textDecoration:"underline", color:"blue", cursor:"pointer"}} onClick={(e) => {this.showDialog(index,9)}}>{this.showData(eachrow.target_query,9)}</div> */}
                            </Tooltip>
                    </TableCell>
                    
                    <TableCell >
                        {this.showMinus()?
                        
                            <IconButton  onClick={() => this.deleteRow(index)}>
                                <MinusCircle />
                            </IconButton>
                            :""
                        }
                    </TableCell>
            </TableRow>
            
            )})}
        </TableBody>
        )  
}
export default (BodyTable);
