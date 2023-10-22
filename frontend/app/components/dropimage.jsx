import { useState } from "react";

export default function PrivatePage(props) {
  const [image, setImage] = useState(null);
  const [createObjectURL, setCreateObjectURL] = useState(null);

  const uploadToClient = (event) => {
    if (event.target.files && event.target.files[0]) {
      const i = event.target.files[0];

      setImage(i);
      setCreateObjectURL(URL.createObjectURL(i));
    }
  };

  const uploadToServer = async (event) => {
    const body = new FormData();
    body.append("file", image);
    const response = await fetch("http://localhost:3001/api/file", {
      method: "POST",
      body
    });


    if (response.ok) {
      alert("File uploaded successfully!");
    } else {
      alert("File upload failed. " + await response.text());
    }
  };


  return (
    <div className="flex flex-col items-center space-y-6">
      <img src={createObjectURL} alt="Uploaded Preview" className="w-1/2 h-1/2 object-contain" />
      <h4 className="text-lg font-semibold">Select Image</h4>
      <div className="flex flex-col space-y-4 items-center">
        <label className="btn btn-outline btn-circle">
          <input type="file" name="myImage" onChange={uploadToClient} className="hidden" />
          Choose Image
        </label>
        <button className="btn btn-primary" onClick={uploadToServer}>
          Send to server
        </button>
      </div>
    </div>
  );
}
