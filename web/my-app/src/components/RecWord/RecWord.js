import React, { useEffect, useState } from 'react';
import { Spin, Typography, Collapse } from "antd";
import axios from 'axios';
import { getOrDefault } from '../../utils/utils'

const { Panel } = Collapse;
const { Paragraph } = Typography;

const RecWord = ({ query }) => {
    const [loading, setLoading] = useState(false);
    const [keywords, setKeywords] = useState([])

    useEffect(() => {
        if (query === "") {
            return;
        }

        setLoading(true);
        axios.get(`knowledgegraph/w2w`, {
            params: {
                target_query: query,
                model_query: "air"
            }
        }).then(res => {
            const d = res.data;
            setKeywords(getOrDefault(d.rec_result, []));
            setLoading(false);
        }).catch(function (error) {
            setKeywords([]);
            console.log(error.toJSON());
            setLoading(false);
        })
    }, [query])

    const keywordListItems = renderKeywordList(keywords);

    return (
        <>
            <Collapse accordion>
                <Panel header="Word Queries You Can Start From" key="1">
                    <Spin spinning={loading}>
                        <Paragraph>{keywordListItems}</Paragraph>
                    </Spin>
                </Panel>
            </Collapse>
        </>
    );
};

function renderKeywordList(keywords) {
    if (keywords === undefined) {
        return "";
    }

    return keywords.join(", ");
}

export default RecWord;