import logo from "../assets/logo4.png"
const Home = () => {
    return (
        <div className="home">
            <h1 className={"title"}>Welcome to UniOptima!</h1>
            <img className={"logo"} src={logo} alt={"logo"}/>
        </div>
    )
}

export default Home