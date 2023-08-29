import React, { useState } from 'react';

const SearchForm = ({ query, setQuery }) => {
    const handleSubmit = (event) => {
        event.preventDefault();
        console.log(query);
    };

    return (
        <>
            <div className="row">
                <form onSubmit={handleSubmit}>
                    <label>
                        Query:
                        <input type="text" value={query} onChange={(event) => setQuery(event.target.value)} />
                    </label>
                    <input type="submit" value="Submit" />
                </form>
            </div>
        </>
    );
};



export default SearchForm;