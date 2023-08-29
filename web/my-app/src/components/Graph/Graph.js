import React, { useEffect, useRef, useState } from "react";
import Neovis from "neovis.js/dist/neovis.js";
import { Row, Col, Card, Input, Form, Button, Space } from 'antd';
import logo from '../../logo.png';

const CYPHER = `WITH "(?i).*"+"{QUERY}"+".*" as query
MATCH p = (head)-[r]->(tail) 
WHERE head.id contains query or tail.id contains query or tail.id =~query or head.id =~query or head.id = toInteger("{QUERY}") or tail.id = toInteger("{QUERY}")
RETURN p`;

const Graph = ({ setNodeInfo, query, setQuery }) => {
    const visRef = useRef();
    const neoVis = useRef();

    useEffect(() => {
        const config = {
            container_id: visRef.current.id,
            server_url: process.env.REACT_APP_NEO4J_URL,
            server_user: process.env.REACT_APP_NEO4J_USER,
            server_password: process.env.REACT_APP_NEO4J_PASSWORD,
            labels: {
                "NER_Bio": {
                    caption: "name",
                    size: 5.0,
                    sizeCypher: "MATCH (n) WHERE id(n) = {id} RETURN SIZE((n)-[]->()) AS s;",
                    font: {
                        size: 20
                    },
                    group: 'community',
                },
                "Paper": {
                    caption: "name",
                    size: 3.0,
                    sizeCypher: "MATCH (n) WHERE id(n) = {id} RETURN SIZE((n)-[]->()) AS s;",
                    font: {
                        size: 20
                    },
                    nodes: {
                        shape: 'neo',
                    },
                    group: 'community',
                }
            },
            relationships: {
                font: {
                    size: 10
                }
            },
            initial_cypher: "MATCH p = (bio_ner_h)-[r*1..3]->(bio_ner_t) WHERE bio_ner_t.name = 35061102 or bio_ner_h.name = 35061102 RETURN p",
            arrows: true,
        };
        neoVis.current = new Neovis(config);
        neoVis.current.render();
        neoVis.current.registerOnEvent('clickNode', (e) => {
            // e: { nodeId: number; node: Node }
            console.info(e);
            setNodeInfo({
                group: e.node.group,
                id: e.node.id,
                label: e.node.label,
                shape: e.node.shape,
                title: e.node.title,
                value: e.node.value,
            });
        });
    }, []);

    const onFinish = (values) => {
        setQuery(values.input);
        let cypher = CYPHER.replace(new RegExp('{QUERY}', 'g'), values.input);
        console.log("queryWithCypher: ", cypher);
        neoVis.current.renderWithCypher(cypher);
    };

    return (
        <>
            <Card>
                <Row>
                    <Col span={24}>
                        <Row>
                            <Col span={24}>
                                <Space wrap>
                                    <img src={logo} alt="Logo" style={{ width: "50px", height: "auto" }} />
                                    <Form
                                        layout="inline"
                                        name="query"
                                        onFinish={onFinish}
                                        style={{ display: 'flex', flexDirection: 'row', alignItems: 'center' }}>
                                        <Form.Item
                                            name="input"
                                            style={{ marginBottom: 0 }}>
                                            <Input style={{ width: 200 }} />
                                        </Form.Item>
                                        <Form.Item style={{ marginBottom: 0 }}>
                                            <Button type="primary" htmlType="Submit">
                                                Find Relationship
                                            </Button>
                                        </Form.Item>
                                    </Form>
                                </Space>
                            </Col>
                        </Row>
                        <Row>
                            <Col span={24}>
                                <div
                                    id="graph-id"
                                    ref={visRef}
                                    style={{
                                        width: `100%`,
                                        height: `50vh`,
                                        backgroundColor: `"#d3d3d3"`,
                                    }}
                                >
                                </div>
                            </Col>
                        </Row>
                    </Col>
                </Row>
            </Card>
        </>
    );
}

export default Graph;