/* eslint-disable react-hooks/exhaustive-deps */
import React, { useEffect, useState } from 'react';

import './styles/SearchBar.css'
import { MDBIcon } from "mdbreact";
import { Row, Col, Form, InputGroup } from 'react-bootstrap';

const SearchBar = ({ onSearchSubmit, clearResults }) => {
    const [term, setTerm] = useState('');
    const [debouncedTerm, setDebouncedTerm] = useState(term);

    // update 'term' value after 1 second from the last update of 'debouncedTerm'
    useEffect(() => {
        const timer = setTimeout(() => setTerm(debouncedTerm), 1000);
        return () => clearTimeout(timer);
    }, [debouncedTerm])

    // submit a new search
    useEffect(() => {
        if (term !== '') {
            onSearchSubmit(term);
        }
        else {
            clearResults();
        }
    }, [term]);

    return (
        <div className='searchbar' style={{ backgroundColor: 'rgba(255, 255, 255, .13)' }}>






            <Form.Control size="lg" type="text" placeholder="Search users to add to your league" onChange={e => setDebouncedTerm(e.target.value)}
                value={debouncedTerm} />






        </div>
    );
};

export default SearchBar;