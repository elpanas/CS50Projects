class AppSearch extends React.Component {
    constructor(props) {
        super(props);
        this.state = {value: ''};
        this.handleChange = this.handleChange.bind(this);
      }

    handleChange(event) { this.setState({ value: event.target.value }); }

    render() {
        return (            
                <FormComp id="formsearch"
                          class="mx-auto text-center"
                          style={{width: '60%'}}
                          action="/estabsearch"
                          method="GET">
                    <DivComp class="form-group" >                                      
                        <InputComp autofocus={true}
                                    class="form-control"
                                    type="text"
                                    name="place"
                                    placeholder="Place"
                                    required={true}
                                    value={this.state.value}
                                    onChange={this.handleChange} />   
                    </DivComp> 
                    <DivComp class="form-group" >                                      
                        <InputComp autofocus={true}
                                    class="form-control"
                                    type="number"
                                    name="zipcode"
                                    placeholder="zipcode"
                                    required={true}
                                    value={this.state.value}
                                    onChange={this.handleChange} />   
                    </DivComp> 
                    <input type="submit" className="btn btn-dark" value="Search" />
                </FormComp>
        );
    }
}

class AppLogin extends React.Component {
    constructor(props) {
        super(props);
        this.state = {value: ''};
        this.handleChange = this.handleChange.bind(this);
      }

    handleChange(event) { this.setState({ value: event.target.value }); }

    render() {
        return (            
                <FormComp id="formlogin"
                          class="mx-auto"
                          style={{width: '60%'}}
                          action="/login"
                          method="POST">
                    <DivComp class="form-group" >  
                        <LabelComp for="usernameid" name="Username"/>                                  
                        <InputComp id="usernameid"
                                    autofocus={true}
                                    class="form-control"
                                    type="text"
                                    name="username"
                                    placeholder="Username"
                                    required={true}
                                    value={this.state.value}
                                    onChange={this.handleChange} />                          
                    </DivComp>
                    <DivComp class="form-group" >  
                        <LabelComp for="pswid" name="Password"/>                                  
                        <InputComp id="pswid"
                                    autofocus={false}
                                    class="form-control"
                                    type="password"
                                    name="password"
                                    placeholder="Password"
                                    required={true}
                                    value={this.state.value}
                                    onChange={this.handleChange} />                          
                    </DivComp>                     
                    <p class="text-center">
                        <input type="submit" className="btn btn-dark" value="Login" />
                    </p>                    
                    <p class="mx-auto text-center">
                        Don't have an account? <a href="/register">Register here.</a>
                    </p>
                </FormComp>
        );
    }
}

class AppReg extends React.Component {
    constructor(props) {
        super(props);
        this.state = {value: ''};
        this.handleChange = this.handleChange.bind(this);
      }

    handleChange(event) { this.setState({ value: event.target.value }); }

    render() {
        return (            
                <FormComp id="formreg"
                          class="mx-auto"
                          style={{width: '60%'}}
                          action="/register"
                          method="POST">
                    <DivComp class="form-group" >
                        <DivComp class="form-row">
                            <DivComp class="col">
                            <InputComp autofocus={true}
                                        class="form-control"
                                        type="text"                                    
                                        placeholder="First Name"                                    
                                        value={this.state.value}
                                        onChange={this.handleChange} />   
                            </DivComp>
                        </DivComp>              
                    </DivComp>
                    <DivComp class="form-group">
                        <InputComp class="form-control"
                                    type="email"
                                    name="email"                                    
                                    placeholder="Email Address"                                    
                                    value={this.state.value}
                                    onChange={this.handleChange} /> 
                    </DivComp>
                    <DivComp class="form-group">
                        <InputComp autofocus={true}
                                    required={true}
                                    class="form-control"
                                    type="username"
                                    name="username"                                    
                                    placeholder="Username"                                    
                                    value={this.state.value}
                                    onChange={this.handleChange} /> 
                    </DivComp>
                    <DivComp class="form-group">
                        <InputComp  required={true}
                                    class="form-control"
                                    type="password"
                                    name="password"                                    
                                    placeholder="Password"                                    
                                    value={this.state.value}
                                    onChange={this.handleChange} /> 
                    </DivComp>
                    <DivComp class="form-group">
                        <InputComp  required={true}
                                    class="form-control"
                                    type="password"
                                    name="confirmation"                                    
                                    placeholder="Confirm Password"                                    
                                    value={this.state.value}
                                    onChange={this.handleChange} /> 
                    </DivComp>
                    <p class="text-center">
                        <input type="submit" className="btn btn-dark" value="Register" />
                    </p>                   
                    <DivComp class="form-group">
                        <DivComp class="form-check">
                            <InputComp id="gridCheck"
                                        class="form-check-input"
                                        type="checkbox"
                                        name="manager" />
                            <LabelComp class="form-check-label"
                                       for="gridCheck"
                                       name="Check me out if you are a manager">                                        
                            </LabelComp>
                        </DivComp>
                    </DivComp>                    
                    <DivComp class="mx-auto text-center"
                             style={{width: '60%'}}>
                        Already have an account? <a href="/login">Log In here.</a>
                    </DivComp>
                </FormComp>
        );
    }
}


class FormComp extends React.Component {  
    render() {
        return (
            <form id={this.props.id}
                  className={this.props.class}
                  style={this.props.style} 
                  action={this.props.action}
                  method={this.props.method}>
                      {this.props.children}
            </form>                  
        );
    }
}


class LabelComp extends React.Component {
    render() {
        return(
            <label for={this.props.for}><strong>{this.props.name}</strong></label>
        );
    }
}


class InputComp extends React.Component {
    render() {
        return <input   id={this.props.id}
                        autoFocus={this.props.autofocus}
                        className={this.props.class}
                        type={this.props.type}
                        name={this.props.name}
                        placeholder={this.props.placeholder}
                        required={this.props.required}/>; 
    }    
}

class DivComp extends React.Component {
    render() {
        return (
        <div className={this.props.class}>{this.props.children}</div>
        );
    }
}

const login = document.querySelector('#login');

if (login) {
    document.querySelector('#login').addEventListener('click', () => LoginPage());
    document.querySelector('#register').addEventListener('click', () => RegisterPage());
}

function IndexPage() {
    deActivateLinks('#home');
    ReactDOM.render(<AppSearch />, document.querySelector('#app'));
}

function LoginPage() {
    deActivateLinks('#login');
    ReactDOM.render(<AppLogin />, document.querySelector('#app'));
}


function RegisterPage() {
    deActivateLinks('#register');
    ReactDOM.render(<AppReg />, document.querySelector('#app'));
}


function deActivateLinks(id) {
    document.querySelector('#home').className = 'nav-link';
    document.querySelector(id).className = 'nav-link active';  

    const login = document.querySelector('#login');

    if (login) {
        document.querySelector('#login').className = 'nav-link';
        document.querySelector('#register').className = 'nav-link';
    }    
}

IndexPage();