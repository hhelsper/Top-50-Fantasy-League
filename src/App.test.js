import { render, cleanup, screen } from '@testing-library/react';
import axios from 'axios';
import React from 'react';
import App from './App.js'
import Select from './Select';
import { fetchArtists } from "./utils.js"



afterEach(cleanup);

describe("render elements", () => {
  it('Elements inner text to be in Select function', () => {

    render(<Select />);
    expect(screen.getByText("Select 5 Artists for your Bracket")).toBeInTheDocument();

    expect(screen.getByText("Save Bracket")).toBeInTheDocument();

  });
});

jest.mock("axios");

describe("fetchUsers", () => {
  it("should return artists list", async () => {

    const artists = [
      {
        id: 1266,
        artist_name: 'Jaymes Young',
        artist_img: 'https://i.scdn.co/image/ab6761610000517487528aedec4b8d5586768014',
        artist_rank: 25
      },
      {
        id: 1275,
        artist_name: 'Jnr Choi',
        artist_img: 'https://i.scdn.co/image/ab676161000051744203b11d1dcae83df0934d1e',
        artist_rank: 16
      },
      {
        id: 1280,
        artist_name: 'Lauren Spencer-Smith',
        artist_img: 'https://i.scdn.co/image/ab67616100005174cb07ca00a965720e34bf713f',
        artist_rank: 11
      }
    ];

    axios.get.mockResolvedValueOnce(artists)
    const result = await fetchArtists();


    expect(axios.get).toHaveBeenCalledWith(`/get_artists`);
    expect(result).toEqual(artists);

  });

  it("should return empty users list", async () => {

    const message = "Error";
    axios.get.mockRejectedValueOnce(new Error(message));


    const result = await fetchArtists();


    expect(axios.get).toHaveBeenCalledWith(`/get_artists`);
    expect(result).toEqual([]);
  });
});

