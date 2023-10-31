"use client"

import Application from "./questionnaire/page"

function Details() {
  return (
    <div>
      hello
    </div>
  );
}

export default Details;
// import { useState } from 'react';
// import Modal from './landingpage/components/modal';

// import {
//   Card,
//   CardContent,
//   CardDescription,
//   CardHeader,
//   CardTitle,
// } from "@/components/ui/card"
// import { Button } from "@/components/ui/button"


// const Application = () => {
//   // State to manage form responses
//   const [formState, setFormState] = useState({
//     moreThanTwoConvictions: '',
//     moreThanOneFelony: '',
//     lessThanTenYears: '',
//     registerSexOffender: '',
//     ineligibleOffense: '',
//     openCriminalCase: '',
//   });

//   const [isModalOpen, setIsModalOpen] = useState(false);
//   const [modalContent, setModalContent] = useState('');

//   const handleSubmit = () => {
//     let isEligible = true;
//     let issues = [];

//     // Check the conditions based on the formState and update isEligible accordingly
//     for (const [key, value] of Object.entries(formState)) {
//       if (value === 'yes') {
//         isEligible = false;
//         issues.push(key); // Collect the issues to display specific reasons
//       }
//     }

//     if (isEligible) {
//       setModalContent('You are eligible. You will be redirected to a page to upload documents.');
//       // Here, you can also implement the redirection logic after a certain time.
//       setTimeout(() => {
//         // Redirect to the documents upload page
//         window.location.href = '/upload'; // Replace '/upload' with your actual upload page route
//       }, 3000); // 3 seconds delay for redirection
//     } else {
//       // Construct the message to indicate which issues make the user ineligible
//       const issuesString = issues.join(', ');
//       setModalContent(`You are not eligible due to the following: ${issuesString}.`);
//     }

//     // Open the modal
//     setIsModalOpen(true);
//   };

//   const handleInputChange = (e) => {
//     const { name, value } = e.target;
//     setFormState((prev) => ({
//       ...prev,
//       [name]: value,
//     }));
//   };


//   // Helper function to create the form sections
//   const createFormSection = (question, description, stateName) => (
//     <Card>
//       <CardHeader>
//         <CardTitle>{question}</CardTitle>
//         <CardDescription>{description}</CardDescription>
//       </CardHeader>
//       <CardContent>
//         <input
//           type="radio"
//           id={`${stateName}Yes`}
//           name={stateName}
//           value="yes"
//           onChange={handleInputChange}
//         />
//         <label htmlFor={`${stateName}Yes`}>Yes</label>

//         <input
//           type="radio"
//           id={`${stateName}No`}
//           name={stateName}
//           value="no"
//           onChange={handleInputChange}
//         />
//         <label htmlFor={`${stateName}No`}>No</label>
//       </CardContent>
//     </Card>
//   );

//   return (
//     <>
//       <div className="flex justify-center items-center min-h-screen">
//         <div className="container">
//           <h1>C.P.L. §160.59 PRO SE APPLICATION</h1>
//           <p>PLEASE READ THESE INSTRUCTIONS COMPLETELY BEFORE STARTING THE APPLICATION</p>

//           <h2>ARE YOU ELIGIBLE?</h2>

//           {/* Form sections */}
//           {createFormSection(
//             'DO YOU HAVE MORE THAN TWO (2) CRIMINAL CONVICTIONS (MISDEMEANOR OR FELONY)?',
//             `(If you have more than one conviction that was “committed as part of the same criminal transaction,” they count as a single
//                 conviction under this law.)`,
//             'moreThanTwoConvictions'
//           )}
//           {createFormSection('DO YOU HAVE MORE THAN ONE FELONY CONVICTION?',
//             `(If you have more than one conviction that was “committed as part of the same criminal transaction,” they count as a single
//             conviction under this law.)`,
//             'moreThanOneFelony')}
//           {createFormSection('HAVE LESS THAN TEN YEARS PASSED SINCE YOUR LAST CRIMINAL CONVICTION?',
//             `(Start counting the ten-year period from the date you were sentenced OR, if you were incarcerated after being sentenced, from
//             the date you were released from incarceration. Time spent on probation or parole counts toward the ten-year period.)`,
//             'lessThanTenYears')}
//           {createFormSection('ARE YOU REQUIRED TO REGISTER AS A SEX OFFENDER?',
//             ``,
//             'registerSexOffender')}

//           {createFormSection('ARE YOU APPLYING TO SEAL AN INELIGIBLE OFFENSE?',
//             `(INELIGIBLE offenses include sex offenses, sexual performance by a child, homicide, violent felonies, Class A felonies, felony
//             level conspiracy cases to commit an ineligible offense, and attempts to commit ineligible offenses if the offense still constitutes a
//             felony.`, 'ineligibleOffense')}

//           {createFormSection('DO YOU CURRENTLY HAVE AN OPEN CRIMINAL CASE?',
//             "",
//             'openCriminalCase')}

//           <Button
//             onClick={handleSubmit} // Updated to call the new handleSubmit function
//           >
//             Submit
//           </Button>
//         </div>
//       </div>

//       {/* Modal */}
//       <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)}>
//         <p>{modalContent}</p>
//       </Modal>




//     </>
//   );
// };

// export default Application;
