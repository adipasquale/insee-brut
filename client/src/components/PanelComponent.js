import React from "react";

const PanelComponent = ({ menu }) => {
  return (
    <div className="bg-moon-gray vh-100 fl w-10">
      <ul>
        {menu.map(el => {
          return <li>{el.id}</li>;
        })}
      </ul>
    </div>
  );
};

export default PanelComponent;
