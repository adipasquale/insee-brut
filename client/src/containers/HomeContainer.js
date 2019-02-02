import React, { Fragment } from "react";
import PanelComponent from "../components/PanelComponent";

const tree = [
  {
    id: 0,
    title: "1.0.0",
    key: "location"
  },
  {
    id: 1,
    title: "2.0.0 *",
    children: [
      {
        id: 11,
        title: "2.1.0",
        key: "location"
      },
      {
        id: 12,
        title: "2.2.0 *",
        key: "location",
        children: [
          {
            id: 121,
            title: "2.2.1",
            key: "location"
          },
          {
            id: 122,
            title: "2.2.2",
            key: "location"
          },
          {
            id: 123,
            title: "2.2.3",
            key: "location"
          },
          {
            id: 124,
            title: "2.2.4",
            key: "location"
          }
        ]
      },
      {
        id: 13,
        title: "2.3.0",
        key: "location"
      },
      {
        id: 14,
        title: "2.4.0",
        key: "location"
      }
    ]
  },
  {
    id: 2,
    title: "3.0.0",
    key: "location"
  },
  {
    id: 3,
    title: "4.0.0",
    key: "location"
  },
  {
    id: 4,
    title: "5.0.0",
    key: "location"
  },
  {
    id: 5,
    title: "6.0.0",
    key: "location"
  }
];

class HomeContainer extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      clicked: [],
      lastClicked: null
    };
  }

  clicked = id => {
    const { clicked } = this.state;
    clicked.push(id);
    this.setState({ clicked });
    const lastId = clicked[clicked.length - 1];

    let { lastClicked } = this.state;
    lastClicked = this.getElementById(tree, lastId);
    if (lastClicked.children) {
      this.setState({ lastClicked });
    }
  };

  getElementById = (tree, id) => {
    const item = tree.find(el => el.id === id);

    if (item) {
      return item;
    }

    let isFound = null;
    let i = 0;
    while (i < tree.length || !isFound) {
      if (tree[i].children) {
        isFound = this.getElementById(tree[i].children, id);
      }
      i++;
    }
    return isFound;
  };

  render() {
    const { clicked } = this.state;
    const { lastClicked } = this.state;
    return (
      <Fragment>
        <PanelComponent menu={tree} clickedItem={this.clicked} />
        {lastClicked !== null &&
          lastClicked.children &&
          clicked.map(el => (
            <PanelComponent
              key={el.id}
              menu={lastClicked.children}
              clickedItem={this.clicked}
            />
          ))}
      </Fragment>
    );
  }
}

export default HomeContainer;
