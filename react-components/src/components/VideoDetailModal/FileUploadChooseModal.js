import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';

import Modal from 'react-bootstrap/Modal';
import Form from 'react-bootstrap/Form';

import 'regenerator-runtime/runtime.js';

export const FileUploadChooseModal = ({
    isModalOpen,
    onModalClose = null,
    onModalOpen = null,
}) => {
    const { acceptedFiles, getRootProps, getInputProps } = useDropzone();
    const files = acceptedFiles.map(file => (
        <li key={file.path}>
            {file.path} - {file.size} bytes
        </li>
    ));

    const handleChange = (e) => {
        console.log(e);
    }

    const renderModal = () => (
        <>
            {isModalOpen && (
                <Modal show={isModalOpen}>
                    <Modal.Header closeButton>
                        <Modal.Title>Upload videos</Modal.Title>
                    </Modal.Header>
                    <Modal.Body>
                        <div {...getRootProps({ className: 'dropzone d-flex flex-column align-items-center' })}>
                            <div className="d-flex flex-column align-items-center">
                                <div className="mt-3 mb-2 d-inline-flex align-self-center align-items-center justify-content-center bg-light rounded-circle"
                                    style={{ width: '150px', height: '150px' }}>
                                    <i className="material-icons  text-secondary" style={{ fontSize: '72px' }}>publish</i>
                                </div>
                                <input {...getInputProps()} />
                                <p>Drag and drop video files here to upload</p>
                                <p className="text-muted align-self-center">Your videos will be private until you publish them.</p>
                                <p><button type="button" class="btn btn-primary">Select Files</button></p>
                            </div>
                            <aside className="d2-none">
                                <h4>Files</h4>
                                <ul>{files}</ul>
                            </aside>
                        </div>
                    </Modal.Body>
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
