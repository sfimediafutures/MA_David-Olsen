import React from 'react';

import './footer.scss';

import { Link } from 'react-router-dom';

import logo from '../../assets/visfeat.png';
import medialogo from '../../assets/mediafuturesblack.png';


const Footer = () => {
    return (
        <div className="footer">
            <div className="footer__content container">
                <div className="footer__content__logo">
                    <div className="logo">
                        <img src={logo} alt="" />
                        <Link to="/">vis.features x MediaFutures</Link>
                        <img src={medialogo} alt=""/>

                    </div>
                </div>
            </div>
        </div>
    );
}

export default Footer;
