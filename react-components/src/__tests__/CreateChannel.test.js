import React from 'react';
import Enzyme from 'enzyme';

import Adapter from 'enzyme-adapter-react-16';

import { CreateChannelContainer } from '../components/CreateChannel';

const setUp = (props = {}) => {
  const component = Enzyme.shallow(<CreateChannelContainer {...props} />);
  return component;
};

Enzyme.configure({ adapter: new Adapter() });

describe('CreateChannel-Component', () => {
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

  //   //it('Should contain a CreateChannelButton component', () => {
  //     console.log(component)
  //     //expect(component.find(CreateChannelButton).length).toBe(1);
  //   });

  //   it('Should contain a button', () => {
  //     const dom = component.find(CreateChannelButton).dive().find('Create Channel');
  //     expect(dom.length).toBe(1);
  //     //expect(component.find(Modal).length).toBe(1);
  //   });
});
