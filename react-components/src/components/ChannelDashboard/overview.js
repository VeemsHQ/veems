import React, { useRef, useEffect, useState } from 'react';
import Modal from 'react-bootstrap/Modal';
import "regenerator-runtime/runtime.js";

// Styling
/* Todo: Move all embedded css into here so we can properly pass and use props
  and remove all ugly className syntax.
*/

export const Overview = ({
  children,
  onCreateChannel,
  ...props
}) => {
  const chartRef = useRef(null);
  const [showChannelModal, setShowChannleModal] = useState(false);

  const [channelName, setChannelName] = useState('My Awesome Channel');
  const [channelDescription, setChannelDescription] = useState('Tell viewers about your channel. Your description will appear in the About section of your channel and search results, among other places.');
  const [channelSync, setChannelSync] = useState(false);

  useEffect(() => {
    if (chartRef.current) {
      const myChart = new Chart(chartRef.current, {
        type: 'line',
        data: {
            labels: ["Mon", "Tues", "Weds", "Thurs", "Fri", "Sat", "Sun"],
            datasets: [{
                label: 'Total Channel Views', // Name the series
                data: [14040, 14141, 4111, 4544, 47, 5555, 6811], // Specify the data values array
                fill: true,
                borderColor: '#2196f3', // Add custom color border (Line)
                backgroundColor: 'rgb(33,150,243, 0.15)', // Add custom color background (Points and Fill)
                borderWidth: 1 // Specify bar border width
            }]
        },
        options: {
            responsive: true, // Instruct chart js to respond nicely.
            maintainAspectRatio: false, // Add to prevent default behaviour of full-width/height
        }
      });
    }
  }, []);

  const createChannel = () => {
    setShowChannleModal(false);
    // Todo: Add some warnings to form validation for failed create.
    onCreateChannel(channelName, channelDescription, channelSync);
  };

  const renderModal = () => {
    return (
      <>
        <Modal show={showChannelModal} onHide={() => setShowChannleModal(false)}>
          <Modal.Header closeButton>
            <Modal.Title>Create a channel</Modal.Title>
          </Modal.Header>
          <Modal.Body>
            <div className="form-group">
                <label>Channel Name</label>
                <input placeholder={channelName} onInput={e => setChannelName(e.target.value)} type="text" className="form-control" id="customInput2"
                    placeholder="My Awesome Channel" />
            </div>
            <div className="form-group">
                <label>Channel Description</label>
                <textarea placeholder={channelDescription} onInput={e => setChannelDescription(e.target.value)} className="form-control" rows="3" id="customTextArea2"></textarea>
            </div>
            <div className="form-group">
                <div className="custom-control custom-checkboxWW">
                    <input onChange={e => {setChannelSync(e.target.value)}} type="checkbox" className="custom-control-input" id="customCheck2" />
                    <label className="custom-control-label d-flex">I'd like to sync videos
                        from my YouTube Channel.</label><a href="#">Learn more about channel syncing</a>.
                </div>
            </div>
            <p className="text-muted">
                By clicking "Create channel", you agree to our <a href="#">Terms of Service</a>.
            </p>
          </Modal.Body>
          <Modal.Footer>
                <button onClick={() => setShowChannleModal(false)} type="button" className="btn btn-light">Cancel</button>
                <a href="#" onClick={() => createChannel()} className="btn btn-primary">Create Channel</a>
          </Modal.Footer>
        </Modal>
      </>
    )
  };

  return (
    <>
      <div className="col d-block d-lg-none">
          <p className="alert alert-secondary">Channel link<br /><a href="#">https://veems.com/c/UCASvHD</a></p>
      </div>

      <div className="col-12 col-lg-4 mb-3">
          <div className="border rounded p-3">
              <div className="row">
                  <div className="col">
                      <div className="d-flex align-items-center">
                          <h2 className="h5">Last 7 days</h2>
                      </div>
                      <canvas width="100%" height="100%" style={{ maxHeight: '400px' }} ref={chartRef} />
                  </div>
              </div>
          </div>
      </div>

      <div className="col-12 col-lg-4">

          <div className="border rounded p-3">
              <div className="row">
                  <div className="col">
                      <div>
                          <h2 className="h5">Channel Analytics</h2>
                          <p>Current subscribers</p>
                          <p className="h3">43,404</p>
                      </div>
                      <hr />
                      <div>
                          <h3 className="h6">Summary</h3>
                          <p className="text-muted">Last 28 days</p>

                          <div className="metrics-table">
                              <div className="d-flex flex-row">
                                  <div className="text-muted">Views</div>
                                  <div className="ml-auto">42,304</div>
                              </div>
                              <div className="d-flex flex-row">
                                  <div className="text-muted">Watch time (hours)</div>
                                  <div className="ml-auto">433</div>
                              </div>
                          </div>
                      </div>
                      <hr />
                      <div>
                          <h3 className="h6">Top videos</h3>
                          <p className="text-muted">Last 7 days (views)</p>

                          <div className="metrics-table">
                          </div>
                      </div>
                  </div>
              </div>
          </div>
      </div>

      <div className="col">
        <p className="alert alert-secondary">Channel link<br /><a href="#">https://veems.com/c/UCASvHD</a></p>
        <div className="border my-3 rounded p-3">
            <h4>News</h4>
            <p>No new updates, but check back regularly to see announcements geared specifically for creators.
                Also take a look at: </p>
            <p><a href="#"><img src="{% static 'images/social-icons/discord.svg' %}" className="social-icon mr-1" /> Veems on Discord</a></p>
            <p><a href="#"><img src="{% static 'images/social-icons/twitter.svg' %}" className="social-icon mr-1" /> Veems on Twitter</a></p>
        </div>
        <div className="border my-3 rounded p-3">
            <h4>Actions</h4>
            <div><a href="#" className="btn btn-outline-secondary" data-toggle="modal" data-target="#uploadModal"><i
                        className="material-icons align-middle">backup</i> Upload
                    Video</a>
            </div>
            <div><a href="{% url 'channel-manager-sync' %}" className="mt-2 btn btn-outline-secondary"><i className="material-icons align-middle">sync</i>
                    Sync
                    YouTube
                    Videos</a></div>
            <div><a onClick={() => setShowChannleModal(true)} className="mt-2 btn btn-outline-secondary"><i className="material-icons align-middle">add_circle_outline</i> Create Channel</a></div>
            <div><a href="{% url 'logout' %}" className="mt-2 btn btn-outline-secondary"><i className="material-icons align-middle">exit_to_app</i> Logout</a></div>
        </div>
      </div>
      {renderModal()}
    </>
  );
};

export default Overview;
