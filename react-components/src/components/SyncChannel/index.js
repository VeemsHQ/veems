import React from 'react';
import ReactDOM from 'react-dom';

// Redux
import { connect, Provider } from 'react-redux';
import { bindActionCreators } from 'redux';
import { PersistGate } from 'redux-persist/integration/react';
import { configureStore } from '../../store';

// Components
import SyncChannelButton from './SyncChannelButton';

// Actions
import {
  setSyncModalOpenAction,
} from '../../actions/index';

// api
// import { syncChannelRequest } from '../../api/api';

const { store, persistor } = configureStore.getInstance();

// Component connected to Redux store
const Container = ({
  isSyncModalOpen,
  setSyncModalOpen,
}) => {
  const handleSyncChannel = () => {
    // todo when server calls in place
    // syncChannelRequest();
  };
  const handleModalClose = () => setSyncModalOpen(false);
  const handleModalOpen = () => setSyncModalOpen(true);
  return (
    <SyncChannelButton
      isModalOpen={isSyncModalOpen}
      onSyncChannel={handleSyncChannel}
      onModalOpen={() => handleModalOpen}
      onModalClose={() => handleModalClose}
    />
  );
};

const mapDispatchToProps = (dispatch) => ({
  dispatch,
  ...bindActionCreators({
    setSyncModalOpen: setSyncModalOpenAction,
  }, dispatch),
});

const mapStateToProps = (state) => ({
  isSyncModalOpen: state.channels.isSyncModalOpen,
});

export const ConnectedContainer = connect(mapStateToProps, mapDispatchToProps)(Container);

/* Entry point for DOM element render and subsequent button render.
This only deal with the above and handling API requests. The SyncChannel
component will manage logic.
*/
export const SyncChannelContainer = ({
  element,
  ...params
}) => (
  ReactDOM.render(
    <Provider store={store}>
      <PersistGate loading={null} persistor={persistor}>
        <ConnectedContainer {...params} />
      </PersistGate>
    </Provider>,
    element || document.createElement('div'), // for testing purposes
  )
);
