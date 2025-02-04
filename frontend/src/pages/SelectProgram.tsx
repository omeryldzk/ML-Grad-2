import InputWithDropdown from "../components/InputWithDropdown.tsx";
import "../styles/SelectProgram.css";
import { useEffect, useState } from "react";
import useAxios from "../interceptors/AxiosInstance.tsx";
import { Modal, Button } from "react-bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";

type metadata = {
    university: string | null;
    department: string | null;
};

type prediction_response = {
    prediction: number | null;
    confidence: number | null;
    metadata: metadata;
};

const SelectProgram = () => {
    const [universityName, setUniversityName] = useState<string | null>(null);
    const [universities, setUniversities] = useState<string[]>([]);
    const [faculty, setFaculty] = useState<string | null>(null);
    const [faculties, setFaculties] = useState<string[]>([]);
    const [departmentName, setDepartmentName] = useState<string | null>(null);
    const [departments, setDepartments] = useState<string[]>([]);
    const [scholarshipRate, setScholarshipRate] = useState<string | null>(null);
    const [scholarships, setScholarships] = useState<string[]>([]);
    const [language, setLanguage] = useState<string | null>(null);
    const [languages, setLanguages] = useState<string[]>([]);

    const [predictionResult, setPredictionResult] = useState<prediction_response | null>(null);
    const [showModal, setShowModal] = useState(false);
    const [showModal2, setShowModal2] = useState(false);

    const axios = useAxios();

    useEffect(() => {
        const fetchUniversities = async () => {
            const response = await axios.get("http://127.0.0.1:8001/universities");
            if (response.status === 200) {
                const set: string[] = response.data;
                setUniversities(set.sort());
            }
        };
        fetchUniversities();
    }, []);

    useEffect(() => {
        const fetchFaculties = async () => {
            const response = await axios.get("http://127.0.0.1:8001/faculties", {
                params: { university_name: universityName },
            });
            if (response.status === 200) {
                const set: string[] = response.data;
                setFaculties(set.sort());
            }
        };
        if (universityName !== null) {
            fetchFaculties();
        } else {
            setFaculties([]);
            setFaculty(null);
            setDepartmentName(null);
            setLanguage(null);
            setScholarshipRate(null);
        }
    }, [universityName]);

    useEffect(() => {
        const fetchDepartments = async () => {
            const response = await axios.get("http://127.0.0.1:8001/departments", {
                params: { university_name: universityName, faculty: faculty },
            });
            if (response.status === 200) {
                const set: string[] = response.data;
                setDepartments(set.sort());
            }
        };
        if (universityName !== null && faculty !== null) {
            fetchDepartments();
        } else {
            setDepartments([]);
            setDepartmentName(null);
            setLanguage(null);
            setScholarshipRate(null);
        }
    }, [universityName, faculty]);

    useEffect(() => {
        const fetchLanguages = async () => {
            const response = await axios.get("http://127.0.0.1:8001/languages", {
                params: { university_name: universityName, faculty: faculty, department: departmentName },
            });
            if (response.status === 200) {
                const set: string[] = response.data;
                setLanguages(set.sort());
            }
        };
        if (universityName !== null && faculty !== null && departmentName !== null) {
            fetchLanguages();
        } else {
            setLanguages([]);
            setLanguage(null);
            setScholarshipRate(null);
        }
    }, [universityName, faculty, departmentName]);

    useEffect(() => {
        const fetchScholarships = async () => {
            const response = await axios.get("http://127.0.0.1:8001/scholarships", {
                params: { university_name: universityName, faculty: faculty, department: departmentName, language: language },
            });
            if (response.status === 200) {
                const set: string[] = response.data;
                setScholarships(set.sort());
            }
        };
        if (universityName !== null && faculty !== null && departmentName !== null && language !== null) {
            fetchScholarships();
        } else {
            setScholarships([]);
            setScholarshipRate(null);
        }
    }, [universityName, faculty, departmentName, language]);

    const handlePredict = async () => {
        if (universityName !== null && faculty !== null && departmentName !== null && language !== null && scholarshipRate !== null) {
            const response = await axios.post("http://127.0.0.1:8001/predict", {
                university_name: universityName,
                faculty: faculty,
                department: departmentName,
                language: language,
                scholarship_rate: Number(scholarshipRate),
            });
            if (response.status === 200) {
                setPredictionResult(response.data);
                setShowModal(true);
            } else {
                setShowModal2(true);
            }
        } else {
            setShowModal2(true);
        }
    };

    return (
        <div className="select-program">
            <div className="title">
                <p>Predict ranking of the last person who will enter the selected program!</p>
            </div>
            <div className="inputs">
                <p style={{ fontSize: "30px", fontWeight: "bold", marginBottom: "5px", textAlign: "center" }}>Select Program</p>
                <InputWithDropdown selections={universities} displayName={"University Name"} setInput={setUniversityName} input={universityName} />
                <InputWithDropdown selections={faculties} displayName={"Faculty"} setInput={setFaculty} input={faculty} />
                <InputWithDropdown selections={departments} displayName={"Department Name"} setInput={setDepartmentName} input={departmentName} />
                <InputWithDropdown selections={languages} displayName={"Language"} setInput={setLanguage} input={language} />
                <InputWithDropdown selections={scholarships} displayName={"Scholarship Rate"} setInput={setScholarshipRate} input={scholarshipRate} />

                <div className="button">
                    <button onClick={handlePredict}>Predict!</button>
                </div>
            </div>

            {/* Prediction Result Modal */}
            <Modal show={showModal} onHide={() => setShowModal(false)}>
                <Modal.Header closeButton>
                    <Modal.Title>Prediction Results</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    Predicted base ranking for {predictionResult?.metadata.university}'s {predictionResult?.metadata.department} department is: {predictionResult?.prediction}
                </Modal.Body>
                <Modal.Footer>
                    <Button variant="secondary" onClick={() => setShowModal(false)}>
                        Close
                    </Button>
                </Modal.Footer>
            </Modal>

            {/* Error Modal */}
            <Modal show={showModal2} onHide={() => setShowModal2(false)}>
                <Modal.Header closeButton>
                    <Modal.Title>WARNING!</Modal.Title>
                </Modal.Header>
                <Modal.Body>Please select all of the fields properly!</Modal.Body>
                <Modal.Footer>
                    <Button variant="secondary" onClick={() => setShowModal2(false)}>
                        Close
                    </Button>
                </Modal.Footer>
            </Modal>
        </div>
    );
};

export default SelectProgram;
