import React, { Component } from 'react';
import axios from 'axios';
// import API from './utils/api'
import {PacmanLoader } from 'react-spinners';
import {Button} from 'reactstrap';
import './App.css';
import Transactions from './Components/transactions/Transactions';

class App extends Component {
  
  state = {
    requestError : null,
    minedBlocks : [],
    loading: true,
  };
  
  componentDidMount() {
  
    axios.get('http://localhost:5000/chain')
    .then(response => response.data )
    .then(data => this.setState({minedBlocks: data.chain, loading:false}))
    .catch(err => {
      this.setState({requestError: err})
    })
  };

  refreshHandler = () => {

    this.setState((state) => {
      return {
        ...state,
        loading: true,
      }
    })

   setTimeout(() => {
     axios.get('http://localhost:5000/chain')
       .then(response => response.data)
       .then(data => this.setState((state) => {
         return {
           ...state,
           minedBlocks: data.chain,
           loading: false,
         }
       }))
       .catch(err => {
         this.setState({ requestError: err })
       })
   }, 3000);
    
  }

  render() {

    let displayResult;

    if (this.state.loading === false) {
      displayResult = (
        this.state.minedBlocks.map((item, index) => (
          <div>
            <h1>
              Bloco {item.index}
            </h1>
            <div>
              <Transactions data={item.transactions} />
            </div>
          </div>
        )
      )
      )}
    else {
      displayResult = (
      <div className='icon_container'>
          <PacmanLoader color='#ff9900'   className='loading_icon'/>
      </div>
      )
    }

    return (
      <div className='container'>
        <Button color='primary' size = 'lg' block className='refresh_button' onClick={this.refreshHandler}> Atualizar </Button>
        
        {displayResult}
        {/* {this.state.minedBlocks.map((item, index) => (
          <div>
            <h1> 
              Bloco {item.index} 
            </h1>
            <div>
              <Transactions data={item.transactions}/>
            </div>
          </div> */}
      </div>  
    );
  }
}

export default App;
