/* eslint-disable react/style-prop-object */
/* eslint-disable react-hooks/exhaustive-deps */
import React, { useState } from 'react';
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import Form from 'react-bootstrap/Form';
import { Navbar, Nav, Row, Col } from 'react-bootstrap';

import SearchBar from './SearchBar';
import { requestUsers } from './requestUsers';
import bill from './b&wBill.jpeg';

import './App.css';

function Create() {

    const [users, setUsers] = useState([]);
    const [noResults, setNoResults] = useState(false);
    const [selectedList, setSelectedList] = useState([]);
    const [date, setDate] = useState();

    const onSearchSubmit = async search => {
        console.log('New Search submit:', search);
        const userArray = await requestUsers(search.toLowerCase());
        console.log(userArray);
        setNoResults(userArray.length === 0);
        setUsers(userArray);
        console.log(users);
    };

    const clearResults = () => setUsers([]);


    function selectUser(id) {
        if (selectedList.length !== 5) {
            const selectedArtistList = selectedList.concat((id));
            setSelectedList(selectedArtistList);
            console.log(selectedList);
        }

    }
    function removeUser(id) {
        const removedList = selectedList.filter((user) => user !== id);

        setSelectedList(removedList);

    }



    const renderedQuotes = users.map((user) => {
        return <User key={user.id} user={user} onSelect={selectUser} onRemove={removeUser} />
    })



    return (
        <div className='app'>
            <Navbar class="navbar" variant='dark' style={{ backgroundColor: "rgb(0,0,0)", color: "rgb(255,255,255)", marginTop: "14px", marginLeft: "14px", marginRight: "14px", height: "86px" }}>
                <img class="custom" src={bill} alt='' width='10px' height='10px' />


                <Nav className="me-auto" defaultActiveKey="#">
                    <Nav.Link to="/profile" href="/profile" style={{ marginLeft: "16px" }}>Profile</Nav.Link>
                    <Nav.Link to="/artists" href="/artists">Artists</Nav.Link>
                    <Nav.Link to="/leader_board" href="/leader_board">Leader Board</Nav.Link>
                    <Nav.Link to="/my_leagues" href="/my_leagues">My Leagues</Nav.Link>
                    <Nav.Link to="#" href="#">Create A League</Nav.Link>
                    <Nav.Link to="/about_us" href="/about_us">About Us</Nav.Link>
                    <Nav.Link id="navbar-right" to="/logout" href="/logout">Logout</Nav.Link>
                </Nav>

            </Navbar>
            <br></br>
            <br></br>
            <center>
                <h1 className='head' style={{ fontSize: "60pt" }}>Create Your League
                </h1>
            </center>
            <br></br>
            <br></br>
            <br></br>

            <form method="POST"
                action="/create_league">
                <input type="hidden" name="users" value={selectedList} />
                <input type="hidden" name="end_date" value={date} />
                {/* TODO WRITE CREATE LEAGUE ROUTE IN PYTHON */}
                <center>
                    <Button variant="dark" size="lg" type="submit" style={{ width: "300px" }}>
                        Create League
                    </Button>
                </center>
                <br></br>

                <Form.Group className="mb-3" controlId="formBasicEmail" style={{ marginLeft: '6rem' }}>
                    <center><Row>
                        <Form.Label column="lg" lg={2} className='head' style={{ fontSize: "20pt" }}>
                            League Name
                        </Form.Label>
                        <Col xs={7}>
                            <Form.Control size="lg" type="text" placeholder="League Name" name='name' />
                        </Col>
                    </Row>
                    </center>
                    <br></br>
                    <center><Row>
                        <Form.Label column="lg" lg={2} className='head' style={{ fontSize: "20pt" }}>
                            End Date
                        </Form.Label>
                        <Col xs={7}>
                            <Form.Select size="lg" value={date} onChange={(e) => setDate(e.target.value)}>
                                <option>Choose an end date</option>
                                <option value="1">One Week</option>
                                <option value="2">Two Weeks</option>
                                <option value="3">Three Weeks</option>
                                <option value="4">Four Weeks</option>
                                <option value="5">Five Weeks</option>
                            </Form.Select>
                        </Col>
                    </Row>
                    </center>

                </Form.Group>




            </form>
            <br></br>

            <Form.Group className="mb-3" controlId="formBasicEmail" style={{}}>
                <center>
                    <Row>
                        <Form.Label column="lg" lg={2} className='head' style={{ fontSize: "20pt", marginLeft: '6rem' }}>
                            Search
                        </Form.Label>
                        <Col xs={7} style={{ width: "800px" }}>
                            <SearchBar onSearchSubmit={onSearchSubmit} clearResults={clearResults} />
                        </Col>
                    </Row>
                </center>
            </Form.Group>


            {
                noResults &&
                <center><p className='no-results'>
                    No results found.
                </p></center>
            }
            <div className='main-content'>
                {renderedQuotes}
            </div>

        </div >
    );
};

function User({ user, onSelect, onRemove }) {
    const [show, toggleShow] = useState(true);
    return (
        <>{!show &&

            <Card style={{ boxShadow: '10 10px 15px 8px rgba(0,0,0,0.06)', backgroundColor: "rgb(238, 217, 26)", marginLeft: '21rem', marginRight: '22rem' }}>

                <Card.Body>
                    <Card.Title className='head' style={{ fontSize: "40pt" }}> {user.user_name}</Card.Title>

                    <Button variant="dark"
                        onClick={() => { onRemove(user.id); toggleShow(true) }}
                    >Select</Button>
                </Card.Body>
                <br></br>
            </Card>


        }
            {show &&

                <Card style={{ boxShadow: '10 10px 15px 8px rgba(0,0,0,0.06)', marginLeft: '21rem', marginRight: '22rem' }}>

                    <Card.Body>
                        <Card.Title className='head' style={{ fontSize: "40pt" }}> {user.user_name}</Card.Title>

                        <Button variant="dark" onClick={() => {

                            onSelect(user.id); toggleShow(false);

                        }}>Select</Button>
                    </Card.Body>
                    <br></br>
                </Card>
            }

        </>
    );
}

export default Create;
