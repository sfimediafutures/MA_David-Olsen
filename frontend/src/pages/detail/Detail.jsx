import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router';
import ColorList from "react-color-list"

import tmdbApi from '../../api/tmdbApi';
import apiConfig from '../../api/apiConfig';

import './detail.scss';

import MovieList from '../../components/movie-list/MovieList';

const Detail = () => {

    const { category, id } = useParams();

    const [item, setItem] = useState(null);
    const [color, setColor] = useState(["#bf4040","#ab3f3f","#9f3737","#8d3434","#812929"])

    useEffect(() => {
        const getDetail = async () => {
            const response = await tmdbApi.detail(category, id, {params:{}});
            setItem(response);
            window.scrollTo(0,0);
        }
        getDetail();
    }, [category, id]);

    return (
        <>
            {
                item && (
                    <>
                        <div className="banner"></div>
                        <div className="mb-3 movie-content container">
                            <div className="movie-content__poster">
                                <div className="movie-content__poster__img" style={{backgroundImage: `url(${apiConfig.originalImage(item.poster_path)})`}}></div>
                            </div>
                            <div className="movie-content__info">
                                <h1 className="title">
                                    {item.title || item.name}
                                </h1>
                                <div className="genres">
                                    {
                                        item.genres && item.genres.slice(0, 5).map((genre, i) => (
                                            <span key={i} className="genres__item">{genre.name}</span>
                                        ))
                                    }
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
                                <p className="overview">{item.overview}</p>
                            </div>
                        </div>
                        <div className="container">
                            <div className="section mb-3">
                                <div className="section__header mb-2">
                                    <h2>Similar</h2>
                                </div>
                                <MovieList category={category} type="similar" id={item.id}/>
                            </div>
                        </div>
                    </>
                )
            }
        </>
    );
}

export default Detail;
