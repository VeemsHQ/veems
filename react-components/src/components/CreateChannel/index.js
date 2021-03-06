import React from 'react';
import ReactDOM from 'react-dom';

import { connect, Provider } from 'react-redux';
import { bindActionCreators } from 'redux';
import { PersistGate } from 'redux-persist/integration/react';
import { configureStore } from '../../store';

import CreateChannelButton from './component';
import {
  createChannel,
  setCreateChannelShowModal,
} from '../../actions/index';

const { store, persistor } = configureStore.getInstance();

const Container = ({
  setCreateChannelShowModal,
  createChannel,
  apiErrors,
  showModal,
}) => {

  return (
    <CreateChannelButton
      createChannel={createChannel}
      setCreateChannelShowModal={setCreateChannelShowModal}
      apiErrors={apiErrors}
      showModal={showModal}
    />
  );
};

const mapDispatchToProps = (dispatch) => ({
  dispatch,
  ...bindActionCreators({
    createChannel: createChannel,
    setCreateChannelShowModal: setCreateChannelShowModal,
  }, dispatch),
});

const mapStateToProps = (state) => {
  return {
    apiErrors: state.channels.createChannelForm.apiErrors,
    showModal: state.channels.createChannelForm.showModal,
  };
};

const ConnectedContainer = connect(mapStateToProps, mapDispatchToProps)(Container);

export const CreateChannelContainer = ({
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
