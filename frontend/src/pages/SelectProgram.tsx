import InputWithDropdown from "../components/InputWithDropdown.tsx";
import "../styles/SelectProgram.css"
import {useState} from "react";
import useAxios from "../interceptors/AxiosInstance.tsx";

type Program = {
    universityName: string,
    faculty: string,
    departmentName: string,
    scholarshipRate: string,
    language: string,
}


const SelectProgram = () => {
    const [universityName, setUniversityName] = useState<string | null>(null);
    const [faculty, setFaculty] = useState<string | null>(null);
    const [departmentName, setDepartmentName] = useState<string | null>(null);
    const [scholarshipRate, setScholarshipRate] = useState<string | null>(null);
    const [language, setLanguage] = useState<string | null>(null);


    return (
        <div className="select-program">
            <div className="title">
                <p>
                Predict ranking of the last person who will enter the selected program!
                </p>
            </div>
            <div className="inputs">
                <p style={{"fontSize": "30px", "fontWeight": "bold", "marginBottom": "5px", "textAlign": "center"}}>Select Program</p>
                <InputWithDropdown inputName={"universities"} displayName={"University Name"} setInput={setUniversityName} />
                <InputWithDropdown inputName={"faculties"} displayName={"Faculty"} setInput={setFaculty} />
                <InputWithDropdown inputName={"departments"} displayName={"Department Name"} setInput={setDepartmentName} />
                <InputWithDropdown inputName={"languages"} displayName={"Language"} setInput={setLanguage} />
                <InputWithDropdown inputName={"scholarships"} displayName={"Scholarship Rate"} setInput={setScholarshipRate} />

                <div className="button">
                    <button onClick={() => {}}>Predict!</button>
                </div>



            </div>

        </div>
    )
}
export default SelectProgram