import React, { useState, useCallback } from 'react';

import Modal from 'react-bootstrap/Modal';
import Form from 'react-bootstrap/Form';

import 'regenerator-runtime/runtime.js';

export const FileUploadChooseModal = ({
    isModalOpen,
    onModalClose = null,
    onModalOpen = null,
}) => {

    const renderModal = () => (
        <>
            {isModalOpen && (
                <Modal show={isModalOpen}>
                    <Form>
                        <Modal.Header closeButton>
                            <Modal.Title>Upload videos</Modal.Title>
                        </Modal.Header>
                        <Modal.Body>
                            <div class="d-flex flex-column align-items-center">
                                <div class="my-3 d-inline-flex align-self-center align-items-center justify-content-center bg-light rounded-circle"
                                    style={{ width: '150px', height: '150px' }}>
                                    <i class="material-icons  text-secondary" style={{ fontSize: '72px' }}>publish</i>
                                </div>
                                <Form className="mt-3 col-md-8 col-lg-6">
                                    <Form.File
                                        id="file"
                                        label="Choose video file to upload"
                                        custom
                                    />
                                </Form>
                                <p class="mt-3 align-self-center">Your videos will be private until you
                        publish them.</p>
                            </div>
                        </Modal.Body>

                    </Form>
                </Modal>
            )}
        </>
    );

    return (
        <>
            {renderModal()}
        </>
    );
};

export default FileUploadChooseModal;
