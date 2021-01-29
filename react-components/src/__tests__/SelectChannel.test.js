import React from 'react';
import Enzyme from 'enzyme';

import Adapter from 'enzyme-adapter-react-16';

import { CreateSelectChannelContainer } from '../components/SelectChannel';

const setUp = (props = {}) => {
  const component = Enzyme.shallow(<CreateSelectChannelContainer {...props} />);
  return component;
};

Enzyme.configure({ adapter: new Adapter() });

describe('SelectChannel-Component', () => {
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
