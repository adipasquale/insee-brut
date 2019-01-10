import React, { Fragment } from 'react';
import PropTypes from 'prop-types';

interface propTypes {
  menu: Array;
}
const PanelComponenent = ({ menu }) => (
  <Fragment>
    <div className="bg-moon-gray vh-100 fl w-10">
      <ul>
        {menu.map(element => (
          <li>
            <a href="#">{element.title}</a>
          </li>
        ))}
      </ul>
    </div>
    {/* <PanelComponenent menu2={menu.link} /> */}
  </Fragment>
);

export default PanelComponenent;
