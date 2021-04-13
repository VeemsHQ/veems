import React from 'react';

import 'regenerator-runtime/runtime.js';

export const SelectActiveChannelDropdown = ({
  onSelectChannel,
  activeID,
  channels,
}) => {
  const renderDropdown = () => (
    <>
      <select
        value={activeID}
        onChange={onSelectChannel}
        className="custom-select custom-select-sm d-inline-block w-auto"
      >
        {channels.map((channel) => (
          <option key={channel.id} value={channel.id}>{channel.name}</option>
        ))};
      </select>
    </>
  );

  return (
    <>
      {renderDropdown()}
    </>
  );
};

export default SelectActiveChannelDropdown;
