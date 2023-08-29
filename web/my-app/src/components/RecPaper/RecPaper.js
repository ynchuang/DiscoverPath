import React, { useEffect, useState } from 'react';
import { List, Typography, Collapse, Spin } from "antd";
import axios from 'axios';
import { getOrDefault } from '../../utils/utils'

const { Panel } = Collapse;
const { Text, Paragraph } = Typography;

const RecPaper = ({ query }) => {
    const [loading, setLoading] = useState(false);
    const [papers, setPapers] = useState([])

    useEffect(() => {
        if (query === "") {
            return;
        }

        setLoading(true);
        axios.get(`knowledgegraph/w2p`, {
            params: {
                target_query: query,
                model_query: "air"
            }
        }).then(res => {
            const d = res.data;
            setPapers(extractPapers(d));
            setLoading(false);
        }).catch(function (error) {
            setPapers([]);
            console.log(error.toJSON());
            setLoading(false);
        })
    }, [query])

    return (
        <>
            <Collapse accordion>
                <Panel header="Paper Queries You May Want" key="1">
                    <Spin spinning={loading}>
                        <List
                            bordered
                            dataSource={papers}
                            renderItem={(item) => (
                                <List.Item>
                                    {<a href={item.url}>&lt;{item.id}&gt; {item.title}</a>}
                                </List.Item>
                            )}
                        />
                    </Spin>
                </Panel>
            </Collapse>
        </>
    );
};

function extractPapers(data) {
    let ids = getOrDefault(data.rec_id_result, []);
    let titles = getOrDefault(data.rec_title_result, []);
    let urls = getOrDefault(data.rec_url_result, []);

    return ids.map(function (id, i) {
        return { id: id, title: getOrDefault(titles[i], ""), url: getOrDefault(urls[i], "") };
    })
}

export default RecPaper;