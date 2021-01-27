import React from 'react';

import 'regenerator-runtime/runtime.js';
import PropTypes from 'prop-types';

// Styling
/* Todo: Move all embedded css into here so we can properly pass and use props
  and remove all ugly className syntax.
*/

export const SelectChannelDropdown = ({
  onSelectChannel,
  activeID,
  channels,
}) => {
  const renderDropdown = () => (
    <>
      <h1 className="h2 m-0 p-0 d-inline-block">Channel Manager</h1>
      <select value={activeID} onChange={onSelectChannel} className="custom-select custom-select-sm d-inline-block w-auto ml-3">
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

/** Props Types */
SelectChannelDropdown.propTypes = {
  activeID: PropTypes.string,
  channels: PropTypes.arrayOf(PropTypes.shape()),
  onSelectChannel: PropTypes.func,
};

/** Default Props. */
SelectChannelDropdown.defaultProps = {
  activeID: '',
  onSelectChannel: () => { Error('No callback defined for SelectChannelDropdown'); },
  channels: [],
};

export default SelectChannelDropdown;
