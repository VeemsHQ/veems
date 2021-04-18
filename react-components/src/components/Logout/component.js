import React, { useState } from 'react';
import 'regenerator-runtime/runtime.js';

export const Logout = ({
    destroySession,
}) => {
    return (
        <div>
            <a onClick={() => destroySession()} href="/accounts/logout/" className="mt-2 btn btn-outline-secondary"><i
            className="material-icons align-middle">exit_to_app</i> Logout</a>
        </div>
    );
};

export default Logout;
