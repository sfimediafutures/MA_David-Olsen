import React, { useEffect, useState, useHistory, useCallback } from 'react';
//import { useParams } from 'react-router';
//import ColorList from "react-color-list"

//import tmdbApi from '../../api/tmdbApi';
//import apiConfig from '../../api/apiConfig';

import './Upload.scss';
import Button, { OutlineButton } from '../../components//button/Button';
import Input from '../../components/input/Input'
//import MovieList from '../../components/movie-list/MovieList';

const Upload = props => {
    const [keyword, setKeyword] = useState('');
    
    
    return (
        <>
        <div className="banner"></div>
        <div className="mb-3 movie-content container">
            <div className="movie-content__poster">
                <div className="movie-content__poster__img" style={{backgroundImage: `url(https://i.imgur.com/SPAtszY.jpeg)`}}></div>
            </div>
            <div className="movie-content__info">
            <Input
                type="text"
                placeholder="Enter keyword"
                value={keyword}
                onChange={(e) => setKeyword(e)}
            />
            <Button className="small" onClick={GetFeatures(props.keyword)}>Search</Button>
            <p id="demo"></p>
            </div>
        </div>
    </>
    )
}

const GetFeatures = (keyword) => {

    const url = 'http://127.0.0.1:5000/features/' + keyword;
    fetch(url)
    .then(response => response.json())  
    .then(json => {
        console.log(json);
        document.getElementById("demo").innerHTML = JSON.stringify(json)
    })
}


export default Upload;


/* 

<div className="mb-3 movie-content container">
                        <div className="movie-content__poster">
                            <div className="movie-content__poster__img" style={{backgroundImage: `url(https://i.imgur.com/SPAtszY.jpeg)`}}></div>
                        </div>
                        <div className="movie-content__info">
                            <h1 className="title">
                                Test
                            </h1>
                            <div className="genres">
                                Genre Test
                            </div>

                            <div className='features'>
                                <ul>
                                    <h3>Saturation: Medium</h3>
                                    <h3>Brightness: High</h3>
                                    <h3>Colorfulness: High</h3>
                                    <h3>Entropy: Medium</h3>
                                    <h3>Sharpness: High</h3>
                                    <h3>Contrast: Medium</h3>
                                </ul>
                            </div>
                            <p className="overview">{"ding dong"}</p>
                        </div>
                    </div>

*/ 