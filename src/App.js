/* eslint-disable react/style-prop-object */
/* eslint-disable react-hooks/exhaustive-deps */
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import billboard from './white.png';

import './App.css';

function App() {

  console.log('1');

  const [list, setList] = useState([]);
  const [list2, setList2] = useState([]);

  useEffect(async () => {
    const artistsList = await axios(
      '/get_artists',
    );
    console.log({ artistsList });
    console.log('1');

    setList(artistsList.data);
  }, []);

  function selectArtist(id) {
    const selectedList = list2.concat((id));

    setList2(selectedList);

  }
  // function removeArtist(id) {
  //   const newList = list2.filter((artist) => artist.id !== id);
  //   setList2(newList)
  // }



  return (
    <div className="App">
      <img src={billboard} alt="..." style={{ width: '450px', height: '200px' }} />
      <center>
        <h1 className='head'>Select 5 Artists for
          your
          Bracket
        </h1>
      </center>
      <br></br>
      <br></br>
      <br></br>
      <form
        method="POST"
        action="/save_artists"
      >
        <input type="hidden" name="artists_list" value={list2} />
        <div className="mb-2">
          <center>
            <Button variant="primary" size="lg" type="submit">
              Save Bracket
            </Button>
          </center>

        </div>
      </form>
      <br></br>
      <br></br>
      <div class="container">
        <List list={list} onSelect={selectArtist} />
      </div>
      <br></br>
      <br></br>




    </div>
  );
}

function List({ list, onSelect }) {
  return (
    <div class="container">
      {list.map((artist) => <Artist key={artist.id} artist={artist} onSelect={onSelect} />)}
    </div>
  );
}

function Artist({ artist, onSelect }) {
  const [show, toggleShow] = useState(true);
  return (
    <>{!show &&

      <Card style={{ borderRadius: '8%', boxShadow: '10 10px 15px 8px rgba(0,0,0,0.06)', backgroundColor: "rgb(226, 209, 52)" }}>
        <Card.Img variant="top" src={artist.artist_img} style={{ borderRadius: '8%' }} />
        <Card.Body>
          <Card.Text> {artist.artist_name}</Card.Text>
          <Button variant="primary"
          //onClick={() => { onRemove(artist.id); toggleShow(true) }}
          >Select</Button>
        </Card.Body>
      </Card>

    }
      {show && <Card style={{ borderRadius: '8%', boxShadow: '10 10px 15px 8px rgba(0,0,0,0.06)' }}>
        <Card.Img variant="top" src={artist.artist_img} style={{ borderRadius: '8%' }} />
        <Card.Body>
          <Card.Text> {artist.artist_name}</Card.Text>
          <Button variant="primary" onClick={() => { onSelect(artist.id); toggleShow(false) }}>Select</Button>
        </Card.Body>
      </Card>}
    </>
  );
}


export default App;
