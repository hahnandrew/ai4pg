import { useState } from "react";
// TODO change to Image from next/image

export default function PrivatePage(props) {
  const [image, setImage] = useState(null);
  const [createObjectURL, setCreateObjectURL] = useState(null);
  const [serverResponse, setServerResponse] = useState(null);  // New state variable

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
    // const route = "https://ai4pgprod.onrender.com/validate/receive_rap_sheet";
    const route = "http://localhost:3000/validate/receive_rap_sheet";

    try {
      const response = await fetch(route, {
        method: "POST",
        body,
      });

      if (response.ok) {
        const responseData = await response.json();
        setServerResponse(JSON.stringify(responseData, null, 2)); // Convert JSON object to formatted string
        alert("File uploaded successfully!");
      } else {
        alert("File upload failed. " + await response.text());
      }
    } catch (error) {
      console.error("There was an error uploading the file:", error);
      alert("There was an error uploading the file. Please check the console for more details.");
    }
  };

  return (
    <div className="flex flex-col items-center space-y-6">
      <img src={createObjectURL} alt="Uploaded Preview" className="w-1/2 h-1/2 object-contain" />
      <h4 className="text-lg font-semibold">Select Image</h4>
      <div className="flex flex-col space-y-4 items-center">
        {/* Image selection button */}
        <button
          className="btn btn-outline btn-circle"
          onClick={() => document.getElementById('myImageInput').click()}
        >
          Choose Image
        </button>
        <input
          id="myImageInput"
          type="file"
          name="myImage"
          onChange={uploadToClient}
          className="hidden"
        />

        <button className="btn btn-primary" onClick={uploadToServer}>
          Send to server
        </button>

        {/* Displaying the server response */}
        {serverResponse && <pre className="mt-4 text-center">{serverResponse}</pre>}
      </div>
    </div>
  );
}
