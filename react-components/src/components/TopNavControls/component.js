import React from 'react';

export const TopNavControls = ({
    onToggleVideoLikeClicked,
    onToggleVideoDislikeClicked,
    video,
}) => {
    return (
        <>
            <a href="#" class="icon-link text-dark d-flex d-md-none justify-content-center ml-3 bg-light rounded-circle"><i
                class="material-icons align-self-center">search</i></a>
            <a href="/upload/"
                class="icon-link text-dark d-flex justify-content-center ml-3 bg-light rounded-circle"><i
                    class="small material-icons align-self-center">cloud_upload</i></a>
            <a href="#" class="icon-link text-dark d-none d-lg-flex justify-content-center ml-3 bg-light rounded-circle">
                <i class="small material-icons align-self-center">notifications_none</i></a>
        </>
    );
};

export default TopNavControls;
