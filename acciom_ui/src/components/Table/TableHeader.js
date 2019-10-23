import React from 'react';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import TableSortLabel from '@material-ui/core/TableSortLabel';
import { withStyles } from '@material-ui/core/styles';



function TableHeader(props) {
    const { headers, orderBy, order, handleSort, actionLabel,classes } = props;
    return(

        <TableHead className="commonTableHead">
            <TableRow className="commonTableLineheight">
                {headers.map(header => (
                    <TableCell
                        className="commonTableData"

                        key={header.id}
                        align='left'
                    
                        sortDirection={orderBy === header.id ? order : false}
                      
                    >
                        <TableSortLabel
                            className="commonTableHovercolor"
                            direction={order}
                            onClick={() => handleSort(header.id)}
                            align ='left'
                        
                        >
                    
                        {header.label}
                        </TableSortLabel>
                    </TableCell>
                ))}

                    <TableCell 
                    align ='right'
                   
                     className="commonTableCellWidth"
                 >
                        {actionLabel}
                    </TableCell>
            </TableRow>
        </TableHead>
    )
}
export default (TableHeader);
