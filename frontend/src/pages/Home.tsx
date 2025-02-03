import logo from "../assets/logo4.png"
import "../styles/Home.css"
import React from "react";

interface CustomCSSProperties extends React.CSSProperties {
    "--angle"?: string;
}


const Home: React.FC = () => {
    return (
        <div className="home">
            <div className="welcome">
                <img className={"logo"} src={logo} alt={"logo"}/>
                <h1 className={"title"}>Welcome <br/> to UniOptima!</h1>
            </div>
            <div className="buttons">
                <div className="circle-button-wrapper" style={{ "--angle": "0deg" } as CustomCSSProperties}>
                    <button className="circle-button">1</button>
                </div>
                <div className="circle-button-wrapper" style={{ "--angle": "60deg" } as CustomCSSProperties}>
                    <button className="circle-button">2</button>
                </div>
                <div className="circle-button-wrapper" style={{ "--angle": "120deg" } as CustomCSSProperties}>
                    <button className="circle-button">3</button>
                </div>
                <div className="circle-button-wrapper" style={{ "--angle": "180deg" } as CustomCSSProperties}>
                    <button className="circle-button">4</button>
                </div>

            </div>
        </div>
            )
        }
export default Home