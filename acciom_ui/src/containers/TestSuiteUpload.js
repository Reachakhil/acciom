import React from 'react';
import { connect } from 'react-redux';
import XLSX from 'xlsx';
import { Panel, Button, Table, Tabs, Tab } from 'react-bootstrap';
import { showProjectSwitchPage } from '../actions/appActions';
import { 
	onTestSuiteSheetSelect, 
	testCaseSelectionChange, 
	testCaseSelectAllToggle,
	testSuiteFileUploadSuccess,
	testSuiteSheetloadSuccess,
	uploadTestCases,
	resetTestSuiteUploadData, 
	onSheetNameChange,
	resetDataForSheetPage,
	resetDataForCasePage
} from '../actions/testSuiteUploadActions';
import { 
	getAllTestSuites,
} from '../actions/testSuiteListActions';
import { red } from '@material-ui/core/colors';

const TAB_UPLOAD_FILE = 1;
const TAB_UPLOAD_SHEET = 2;
const TAB_UPLOAD_CASES = 3;

class TestSuiteUpload extends React.Component {

	constructor(props) {
		super(props);
		this.state = {
			key: TAB_UPLOAD_FILE,
			sheets:[]
		};
		this.testSuiteFile = null;
		this.selectedSheet = null;
		this.workbook = {};
		this.pages = [];
		this.isNameAlreadyExist = false;
	}

	componentDidMount() {
		this.props.resetTestSuiteUploadData();
	}

	static getDerivedStateFromProps = (nextProps, prevState) => {
		let newState = prevState;

		if (nextProps.moveToSelectSheetPage) {
			newState = { ...prevState, key: TAB_UPLOAD_SHEET };
			nextProps.resetDataForSheetPage();
			nextProps.onSheetSelect(
				nextProps.pages && nextProps.pages.length > 0 
				?
				nextProps.pages[0]:[])
		} else if (nextProps.moveToSelectCasePage) {
			newState = { ...prevState, key: TAB_UPLOAD_CASES };
			nextProps.resetDataForCasePage();
			let project_id = nextProps.currentProject.project_id;
			nextProps.getAllTestSuites(project_id);
			
		} else if (nextProps.redirectToSuiteList) {
			nextProps.history.push('/startup');
		}
		return newState;
	}

	loadTestSuiteFile = (selectedFiles) => {
		const file = selectedFiles[0];
		const fileReader = new FileReader();
	
		fileReader.onload = (evt) => {
			const arrayBuffer = fileReader.result;
			const data = new Uint8Array(arrayBuffer);
			const arr = [];
	
			for (let i = 0; i !== data.length; ++i) {
				arr[i] = String.fromCharCode(data[i]);
			}
			
			const bstr = arr.join("");
			this.workbook = XLSX.read(bstr, {type:"binary"});
	
			if (typeof this.pages !== 'undefined' && this.pages.length > 0) {
				this.pages = [];
			}
	
			for ( let x=0; x!==data.length; x++) {
				if (!this.workbook.SheetNames[x]) {
					break;
				} else {
					this.pages.push(this.workbook.SheetNames[x]);
				}
			}
			this.props.testSuiteFileUploadSuccess(this.pages, selectedFiles[0].name);
		};
	
		this.testSuiteFile = file;
		fileReader.readAsArrayBuffer(file);
	};

	loadTestSuiteSheet = (page) => {
		this.selectedSheet = page;
		const index = this.pages.findIndex(page_p=>page_p===page);
		const sheetName = this.workbook.SheetNames[index];
		const sheet = this.workbook.Sheets[sheetName];
		const resfinal = (XLSX.utils.sheet_to_json(sheet, {raw:true}));
		
		const dbDetailsList = [];
		const allCases = [];
	
		for (let i=0; i<resfinal.length; i++)
		{
			dbDetailsList.push(resfinal[i]['DB Details']); //TO DO:HARD CODED.['Test Class']
			allCases.push({'id':i,'name':resfinal[i]['Test Class'],'selected':false, 'description':resfinal[i]['Description']});
		}
	
		this.props.testSuiteSheetloadSuccess({ dbDetailsList, allCases });
	};

	getPostFilePayloadData = (fileToUpload, selectedSheet, selectedCase, suiteName, executeValue, projectId) => {
		const payload = new FormData();
		payload.append('inputFile',fileToUpload);
		payload.append('sheet_name',selectedSheet);
		payload.append('case_id_list',selectedCase);
		payload.append('suite_name',suiteName);
		payload.append('upload_and_execute',executeValue);
		payload.append('project_id', projectId);
		return payload;
	};

	onUploadBtnClick = (mode) => {
		let suiteName = '';
		const selectedTestCases = [];

		this.props.allCases.forEach((item) => {
			if (item.selected) {
				selectedTestCases.push(item.id);
			}
		});

		this.props.pages.forEach((item) => {
			if (item.selected) {
				suiteName = item.displayName;
			}
		});

		const projectId = this.props.currentProject.project_id;
		const body = this.getPostFilePayloadData(this.testSuiteFile, this.selectedSheet, selectedTestCases, suiteName, mode, projectId);
		
		this.props.uploadTestCases(body);
	};

	render() {
		const MODE_UPLOAD = 0;
		const MODE_UPLOAD_AND_EXECUTE = 1;

		const handleTestSuiteUploadClick = () => {
			document.getElementById("testSuiteUploadFile").click();
		};

		const handleChange = (event) => {
			const selectedFiles = event.target.files;
			if (selectedFiles) {
				this.loadTestSuiteFile(selectedFiles);	
			}
		};

		const handleSheetCheckChange = (page) => {
			this.props.onSheetSelect(page);
		};

		const onContinueClick = (event) => {
			this.props.pages.forEach(page => {
				if (page.selected) {
					this.loadTestSuiteSheet(page.name);
				}
			});
		};

		const handleTestCaseCheckChange = (testCase) => {
			this.props.testCaseSelectionChange(testCase);
		};

		const handleSelectAllChange = () => {
			this.props.testCaseSelectAllToggle();
		};

		const checkNameAlreadyExist = (testSuites,displayName) => {
			let isNameAlreadyExist = false;
			for(let data of testSuites ){
				if(data.test_suite_name === displayName){
					isNameAlreadyExist = true;
					break;
				}
			}
			return isNameAlreadyExist;
		}

		const handleInputChange = (e, index) => {
			this.props.onSheetNameChange({sheetIndex:index,  displayName: e.target.value});
			let testSuites = this.props.testSuites;
			let displayName = e.target.value;
			this.isNameAlreadyExist = checkNameAlreadyExist(testSuites,displayName);
			
		};

		const getSheetsList = () => {
			let element;
			let sheets = this.state.sheets;
			if (this.props.pages.length > 0) {
				const sheetList = this.props.pages.map((page, index) => {
					sheets[index] = {
						name: page.name
					};
					return (
						<div key={index} className='sheetListItem'>
							<label className="form-check-label">
								<input
									type="radio"
									className="form-check-input"
									value={page.name}
									checked={page.selected}
									onChange={ (e) => handleSheetCheckChange(page)}
								/>
								{page.name}
							</label>
						</div>
					);
				});

				element = (
					<div>
						<h5 className="margin-title">Please select the sheet to be loaded</h5>
						<div>{ sheetList } </div>
						<div className="margin-button">
							<Button bsStyle="primary" onClick={ (e) => onContinueClick()}>Load Test Cases</Button> 
						</div>
					</div>
				);
			}
			return element;
		};

		const getTestCasesList = () => {
			let testCasesList = [];
			if (this.props.allCases && this.props.allCases.length > 0) {

				testCasesList = this.props.allCases.map((testCase, index) => {
					return (
						<tr key={index}>
							<td>{testCase.description}</td>
							<td>{testCase.name}</td>
							<td>
								<input
									type="checkbox"
									value={testCase.selected}
									id={testCase.name}
									name={testCase.name}
									checked={testCase.selected}
									onChange={ (e) => handleTestCaseCheckChange(testCase)}
								/>
							</td>
						</tr>	
					)
				});
				
				return (
					<div className='testCaseListContainer'>
						<Panel className='testCaseListPanel'>
							<Panel.Body>
								<Table responsive>
									<thead>
										<tr>
											<th>Test Case Description</th>
											<th>Test Class</th>
											<th>
												<input
													type="checkbox"
													value="Select All"
													id="Select All"
													name="Select All"
													checked= {this.props.selectAll}
													onChange={ (e) => handleSelectAllChange()}
												/> Select All
											</th>
										</tr>
									</thead>
									<tbody>
										{testCasesList}
									</tbody>
								</Table>
								<div>
									<Button bsStyle="primary" onClick={ (e) => this.onUploadBtnClick(MODE_UPLOAD_AND_EXECUTE)} disabled={this.isNameAlreadyExist || !isValid()}>Upload and Execute</Button>								
									<Button bsStyle="primary" onClick={ (e) => this.onUploadBtnClick(MODE_UPLOAD)} disabled={this.isNameAlreadyExist || !isValid()}>Upload</Button> 
								</div>
							</Panel.Body>
						</Panel>
					</div>
				)
			}
		};

		const renderTestSuiteName = () => {
			let element = null;
			let testSuites = this.props.testSuites;
			let i;
			let pages = this.props.pages;
			let selectedPage;
			if(pages.length > 0) {
				for(i=0; i<=pages.length; i++) {
					let page = pages[i];
					if(page && page.selected) {
						selectedPage = page;
						break;
					}
				}
				let displayName = selectedPage ? selectedPage.displayName : '';
				this.isNameAlreadyExist = checkNameAlreadyExist(testSuites,displayName);
				element = (
					<div className="row">
						<h5 className="suite-name-title">Test Suite Name: </h5>
						<input type="textbox" className="suite-test-input" onChange={e => handleInputChange(e,i)} value={ displayName } />
						{this.isNameAlreadyExist &&
							<span style={{color:"red", paddingLeft:"10px"}}>Test suite Name already exist</span>
						}
					</div>
				);
			}
			return element;
		}

		const handleSelect = (key) => {
			this.setState({ key });
		};

		const handleSwitchProject = () => {
			this.props.showProjectSwitchPage(true);
		};
		
		const isValid = () => {
			return this.props.allCases.some((data) => {
				return data.selected === true
			})
		}
		return (
			
			<div id="suite-upload">
				<div>
					<h4 className='pageTitle update-data-profiling-title main_titles'>Update Data Profiling</h4>
					<div className='project-switch brows-btn'><Button className="button-colors" bsStyle="primary" onClick={ (e) => handleSwitchProject()}>Switch Project</Button> </div>
				</div>
				<Tabs activeKey={this.state.key} onSelect={handleSelect} id="controlled-tab-example" >
					<Tab className="updatedataprofilingtab" eventKey={TAB_UPLOAD_FILE} title="Upload Data Profiling">
						<div className='testSuiteUploadOptions'>
							<div className="hideElement">
								<input  id="testSuiteUploadFile" type="file" className="file" placeholder="Upload file" accept=".xlsx" 
									onChange={ (e) => handleChange(e)}/>
							</div>
							<input className="browse-txt" type="textbox" placeholder="&nbsp; example.xlsx" value={this.props.file} disabled/>
							<Button className="button-colors" bsStyle="primary" onClick={ (e) => handleTestSuiteUploadClick()}>Browse File</Button>							
						</div>
					</Tab>
			
					<Tab eventKey={TAB_UPLOAD_SHEET} title="Select Sheet" disabled={this.props.isSheetListPageDisabled}>
						{ getSheetsList() }
					</Tab>

					<Tab eventKey={TAB_UPLOAD_CASES} title="Select Test Cases" disabled={this.props.isCaseListPageDisabled}>
						<div>
							{ renderTestSuiteName() }
						</div>
						{ getTestCasesList() }
					</Tab>
				</Tabs>
			</div>
		)
	}
}

const mapStateToProps = (state) => {
	return {
		currentProject: state.appData.currentProject,
		pages: state.testSuiteUploadData? state.testSuiteUploadData.sheets : [],
		file: state.testSuiteUploadData.file,
		allCases: state.testSuiteUploadData && 
			state.testSuiteUploadData.sheetData ? state.testSuiteUploadData.sheetData.allCases : [],
		selectAll: state.testSuiteUploadData ? state.testSuiteUploadData.selectAll : false,
		isUpdateSuitePageDisabled: state.testSuiteUploadData.isUpdateSuitePageDisabled,
		isSheetListPageDisabled: state.testSuiteUploadData.isSheetListPageDisabled,
		isCaseListPageDisabled: state.testSuiteUploadData.isCaseListPageDisabled,
		moveToSelectSheetPage: state.testSuiteUploadData.moveToSelectSheetPage,
		moveToSelectCasePage: state.testSuiteUploadData.moveToSelectCasePage,
		redirectToSuiteList: state.testSuiteUploadData.redirectToSuiteList,
		testSuites: state.testSuites.testSuiteList? state.testSuites.testSuiteList: [],
	};
};

const mapDispatchToProps = dispatch => ({
	testSuiteFileUploadSuccess: (data) => dispatch(testSuiteFileUploadSuccess(data)),
	testSuiteSheetloadSuccess: (data) => dispatch(testSuiteSheetloadSuccess(data)),
	onSheetSelect: (data) => dispatch(onTestSuiteSheetSelect(data)),
	uploadTestCases: (data) => dispatch(uploadTestCases(data)),
	testCaseSelectionChange: (data) => dispatch(testCaseSelectionChange(data)),
	testCaseSelectAllToggle: () => dispatch(testCaseSelectAllToggle()),
	resetTestSuiteUploadData: () => dispatch(resetTestSuiteUploadData()),
	showProjectSwitchPage: (data) => dispatch(showProjectSwitchPage(data)),
	onSheetNameChange: (data) => dispatch(onSheetNameChange(data)),
	resetDataForSheetPage: () => dispatch(resetDataForSheetPage()),
	resetDataForCasePage: () => dispatch(resetDataForCasePage()),
	getAllTestSuites  : (data)=> dispatch(getAllTestSuites(data)),
});

export default connect(
	mapStateToProps,
	mapDispatchToProps
) (TestSuiteUpload);