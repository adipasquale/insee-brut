import React from "react";

const PanelComponent = ({ menu, clickedItem, panelId }) => {
  return (
    <div className="bg-moon-gray vh-100 fl w-10">
      <ul>
        {menu.map(el => {
          return (
            <li key={el.id}>
              <button key={el.id} onClick={() => clickedItem(panelId, el.id)}>
                {el.id}
              </button>
            </li>
          );
        })}
      </ul>
    </div>
  );
};

export default PanelComponent;
