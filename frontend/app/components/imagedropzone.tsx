import { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import fs from 'fs';
import path from 'path';

const ImageDropzone = () => {
  const onDrop = useCallback((acceptedFiles) => {
    acceptedFiles.forEach((file: any) => {
      const reader = new FileReader();

      reader.onabort = () => console.error('file reading was aborted');
      reader.onerror = () => console.error('file reading has failed');
      reader.onload = () => {
        const binaryStr = reader.result;
        // Specify your path here; for example, 'public/images'
        const filePath = path.join(process.cwd(), 'public/images', file.name);
        fs.writeFileSync(filePath, new Buffer(binaryStr as ArrayBuffer));
      };
      reader.readAsArrayBuffer(file);
    });
  }, []);

  const { getRootProps, getInputProps } = useDropzone({
    onDrop,
    accept: 'image/*',
  });

  return (
    <div {...getRootProps()}>
      <input {...getInputProps()} />
      <p>Drag 'n' drop an image here, or click to select one</p>
    </div>
  );
}

export default ImageDropzone;
