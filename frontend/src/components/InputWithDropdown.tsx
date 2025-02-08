import React, {useEffect, useState, useRef} from "react"
import "../styles/InputWithDropdown.css"
import useAxios from "../interceptors/AxiosInstance.tsx";
import {Simulate} from "react-dom/test-utils";
import close = Simulate.close;

type Props = {
    displayName: string,
    selections: string[],
    setInput: React.Dispatch<React.SetStateAction<string | null>>,
    input: string
}


const InputWithDropdown = (props:Props) => {
    const [query, setQuery] = useState<string | null>("");
    const [showDropdown, setShowDropdown] = useState(false);
    const [filteredSelections, setFilteredSelections] = useState<string[]>([]);
    const [selected, setSelected] = useState<string | null>(null);

    useEffect(() => {
        if (query) {
            setFilteredSelections(
                props.selections.filter((item) => item.toLowerCase().includes(query.toLowerCase()))
            )
        }
        else
            setFilteredSelections(props.selections);
    }, [query, props.selections]);

    useEffect(() => {
        if (props.input === null)
            setSelected(null)
    }, [props.input]);


    const handleSelect = (value: string) => {
        props.setInput(value);
        setShowDropdown(false)
        setSelected(value)
    }

    const dropdownRef = useRef(null);

    const handleClickOutside = (event: MouseEvent) => {
        // If the click is outside the dropdown, hide it
        if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
            setShowDropdown(false);
        }
    };

    useEffect(() => {
        // Add the event listener for detecting clicks outside
        document.addEventListener("mousedown", handleClickOutside);

        // Clean up the event listener when the component unmounts
        return () => {
            document.removeEventListener("mousedown", handleClickOutside);
        };
    }, []);


    return (

        <div className={"selection-with-search"} ref={dropdownRef}>
            <div className={"form-title"}>{props.displayName + ":"}</div>
            <div className={"results"} onClick={() => setShowDropdown(!showDropdown)}>
                <p>{selected === null ? "Please Select..." : selected}</p>
                <div className={"results-group"}>
                    <div className={"x-mark"}>
                        <p onClick={() => {setQuery(null); setSelected(null); props.setInput(null)}}>×</p>
                    </div>
                    <p>&#9660;</p>
                </div>
            </div>
            {showDropdown && (
                <div className="input-with-dropdown">
                    <input
                        className={"input-bar"}
                        type={"text"}
                        value={query}
                        onChange={(e) => {setQuery(e.target.value)}}
                        placeholder={"Enter " + props.displayName + "..."}
                    />
                    <ul className="select-list">
                        {filteredSelections.length !== 0 ? filteredSelections.map((name: string) => (
                            <li className={"clickable"} key={name} onClick={() => handleSelect(name)}>
                                {name}
                            </li>
                        )) : <li style={{"paddingLeft": "2%"}} key={"not found"}>
                            Not Found
                        </li>}
                    </ul>
                </div>
            )}

        </div>
    )
}
export default InputWithDropdown
