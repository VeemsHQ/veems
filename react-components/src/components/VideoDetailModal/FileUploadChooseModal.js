import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';

import Modal from 'react-bootstrap/Modal';
import Form from 'react-bootstrap/Form';
import Spinner from 'react-bootstrap/Spinner'

import 'regenerator-runtime/runtime.js';

export const FileUploadChooseModal = ({
    isModalOpen,
    isFileSelected,
    onFileSelect,
    onModalClose = null,
    onModalOpen = null,
}) => {
    const { getRootProps, getInputProps } = useDropzone({
        onDrop: onFileSelect, disabled: isFileSelected
    });
    const renderModal = () => (
        <Modal show={isModalOpen} onHide={onModalClose()}>
            <Modal.Header closeButton>
                <Modal.Title>Upload video</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <div {...getRootProps({ className: 'dropzone d-flex flex-column align-items-center' })}>
                    <div className="d-flex flex-column align-items-center">
                        <div className="mt-3 mb-2 d-inline-flex align-self-center align-items-center justify-content-center bg-light rounded-circle"
                            style={{ width: '150px', height: '150px' }}>
                            {isFileSelected && (
                                <Spinner animation="border" size="xl" variant="secondary" />
                            )}
                            {!isFileSelected && (
                                <i className="material-icons  text-secondary" style={{ fontSize: '72px' }}>publish</i>
                            )}
                        </div>
                        <input {...getInputProps()} />
                        <p>{!isFileSelected && 'Drag and drop video files here to upload'}{isFileSelected && 'Hang tight, uploading...'}</p>
                        <p className="text-muted align-self-center">Your videos will be private until you publish them.</p>
                        <p><button type="button" className="btn btn-primary" disabled={isFileSelected}>Select Files</button></p>
                    </div>
                </div>
            </Modal.Body>
        </Modal>
    );

    return (
        <>
            {renderModal()}
        </>
    );
};

export default FileUploadChooseModal;
