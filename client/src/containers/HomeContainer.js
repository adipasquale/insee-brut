import React, { Fragment } from 'react';
import PanelComponent from '../components/PanelComponent';

const tree = [
  {
    id: 0,
    title: '1.0.0',
    selected: false,
    key: 'location'
  },
  {
    id: 1,
    title: '2.0.0 *',
    children: [
      {
        id: 11,
        title: '2.1.0',
        selected: false,
        key: 'location'
      },
      {
        id: 12,
        title: '2.2.0 *',
        selected: false,
        key: 'location',
        children: [
          {
            id: 121,
            title: '2.2.1',
            selected: false,
            key: 'location'
          },
          {
            id: 122,
            title: '2.2.2',
            selected: false,
            key: 'location'
          },
          {
            id: 123,
            title: '2.2.3',
            selected: false,
            key: 'location'
          },
          {
            id: 124,
            title: '2.2.4',
            selected: false,
            key: 'location'
          }
        ]
      },
      {
        id: 13,
        title: '2.3.0',
        selected: false,
        key: 'location'
      },
      {
        id: 14,
        title: '2.4.0',
        selected: false,
        key: 'location'
      }
    ]
  },
  {
    id: 2,
    title: '3.0.0',
    selected: false,
    key: 'location'
  },
  {
    id: 3,
    title: '4.0.0',
    selected: false,
    key: 'location'
  },
  {
    id: 4,
    title: '5.0.0',
    selected: false,
    key: 'location'
  },
  {
    id: 5,
    title: '6.0.0',
    selected: false,
    key: 'location'
  }
];
class HomeContainer extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      clicked: []
    };
  }

  clicked = id => {
    const { clicked } = this.state;
    clicked.push(id);
    this.setState({ clicked });
  };

  render() {
    const { clicked } = this.state;
    console.log(clicked);
    return (
      <Fragment>
        <PanelComponent menu={tree} onItemClick={this.clicked} />
        {clicked.map(element => (
          <PanelComponent menu={tree} onItemClick={this.clicked} />
        ))}
      </Fragment>
    );
  }
}

export default HomeContainer;
