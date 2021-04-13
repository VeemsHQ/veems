import React from 'react';

export const TopNavControls = ({
    openUploadVideoModal,
}) => {
    return (
        <>
            <a href="#" className="icon-link text-dark d-flex d-md-none justify-content-center ml-3 bg-light rounded-circle"><i
                className="material-icons align-self-center">search</i></a>
            <a href="/upload/" onClick={openUploadVideoModal}
                className="icon-link text-dark d-flex justify-content-center ml-3 bg-light rounded-circle"><i
                    className="small material-icons align-self-center">cloud_upload</i></a>
            <a href="#" className="icon-link text-dark d-none d-lg-flex justify-content-center ml-3 bg-light rounded-circle">
                <i className="small material-icons align-self-center">notifications_none</i></a>
        </>
    );
};

export default TopNavControls;
