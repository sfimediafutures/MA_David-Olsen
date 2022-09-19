import React, { useEffect, useState } from 'react';
//import { useParams } from 'react-router';
//import ColorList from "react-color-list"

//import tmdbApi from '../../api/tmdbApi';
//import apiConfig from '../../api/apiConfig';

import './Upload.scss';

//import MovieList from '../../components/movie-list/MovieList';

const Upload = () => {

    //const { category, id } = useParams();

    //const [item, setItem] = useState(null);
    //const [color, setColor] = useState(["#bf4040","#ab3f3f","#9f3737","#8d3434","#812929"])
    
    //useEffect(() => {
    //    const getDetail = async () => {
    //        const response = await tmdbApi.detail(category, id, {params:{}});
    //        setItem(response);
    //        window.scrollTo(0,0);
    //    }
    //    getDetail();
    //}, [category, id]);
    
    return (
                <>
                    <div className="banner"></div>
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
                </>
);
}

export default Upload;
