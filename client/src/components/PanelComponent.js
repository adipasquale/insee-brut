import React from "react";

const PanelComponent = ({ menu, clickedItem }) => {
  return (
    <div className="bg-moon-gray vh-100 fl w-10">
      <ul>
        {menu.map(el => {
          return (
            <li>
              <a href="#" onClick={() => clickedItem(el.id)}>
                {el.title}
              </a>
            </li>
          );
        })}
      </ul>
    </div>
  );
};

export default PanelComponent;
