import React from 'react';
import TableRow from '@material-ui/core/TableRow';
import TableCell from '@material-ui/core/TableCell';
import TableBody from '@material-ui/core/TableBody';
import { TextField } from '@material-ui/core';
import { PROJECTNAME } from '../../constants/FieldNameConstants';

function TableListBody(props) {
    const {page, rowsPerPage, orderBy, order, search, bodyData, headers, stableSort, getSorting, searchingFor,editIdx,handleChange,projectNameValue,projectDescriptionValue } = props;

    return(

        <TableBody className="commonTableBody">

            {bodyData.length > 0 &&
            stableSort(bodyData, getSorting(order, orderBy))
            .filter(searchingFor(search,headers))
            .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
             .map((item,index) => {
               let currentIndex =rowsPerPage*page+index;
                    const currentlyEditing =editIdx===currentIndex
                    return(
                <TableRow  tabIndex={-1} key={index} >
                    { headers.map(header => {
                        
                        return(
                        <TableCell key={`${header.id}-${index}`}
                       className="commonTableCellTextColor" >
                            {currentlyEditing?  
                            <TextField
                            name ={header.id}
                            onChange={(e) =>handleChange(e)}
                            value={header.id === PROJECTNAME ? projectNameValue : projectDescriptionValue}
  
                            />:item[header.id]}
                        </TableCell>
                  )})}
                    <TableCell align="right"
                    padding="checkbox"
                    className="commonTableCellBorder"
                  
                    >
                        {currentlyEditing?item.editingIconAction:item.action}
                    </TableCell>
                  
                </TableRow>
          
                 ) })
            }
        </TableBody>
    )
}
export default (TableListBody);
