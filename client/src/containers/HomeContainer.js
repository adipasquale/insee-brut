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
      clickedItems: [],
      lastItemClicked: null
    };
  }

  clickedItem = (panelId, itemId) => {
    console.log("--- item ID", itemId);
    console.log("--- panel ID", panelId);

    const lastId = itemId;
    let { lastItemClicked } = this.state;
    lastItemClicked = this.getElementById(tree, lastId);
    this.setState({ lastItemClicked });

    if (lastItemClicked.children) {
      const { clickedItems } = this.state;
      console.log("--- clickedItems length", clickedItems.length);
      if (panelId === clickedItems.length) {
        clickedItems.push(lastId);
        console.log("--- NEW clickedItems length", clickedItems.length);
        this.setState({ clickedItems });
      } else if (panelId < clickedItems.length) {
        const itemsToDelete = clickedItems.length - panelId;
        clickedItems.splice(panelId, itemsToDelete);
      }
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
    const { clickedItems } = this.state;
    const { lastItemClicked } = this.state;
    return (
      <Fragment>
        <PanelComponent
          panelId={0}
          menu={tree}
          clickedItem={this.clickedItem}
        />
        {lastItemClicked !== null && !lastItemClicked.children && (
          <p>Contenu de l'item avec l'id {lastItemClicked.id}</p>
        )}
        {lastItemClicked !== null &&
          lastItemClicked.children &&
          clickedItems.map(el => (
            <PanelComponent
              key={el.id}
              menu={lastItemClicked.children}
              clickedItem={this.clickedItem}
              panelId={el}
            />
          ))}
      </Fragment>
    );
  }
}

export default HomeContainer;
