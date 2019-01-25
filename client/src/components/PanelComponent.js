import React, { Fragment } from 'react';
// import PropTypes from 'prop-types';

const PanelComponenent = ({ menu, onItemClick }) => (
  <Fragment>
    <div className="bg-moon-gray vh-100 fl w-10">
      <ul>
        {menu.map(element => (
          <li>
            <a href="#" onClick={() => onItemClick(element.id)}>
              {element.title}
            </a>
          </li>
        ))}
      </ul>
    </div>
  </Fragment>
);

export default PanelComponenent;
