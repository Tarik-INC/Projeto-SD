import React, { Component } from 'react';
import API from './utils/api'
import axios from 'axios'
import { PacmanLoader } from 'react-spinners';
import { Button } from 'reactstrap';
import './App.css';
import Transactions from './Components/transactions/Transactions';
import Sound from 'react-sound';


class App extends Component {

  state = {
    requestError: null,
    minedBlocks: [],
    loading: true,
    isMining: false,
    nodes: [],
  };

  componentDidMount() {

    API.get('nodes')
      .then(response => response.data)
      .then(data => this.setState({ nodes: data }))
      .catch(err => {
        this.setState({ requestError: err })
      })

    API.get('chain')
      .then(response => response.data)
      .then(data => this.setState({ minedBlocks: data.chain, loading: false }))
      .catch(err => {
        this.setState({ requestError: err })
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
      API.get('chain')
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

  miningHandler = () => {

    this.setState({ isMining: true })


    axios.get("http://localhost:5000/mine")
      .then(response => response.data)
      .then(data => this.refreshHandler())
      .catch(err =>
        this.setState({ requestError: err }))

    this.state.nodes.forEach((num, index) => {
      let url_string = "http://" + num + "/mine"
      axios.get(url_string)
        .then(response => response.data)
        .then(data => this.refreshHandler())
        .catch(err =>
          this.setState({ requestError: err }))
    })

    setTimeout(() => {
      this.setState({ isMining: false })
    }, 4000);

    this.refreshHandler()
  }

  render() {

    let displayResult;

    if (this.state.loading === false) {
      displayResult = (
        this.state.minedBlocks.map((item, index) => (
          <div className='block' key={index}>
            <h1> Bloco {item.index === 1 ? 'Gênesis' : item.index} </h1>
            <div>
              <Transactions data={item.transactions} />
            </div>
          </div>
        )
        )
      )
    }
    else {
      displayResult = (
        <div className='icon_container'>
          <PacmanLoader color='#ff9900' className='loading_icon' />
        </div>
      )
    }

    return (
      <div className='container'>
        <Button disabled={this.state.isMining} ref='mining_btn' color='warning' size='lg' onClick={this.miningHandler} className='mining_button'> {this.state.isMining ? 'Minerando...' : 'Minerar'} </Button>
        <Button color='primary' size='lg' className='refresh_button' onClick={this.refreshHandler}> Atualizar </Button>
        <Sound url='jackhammer.mp3' autoLoad={true} playStatus={this.state.mining ? Sound.status.PLAYING : Sound.status.STOPPED}/>
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
