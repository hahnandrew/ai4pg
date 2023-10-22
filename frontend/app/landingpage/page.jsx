"use client"
import { useState } from 'react';

const Application = () => {
  // State to manage form responses
  const [responses, setResponses] = useState({
    moreThanTwoConvictions: '',
    moreThanOneFelony: '',
    lessThanTenYears: '',
    registerSexOffender: '',
    ineligibleOffense: '',
    openCriminalCase: '',
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setResponses((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  return (
    <div>
      <h1>C.P.L. §160.59 PRO SE APPLICATION</h1>
      <p>PLEASE READ THESE INSTRUCTIONS COMPLETELY BEFORE STARTING THE APPLICATION</p>

      <h2>ARE YOU ELIGIBLE?</h2>

      <div>
        <p>DO YOU HAVE MORE THAN TWO (2) CRIMINAL CONVICTIONS (MISDEMEANOR OR FELONY)?</p>
        <input
          type="radio"
          id="moreThanTwoConvictionsYes"
          name="moreThanTwoConvictions"
          value="yes"
          onChange={handleInputChange}
        />
        <label htmlFor="moreThanTwoConvictionsYes">Yes</label>
        <input
          type="radio"
          id="moreThanTwoConvictionsNo"
          name="moreThanTwoConvictions"
          value="no"
          onChange={handleInputChange}
        />
        <label htmlFor="moreThanTwoConvictionsNo">No</label>
      </div>

      {/* Repeat similar divs for other questions */}

      {/* Example for the second question */}
      <div>
        <p>DO YOU HAVE MORE THAN ONE FELONY CONVICTION?</p>
        <input
          type="radio"
          id="moreThanOneFelonyYes"
          name="moreThanOneFelony"
          value="yes"
          onChange={handleInputChange}
        />
        <label htmlFor="moreThanOneFelonyYes">Yes</label>
        <input
          type="radio"
          id="moreThanOneFelonyNo"
          name="moreThanOneFelony"
          value="no"
          onChange={handleInputChange}
        />
        <label htmlFor="moreThanOneFelonyNo">No</label>
      </div>

      {/* ... other questions ... */}

      {/* After all questions */}
      <div>
        <button
          onClick={() => {
            console.log(responses); // Or handle the responses as needed
          }}
        >
          Submit
        </button>
      </div>
    </div>
  );
};

export default Application;
