import React, { Fragment } from "react";
import PanelComponent from "../components/PanelComponent";

const tree = {
  children: {
  0: {
    id: 0,
    title: "1.0.0",
    key: "location"
  },
  1: {
    id: 1,
    title: "2.0.0 *",
    children: {
      11: {
        id: 11,
        title: "2.1.0",
        key: "location"
      },
      12: {
        id: 12,
        title: "2.2.0 *",
        key: "location",
        children: {
          121: {
            id: 121,
            title: "2.2.1",
            key: "location"
          },
          122: {
            id: 122,
            title: "2.2.2",
            key: "location"
          },
          123: {
            id: 123,
            title: "2.2.3",
            key: "location"
          },
          124: {
            id: 124,
            title: "2.2.4",
            key: "location"
          }
        }
      },
      13: {
        id: 13,
        title: "2.3.0",
        key: "location"
      },
      14: {
        id: 14,
        title: "2.4.0",
        key: "location"
      }
    }
  },
  2: {
    id: 2,
    title: "3.0.0",
    key: "location"
  },
  3: {
    id: 3,
    title: "4.0.0",
    key: "location"
  },
  4: {
    id: 4,
    title: "5.0.0",
    key: "location"
  },
  5: {
    id: 5,
    title: "6.0.0",
    key: "location"
  }
  }
};

class HomeContainer extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      clickedItemIds: [],
      lastItemClicked: null
    };
  }

  onItemClicked = (itemId, level) => {
    // console.log(`onItemClicked for level ${level} and id ${itemId}`)
    let { clickedItemIds } = this.state;
    clickedItemIds[level] = itemId;
    // drops clicked elements with a level higher than the newly clicked one
    clickedItemIds.splice(level + 1);
    this.setState({clickedItemIds});
  };

  render() {
    const { clickedItemIds } = this.state;
    const { lastItemClicked } = this.state;
    return (
      <Fragment>
        <PanelComponent
          level={0}
          menuTree={tree}
          onItemClicked={this.onItemClicked}
        />
        {lastItemClicked !== null && !lastItemClicked.children && (
          <p>Contenu de l'item avec l'id {lastItemClicked.id}</p>
        )}
        {clickedItemIds.map((itemId, idx) => {
            const level = idx + 1;
            // get all the clicked item ids up to this one
            const itemIds = clickedItemIds.slice(0, level);
            // looks complicated but isn't: this iterates on the itemIds
            // and accesses the tree.children[id] each time, to 'dig' into
            // the array until the subtree we're interested in
            const itemTree = itemIds.reduce(
              (currentTree, idx) => currentTree.children[idx],
              tree
            )
            if (itemTree.children) {
              return <PanelComponent
                key={itemId}
                menuTree={itemTree}
                onItemClicked={this.onItemClicked}
                level={level}
              />
            } else {
              return null
            }
          })}
      </Fragment>
    );
  }
}

export default HomeContainer;
