import React, { Fragment } from 'react';

const PanelComponenent = greeting => (
  <Fragment>
    <div className="bg-moon-gray vh-100 fl w-10">{greeting}</div>
  </Fragment>
);

export default PanelComponenent;
