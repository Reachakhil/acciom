import React from 'react';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';

function Header(props) {
    return(
        <TableHead>
            <TableRow  className="table-row">
                {props.headerData.map((item,key)=>(
                !item.required?<TableCell className="tableCell" >{item.label}</TableCell>:
                <TableCell className="tableCell">{item.label}<span className="mandatory">*</span></TableCell>
                ))}      
            </TableRow>
        </TableHead>
    )
}
export default (Header);
