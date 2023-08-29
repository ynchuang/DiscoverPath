import React, { useState } from 'react';
import './App.css';
import { Row, Col } from 'antd';
import Graph from '../Graph/Graph';
import NodeDetails from '../NodeDetails/NodeDetails';
import RecPaper from '../RecPaper/RecPaper';
import RecWord from '../RecWord/RecWord'
import axios from 'axios';
import { DefaultDocInfo } from '../NodeDetails/NodeDetails'

function App() {
  const [nodeInfo, setNodeInfo] = useState(DefaultDocInfo);
  const [query, setQuery] = useState('');

  axios.defaults.baseURL = process.env.REACT_APP_API;

  return (
    <div className="App">
      <header>
        <Row gutter={16}>
          <Col span={14}>
            <Row>
              <Col span={24}>
                <Graph setNodeInfo={setNodeInfo} query={query} setQuery={setQuery} />
              </Col>
            </Row>
            <Row>
              <Col span={24}>
                <RecPaper query={query} />
              </Col>
            </Row>
            <Row>
              <Col span={24}>
                <RecWord query={query} />
              </Col>
            </Row>
          </Col>
          <Col span={10}>
            <NodeDetails nodeInfo={nodeInfo} />
          </Col>
        </Row>
      </header >
    </div >
  );
}

export default App;
