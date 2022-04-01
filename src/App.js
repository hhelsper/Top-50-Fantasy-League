/* eslint-disable react/style-prop-object */
/* eslint-disable react-hooks/exhaustive-deps */
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import billboard from './white.png';

import './App.css';

function App() {



  const [list, setList] = useState([]);
  const [selectedList, setSelectedList] = useState([]);

  useEffect(async () => {
    const artistsList = await axios(
      '/get_artists',
    );


    setList(artistsList.data);
  }, []);

  function selectArtist(id) {
    if (selectedList.length !== 5) {
      const selectedArtistList = selectedList.concat((id));
      setSelectedList(selectedArtistList);
    }

  }
  function removeArtist(id) {
    const removedList = selectedList.filter((artist) => artist !== id);

    setSelectedList(removedList);

  }



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
        <input type="hidden" name="artists_list" value={selectedList} />
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
        <List list={list} onSelect={selectArtist} onRemove={removeArtist} selectedListLength={selectedList.length} />
      </div>
      <br></br>
      <br></br>




    </div>
  );
}

function List({ list, onSelect, onRemove, selectedListLength }) {
  return (
    <div class="container">
      {list.map((artist) => <Artist key={artist.id} artist={artist} onSelect={onSelect} onRemove={onRemove} selectedListLength={selectedListLength} />)}
    </div>
  );
}

function Artist({ artist, onSelect, onRemove, selectedListLength }) {
  const [show, toggleShow] = useState(true);
  return (
    <>{!show &&

      <Card style={{ borderRadius: '8%', boxShadow: '10 10px 15px 8px rgba(0,0,0,0.06)', backgroundColor: "rgb(238, 217, 26)" }}>
        <Card.Img variant="top" src={artist.artist_img} style={{ borderRadius: '8%' }} />
        <Card.Body>
          <Card.Text> {artist.artist_name}</Card.Text>
          <Button variant="primary"
            onClick={() => { onRemove(artist.id); toggleShow(true) }}
          >Select</Button>
        </Card.Body>
      </Card>

    }
      {show && <Card style={{ borderRadius: '8%', boxShadow: '10 10px 15px 8px rgba(0,0,0,0.06)' }}>
        <Card.Img variant="top" src={artist.artist_img} style={{ borderRadius: '8%' }} />
        <Card.Body>
          <Card.Text> {artist.artist_name}</Card.Text>
          <Button variant="primary" onClick={() => {
            if (selectedListLength !== 5) {
              onSelect(artist.id); toggleShow(false);
            }
          }}>Select</Button>
        </Card.Body>
      </Card>}
    </>
  );
}


export default App;
