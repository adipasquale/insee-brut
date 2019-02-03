import React from "react";

const PanelComponent = ({ menuTree, onItemClicked, level }) => {
  return (
    <div className="bg-moon-gray vh-100 fl w-10">
      <ul>
        {Object.values(menuTree.children).map(el => {
          return (
            <li key={el.id}>
              <button key={el.id} onClick={() => onItemClicked(el.id, level)}>
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
