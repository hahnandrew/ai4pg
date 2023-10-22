"use client"
import ImageDropzone from '../components/dropimage';

function YourPageComponent() {
  return (
    <div className="flex w-full h-full justify-center items-center bg-gray-100 py-10">
      <div className="p-8 bg-white shadow-lg rounded-lg w-1/2">
        <ImageDropzone />
      </div>
    </div>
  );
}

export default YourPageComponent;
