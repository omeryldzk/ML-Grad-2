import React, {useEffect, useState} from "react"
import "../styles/InputWithDropdown.css"
import useAxios from "../interceptors/AxiosInstance.tsx";

type Props = {
    inputName: string,
    displayName: string,
    setInput: React.Dispatch<React.SetStateAction<string | null>>,
}
/*
function capitalizeFirstLetter(str:string) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}
*/


const InputWithDropdown = (props:Props) => {
    const [query, setQuery] = useState<string | null>("");
    const [showDropdown, setShowDropdown] = useState(false)
    const [selections, setSelections] = useState<string[]>([])
    const [filteredSelections, setFilteredSelections] = useState<string[]>([]);
    const [selected, setSelected] = useState<string | null>(null);

    useEffect(() => {
        setSelections(["a", "b", "c", "d", "e", "f", "g", "h", "i"]);
        setFilteredSelections(selections);
    }, [])

    useEffect(() => {
        if (query) {
            setFilteredSelections(
                selections.filter((item) => item.toLowerCase().includes(query.toLowerCase()))
            )
        }
        else
            setFilteredSelections(selections);
    }, [query, selections]);
    /*const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const value = e.target.value;
        setQuery(value)
    }*/

    const handleSelect = (value: string) => {
        props.setInput(value);
        setShowDropdown(false)
        setSelected(value)
    }

    return (

        <div className={"selection-with-search"}>
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
