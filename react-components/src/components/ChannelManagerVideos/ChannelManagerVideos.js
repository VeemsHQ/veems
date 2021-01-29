import React from 'react';

import 'regenerator-runtime/runtime.js';

export const ChannelManagerVideos = ({
  videos,
  channelId,
}) => (
  <>
    <table className="table mt-4">
      <thead>
        <tr className="text-muted">
          <th scope="col">Video</th>
          <th scope="col">Visibility</th>
          <th scope="col">Date</th>
          <th scope="col">Earnings</th>
          <th scope="col">Views</th>
          <th scope="col">Comments</th>
          <th scope="col">Likes/dislikes</th>
        </tr>
      </thead>
    </table>
  </>
);

export default ChannelManagerVideos;
