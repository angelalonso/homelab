import App from './static/js';
it('should display a submit button to send question to the Internet Gods', () => {
    const wrapper = shallow(<App />);
    expect(wrapper.find('button[type="submit"]').length).toBe(1);
});
