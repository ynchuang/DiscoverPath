import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Card, List, Space, Button, Typography, Spin, Empty, Tag } from "antd";
import { LikeOutlined, DislikeOutlined, LinkOutlined, MailOutlined } from '@ant-design/icons';

const { Title, Paragraph } = Typography;

const NODE_TYPE_EMPTY = 0
const NODE_TYPE_PAPER = 1
const NODE_TYPE_WORD = 2

export const DefaultDocInfo = {
    "given": "",
    "abstract": "",
    "title": "",
    "author_list": [],
    "keyword": [],
    "download_url": "",
    "nih_url": "",
    "pmid": "",
    "pmcid": "",
    "doi": ""
}

const NodeDetails = ({ nodeInfo }) => {
    const [docInfo, setDocInfo] = useState(DefaultDocInfo);
    const [loading, setLoading] = useState(false);
    const [nodeType, setNodeType] = useState(NODE_TYPE_EMPTY);
    const [nodeDisplayText, setNodeDisplayText] = useState('')

    useEffect(() => {
        if (nodeInfo.given === "") {
            return;
        }

        setLoading(true);
        let paperId = 0;
        if (nodeInfo.group === "Paper") {
            paperId = nodeInfo.label;
            setNodeType(NODE_TYPE_PAPER)
            setNodeDisplayText(paperId)
        } else {
            // EXAMPLE: "<strong>name:</strong> CSF biomar...<br><strong>Source:</strong> 35061102<br><strong>id:</strong> CSF biomarker levels<br>"
            const regexPaperId = /Source:<\/strong> (\d+)<br>/g.exec(nodeInfo.title);
            if (regexPaperId && regexPaperId[1] !== undefined) {
                paperId = regexPaperId[1]
                setNodeType(NODE_TYPE_WORD)
            }

            const regexDisplayText = /id:<\/strong> (.*)<br>/g.exec(nodeInfo.title);
            if (regexDisplayText && regexDisplayText[1] !== undefined) {
                setNodeDisplayText(regexDisplayText[1])
            }
        }

        axios.get(`knowledgegraph/details`, {
            params: {
                id: paperId
            }
        }).then(res => {
            const d = res.data;
            setDocInfo(checkResp(d));
            setLoading(false);
        }).catch(function (error) {
            setDocInfo(DefaultDocInfo);
            console.log(error.toJSON());
            setLoading(false);
        })
    }, [nodeInfo])


    const keywordListItems = renderKeywordList(docInfo.keyword);
    const authorListItems = renderAuthorList(docInfo.author_list);

    let nodeTypeTag;
    if (nodeType === NODE_TYPE_PAPER) {
        nodeTypeTag = <Tag color="gold">Paper</Tag>
    } else if (nodeType === NODE_TYPE_WORD) {
        nodeTypeTag = <Tag color="blue">Word</Tag>
    }

    let nodeDisplayTextTag;
    if (nodeType === NODE_TYPE_PAPER || nodeType === NODE_TYPE_WORD) {
        nodeDisplayTextTag = <Tag color="default">{nodeDisplayText}</Tag>
    }

    const handleLinkClick = () => {
        window.open(docInfo.download_url, '_blank');
    };

    let detailsCard;
    if (nodeInfo.given === "") {
        detailsCard =
            <Spin spinning={loading}>
                <Card><Empty /></Card>
            </Spin>
    } else {
        detailsCard =
            <Spin spinning={loading}>
                <Card>
                    <Space direction="vertical">
                        <Space wrap>
                            <Button icon={<LikeOutlined />}>Like</Button>
                            <Button icon={<DislikeOutlined />}>Dislike</Button>
                            <Button icon={<MailOutlined />} href="mailto:yc146@rice.edu">Report</Button>
                        </Space>
                        <Space wrap>
                            {nodeTypeTag}
                            {nodeDisplayTextTag}
                        </Space>
                    </Space>
                    <List>
                        <Title level={4}>{docInfo.title}</Title>
                        <Paragraph>{authorListItems}</Paragraph>
                        <Paragraph>PMID: {docInfo.pmid}</Paragraph>
                        <Paragraph>PMCID: {docInfo.pmcid}</Paragraph>
                        <Paragraph>DOI: {docInfo.doi}</Paragraph>
                        <Paragraph>Keyword: {keywordListItems}</Paragraph>
                    </List>
                    <Space wrap>
                        <Button onClick={handleLinkClick} icon={<LinkOutlined />}>Full text links</Button>
                        {/* <Button>Cite</Button> */}
                    </Space>
                    <Title level={4}>Abstract</Title>
                    <Paragraph>{docInfo.abstract}</Paragraph>
                </Card>
            </Spin>
    }

    return (
        <>
            {detailsCard}
        </>
    );
};

function renderKeywordList(keywords) {
    if (keywords === undefined) {
        return "";
    }

    return keywords.join(", ");
}

function renderAuthorList(authors) {
    if (authors === undefined) {
        return "";
    }

    return authors.map((author) =>
        author.ForeName + " " + author.LastName
    ).join(", ");
}

function checkResp(resp) {
    let out = DefaultDocInfo;

    if (resp.given !== undefined) {
        out.given = resp.given
    }
    if (resp.abstract !== undefined) {
        out.abstract = resp.abstract
    }
    if (resp.title !== undefined) {
        out.title = resp.title
    }
    if (resp.author_list !== undefined) {
        out.author_list = resp.author_list
    }
    if (resp.keyword !== undefined) {
        out.keyword = resp.keyword
    }
    if (resp.download_url !== undefined) {
        out.download_url = resp.download_url
    }
    if (resp.nih_url !== undefined) {
        out.nih_url = resp.nih_url
    }
    if (resp.pmid !== undefined) {
        out.pmid = resp.pmid
    }
    if (resp.pmcid !== undefined) {
        out.pmcid = resp.pmcid
    }
    if (resp.doi !== undefined) {
        out.doi = resp.doi
    }

    return out;
}

export default NodeDetails;