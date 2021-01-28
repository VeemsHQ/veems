import React from 'react';
import Enzyme from 'enzyme';

import Adapter from 'enzyme-adapter-react-16';

import { CreateSyncChannelButtonContainer } from '../components/SyncChannel';

const setUp = (props = {}) => {
  const component = Enzyme.shallow(<CreateSyncChannelButtonContainer {...props} />);
  return component;
};

Enzyme.configure({ adapter: new Adapter() });

describe('SyncChannel-Component', () => {
  let component;

  beforeEach(() => {
    const props = {};
    component = setUp(props);
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  it('Should render without errors', () => {
    expect(component.exists()).toBe(true);
  });
});
