import React from 'react';
import ReactDOM from 'react-dom';

import Toast from 'react-bootstrap/Toast';
import { connect, Provider } from 'react-redux';
import { bindActionCreators } from 'redux';
import { PersistGate } from 'redux-persist/integration/react';
import { configureStore } from '../../store';

import {
  removeToastAction,
} from '../../actions/index';

const { store, persistor } = configureStore.getInstance();
const DELAY = 3000;
const AUTOHIDE = true;

const Container = ({
  show = true,
  header = '',
  body = '',
  isError = false,
  removeToast,
}) => {
  const handleToastClose = () => {
    removeToast();
  };

  const renderToast = (headerClassName) => (
    <div
      aria-live="polite"
      aria-atomic="true"
      style={{
        position: 'fixed',
        bottom: '0',
        right: '0',
        height: '2px',
        width: '100%',
        zIndex: '9999',
      }}
    >
      <Toast
        style={{
          position: 'absolute',
          bottom: '0px',
          left: '50%',
          transform: 'translate(-50%, -50%)',
        }}
        show={show}
        delay={DELAY}
        autohide={AUTOHIDE}
        onClose={handleToastClose}
      >
        <Toast.Header>
          <strong className={`mr-auto ${headerClassName}`}>{header}</strong>
        </Toast.Header>
        <Toast.Body>{body}</Toast.Body>
      </Toast>
    </div>
  );

  if (isError === true) {
    return renderToast('text-danger');
  }
  return renderToast('text-success');
};

const mapStateToProps = (state) => {
  if (state.globals.toast === null) {
    return { show: false };
  }
  const props = { ...{ show: true }, ...state.globals.toast };
  return props;
};

const mapDispatchToProps = (dispatch) => ({
  dispatch,
  ...bindActionCreators({
    removeToast: removeToastAction,
  }, dispatch),
});

const ConnectedContainer = connect(mapStateToProps, mapDispatchToProps)(Container);

export const CreateToastContainer = ({
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
