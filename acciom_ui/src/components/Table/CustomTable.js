import React from 'react';
import TableToolbar from './TableToolbar';
import TableHeader from './TableHeader';
import TableListBody from './TableListBody';
import TablePagination from '@material-ui/core/TablePagination';
import { withStyles } from '@material-ui/core/styles';
import Paper from '@material-ui/core/Paper';
import { Table } from '@material-ui/core';
import { PROJECTNAME, PROJECTDESCRIPTION, ORGANIZATIONNAME } from '../../constants/FieldNameConstants';


const desc = (a, b, orderBy) => {
    if (b[orderBy] < a[orderBy]) {
      return -1;
    }
    if (b[orderBy] > a[orderBy]) {
      return 1;
    }
    return 0;
  }
  
const stableSort = (array, cmp) => {
    const stabilizedThis = array.map((el, index) => [el, index]);
    stabilizedThis.sort((a, b) => {
      const order = cmp(a[0], b[0]);
      if (order !== 0) return order;
      return a[1] - b[1];
    });
    return stabilizedThis.map(el => el[0]);
}
  
const getSorting = (order, orderBy) => {
    return order === 'desc' ? (a, b) => desc(a, b, orderBy) : (a, b) => -desc(a, b, orderBy);
}
  
const searchingFor = (search,headers) => {

    return function(sortData){
   
      return headers.some(data => {
      
        return sortData[data.id] !== null && sortData[data.id].toLowerCase().includes(search.toLowerCase());
      });
    }
}


const styles = theme => ({
    root: {
      marginTop: theme.spacing.unit * 3,
    },
    tableWrapper: {
      overflowX: 'auto'
    },
    table: {
      minWidth: 900,
    
     
     
    },
  
  });

class CustomTable extends React.Component {
    constructor(props){
        super(props);
        this.state = {
          order: 'asc',
          orderBy: '',
          page: 0,
          rowsPerPage: 10,
          search:'',      
        };
    }

    handleSort = (property) => {
      const orderBy = property;
      let order = 'desc';
      if (this.state.orderBy === property && this.state.order === 'desc') {
        order = 'asc';
      }
      this.setState({ order, orderBy });
    };

    handleChangePage = (event, page) => {
      this.setState({ page });
    };
  
    handleChangeRowsPerPage = event => {
      this.setState({ rowsPerPage: event.target.value, page:0 });
    };

    handleClear=()=>{
      this.setState({search:''});
    }
    handleSearch=(event)=>{
      this.setState({search:event.target.value})
    }
   

    render(){
      const {classes, headers, bodyData, actionLabel,editIdx,handleChange,projectNameValue,projectDescriptionValue,orgNameValue,orgDescriptionValue} = this.props;
      const { order, orderBy, page, rowsPerPage, search } = this.state;
        return(
          <Paper className="commonTablePaperMargin">
            <Table size='medium'>
            <TableToolbar
            handleSearch = {this.handleSearch}
            handleClear = {this.handleClear}
            search = {search}
            />
            <div className={classes.tableWrapper}>
              <Table className={classes.table} aria-labelledby="tableTitle" size='medium'>
              <TableHeader 
                headers={headers}
                handleSort={this.handleSort}
                actionLabel={actionLabel} 
                order = {order}
                orderBy = {orderBy}
              />
              <TableListBody
                bodyData = {bodyData} 
                order = {order}
                orderBy = {orderBy}
                page = {page}
                rowsPerPage = {rowsPerPage}
                search = {search}
                stableSort = {stableSort}
                getSorting = {getSorting}
                headers = {headers}
                searchingFor={searchingFor}
                editIdx={editIdx}
                handleChange={handleChange}
                projectNameValue={projectNameValue}
                projectDescriptionValue={projectDescriptionValue}
                orgNameValue={orgNameValue}
                orgDescriptionValue={orgDescriptionValue}
                />
              </Table>
            </div>
            <TablePagination
              rowsPerPageOptions={[10,15,20,25]}
              component="div"
              count={bodyData.length}
              rowsPerPage={rowsPerPage}
              page={page}
              backIconButtonProps={{
                'aria-label': 'Previous Page',
              }}
              nextIconButtonProps={{
                'aria-label': 'Next Page',
              }}
              onChangePage={this.handleChangePage}
              onChangeRowsPerPage={this.handleChangeRowsPerPage}
          />
          </Table>
          </Paper>
        )
    }
}

export default withStyles(styles)(CustomTable);