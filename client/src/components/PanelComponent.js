import React from "react";

const PanelComponent = ({ menu, clickedItem, key }) => {
  return (
    <div className="bg-moon-gray vh-100 fl w-10">
      <ul>
        {menu.map(el => {
          return (
            <li key={key}>
              <button key={key} onClick={() => clickedItem(el.id)}>
                {el.title}
              </button>
            </li>
          );
        })}
      </ul>
    </div>
  );
};

export default PanelComponent;
