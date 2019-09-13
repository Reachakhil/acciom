import React from 'react';
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';
import { Button,  Modal, ButtonGroup, DropdownButton, Item , MenuItem as MenuItemBS  } from 'react-bootstrap';

import clsx from 'clsx';
import { makeStyles, useTheme } from '@material-ui/core/styles';
import Drawer from '@material-ui/core/Drawer';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import List from '@material-ui/core/List';
import CssBaseline from '@material-ui/core/CssBaseline';
import Typography from '@material-ui/core/Typography';
import Divider from '@material-ui/core/Divider';
import IconButton from '@material-ui/core/IconButton';
import MenuIcon from '@material-ui/icons/Menu';
import ChevronLeftIcon from '@material-ui/icons/ChevronLeft';
import ChevronRightIcon from '@material-ui/icons/ChevronRight';
import MenuList from '@material-ui/core/MenuList';
import MenuItem from '@material-ui/core/MenuItem';
import SvgIcon from '@material-ui/core/SvgIcon';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import AccountCircleIcon from '@material-ui/icons/AccountCircle';
import Icon from '@material-ui/core/Icon';

import ChangeOrganisation from '../components/ChangeOrganisation'
import { logoutFromPortal } from '../actions/loginActions';
import { showOrgChangePage } from '../actions/appActions';
import logo from '../assets/images/logo.png';

const drawerWidth = 240;

const useStyles = makeStyles(theme => ({
	root: {
		display: 'flex',
	},
	appBar: {
		zIndex: theme.zIndex.drawer + 1,
		transition: theme.transitions.create(['width', 'margin'], {
			easing: theme.transitions.easing.sharp,
			duration: theme.transitions.duration.leavingScreen,
		}),
		height: `70px`
	},
	appBarShift: {
		marginLeft: drawerWidth,
		width: `calc(100% - ${drawerWidth}px)`,
		transition: theme.transitions.create(['width', 'margin'], {
			easing: theme.transitions.easing.sharp,
			duration: theme.transitions.duration.enteringScreen,
		}),
	},
	menuButton: {
		marginRight: 36,
	},
	hide: {
		display: 'none',
	},
	drawer: {
		width: drawerWidth,
		flexShrink: 0,
		whiteSpace: 'nowrap',
	},

	drawerOpen: {
		width: drawerWidth,
		transition: theme.transitions.create('width', {
			easing: theme.transitions.easing.sharp,
			duration: theme.transitions.duration.enteringScreen,
		}),
	},
	drawerClose: {
		transition: theme.transitions.create('width', {
			easing: theme.transitions.easing.sharp,
			duration: theme.transitions.duration.leavingScreen,
		}),
		overflowX: 'hidden',
		width: theme.spacing(7) + 1,
		[theme.breakpoints.up('sm')]: {
			width: theme.spacing(9) + 1,
		},
	},
	toolbar: {
		display: 'flex',
		alignItems: 'center',
		justifyContent: 'flex-end',
		padding: '0 8px',
		...theme.mixins.toolbar,
	},
	content: {
		flexGrow: 1,
		padding: theme.spacing(3),
	},
	accountbtn : {
		position: 'absolute',
		right: '37px',
		width: '125px',
		height: '30px',
		color: '#3b6d9e',
		fontSize: '16px',
		// textAlign: "center"
	},
	
  	dashboard : {
		color: 'white'
	},
	home : {
		color: 'white'
	},
	startup : {
		color: 'white'
	},
	acciom : {
		color: 'cadetblue'
	},
	acciomimg : {
		width: '70px'
	},
	loginLink : {
	
	}
}

));

const someHandler =() => {
	return (
		<div>
			<a>Forget Password</a>
			<a>Access Token</a>
			<a>LogOut</a>
		</div>
	)
}

const handleShowOrg  = (props, isShow) => {
	props.showOrgChangePage(isShow);
};

const getLoginOptions = (props, classes) => {
	let options = null;
	
	const getLoginElements = () => {
		if (props.loginData && props.loginData.token) {
			return ( <div>
				<DropdownButton id="account_button" className="button-colors"  title="Account" bsStyle="primary" bsSize="small" pullRight noCaret
					onClick={(event) => { event.preventDefault();}}>
					<MenuItemBS eventKey="1" className={classes.width}>
						<Link to="/access_token"  className={classes.width}>Access Token</Link>
					</MenuItemBS>
					<MenuItemBS eventKey="2">
						<Link to="/change_password">Change Password</Link>
					</MenuItemBS>
					
					<MenuItemBS eventKey="4">
						{/* <Link to="/change_password">Change Password</Link> */}
						<span id="change_organisation" onClick={(event) => { handleShowOrg(props, true);}}>Change Organisation</span>
					</MenuItemBS>
					<MenuItemBS eventKey="5">
						<Link to="/user_management">User Management</Link>
					</MenuItemBS>
					<MenuItemBS eventKey="6">
						<Link id="logoutLink" className={classes.loginbtn} onClick={(event) => { event.preventDefault(); props.logoutFromPortal() }}>Logout</Link>
					</MenuItemBS>
				</DropdownButton>
			</div>
			);
		} else {
			return (
				<div>
					<DropdownButton  title="Account" bsStyle="primary" bsSize="small" id="dropdown-no-caret loginLink" pullRight noCaret
						onClick={(event) => { event.preventDefault();}}>
						<MenuItemBS eventKey="3">
							<Link to="/forgot_password">Forgot Password</Link>
						</MenuItemBS>
						<MenuItemBS eventKey="3">
							<Link to='/login'>Login</Link>
						</MenuItemBS>
					</DropdownButton>
				</div>
			);
		}
	};

	options = (
		<div className={classes.accountbtn}>
			{ getLoginElements() }
		</div>
	)

	return options;
};

function NavigationBar(props) {
	const classes = useStyles();
	const theme = useTheme();
	
	const [open, setOpen] = React.useState(false);

	function handleDrawerOpen() {
		setOpen(true);
	}

	function handleDrawerClose() {
		setOpen(false);
	}

	return (
		<div className={classes.root}>
			<CssBaseline />
			<AppBar
				id="db_top_bar"
				position="fixed"
				className={clsx(classes.appBar, {
					[classes.appBarShift]: open,
				})}>
				<Toolbar>
				{/*	<IconButton
						color="inherit"
						aria-label="Open drawer"
						onClick={handleDrawerOpen}
						edge="start"
						className={clsx(classes.menuButton, {
							[classes.hide]: open,
						})}> 
						<MenuIcon />
					</IconButton> */}
					<img className="logo" src={logo} alt="logo" />
					<div className="loginOptions">
						{ getLoginOptions(props, classes) }
					</div>
				</Toolbar> 
			</AppBar>
			<Drawer
				variant="permanent"
				className={clsx(classes.drawer, {
					[classes.drawerOpen]: open,
					[classes.drawerClose]: !open,
				})}
				classes={{
					paper: clsx({
						[classes.drawerOpen]: open,
						[classes.drawerClose]: !open,
					}),
				}}
				open={open} >
				<Divider />
				<List>
					<MenuList className="sideNavBar">
						<MenuItem>
							<ListItemIcon>
								<Link to= {'/dashboard'} color= 'primary' >
									<Icon className={clsx(classes.icon, 'fas fa-business-time fa-2x')} color="primary" />	
								</Link>
							</ListItemIcon>
							<Link to={`/dashboard`} id="dashbcolor" className = {classes.dashboard} className = {classes.hovercolor} > Dashboard </Link> <br />
						</MenuItem>
						<MenuItem>
							<ListItemIcon>
								<Link to={`/test_suite_upload`} className = {classes.home}>
									<Icon className={clsx(classes.icon, 'fas fa-upload fa-2x')} color="primary" />  
								</Link> 
							</ListItemIcon>
							<Link to={`/test_suite_upload`} id="dashbcolor"  className = {classes.home}> Upload Data Profiling </Link> <br />
						</MenuItem>
						<MenuItem>
							<ListItemIcon>
								<Link to ={`/startup`} className = {classes.startup}>
									<Icon className={clsx(classes.icon, 'fas fa-list-alt fa-2x')} color="primary" />
								</Link>
							</ListItemIcon>
							<Link to={`/startup`} id="dashbcolor"  className = {classes.startup}>Data Profiling</Link>
						</MenuItem>
						<MenuItem>
							<ListItemIcon>
								<Link to ={`/view_db_details`} className = {classes.startup}>
									<Icon className={clsx(classes.icon, 'fas fa-database fa-2x')} color="primary" />
								</Link>
							</ListItemIcon>
							<Link to={`/view_db_details`} id="dashbcolor"  className = {classes.startup}>View DB Details</Link>
						</MenuItem>
						
					</MenuList>
				</List>
			</Drawer>
			<div className="left_dropdown_btn">
						{open ? <IconButton className="leftbar_closebtn" onClick={handleDrawerClose}>
							<ChevronLeftIcon />
						</IconButton> : 
							<IconButton
								color="inherit"
								aria-label="Open drawer"
								onClick={handleDrawerOpen}
								edge="start"
								className={clsx(classes.menuButton,classes.leftbarscrollbtn, {
								[classes.hide]: open,
							})}> 
							<MenuIcon />
						</IconButton>}
						</div>
		</div>
	);
}

const mapStateToProps = (state) => {
	return {
		loginData: state.loginData
	}
};
const mapDispatchToProps = (dispatch) => ({
	logoutFromPortal: () => dispatch(logoutFromPortal()),
	showOrgChangePage: (data) => dispatch(showOrgChangePage(data))
});

export default connect(mapStateToProps, mapDispatchToProps)(NavigationBar);