import React, { Fragment } from 'react';
import PanelComponent from '../components/PanelComponent';

// const tree = {
//   location: [
//     {
//       id: 0,
//       title: 'New York',
//       selected: false,
//       key: 'location'
//     },
//     {
//       id: 1,
//       title: 'Dublin',
//       selected: false,
//       key: 'location'
//     },
//     {
//       id: 2,
//       title: 'California',
//       selected: false,
//       key: 'location'
//     },
//     {
//       id: 3,
//       title: 'Istanbul',
//       selected: false,
//       key: 'location'
//     },
//     {
//       id: 4,
//       title: 'Izmir',
//       selected: false,
//       key: 'location'
//     },
//     {
//       id: 5,
//       title: 'Oslo',
//       selected: false,
//       key: 'location'
//     }
//   ]
// };
class HomeContainer extends React.Component {
  constructor() {
    super();
    this.state = {};
  }

  render() {
    const greeting = 'Bonjour!';
    return (
      <Fragment>
        <PanelComponent greeting={greeting} />
      </Fragment>
    );
  }
}

export default HomeContainer;
